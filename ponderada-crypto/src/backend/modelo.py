import pandas as pd
import numpy as np
from arch import arch_model
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.preprocessing import MinMaxScaler
import os

def processar_dataframe(df, nome_cripto):
    print(f"Colunas do DataFrame {nome_cripto}:", df.columns)

    # Renomeando colunas
    df.rename(columns={
        'open_price': 'Abertura',
        'close_price': 'Ultimo',
        'total_volume': 'Vol',
        'max_price': 'Maxima',
        'min_price': 'Minima',
        'volatility': 'Volatilidade'
    }, inplace=True)

    # Verificar se todas as colunas esperadas estão presentes
    expected_columns = ['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']
    missing_columns = [col for col in expected_columns if col not in df.columns]
    
    if missing_columns:
        print(f"As seguintes colunas estão faltando no DataFrame {nome_cripto}: {missing_columns}")
        return None
    
    # Normalizando os dados
    scaler = MinMaxScaler()
    df[['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']] = scaler.fit_transform(df[['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']])

    # Convertendo a coluna de data
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

    # Removendo linhas com datas inválidas ou valores nulos
    df.dropna(subset=['date', 'Ultimo'], inplace=True)

    # Verificar se a coluna 'Ultimo' contém valores válidos
    df['Ultimo'] = df['Ultimo'].replace(0, np.nan)
    df.dropna(subset=['Ultimo'], inplace=True)

    if df['Ultimo'].nunique() <= 1:
        print(f"A coluna 'Ultimo' do {nome_cripto} contém valores idênticos ou não variáveis, impossibilitando o cálculo de retorno logarítmico.")
        return None
    
    # Calcular o retorno logarítmico
    df['log_return'] = np.log(df['Ultimo'] / df['Ultimo'].shift(1))
    df.dropna(subset=['log_return'], inplace=True)

    if df.empty:
        print(f"O DataFrame {nome_cripto} ficou vazio após o cálculo do retorno logarítmico.")
        return None

    # Modelo GARCH (1,1)
    model = arch_model(df['log_return'], vol='Garch', p=1, q=1)
    garch_fit = model.fit()

    # Previsão da volatilidade para os próximos 10 dias
    forecast_horizon = 10
    forecasts = garch_fit.forecast(horizon=forecast_horizon)
    volatility_forecast = forecasts.variance.values[-1]

    # Criar DataFrame para previsões
    last_date = df['date'].max()
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon)
    forecast_df = pd.DataFrame(volatility_forecast, index=forecast_dates, columns=['forecast_volatility'])

    # Previsão do preço usando ARIMA
    arima_model = ARIMA(df['Ultimo'], order=(5, 1, 0))
    arima_fit = arima_model.fit()

    # Prever o preço para os próximos 10 dias
    price_forecast = arima_fit.forecast(steps=forecast_horizon)
    forecast_df['forecast_price'] = price_forecast

    # Adicionar a coluna do preço médio da semana passada para comparação
    one_week_ago = df.index[-7:]
    prices_last_week = df.loc[one_week_ago, 'Ultimo'].mean()

    forecast_df['previous_week_avg'] = prices_last_week

    # Adicionar sinal de compra
    forecast_df['buy_signal'] = forecast_df['forecast_price'] < forecast_df['previous_week_avg']

    # Obter previsões para os próximos 5 dias
    forecast_5_days = forecast_df.head(5)

    # Modelo Holt-Winters (Triple Exponential Smoothing)
    hw_model = ExponentialSmoothing(df['Ultimo'], trend='add', seasonal='add', seasonal_periods=7)
    hw_fit = hw_model.fit()

    # Prever os preços para os próximos 10 dias
    hw_forecast = hw_fit.forecast(steps=forecast_horizon)

    # Adicionar a previsão de Holt-Winters ao DataFrame de previsão
    forecast_df['holt_winters_forecast'] = hw_forecast.values

    # Diagnóstico das previsões
    print(f"Previsões de preços e sinais de compra para os próximos 5 dias ({nome_cripto}):")
    print(forecast_5_days)
    print(f"Descrição das previsões de preços e sinais de compra ({nome_cripto}):")
    print(forecast_5_days.describe())

    # Definir threshold baseado na volatilidade
    percentil = 10
    threshold = np.percentile(forecast_df['forecast_volatility'], percentil)
    best_forecast_days = forecast_df[forecast_df['forecast_volatility'] <= threshold]

    # Exibir os melhores dias para comprar
    print(f"Melhores dias para comprar {nome_cripto} (baseado em baixa volatilidade e previsão de preço menor que o preço da semana passada):")
    print(best_forecast_days)

    return [f'melhores dias: {best_forecast_days}', f'Previsão para os próximos dias: {forecast_5_days}', f'Holt-Winters Forecast: {hw_forecast.tail()}']


def executar_modelo():
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Caminho completo para os arquivos CSV
    csv_path_btc = os.path.join(current_dir, '/home/gabriellemitoso/modulo7-engcomp/ponderada-crypto/src/backend/database/dados-puros/bitcoin_daily_data.csv')
    csv_path_eth = os.path.join(current_dir, '/home/gabriellemitoso/modulo7-engcomp/ponderada-crypto/src/backend/database/dados-puros/ethereum_daily_data.csv')

    # Carregar os arquivos CSV
    df_btc = pd.read_csv(csv_path_btc)
    df_eth = pd.read_csv(csv_path_eth)

    # Processar DataFrames
    resultados_btc = processar_dataframe(df_btc, 'Bitcoin')
    resultados_eth = processar_dataframe(df_eth, 'Ethereum')

    # Exibir resultados
    if resultados_btc:
        for resultado in resultados_btc:
            print(resultado)
    
    if resultados_eth:
        for resultado in resultados_eth:
            print(resultado)

# Chamar a função
executar_modelo()