import sqlite3
import random
import pandas as pd

from src.config.settings import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

companies = pd.read_sql(
    "SELECT id FROM companies",
    conn,
)

sample = random.sample(companies["id"].tolist(), 5)

print("=" * 80)
print("RANDOMLY SELECTED COMPANIES")
print("=" * 80)

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
]

for company in sample:

    print("\n" + "=" * 80)
    print(company)
    print("=" * 80)

    for table in tables:

        df = pd.read_sql(
            f"""
            SELECT year
            FROM {table}
            WHERE company_id = ?
            ORDER BY year
            """,
            conn,
            params=[company],
        )

        years = (
            df["year"]
            .dropna()
            .astype(int)
            .tolist()
        )

        print(f"{table:<20} {years}")
conn.close()