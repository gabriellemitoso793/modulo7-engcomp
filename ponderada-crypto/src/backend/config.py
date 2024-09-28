from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "database" / "dados-puros" / "crypto_data.db"  

FORECAST_HORIZON = 10
PERCENTIL_THRESHOLD = 10

# Verificando a existência do banco de dados
if not DATA_DIR.exists():
    print(f"Erro: O banco de dados não foi encontrado em {DATA_DIR}.")
else:
    print(f"Banco de dados encontrado em {DATA_DIR}.")

print(f"BASE_DIR: {BASE_DIR}")
print(f"DATA_DIR: {DATA_DIR}")
