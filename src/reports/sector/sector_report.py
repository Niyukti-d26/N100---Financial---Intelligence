import os
import sqlite3
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

DB_PATH = "db/nifty100.db"

os.makedirs(
    "reports/sector",
    exist_ok=True
)


def generate_sector_reports():

    conn = sqlite3.connect(DB_PATH)

    sectors = pd.read_sql(
        """
        SELECT DISTINCT broad_sector
        FROM sectors
        ORDER BY broad_sector
        """,
        conn
    )

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    companies = pd.read_sql(
        """
        SELECT id,
               company_name
        FROM companies
        """,
        conn
    )

    sector_map = pd.read_sql(
        """
        SELECT company_id,
               broad_sector
        FROM sectors
        """,
        conn
    )

    conn.close()

    latest_year = ratios["year"].max()

    latest_ratios = ratios[
        ratios["year"] == latest_year
    ]

    master = (
        latest_ratios
        .merge(
            sector_map,
            left_on="company_id",
            right_on="company_id",
            how="left"
        )
        .merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left"
        )
    )

    styles = getSampleStyleSheet()

    for sector_name in sectors["broad_sector"]:

        sector_df = master[
            master["broad_sector"] == sector_name
        ].copy()

        pdf_path = (
            f"reports/sector/"
            f"{sector_name}_report.pdf"
        )

        doc = SimpleDocTemplate(pdf_path)

        elements = []

        elements.append(
            Paragraph(
                sector_name,
                styles["Title"]
            )
        )

        elements.append(
            Paragraph(
                f"Companies: {len(sector_df)}",
                styles["Normal"]
            )
        )

        elements.append(
            Spacer(1, 12)
        )

        median_roe = sector_df[
            "return_on_equity_pct"
        ].median()

        median_roce = sector_df[
            "return_on_capital_employed_pct"
        ].median()

        median_npm = sector_df[
            "net_profit_margin_pct"
        ].median()

        median_de = sector_df[
            "debt_to_equity"
        ].median()

        median_fcf = sector_df[
            "free_cash_flow_cr"
        ].median()

        median_rev_cagr = sector_df[
            "revenue_cagr_5yr"
        ].median()

        summary = [
            ["Metric", "Median Value"],
            ["ROE", round(median_roe, 2)],
            ["ROCE", round(median_roce, 2)],
            ["Net Profit Margin", round(median_npm, 2)],
            ["Debt / Equity", round(median_de, 2)],
            ["Free Cash Flow", round(median_fcf, 2)],
            ["Revenue CAGR", round(median_rev_cagr, 2)],
        ]

        summary_table = Table(summary)

        summary_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ])
        )

        elements.append(summary_table)

        elements.append(PageBreak())

        elements.append(
            Paragraph(
                "Companies",
                styles["Heading1"]
            )
        )

        company_table = [[
            "Company",
            "ROE",
            "ROCE",
            "NPM",
            "Debt/Equity",
            "FCF",
            "Revenue CAGR"
        ]]

        for _, row in sector_df.iterrows():

            company_table.append([
                row["company_name"],
                round(row["return_on_equity_pct"], 2)
                if pd.notna(row["return_on_equity_pct"])
                else "N/A",

                round(row["return_on_capital_employed_pct"], 2)
                if pd.notna(row["return_on_capital_employed_pct"])
                else "N/A",

                round(row["net_profit_margin_pct"], 2)
                if pd.notna(row["net_profit_margin_pct"])
                else "N/A",

                round(row["debt_to_equity"], 2)
                if pd.notna(row["debt_to_equity"])
                else "N/A",

                round(row["free_cash_flow_cr"], 2)
                if pd.notna(row["free_cash_flow_cr"])
                else "N/A",

                round(row["revenue_cagr_5yr"], 2)
                if pd.notna(row["revenue_cagr_5yr"])
                else "N/A",
            ])

        table = Table(company_table)

        table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ])
        )

        elements.append(table)

        doc.build(elements)

        print(
            f"Created: {pdf_path}"
        )


if __name__ == "__main__":

    generate_sector_reports()