import pandas as pd
import numpy as np
import logging
import sqlite3
from arch import arch_model
from pmdarima import auto_arima
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.preprocessing import RobustScaler
from config import DATA_DIR  
from utils.processar import obter_dados_cripto 

#Configuração do logging
logging.basicConfig(level=logging.INFO)

#Função para processar o DataFrame
def processar_dataframe(df, nome_cripto):
    logging.info(f"Colunas do DataFrame {nome_cripto}: {df.columns}")

    #Renomeando as colunas
    df.rename(columns={
        'open_price': 'Abertura',
        'close_price': 'Ultimo',
        'total_volume': 'Vol',
        'max_price': 'Maxima',
        'min_price': 'Minima',
        'volatility': 'Volatilidade',
        'date': 'Data'
    }, inplace=True)

    #Verificar se as colunas obrigatórias estão na tabela
    required_columns = ['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade', 'Data']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logging.error(f"As seguintes colunas estão faltando no DataFrame {nome_cripto}: {missing_columns}")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    #Normalização usando RobustScaler
    scaler = RobustScaler()
    df[['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']] = scaler.fit_transform(
        df[['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']]
    )

    #Conversão da coluna de data
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d', errors='coerce')
    df.dropna(subset=['Data', 'Ultimo'], inplace=True)

    #Limpeza de dados
    df['Ultimo'].replace(0, np.nan, inplace=True)
    df.dropna(subset=['Ultimo'], inplace=True)

    #Verificação da variabilidade dos preços
    if df['Ultimo'].nunique() <= 1:
        logging.error(f"A coluna 'Ultimo' do {nome_cripto} contém valores idênticos ou não variáveis.")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    #Cálculo do log
    df['log_return'] = np.log(df['Ultimo'] / df['Ultimo'].shift(1))
    df.dropna(subset=['log_return'], inplace=True)

    #Verificando se DataFrame está vazio
    if df.empty:
        logging.error(f"O DataFrame {nome_cripto} ficou vazio após o cálculo do retorno logarítmico.")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    #Modelo GARCH
    model = arch_model(df['log_return'], vol='Garch', p=1, q=1)
    garch_fit = model.fit(disp='off')
    forecast_horizon = 10
    forecasts = garch_fit.forecast(horizon=forecast_horizon)
    volatility_forecast = forecasts.variance.values[-1]

    #Criação do DataFrame para previsões de volatilidade
    last_date = df['Data'].max()
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon)
    forecast_df = pd.DataFrame(volatility_forecast, index=forecast_dates, columns=['forecast_volatility'])

    #Modelo ARIMA usando auto_arima do pmdarima
    model_arima = auto_arima(df['Ultimo'], seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
    price_forecast = model_arima.predict(n_periods=forecast_horizon)

    #Inversão da transformação para os preços previstos
    price_forecast_full = np.full((len(price_forecast), 6), np.nan)
    price_forecast_full[:, 1] = price_forecast
    price_forecast_inverse = scaler.inverse_transform(price_forecast_full)
    forecast_df['forecast_price'] = price_forecast_inverse[:, 1]

    #Modelo Holt-Winters
    holt_model = ExponentialSmoothing(df['Ultimo'], trend='add', seasonal='add', seasonal_periods=7)
    holt_fit = holt_model.fit()
    holt_forecast = holt_fit.forecast(steps=forecast_horizon)

    #Log e print dos resultados
    logging.info(f"Previsão de preço: {price_forecast}")
    logging.info(f"Previsão de volatilidade: {forecast_df['forecast_volatility']}")

    print(f"\n*** Resultados para {nome_cripto} ***")
    print("Modelo GARCH - Previsão de Volatilidade:")
    print(forecast_df['forecast_volatility'])
    print("\nModelo ARIMA - Previsão de Preços:")
    print(price_forecast)
    print("\nModelo Holt-Winters - Previsão:")
    print(holt_forecast)

    return {
        'melhores_dias': [],  #Implementando lógica para calcular os melhores dias
        'previsao_proximos_dias': price_forecast.tolist(),
        'holt_winters_forecast': holt_forecast.tolist()
    }

#Função para salvar os resultados no banco de dados SQLite
def save_to_sqlite(df, table_name):
    db_path = DATA_DIR  #Caminho para o banco de dados existente
    conn = sqlite3.connect(db_path)  #Conectarndo ao banco de dados
    df.to_sql(table_name, conn, if_exists='replace', index=True)  #Salvando o DataFrame na tabela
    conn.close()
    print(f"Estatísticas diárias salvas com sucesso na tabela '{table_name}' do banco de dados '{db_path}'!")

#Função principal para executar o modelo
def executar_modelo():
    #Executa o modelo para Bitcoin e Ethereum e printa os resultados
    bitcoin_data = obter_dados_cripto('bitcoin')
    ethereum_data = obter_dados_cripto('ethereum')

    if bitcoin_data is not None and not bitcoin_data.empty:
        resultado_bitcoin = processar_dataframe(bitcoin_data, 'Bitcoin')
        save_to_sqlite(bitcoin_data, "bitcoin_daily_stats")
    else:
        resultado_bitcoin = {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    if ethereum_data is not None and not ethereum_data.empty:
        resultado_ethereum = processar_dataframe(ethereum_data, 'Ethereum')
        save_to_sqlite(ethereum_data, "ethereum_daily_stats")
    else:
        resultado_ethereum = {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    return {
        'Bitcoin': resultado_bitcoin,
        'Ethereum': resultado_ethereum
    }

if __name__ == "__main__":
    resultados = executar_modelo()
    print("\n*** Resultados Finais ***")
    print(resultados)