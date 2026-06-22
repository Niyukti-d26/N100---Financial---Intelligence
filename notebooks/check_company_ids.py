import pandas as pd

companies = pd.read_csv("data/processed/companies.csv")
documents = pd.read_csv("data/processed/documents.csv")
pros = pd.read_csv("data/processed/prosandcons.csv")

print("=" * 60)
print("Companies")
print("=" * 60)

print(companies["id"].tail(20))

print("\n")

print("=" * 60)
print("Documents")
print("=" * 60)

print(documents["company_id"].tail(20))

print("\n")

print("=" * 60)
print("Pros & Cons")
print("=" * 60)

print(pros["company_id"])