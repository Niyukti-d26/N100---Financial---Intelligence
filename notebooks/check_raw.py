import pandas as pd
from src.config.settings import RAW_DATA_DIR, HEADER_ROWS

file = "profitandloss.xlsx"

header = HEADER_ROWS[file]

df = pd.read_excel(
    RAW_DATA_DIR / file,
    header=header,
)

duplicates = df[df.duplicated()]

print("Total rows :", len(df))
print("Duplicate rows :", len(duplicates))

print()

print(duplicates.head(20))