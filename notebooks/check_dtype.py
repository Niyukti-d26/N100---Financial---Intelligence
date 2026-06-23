import pandas as pd

companies = pd.read_csv("data/processed/companies.csv")
prices = pd.read_csv("data/processed/stock_prices.csv")

print(companies["id"].dtype)
print(prices["company_id"].dtype)

print(companies["id"].head())
print(prices["company_id"].head())