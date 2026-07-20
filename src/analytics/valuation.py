import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = ROOT / "db" / "nifty100.db"
OUTPUT_DIR = ROOT / "data" / "output"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def generate_valuation():

    conn = sqlite3.connect(DATABASE_PATH)

    market = pd.read_sql(
        "SELECT * FROM market_cap",
        conn
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    latest_year = market["year"].max()

    market = market[
        market["year"] == latest_year
    ].copy()

    cashflow = cashflow[
        cashflow["year"] == latest_year
    ].copy()

    market = market.drop_duplicates(
        subset=["company_id"]
    )

    cashflow = cashflow.drop_duplicates(
        subset=["company_id"]
    )

    df = market.merge(
        sectors[
            ["company_id", "broad_sector"]
        ],
        on="company_id",
        how="left"
    )

    df = df.merge(
        companies[
            ["id", "company_name"]
        ],
        left_on="company_id",
        right_on="id",
        how="left"
    )

    df = df.merge(
        cashflow[
            ["company_id", "net_cash_flow"]
        ],
        on="company_id",
        how="left"
    )

    df["net_cash_flow"] = (
        df["net_cash_flow"]
        .fillna(0)
    )

    # FCF Yield
    df["FCF_yield_pct"] = (
        df["net_cash_flow"]
        /
        df["market_cap_crore"]
    ) * 100

    # Sector Median PE
    sector_pe = (
        df.groupby("broad_sector")["pe_ratio"]
        .median()
        .reset_index()
        .rename(
            columns={
                "pe_ratio": "5yr_median_PE"
            }
        )
    )

    df = df.merge(
        sector_pe,
        on="broad_sector",
        how="left"
    )

    # PE vs Sector Median
    df["PE_vs_sector_median_pct"] = (
        (
            df["pe_ratio"]
            -
            df["5yr_median_PE"]
        )
        /
        df["5yr_median_PE"]
    ) * 100

    # Flags
    def get_flag(row):

        if pd.isna(row["pe_ratio"]):
            return "Fair"

        if row["pe_ratio"] > (
            row["5yr_median_PE"] * 1.5
        ):
            return "Caution"

        elif row["pe_ratio"] < (
            row["5yr_median_PE"] * 0.7
        ):
            return "Discount"

        else:
            return "Fair"

    df["flag"] = df.apply(
        get_flag,
        axis=1
    )

    summary = df[
        [
            "company_id",
            "company_name",
            "broad_sector",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "FCF_yield_pct",
            "5yr_median_PE",
            "PE_vs_sector_median_pct",
            "flag"
        ]
    ].copy()

    summary.columns = [
        "company_id",
        "company_name",
        "sector",
        "P/E",
        "P/B",
        "EV/EBITDA",
        "FCF_yield_pct",
        "5yr_median_PE",
        "PE_vs_sector_median_pct",
        "flag"
    ]

    summary.to_excel(
        OUTPUT_DIR / "valuation_summary.xlsx",
        index=False
    )

    flags = summary[
        summary["flag"].isin(
            ["Caution", "Discount"]
        )
    ]

    flags.to_csv(
        OUTPUT_DIR / "valuation_flags.csv",
        index=False
    )

    conn.close()

    print(
        "valuation_summary.xlsx generated"
    )

    print(
        "valuation_flags.csv generated"
    )


if __name__ == "__main__":
    generate_valuation()