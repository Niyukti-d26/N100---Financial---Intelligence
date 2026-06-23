import pandas as pd

companies = pd.read_csv("data/processed/companies.csv")
prices = pd.read_csv("data/processed/stock_prices.csv")

valid = set(companies["id"])

invalid = prices[~prices["company_id"].isin(valid)]

print("Invalid rows:", len(invalid))
print(invalid[["company_id"]].drop_duplicates())