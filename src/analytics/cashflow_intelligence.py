import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

DB_PATH = ROOT / "db" / "nifty100.db"

OUTPUT_DIR = ROOT / "data" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

balancesheet = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()


records = []
distress_records = []

companies = ratios["company_id"].unique()


for company in companies:

    r = ratios[
        ratios["company_id"] == company
    ].copy()

    cf = cashflow[
        cashflow["company_id"] == company
    ].copy()

    bs = balancesheet[
        balancesheet["company_id"] == company
    ].copy()

    sector_row = sectors[
        sectors["company_id"] == company
    ]

    sector = (
        sector_row["broad_sector"].iloc[0]
        if not sector_row.empty
        else "Unknown"
    )

    r = r.dropna(subset=["year"])
    cf = cf.dropna(subset=["year"])
    bs = bs.dropna(subset=["year"])

    r = r.sort_values("year")
    cf = cf.sort_values("year")
    bs = bs.sort_values("year")

    r = r.drop_duplicates(
        subset=["year"],
        keep="last"
    )

    cf = cf.drop_duplicates(
        subset=["year"],
        keep="last"
    )

    bs = bs.drop_duplicates(
        subset=["year"],
        keep="last"
    )

    if r.empty:
        continue

    latest_ratio = r.iloc[-1]

    # --------------------------------
    # CFO QUALITY
    # --------------------------------

    if (
        "cash_from_operations_cr" in r.columns
        and len(r) > 0
    ):

        cfo_pat = (
            r["cash_from_operations_cr"]
            /
            r["free_cash_flow_cr"].replace(
                0,
                np.nan
            )
        )

        cfo_quality_score = round(
            cfo_pat.mean(skipna=True),
            2
        )

    else:

        cfo_quality_score = np.nan

    if cfo_quality_score > 1:

        cfo_quality_label = "High Quality"

    elif cfo_quality_score >= 0.5:

        cfo_quality_label = "Moderate"

    else:

        cfo_quality_label = "Accrual Risk"

    # --------------------------------
    # CAPEX INTENSITY
    # --------------------------------

    capex_intensity = latest_ratio.get(
        "capex_pct",
        np.nan
    )

    capex_label = latest_ratio.get(
        "capex_label",
        "Unknown"
    )

    # --------------------------------
    # FCF CAGR
    # --------------------------------

    fcf_series = (
        r["free_cash_flow_cr"]
        .dropna()
        .tail(5)
    )

    fcf_cagr = np.nan

    if len(fcf_series) >= 2:

        first = fcf_series.iloc[0]
        last = fcf_series.iloc[-1]

        if first > 0 and last > 0:

            years = len(fcf_series) - 1

            fcf_cagr = round(
                (
                    (last / first)
                    ** (1 / years)
                    - 1
                )
                * 100,
                2
            )

    # --------------------------------
    # FCF CONVERSION
    # --------------------------------

    fcf_conversion = latest_ratio.get(
        "fcf_conversion_pct",
        np.nan
    )

    # --------------------------------
    # DISTRESS FLAG
    # CFO < 0 and CFF > 0
    # --------------------------------

    distress_flag = False

    if not cf.empty:

        latest_cf = cf.iloc[-1]

        cfo = latest_cf.get(
            "operating_activity",
            0
        )

        cff = latest_cf.get(
            "financing_activity",
            0
        )

        if (
            cfo < 0
            and cff > 0
        ):

            distress_flag = True

            distress_records.append(
                {
                    "company_id": company,
                    "cfo_value": cfo,
                    "cff_value": cff
                }
            )

    # --------------------------------
    # DELEVERAGING FLAG
    # --------------------------------

    deleveraging_flag = False

    if (
        len(bs) >= 2
        and not cf.empty
    ):

        latest_cf = cf.iloc[-1]

        current_borrowings = (
            bs.iloc[-1]["borrowings"]
        )

        previous_borrowings = (
            bs.iloc[-2]["borrowings"]
        )

        if (
            latest_cf["financing_activity"] < 0
            and current_borrowings
            < previous_borrowings
        ):

            deleveraging_flag = True

    # --------------------------------
    # CAPITAL ALLOCATION LABEL
    # --------------------------------

    if distress_flag:

        capital_allocation = (
            "Distress Signal"
        )

    elif deleveraging_flag:

        capital_allocation = (
            "Deleveraging"
        )

    elif capex_intensity > 8:

        capital_allocation = (
            "Reinvestor"
        )

    else:

        capital_allocation = (
            "Balanced"
        )

    records.append(
        {
            "company_id": company,
            "sector": sector,
            "cfo_quality_score":
                cfo_quality_score,
            "cfo_quality_label":
                cfo_quality_label,
            "capex_intensity_pct":
                capex_intensity,
            "capex_label":
                capex_label,
            "fcf_cagr_5yr":
                fcf_cagr,
            "fcf_conversion_pct":
                fcf_conversion,
            "distress_flag":
                distress_flag,
            "deleveraging_flag":
                deleveraging_flag,
            "capital_allocation_label":
                capital_allocation,
        }
    )


cashflow_intelligence = pd.DataFrame(records)

cashflow_intelligence.to_excel(
    OUTPUT_DIR /
    "cashflow_intelligence.xlsx",
    index=False
)

distress_df = pd.DataFrame(
    distress_records
)

distress_df.to_csv(
    OUTPUT_DIR /
    "distress_alerts.csv",
    index=False
)

print(
    "Cashflow Intelligence Rows:",
    len(cashflow_intelligence)
)

print(
    "Distress Alerts:",
    len(distress_df)
)