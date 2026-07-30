import os
import sqlite3

import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

DB_PATH = "db/nifty100.db"


def trend_arrow(current, previous):
    """Function: trend_arrow"""
    if pd.isna(current) or pd.isna(previous):
        return "→"

    diff_pct = abs(current - previous)

    if diff_pct <= 2:
        return "→"

    if current > previous:
        return "↑"

    return "↓"


def build_portfolio_summary():
    """Function: build_portfolio_summary"""
    print("=" * 80)
    print("BUILDING PORTFOLIO SUMMARY PDF")
    print("=" * 80)

    os.makedirs("reports/portfolio", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn,
    )

    companies = pd.read_sql(
        """
        SELECT
            id,
            company_name
        FROM companies
        """,
        conn,
    )

    sectors = pd.read_sql(
        """
        SELECT
            company_id,
            broad_sector
        FROM sectors
        """,
        conn,
    )

    conn.close()

    ratios = ratios.sort_values(["company_id", "year"])

    summary_rows = []

    for company_id in ratios["company_id"].unique():

        temp = (
            ratios[ratios["company_id"] == company_id]
            .dropna(subset=["year"])
            .sort_values("year")
        )

        if len(temp) < 2:
            continue

        latest = temp.iloc[-1]
        previous = temp.iloc[-2]

        summary_rows.append(
            {
                "company_id": company_id,
                "roe": latest["return_on_equity_pct"],
                "roe_arrow": trend_arrow(
                    latest["return_on_equity_pct"], previous["return_on_equity_pct"]
                ),
                "roce": latest["return_on_capital_employed_pct"],
                "roce_arrow": trend_arrow(
                    latest["return_on_capital_employed_pct"],
                    previous["return_on_capital_employed_pct"],
                ),
                "revenue_cagr": latest["revenue_cagr_5yr"],
                "revenue_arrow": trend_arrow(
                    latest["revenue_cagr_5yr"], previous["revenue_cagr_5yr"]
                ),
                "pat_cagr": latest["pat_cagr_5yr"],
                "pat_arrow": trend_arrow(
                    latest["pat_cagr_5yr"], previous["pat_cagr_5yr"]
                ),
                "eps_cagr": latest["eps_cagr_5yr"],
                "eps_arrow": trend_arrow(
                    latest["eps_cagr_5yr"], previous["eps_cagr_5yr"]
                ),
                "debt_to_equity": latest["debt_to_equity"],
                "de_arrow": trend_arrow(
                    latest["debt_to_equity"], previous["debt_to_equity"]
                ),
                "fcf": latest["free_cash_flow_cr"],
                "fcf_arrow": trend_arrow(
                    latest["free_cash_flow_cr"], previous["free_cash_flow_cr"]
                ),
            }
        )

    summary = pd.DataFrame(summary_rows)

    summary = summary.merge(companies, left_on="company_id", right_on="id", how="left")

    summary = summary.merge(sectors, on="company_id", how="left")

    summary = summary.sort_values("company_id")

    pdf_path = "reports/portfolio/" "portfolio_summary.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    for _, row in summary.iterrows():

        elements.append(Paragraph(row["company_name"], styles["Title"]))

        elements.append(Paragraph(f"Ticker: {row['company_id']}", styles["Normal"]))

        elements.append(Paragraph(f"Sector: {row['broad_sector']}", styles["Normal"]))

        elements.append(Spacer(1, 15))

        metrics = [
            f"ROE: {row['roe']:.2f}% {row['roe_arrow']}",
            f"ROCE: {row['roce']:.2f}% {row['roce_arrow']}",
            f"Revenue CAGR (5Y): {row['revenue_cagr']:.2f}% {row['revenue_arrow']}",
            f"PAT CAGR (5Y): {row['pat_cagr']:.2f}% {row['pat_arrow']}",
            f"EPS CAGR (5Y): {row['eps_cagr']:.2f}% {row['eps_arrow']}",
            f"Debt / Equity: {row['debt_to_equity']:.2f} {row['de_arrow']}",
            f"Free Cash Flow: ₹{row['fcf']:,.0f} Cr {row['fcf_arrow']}",
        ]

        for item in metrics:

            elements.append(Paragraph(item, styles["BodyText"]))

        elements.append(Spacer(1, 20))

        elements.append(PageBreak())

    doc.build(elements)

    print(f"Portfolio Summary Created: {pdf_path}")

    print(f"Companies Included: {len(summary)}")

    print("=" * 80)
    print("DAY 35 COMPLETE")
    print("=" * 80)


if __name__ == "__main__":

    build_portfolio_summary()
