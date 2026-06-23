import pandas as pd

analysis = pd.read_csv("data/processed/analysis.csv")
companies = pd.read_csv("data/processed/companies.csv")

print(companies[companies["id"]=="WIPRO"])

valid_ids = set(companies["id"])

print("=" * 60)
print("Checking Analysis Foreign Keys")
print("=" * 60)

invalid = analysis[~analysis["company_id"].isin(valid_ids)]

if invalid.empty:
    print("No invalid company_ids found.")
else:
    print(invalid[["id", "company_id"]])