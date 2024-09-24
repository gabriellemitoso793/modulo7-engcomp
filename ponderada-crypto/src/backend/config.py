from pathlib import Path

# Caminhos dos arquivos
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "database" / "dados-puros"

# Outros parâmetros de configuração
FORECAST_HORIZON = 10
PERCENTIL_THRESHOLD = 10
