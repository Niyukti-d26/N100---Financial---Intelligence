import pandas as pd

companies = pd.read_csv("data/processed/companies.csv")

print("Total Companies :", len(companies))

print()

print(companies["id"].tolist())