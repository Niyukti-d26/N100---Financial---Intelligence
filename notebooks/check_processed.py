import pandas as pd

df = pd.read_csv("data/processed/companies.csv")

print(df[df["id"] == "WIPRO"])