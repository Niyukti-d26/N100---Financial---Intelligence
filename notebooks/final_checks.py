import sqlite3

from src.config.settings import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "financial_ratios",
    "peer_groups",
    "stock_prices",
]

print("=" * 70)
print("TABLE COUNTS")
print("=" * 70)

for table in tables:

    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table:<20} {count}")

print("\n")

fk = conn.execute(
    "PRAGMA foreign_key_check"
).fetchall()

print("=" * 70)
print("FOREIGN KEY CHECK")
print("=" * 70)

print("Violations :", len(fk))

conn.close()