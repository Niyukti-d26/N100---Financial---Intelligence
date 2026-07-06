import sqlite3
import pandas as pd

from src.config.settings import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        return_on_capital_employed_pct
    FROM financial_ratios
    WHERE year = 2024
    """,
    conn,
)

conn.close()

companies = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1,
)

companies = companies.rename(
    columns={
        "id": "company_id"
    }
)

companies["company_id"] = companies["company_id"].astype(str).str.strip()
ratios["company_id"] = ratios["company_id"].astype(str).str.strip()

df = ratios.merge(
    companies[
        [
            "company_id",
            "roe_percentage",
            "roce_percentage",
        ]
    ],
    on="company_id",
    how="inner",
)

log = []

for _, row in df.iterrows():

    if pd.notna(row["roe_percentage"]):

        roe_diff = abs(
            row["return_on_equity_pct"]
            - row["roe_percentage"]
        )

        if roe_diff > 5:

            log.append(
f"""
============================================================
Company : {row.company_id}
Year : 2024
Metric : ROE

Ratio Engine : {row.return_on_equity_pct:.2f}
Source Value : {row.roe_percentage:.2f}
Difference : {roe_diff:.2f}

Category : Pending
============================================================
"""
            )

    if pd.notna(row["roce_percentage"]):

        roce_diff = abs(
            row["return_on_capital_employed_pct"]
            - row["roce_percentage"]
        )

        if roce_diff > 5:

            log.append(
f"""
============================================================
Company : {row.company_id}
Year : 2024
Metric : ROCE

Ratio Engine : {row.return_on_capital_employed_pct:.2f}
Source Value : {row.roce_percentage:.2f}
Difference : {roce_diff:.2f}

Category : Pending
============================================================
"""
            )

with open(
    "data/output/ratio_edge_cases.log",
    "w",
    encoding="utf-8",
) as f:

    if len(log) == 0:
        f.write("No edge cases found.\n")
    else:
        f.write("\n".join(log))

print("=" * 60)
print("EDGE CASE LOG GENERATED")
print("=" * 60)
print(f"Companies Compared : {len(df)}")
print(f"Total Anomalies : {len(log)}")
print("Saved to : output/ratio_edge_cases.log")