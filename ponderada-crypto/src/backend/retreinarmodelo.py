import requests
import pandas as pd
from arch import arch_model
from sklearn.metrics import mean_squared_error
import datetime

# URL da API da CoinGecko para obter dados de Bitcoin e Ethereum
API_URL = "https://api.coingecko.com/api/v3/coins/{}/market_chart?vs_currency=usd&days=30"
CURRENT_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"

# Função para obter dados de preços
def obter_dados(coin):
    response = requests.get(API_URL.format(coin))
    data = response.json()
    
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    
    # Converter timestamp para datetime e ajustar o DataFrame
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['return'] = df['price'].pct_change().dropna()
    
    return df.dropna(), df['price'].iloc[-1]  # Retornar o preço atual também

# Função para treinar o modelo GARCH
def treinar_modelo(df):
    model = arch_model(df['return'] * 100, vol='Garch', p=1, q=1)
    model_fitted = model.fit(disp="off")
    return model_fitted

# Função para validar o modelo
def validar_modelo(model_fitted, df, current_price):
    returns = df['return'] * 100
    forecast = model_fitted.forecast(horizon=len(returns))
    
    # Obter as previsões de variância da última previsão
    predictions = forecast.variance.iloc[-1].values
    
    if len(returns) != len(predictions):
        returns = returns.iloc[-len(predictions):]  # Ajusta o tamanho dos dados reais
    
    mse = mean_squared_error(returns, predictions)
    
    # Previsão para os próximos 10 dias
    forecast_10_days = model_fitted.forecast(horizon=10)
    forecast_returns = forecast_10_days.mean.iloc[-1].values
    
    # Calcular os preços futuros a partir do preço atual
    future_prices = [current_price * (1 + forecast_return / 100) for forecast_return in forecast_returns]
    
    return mse, future_prices

# Função principal para retreinar o modelo
def retreinar_modelo():
    coins = ['bitcoin', 'ethereum']
    resultados = {}
    
    for coin in coins:
        print(f"Carregando dados para {coin}...")
        df, current_price = obter_dados(coin)
        
        print(f"Treinando o modelo para {coin}...")
        modelo = treinar_modelo(df)
        
        print(f"Validando o modelo para {coin}...")
        mse, forecast_prices = validar_modelo(modelo, df, current_price)
        
        resultados[coin.capitalize()] = {
            'modelo': 'GARCH',
            'validacao_accuracy': 1 - mse,  # Convertendo MSE para uma forma de acurácia
            'data_validacao': datetime.datetime.now(),
            'tamanho_dados': len(df),
            'previsao_proximos_dias': forecast_prices  # Previsões de preços reais
        }
    
    print("*** Resultados Finais do Re-Treinamento ***")
    print(resultados)

if __name__ == "__main__":
    retreinar_modelo()
