import pandas as pd
from src.config.settings import RAW_DATA_DIR

df = pd.read_excel(
    RAW_DATA_DIR / "companies.xlsx",
    header=1
)

print("="*60)
print("Columns")
print("="*60)
print(df.columns)

print("\n")

print("="*60)
print("Search in First Column")
print("="*60)
print(df[df.iloc[:,0].astype(str).str.contains("WIPRO", case=False, na=False)])

print("\n")

print("="*60)
print("Search Entire Excel")
print("="*60)
print(
    df[
        df.astype(str)
          .apply(lambda x: x.str.contains("WIPRO", case=False, na=False))
          .any(axis=1)
    ]
)