from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

file = PROJECT_ROOT / "data" / "output" / "validation_failures.csv"

df = pd.read_csv(file)

print("=" * 60)
print("TOTAL ISSUES")
print("=" * 60)
print(len(df))

print("\n")

print("=" * 60)
print("ISSUES BY RULE")
print("=" * 60)
print(df["rule"].value_counts())

print("\n")

print("=" * 60)
print("ISSUES BY SEVERITY")
print("=" * 60)
print(df["severity"].value_counts())

print("\n")

print("=" * 60)
print("TOP 20 FAILURES")
print("=" * 60)
print(df.head(20))