import sqlite3
import pandas as pd

from src.config.settings import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

df = pd.read_sql("""
SELECT
    company_id,
    year,
    return_on_equity_pct,
    revenue_cagr_5yr
FROM financial_ratios
ORDER BY company_id, year
""", conn)

file_path = "verification/day12_manual_verification.xlsx"

with pd.ExcelWriter(
    file_path,
    engine="openpyxl",
    mode="a",
    if_sheet_exists="replace"
) as writer:
    df.to_excel(writer, sheet_name="DB_VALUES", index=False)

conn.close()

print("DB_VALUES sheet exported successfully.")