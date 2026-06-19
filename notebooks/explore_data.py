import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")

print("=" * 100)
print("N100 DATASET EXPLORER")
print("=" * 100)

files = sorted(RAW_DATA.glob("*.xlsx"))

for file in files:

    print("\n" + "=" * 100)
    print(f"FILE : {file.name}")
    print("=" * 100)

    excel = pd.ExcelFile(file)

    print(f"Sheets : {excel.sheet_names}")

    for sheet in excel.sheet_names:

        print(f"\nSheet : {sheet}")

        preview = pd.read_excel(file, sheet_name=sheet, header=None)

        print("\nFirst 5 Raw Rows")
        print(preview.head())

        if str(preview.iloc[1, 0]).lower() == "id":
            header_row = 1
        elif str(preview.iloc[0, 0]).lower() == "id":
            header_row = 0
        else:
            header_row = 0

        print(f"\nDetected Header Row : {header_row}")

        df = pd.read_excel(file, sheet_name=sheet, header=header_row)

        print(f"Rows    : {df.shape[0]}")
        print(f"Columns : {df.shape[1]}")

        print("\nColumn Names")

        for column in df.columns:
            print(f"   • {column}")

        print("\nMissing Values")

        print(df.isnull().sum())

        print("\nData Types")

        print(df.dtypes)

        print("\nFirst Five Records")

        print(df.head())

        print("\n" + "-" * 100)