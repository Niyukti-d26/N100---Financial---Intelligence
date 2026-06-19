from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"

DATABASE_DIR = PROJECT_ROOT / "db"
DATABASE_PATH = DATABASE_DIR / "nifty100.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"

LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "etl.log"

NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
TEST_DIR = PROJECT_ROOT / "tests"

EXCEL_FILES = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "market_cap": "market_cap.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx",
}

HEADER_ROWS = {
    "companies.xlsx": 1,
    "profitandloss.xlsx": 1,
    "balancesheet.xlsx": 1,
    "cashflow.xlsx": 1,
    "analysis.xlsx": 1,
    "documents.xlsx": 1,
    "prosandcons.xlsx": 1,
    "financial_ratios.xlsx": 0,
    "market_cap.xlsx": 0,
    "peer_groups.xlsx": 0,
    "sectors.xlsx": 0,
    "stock_prices.xlsx": 0,
}

TABLES = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "sectors",
    "stock_prices",
]

for directory in [
    OUTPUT_DIR,
    PROCESSED_DATA_DIR,
    LOG_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)