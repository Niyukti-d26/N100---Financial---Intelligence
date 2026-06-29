import sqlite3
import pandas as pd

from src.config.settings import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
]

for table in tables:

    print("\n" + "=" * 80)
    print(table.upper())
    print("=" * 80)

    df = pd.read_sql(
        f"""
        SELECT
            MIN(year) AS start_year,
            MAX(year) AS end_year,
            COUNT(DISTINCT year) AS total_years
        FROM {table}
        """,
        conn,
    )

    print(df)

conn.close()