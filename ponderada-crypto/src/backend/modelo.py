import pandas as pd
import numpy as np
import warnings
import logging
import os
from arch import arch_model
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from config import DATA_DIR
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error

def processar_dataframe(df, nome_cripto):
    logging.info(f"Colunas do DataFrame {nome_cripto}: {df.columns}")

    # Renomeando as colunas do dataframa
    df.rename(columns={
        'open_price': 'Abertura',
        'close_price': 'Ultimo',
        'total_volume': 'Vol',
        'max_price': 'Maxima',
        'min_price': 'Minima',
        'volatility': 'Volatilidade'
    }, inplace=True)

    # Definindo as colunas necessarias 
    required_columns = ['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']
    missing_columns = [col for col in required_columns if col not in df.columns]

    # Verificando se todas as colunas que serão utilizadas estão presentes
    if missing_columns:
        logging.error(f"As seguintes colunas estão faltando no DataFrame {nome_cripto}: {missing_columns}")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    # Usando a RobustScaler para transformar as colunas numéricas, modelo mais resistente a outliers
    scaler = RobustScaler()
    df[['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']] = scaler.fit_transform(
        df[['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']]
    )

    # Convertendo a coluna de data para o formato datetime e removendo linhas com valores nulos
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
    df.dropna(subset=['date', 'Ultimo'], inplace=True)

    # Removendo zeros da coluna 'Ultimo' e os valores nulos resultantes
    df['Ultimo'] = df['Ultimo'].replace(0, np.nan)
    df.dropna(subset=['Ultimo'], inplace=True)

    # Verificando se a coluna 'Ultimo' tem mais de um valor único
    if df['Ultimo'].nunique() <= 1:
        logging.error(f"A coluna 'Ultimo' do {nome_cripto} contém valores idênticos ou não variáveis.")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    # Calculando o retorno do log
    df['log_return'] = np.log(df['Ultimo'] / df['Ultimo'].shift(1))
    df.dropna(subset=['log_return'], inplace=True)

    # Verificando se o DataFrame ficou vazio após o cálculo
    if df.empty:
        logging.error(f"O DataFrame {nome_cripto} ficou vazio após o cálculo do retorno logarítmico.")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    # Ajustando o modelo GARCH para os retornos do log
    model = arch_model(df['log_return'], vol='Garch', p=1, q=1)
    garch_fit = model.fit(disp='off')

    forecast_horizon = 10  # Número de dias para previsão
    forecasts = garch_fit.forecast(horizon=forecast_horizon)  # Faz a previsão de volatilidade
    volatility_forecast = forecasts.variance.values[-1]  # Extrai a previsão de volatilidade

    # Criando um DataFrame para armazenar as previsões de volatilidade
    last_date = df['date'].max()  # Última data no DataFrame
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon)
    forecast_df = pd.DataFrame(volatility_forecast, index=forecast_dates, columns=['forecast_volatility'])

    # Ajustando o modelo ARIMA para prever preços
    train, test = train_test_split(df['Ultimo'], test_size=0.2, shuffle=False)  # Dividindo os dados em treino e teste
    grid_search = GridSearchCV(estimator=ARIMA(), param_grid={'order': [(p, 1, q) for p in range(1, 6) for q in range(1, 3)]}, cv=3)
    grid_search.fit(train.values)  # Buscando pelos melhores parâmetros

    best_order = grid_search.best_params_['order']  # Melhores parâmetros encontrados
    arima_model = ARIMA(df['Ultimo'], order=best_order)  # Ajusta o modelo ARIMA
    arima_fit = arima_model.fit()  # Treina o modelo

    # Faz a previsão de preços usando o modelo ARIMA
    price_forecast = arima_fit.forecast(steps=forecast_horizon)
    price_forecast_full = np.full((len(price_forecast), 6), np.nan)  # Criando um array para armazenar os preços previstos
    price_forecast_full[:, 1] = price_forecast.values  # Preenchendo com os preços previstos
    price_forecast_inverse = scaler.inverse_transform(price_forecast_full)  # Invertendo a transformação
    price_forecast = price_forecast_inverse[:, 1]  # Extraindo os preços invertidos
    forecast_df['forecast_price'] = price_forecast  # Adicionando ao DataFrame de previsões

    # Cálculo da média da última semana
    one_week_ago = df.index[-7:]  # Seleciona os últimos 7 dias
    prices_last_week = df.loc[one_week_ago, 'Ultimo'].mean()  # Calcula a média dos preços da última semana
    forecast_df['previous_week_avg'] = prices_last_week  # Adiciona a média ao DataFrame de previsões
    forecast_df['buy_signal'] = forecast_df['forecast_price'] < forecast_df['previous_week_avg']  # Sinal de compra

    forecast_5_days = forecast_df.head(5)  # Seleciona as 5 primeiras previsões

    # Ajustando do modelo Holt-Winters para suavização exponencial
    try:
        hw_model = ExponentialSmoothing(df['Ultimo'], trend='add', seasonal='add', seasonal_periods=7)
        hw_fit = hw_model.fit()  # Treina o modelo Holt-Winters
    except Exception as e:
        logging.error(f"Erro ao ajustar o modelo Holt-Winters para {nome_cripto}: {e}")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    hw_forecast = hw_fit.forecast(steps=forecast_horizon)  # Faz a previsão usando Holt-Winters
    hw_forecast_scaled = scaler.transform(np.full((len(hw_forecast), 6), np.nan))  # Transforma para manter a consistência
    hw_forecast_scaled[:, 1] = hw_forecast.values  # Preenche com as previsões
    hw_forecast_inverse = scaler.inverse_transform(hw_forecast_scaled)  # Inverte a transformação
    forecast_df['holt_winters_forecast'] = hw_forecast_inverse[:, 1]  # Adiciona ao DataFrame de previsões

    # Seleciona os melhores dias com base em um percentil da volatilidade prevista
    percentil = 10  # Definindo percentil para selecionar os melhores dias
    threshold = np.percentile(forecast_df['forecast_volatility'], percentil)  # Calculando o limite de volatilidade
    best_forecast_days = forecast_df[forecast_df['forecast_volatility'] <= threshold]  # Filtrando pelos melhores dias para compra

    return {
        'melhores_dias': best_forecast_days,
        'previsao_proximos_dias': forecast_5_days,
        'holt_winters_forecast': forecast_df['holt_winters_forecast'].tolist()
    }

# Função para executar o modelo
def executar_modelo():
    current_dir = os.path.dirname(os.path.realpath(__file__)) 
    csv_path_btc = os.path.join(DATA_DIR, 'bitcoin_daily_data.csv')  # Arquivo CSV do Bitcoin
    csv_path_eth = os.path.join(DATA_DIR, 'ethereum_daily_data.csv')  # Arquivo CSV do Ethereum

    # Lê os dados de preços diários de Bitcoin e Ethereum
    df_btc = pd.read_csv(csv_path_btc)
    df_eth = pd.read_csv(csv_path_eth)

    # Processa os dados de cada criptomoeda
    resultados_btc = processar_dataframe(df_btc, 'Bitcoin')
    resultados_eth = processar_dataframe(df_eth, 'Ethereum')

    resultados = {}
    # Prepara os resultados para cada criptomoeda
    resultados['bitcoin'] = resultados_btc
    resultados['ethereum'] = resultados_eth

    return resultados  # Retorna os resultados processados

# Executa o modelo
if __name__ == "__main__":
    warnings.simplefilter('ignore', ConvergenceWarning)  
    logging.basicConfig(filename='logs/app.log', level=logging.INFO)  # Configura o logger
    resultados = executar_modelo()  # Executa o modelo e obtém os resultados
    print(resultados) 
