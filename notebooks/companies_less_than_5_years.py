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
            company_id,
            COUNT(DISTINCT year) AS total_years
        FROM {table}
        GROUP BY company_id
        HAVING COUNT(DISTINCT year) < 5
        ORDER BY total_years
        """,
        conn,
    )

    if df.empty:
        print("No companies found.")
    else:
        print(df)

conn.close()