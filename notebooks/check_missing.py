import pandas as pd

companies = pd.read_csv("data/processed/companies.csv")

company_ids = set(companies["id"])

tables = [
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

for table in tables:

    df = pd.read_csv(f"data/processed/{table}.csv")

    if "company_id" not in df.columns:
        continue

    missing = sorted(set(df["company_id"]) - company_ids)

    if missing:

        print("=" * 60)
        print(table)
        print("Missing Companies:")
        print(missing)
        