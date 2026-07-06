from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"

companies = pd.read_csv(PROCESSED / "companies.csv")

valid_ids = set(companies["id"].astype(str).str.strip().str.upper())

for file in sorted(PROCESSED.glob("*.csv")):

    if file.stem == "companies":
        continue

    df = pd.read_csv(file)

    if "company_id" not in df.columns:
        continue

    ids = df["company_id"].astype(str).str.strip().str.upper()

    invalid = df.loc[~ids.isin(valid_ids)]

    if len(invalid):

        print("=" * 60)
        print(file.stem)
        print("Invalid IDs:", len(invalid))
        print(invalid["company_id"].unique()[:20])