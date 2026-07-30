import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios"
]

for table in tables:
    print("\n===================")
    print("TABLE:", table)

    df = pd.read_sql(
        f"PRAGMA table_info({table})",
        conn
    )

    print(df[["name", "type"]].to_string(index=False))

conn.close()