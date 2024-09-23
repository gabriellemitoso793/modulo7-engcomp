import requests
import pandas as pd
import numpy as np

# função para puxar dados da API CoinGecko
def fetch_data_from_api(base_url, params):
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao coletar dados: {response.status_code}")
        print(response.json())
        return None

# função para processar os dados em DataFrames
def process_data(data):
    prices = data["prices"]
    volumes = data["total_volumes"]

    df_prices = pd.DataFrame(prices, columns=["timestamp", "price"])
    df_prices["timestamp"] = pd.to_datetime(df_prices["timestamp"], unit='ms')

    df_volumes = pd.DataFrame(volumes, columns=["timestamp", "volume"])
    df_volumes["timestamp"] = pd.to_datetime(df_volumes["timestamp"], unit='ms')
    
    df = pd.merge(df_prices, df_volumes, on="timestamp")
    return df

# função para calcular as métricas 
def calculate_daily_stats(df):
    daily_stats = df.groupby(df["timestamp"].dt.date).agg(
        open_price=("price", "first"),
        close_price=("price", "last"),
        min_price=("price", "min"),
        max_price=("price", "max"),
        total_volume=("volume", "sum")
    )
    
    daily_stats['7_day_MA'] = daily_stats['close_price'].rolling(window=7).mean()
    daily_stats['daily_return'] = daily_stats['close_price'].pct_change()
    daily_stats['volatility'] = daily_stats['daily_return'].rolling(window=7).std()
    daily_stats['VWAP'] = (df['price'] * df['volume']).cumsum() / df['volume'].cumsum()
    
    delta = daily_stats['close_price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    RS = gain / loss
    daily_stats['RSI'] = 100 - (100 / (1 + RS))
    
    daily_stats.index.name = 'date'
    
    return daily_stats

# função para salvar em arquivo CSV
def save_to_csv(df, filename):
    df.to_csv(filename)
    print(f"Estatísticas diárias salvas com sucesso em {filename}!")

# função principal para Bitcoin e Ethereum
def main():
    # Dados do Bitcoin
    base_url_bitcoin = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "365",
        "interval": "daily"
    }
    
    # Coleta e processamento de dados do Bitcoin
    data_bitcoin = fetch_data_from_api(base_url_bitcoin, params)
    
    if data_bitcoin:
        df_bitcoin = process_data(data_bitcoin)
        daily_stats_bitcoin = calculate_daily_stats(df_bitcoin)
        print(daily_stats_bitcoin.head())
        save_to_csv(daily_stats_bitcoin, "bitcoin_daily_data.csv")
    
    # Dados do Ethereum
    base_url_ethereum = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
    
    # Coleta e processamento de dados do Ethereum
    data_ethereum = fetch_data_from_api(base_url_ethereum, params)
    
    if data_ethereum:
        df_ethereum = process_data(data_ethereum)
        daily_stats_ethereum = calculate_daily_stats(df_ethereum)
        print(daily_stats_ethereum.head())
        save_to_csv(daily_stats_ethereum, "ethereum_daily_data.csv")

if __name__ == "__main__":
    main()
