import pandas as pd

df = pd.read_excel(
    "data/output/screener_output.xlsx"
)

df.to_csv(
    "data/output/test_export.csv",
    index=False
)

check = pd.read_csv(
    "data/output/test_export.csv"
)

print(
    "Original Rows =",
    len(df)
)

print(
    "Export Rows =",
    len(check)
)