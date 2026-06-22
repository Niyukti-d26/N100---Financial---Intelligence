import pandas as pd

df = pd.read_csv("data/processed/profitandloss.csv")

rows = df[
    (df["company_id"] == "ADANIPORTS") &
    (df["year"] == 2013)
]

print(rows)

print("\n")

print(rows.drop(columns=["id"]).duplicated())

print("\n")

print(rows.drop(columns=["id"]))