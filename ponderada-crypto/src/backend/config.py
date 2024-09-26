from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "database" / "dados-puros"

FORECAST_HORIZON = 10
PERCENTIL_THRESHOLD = 10

print(f"BASE_DIR: {BASE_DIR}")
print(f"DATA_DIR: {DATA_DIR}")
