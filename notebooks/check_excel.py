import pandas as pd

excel = pd.ExcelFile("data/raw/profitandloss.xlsx")

print("Sheet Names:")
print(excel.sheet_names)

for sheet in excel.sheet_names:
    df = pd.read_excel(excel, sheet_name=sheet, header=None)

    print("\n" + "=" * 60)
    print(sheet)
    print("Rows:", len(df))
    print(df.head(10))