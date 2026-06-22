import pandas as pd
from pathlib import Path

file = Path("data/output/validation_failures.csv")

df = pd.read_csv(file)

print("\nIssues by Rule")
print("=" * 40)
print(df["rule"].value_counts())

print("\nIssues by Severity")
print("=" * 40)
print(df["severity"].value_counts())