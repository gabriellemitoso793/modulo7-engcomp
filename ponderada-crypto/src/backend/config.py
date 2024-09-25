from pathlib import Path

# Caminhos dos arquivos
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "database" / "dados-puros"

# Outros parâmetros de configuração
FORECAST_HORIZON = 10
PERCENTIL_THRESHOLD = 10

# Para verificar o caminho durante a execução
print(f"BASE_DIR: {BASE_DIR}")
print(f"DATA_DIR: {DATA_DIR}")
