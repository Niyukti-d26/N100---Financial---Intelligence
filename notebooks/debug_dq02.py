import pandas as pd
from pathlib import Path

processed = Path("data/processed")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap",
]

for table in tables:

    print("\n" + "=" * 80)
    print(table.upper())
    print("=" * 80)

    df = pd.read_csv(processed / f"{table}.csv")

    duplicates = df[
        df.duplicated(
            subset=["company_id", "year"],
            keep=False,
        )
    ]

    print(f"Duplicate Rows : {len(duplicates)}")

    if len(duplicates) > 0:
        print(
            duplicates[
                ["company_id", "year", "id"]
            ]
            .sort_values(["company_id", "year"])
            .head(30)
        )