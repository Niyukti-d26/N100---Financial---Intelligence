import sqlite3

import pandas as pd

from src.analytics.cashflow_kpis import (
    capital_allocation_pattern,
    cfo_quality_score,
)
from src.config.settings import DATABASE_PATH


def build_capital_allocation():
    """Function: build_capital_allocation"""
    conn = sqlite3.connect(DATABASE_PATH)

    cashflow = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        """,
        conn,
    )

    ratios = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            cash_from_operations_cr,
            free_cash_flow_cr
        FROM financial_ratios
        """,
        conn,
    )

    pl = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            net_profit
        FROM profitandloss
        """,
        conn,
    )

    cashflow = cashflow.dropna(subset=["year"])
    pl = pl.dropna(subset=["year"])
    ratios = ratios.dropna(subset=["year"])

    cashflow["year"] = cashflow["year"].astype(int)
    pl["year"] = pl["year"].astype(int)
    ratios["year"] = ratios["year"].astype(int)

    df = cashflow.merge(
        pl,
        on=["company_id", "year"],
        how="left",
    ).merge(
        ratios,
        on=["company_id", "year"],
        how="left",
    )

    records = []

    for _, row in df.iterrows():

        quality = cfo_quality_score(row["operating_activity"], row["net_profit"])

        pattern = capital_allocation_pattern(
            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"],
            quality,
        )

        records.append(
            {
                "company_id": row["company_id"],
                "year": row["year"],
                "capital_allocation_label": pattern,
            }
        )

    output = pd.DataFrame(records)

    output.to_sql(
        "capital_allocation",
        conn,
        if_exists="replace",
        index=False,
    )

    output.to_csv(
        "data/output/capital_allocation.csv",
        index=False,
    )

    conn.close()

    print("Capital Allocation Rows:", len(output))


if __name__ == "__main__":
    build_capital_allocation()
