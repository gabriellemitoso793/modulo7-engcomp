import pandas as pd
import numpy as np
import warnings
import logging
import os
from arch import arch_model
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.preprocessing import MinMaxScaler
from config import DATA_DIR
from statsmodels.tools.sm_exceptions import ConvergenceWarning

def processar_dataframe(df, nome_cripto):
    logging.info(f"Colunas do DataFrame {nome_cripto}: {df.columns}")

    # Renomeando colunas
    df.rename(columns={
        'open_price': 'Abertura',
        'close_price': 'Ultimo',
        'total_volume': 'Vol',
        'max_price': 'Maxima',
        'min_price': 'Minima',
        'volatility': 'Volatilidade'
    }, inplace=True)

    required_columns = ['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logging.error(f"As seguintes colunas estão faltando no DataFrame {nome_cripto}: {missing_columns}")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    scaler = MinMaxScaler()
    df[['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']] = scaler.fit_transform(df[['Abertura', 'Ultimo', 'Vol', 'Maxima', 'Minima', 'Volatilidade']])

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
    df.dropna(subset=['date', 'Ultimo'], inplace=True)

    df['Ultimo'] = df['Ultimo'].replace(0, np.nan)
    df.dropna(subset=['Ultimo'], inplace=True)

    if df['Ultimo'].nunique() <= 1:
        logging.error(f"A coluna 'Ultimo' do {nome_cripto} contém valores idênticos ou não variáveis.")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}
    
    df['log_return'] = np.log(df['Ultimo'] / df['Ultimo'].shift(1))
    df.dropna(subset=['log_return'], inplace=True)

    if df.empty:
        logging.error(f"O DataFrame {nome_cripto} ficou vazio após o cálculo do retorno logarítmico.")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    model = arch_model(df['log_return'], vol='Garch', p=1, q=1)
    garch_fit = model.fit(disp='off')

    forecast_horizon = 10
    forecasts = garch_fit.forecast(horizon=forecast_horizon)
    volatility_forecast = forecasts.variance.values[-1]

    last_date = df['date'].max()
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon)
    forecast_df = pd.DataFrame(volatility_forecast, index=forecast_dates, columns=['forecast_volatility'])

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', ConvergenceWarning)
        try:
            arima_model = ARIMA(df['Ultimo'], order=(5, 1, 0))
            arima_fit = arima_model.fit()
        except Exception as e:
            logging.error(f"Erro ao ajustar o modelo ARIMA para {nome_cripto}: {e}")
            return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    price_forecast = arima_fit.forecast(steps=forecast_horizon)
    price_forecast_full = np.full((len(price_forecast), 6), np.nan)
    price_forecast_full[:, 1] = price_forecast.values
    price_forecast_inverse = scaler.inverse_transform(price_forecast_full)
    price_forecast = price_forecast_inverse[:, 1]
    forecast_df['forecast_price'] = price_forecast

    one_week_ago = df.index[-7:]
    prices_last_week = df.loc[one_week_ago, 'Ultimo'].mean()
    forecast_df['previous_week_avg'] = prices_last_week
    forecast_df['buy_signal'] = forecast_df['forecast_price'] < forecast_df['previous_week_avg']

    forecast_5_days = forecast_df.head(5)

    try:
        hw_model = ExponentialSmoothing(df['Ultimo'], trend='add', seasonal='add', seasonal_periods=7)
        hw_fit = hw_model.fit()
    except Exception as e:
        logging.error(f"Erro ao ajustar o modelo Holt-Winters para {nome_cripto}: {e}")
        return {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}

    hw_forecast = hw_fit.forecast(steps=forecast_horizon)
    hw_forecast_scaled = scaler.transform(np.full((len(hw_forecast), 6), np.nan))
    hw_forecast_scaled[:, 1] = hw_forecast.values
    hw_forecast_inverse = scaler.inverse_transform(hw_forecast_scaled)
    forecast_df['holt_winters_forecast'] = hw_forecast_inverse[:, 1]

    percentil = 10
    threshold = np.percentile(forecast_df['forecast_volatility'], percentil)
    best_forecast_days = forecast_df[forecast_df['forecast_volatility'] <= threshold]

    return {
        'melhores_dias': best_forecast_days,
        'previsao_proximos_dias': forecast_5_days,
        'holt_winters_forecast': forecast_df['holt_winters_forecast'].tolist()
    }

def executar_modelo():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path_btc = os.path.join(DATA_DIR, 'bitcoin_daily_data.csv')
    csv_path_eth = os.path.join(DATA_DIR, 'ethereum_daily_data.csv')

    df_btc = pd.read_csv(csv_path_btc)
    df_eth = pd.read_csv(csv_path_eth)

    resultados_btc = processar_dataframe(df_btc, 'Bitcoin')
    resultados_eth = processar_dataframe(df_eth, 'Ethereum')

    resultados = {}
    resultados['bitcoin'] = resultados_btc if resultados_btc else {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}
    resultados['ethereum'] = resultados_eth if resultados_eth else {'melhores_dias': [], 'previsao_proximos_dias': [], 'holt_winters_forecast': []}
    
    return resultados

if __name__ == "__main__":
    resultados = executar_modelo()
    print(resultados)
