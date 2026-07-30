import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

ticker = "ATGL"

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "analysis",
    "prosandcons"
]


for table in tables:

    print("\n==========================")
    print(table)

    try:
        df = pd.read_sql(
            f"""
            SELECT *
            FROM {table}
            WHERE company_id='{ticker}'
            """,
            conn
        )

        print("Rows:", len(df))
        print(df.head())

    except Exception as e:
        print("ERROR:", e)


conn.close()