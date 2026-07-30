import sqlite3

import pandas as pd

from src.analytics.cagr import calculate_cagr
from src.analytics.cashflow_kpis import (
    capex_intensity,
    fcf_conversion_rate,
    free_cash_flow,
)
from src.analytics.ratios import (
    asset_turnover,
    debt_to_equity,
    interest_coverage_ratio,
    net_profit_margin,
    operating_profit_margin,
    return_on_assets,
    return_on_capital_employed,
    return_on_equity,
)
from src.config.settings import DATABASE_PATH


def build_ratio_table():
    """Function: build_ratio_table"""
    conn = sqlite3.connect(DATABASE_PATH)

    print("=" * 80)
    print("BUILDING FINANCIAL RATIOS TABLE")
    print("=" * 80)

    # ---------------------------
    # RAW TABLES
    # ---------------------------
    pl = pd.read_sql("SELECT * FROM profitandloss", conn)
    bs = pd.read_sql("SELECT * FROM balancesheet", conn)
    cf = pd.read_sql("SELECT * FROM cashflow", conn)

    # ---------------------------
    # CLEAN MERGE
    # ---------------------------
    df = pl.merge(bs, on=["company_id", "year"], how="left").merge(
        cf, on=["company_id", "year"], how="left"
    )

    df["year"] = df["year"].astype(int)

    # remove duplicates (CRITICAL FIX)
    df = df.drop_duplicates(subset=["company_id", "year"], keep="first")
    df = df.sort_values(["company_id", "year"]).reset_index(drop=True)

    print("\nMerged Columns:")
    print(df.columns.tolist())

    results = []

    # ---------------------------
    # MAIN LOOP
    # ---------------------------
    for _, row in df.iterrows():

        company = row["company_id"]
        year = row["year"]

        # ---------------------------
        # FIXED CAGR LOOKBACK LOGIC
        # ---------------------------
        history = df[(df["company_id"] == company) & (df["year"] == year - 5)]

        if history.empty:
            revenue_cagr = None
            pat_cagr = None
            eps_cagr = None
        else:
            prev = history.iloc[0]

            revenue_cagr, _ = calculate_cagr(prev["sales"], row["sales"], 5)
            pat_cagr, _ = calculate_cagr(prev["net_profit"], row["net_profit"], 5)
            eps_cagr, _ = calculate_cagr(prev["eps"], row["eps"], 5)

        # ---------------------------
        # RATIOS
        # ---------------------------
        npm = net_profit_margin(row["net_profit"], row["sales"])
        opm = operating_profit_margin(row["operating_profit"], row["sales"])

        roe = return_on_equity(
            row["net_profit"],
            row["equity_capital"],
            row["reserves"],
        )

        roce = return_on_capital_employed(
            row["operating_profit"],
            row["equity_capital"],
            row["reserves"],
            row["borrowings"],
        )

        roa = return_on_assets(row["net_profit"], row["total_assets"])

        de = debt_to_equity(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"],
        )

        icr = interest_coverage_ratio(
            row["operating_profit"],
            row["other_income"],
            row["interest"],
        )

        asset_turn = asset_turnover(row["sales"], row["total_assets"])

        fcf = free_cash_flow(
            row["operating_activity"],
            row["investing_activity"],
        )

        capex_pct, capex_label = capex_intensity(
            row["investing_activity"],
            row["sales"],
        )

        fcf_rate = fcf_conversion_rate(fcf, row["operating_profit"])

        book_value = None
        if row["equity_capital"] > 0:
            book_value = (row["equity_capital"] + row["reserves"]) / row[
                "equity_capital"
            ]

        # ---------------------------
        # QUALITY SCORE
        # ---------------------------
        scores = [roe, roce, roa, opm]
        scores = [s for s in scores if s is not None]

        quality = sum(scores) / len(scores) if scores else None

        # ---------------------------
        # FINAL ROW
        # ---------------------------
        results.append(
            {
                "company_id": company,
                "year": year,
                "earnings_per_share": row["eps"],
                "dividend_payout_ratio_pct": row["dividend_payout"],
                "total_debt_cr": row["borrowings"],
                "cash_from_operations_cr": row["operating_activity"],
                "net_profit_margin_pct": npm,
                "operating_profit_margin_pct": opm,
                "return_on_equity_pct": roe,
                "return_on_capital_employed_pct": roce,
                "return_on_assets_pct": roa,
                "debt_to_equity": de,
                "interest_coverage": icr,
                "asset_turnover": asset_turn,
                "free_cash_flow_cr": fcf,
                "capex_pct": capex_pct,
                "capex_label": capex_label,
                "fcf_conversion_pct": fcf_rate,
                "book_value_per_share": book_value,
                "revenue_cagr_5yr": revenue_cagr,
                "pat_cagr_5yr": pat_cagr,
                "eps_cagr_5yr": eps_cagr,
                "composite_quality_score": quality,
            }
        )

    # ---------------------------
    # FINAL OUTPUT
    # ---------------------------
    output = pd.DataFrame(results)

    print("\nFINAL ROWS:", len(output))

    output.to_sql("financial_ratios", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print("=" * 80)
    print("RATIO ENGINE COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":

    build_ratio_table()
