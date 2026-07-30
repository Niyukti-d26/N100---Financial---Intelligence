import sqlite3

import pandas as pd

from src.config.settings import DATABASE_PATH


def run_day32():
    """Function: run_day32"""
    conn = sqlite3.connect(DATABASE_PATH)

    # --------------------------------------------------
    # Load capital allocation table
    # --------------------------------------------------

    capital = pd.read_sql(
        """
        SELECT *
        FROM capital_allocation
        """,
        conn,
    )

    # --------------------------------------------------
    # Latest year
    # --------------------------------------------------

    latest_year = capital["year"].max()

    latest = capital[capital["year"] == latest_year].copy()

    # --------------------------------------------------
    # 1. Distribution Summary
    # --------------------------------------------------

    distribution = (
        latest.groupby("capital_allocation_label")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    distribution.to_csv(
        "data/output/distribution_summary.csv",
        index=False,
    )

    print("Distribution Summary Rows:", len(distribution))

    # --------------------------------------------------
    # 2. Pattern Changes
    # --------------------------------------------------

    changes = []

    for company in capital["company_id"].unique():

        company_df = capital[capital["company_id"] == company].sort_values("year")

        if len(company_df) < 2:
            continue

        latest_row = company_df.iloc[-1]
        previous_row = company_df.iloc[-2]

        if (
            latest_row["capital_allocation_label"]
            != previous_row["capital_allocation_label"]
        ):

            changes.append(
                {
                    "company_id": company,
                    "old_pattern": previous_row["capital_allocation_label"],
                    "new_pattern": latest_row["capital_allocation_label"],
                }
            )

    changes_df = pd.DataFrame(changes)

    changes_df.to_csv(
        "data/output/pattern_changes.csv",
        index=False,
    )

    print("Pattern Changes:", len(changes_df))

    # --------------------------------------------------
    # 3. Update Cashflow Intelligence
    # --------------------------------------------------

    cashflow_file = "data/output/cashflow_intelligence.xlsx"

    cashflow_df = pd.read_excel(cashflow_file)

    latest_labels = latest[
        [
            "company_id",
            "capital_allocation_label",
        ]
    ]

    # remove old column if already present
    if "capital_allocation_label" in cashflow_df.columns:
        cashflow_df = cashflow_df.drop(columns=["capital_allocation_label"])

    if "capital_allocation_label_x" in cashflow_df.columns:
        cashflow_df = cashflow_df.drop(columns=["capital_allocation_label_x"])

    if "capital_allocation_label_y" in cashflow_df.columns:
        cashflow_df = cashflow_df.drop(columns=["capital_allocation_label_y"])

    cashflow_df = cashflow_df.merge(
        latest_labels,
        on="company_id",
        how="left",
    )

    cashflow_df.to_excel(
        cashflow_file,
        index=False,
    )

    print("Updated cashflow_intelligence.xlsx")

    conn.close()

    print("\nDAY 32 COMPLETE")


if __name__ == "__main__":
    run_day32()
