import logging
import sqlite3
import pandas as pd
import os
from config import DATA_DIR

#Conecta ao banco de dados SQLite
def conectar_db():
    try:
        conn = sqlite3.connect(DATA_DIR)
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

#Obtem dados da criptomoeda do banco de dados
def obter_dados_cripto(nome_cripto):
    conn = conectar_db()
    if conn is None:
        return None

    query = f"SELECT * FROM {nome_cripto}_daily_status"
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        logging.error(f"Erro ao obter dados da {nome_cripto}: {e}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    bitcoin_data = obter_dados_cripto('bitcoin')
    ethereum_data = obter_dados_cripto('ethereum')
