import sqlite3
import pandas as pd

from src.config.settings import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 10",
    conn,
)

print(df)

print("\n")

print(df.isnull().sum())

conn.close()