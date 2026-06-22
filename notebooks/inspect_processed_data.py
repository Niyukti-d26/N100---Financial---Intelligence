from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

print("=" * 100)
print("PROCESSED DATASET SCHEMA")
print("=" * 100)

for file in sorted(PROCESSED_DIR.glob("*.csv")):

    print("\n" + "=" * 100)
    print(f"Dataset : {file.stem}")
    print("=" * 100)

    df = pd.read_csv(file, nrows=5)

    print(f"Rows (sample): {len(df)}")
    print(f"Columns ({len(df.columns)}):\n")

    for i, column in enumerate(df.columns, start=1):
        print(f"{i:2}. {column}")

    print("\nFirst 5 Rows:\n")
    print(df.head())

print("\n")
print("=" * 100)
print("SCHEMA INSPECTION COMPLETED")
print("=" * 100)