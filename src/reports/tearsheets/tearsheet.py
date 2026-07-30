import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer

DB_PATH = "db/nifty100.db"


def load_company_data(company_id):
    """Function: load_company_data"""
    conn = sqlite3.connect(DB_PATH)

    company = pd.read_sql(
        f"""
        SELECT *
        FROM companies
        WHERE id='{company_id}'
        """,
        conn,
    )

    sector = pd.read_sql(
        f"""
        SELECT *
        FROM sectors
        WHERE company_id='{company_id}'
        """,
        conn,
    )

    ratios = pd.read_sql(
        f"""
        SELECT *
        FROM financial_ratios
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn,
    )

    pl = pd.read_sql(
        f"""
        SELECT *
        FROM profitandloss
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn,
    )

    bs = pd.read_sql(
        f"""
        SELECT *
        FROM balancesheet
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn,
    )

    cf = pd.read_sql(
        f"""
        SELECT *
        FROM cashflow
        WHERE company_id='{company_id}'
        ORDER BY year
        """,
        conn,
    )

    conn.close()

    return company, sector, ratios, pl, bs, cf


def create_revenue_chart(pl, company_id):
    """Function: create_revenue_chart"""
    data = pl.dropna(subset=["year", "sales"])

    plt.figure(figsize=(6, 3))

    plt.bar(data["year"].astype(int).astype(str), data["sales"])

    plt.title(f"{company_id} Revenue Trend")
    plt.xlabel("Year")
    plt.ylabel("Sales")

    plt.tight_layout()

    path = f"reports/tearsheets/{company_id}_revenue.png"

    plt.savefig(path)
    plt.close()

    return path


def create_profit_chart(pl, company_id):
    """Function: create_profit_chart"""
    data = pl.dropna(subset=["year", "net_profit"])

    plt.figure(figsize=(6, 3))

    plt.bar(data["year"].astype(int).astype(str), data["net_profit"])

    plt.title(f"{company_id} Net Profit Trend")
    plt.xlabel("Year")
    plt.ylabel("Net Profit")

    plt.tight_layout()

    path = f"reports/tearsheets/{company_id}_profit.png"

    plt.savefig(path)
    plt.close()

    return path


def create_roe_chart(ratios, company_id):
    """Function: create_roe_chart"""
    data = ratios.dropna(subset=["year", "return_on_equity_pct"])

    plt.figure(figsize=(6, 3))

    plt.plot(data["year"].astype(int), data["return_on_equity_pct"], marker="o")

    plt.title(f"{company_id} ROE Trend")
    plt.xlabel("Year")
    plt.ylabel("ROE %")

    plt.tight_layout()

    path = f"reports/tearsheets/" f"{company_id}_roe.png"

    plt.savefig(path)
    plt.close()

    return path


def create_roce_chart(ratios, company_id):
    """Function: create_roce_chart"""
    data = ratios.dropna(subset=["year", "return_on_capital_employed_pct"])

    plt.figure(figsize=(6, 3))

    plt.plot(
        data["year"].astype(int), data["return_on_capital_employed_pct"], marker="o"
    )

    plt.title(f"{company_id} ROCE Trend")
    plt.xlabel("Year")
    plt.ylabel("ROCE %")

    plt.tight_layout()

    path = f"reports/tearsheets/" f"{company_id}_roce.png"

    plt.savefig(path)
    plt.close()

    return path


def create_balance_sheet_chart(bs, company_id):
    """Function: create_balance_sheet_chart"""
    data = bs.dropna(
        subset=["year", "equity_capital", "borrowings", "other_liabilities"]
    )

    years = data["year"].astype(int).astype(str)

    plt.figure(figsize=(8, 4))

    plt.bar(years, data["equity_capital"], label="Equity")

    plt.bar(
        years, data["borrowings"], bottom=data["equity_capital"], label="Borrowings"
    )

    plt.bar(
        years,
        data["other_liabilities"],
        bottom=(data["equity_capital"] + data["borrowings"]),
        label="Other Liabilities",
    )

    plt.legend()

    plt.title(f"{company_id} Balance Sheet Composition")

    plt.tight_layout()

    path = f"reports/tearsheets/" f"{company_id}_bs.png"

    plt.savefig(path)
    plt.close()

    return path


def create_cashflow_chart(cf, company_id):
    """Function: create_cashflow_chart"""
    latest = cf.sort_values("year").iloc[-1]

    labels = ["CFO", "CFI", "CFF", "Net CF"]

    values = [
        latest["operating_activity"],
        latest["investing_activity"],
        latest["financing_activity"],
        latest["net_cash_flow"],
    ]

    plt.figure(figsize=(7, 3))

    plt.bar(labels, values)

    plt.title(f"{company_id} Latest Cash Flow")

    plt.tight_layout()

    path = f"reports/tearsheets/" f"{company_id}_cashflow.png"

    plt.savefig(path)
    plt.close()

    return path


def generate_tearsheet(company_id):
    """Function: generate_tearsheet"""
    company, sector, ratios, pl, bs, cf = load_company_data(company_id)

    proscons = pd.read_csv("data/output/pros_cons_generated.csv")

    ratios = ratios.dropna(subset=["year"])

    company_name = company.iloc[0]["company_name"]
    sector_name = sector.iloc[0]["broad_sector"]

    latest_ratio = ratios.sort_values("year").iloc[-1]

    pdf_path = f"reports/tearsheets/" f"{company_id}_tearsheet.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    revenue_chart = create_revenue_chart(pl, company_id)

    profit_chart = create_profit_chart(pl, company_id)

    roe_chart = create_roe_chart(ratios, company_id)

    roce_chart = create_roce_chart(ratios, company_id)

    bs_chart = create_balance_sheet_chart(bs, company_id)

    cashflow_chart = create_cashflow_chart(cf, company_id)

    # PAGE 1

    elements.append(Paragraph(company_name, styles["Title"]))

    elements.append(Paragraph(f"Ticker: {company_id}", styles["Normal"]))

    elements.append(Paragraph(f"Sector: {sector_name}", styles["Normal"]))

    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Key Metrics", styles["Heading1"]))

    metrics = [
        f"ROE: {latest_ratio['return_on_equity_pct']:.2f}%",
        f"ROCE: {latest_ratio['return_on_capital_employed_pct']:.2f}%",
        f"NPM: {latest_ratio['net_profit_margin_pct']:.2f}%",
        f"Debt/Equity: {latest_ratio['debt_to_equity']:.2f}",
        f"FCF: ₹{latest_ratio['free_cash_flow_cr']:,.0f} Cr",
        f"Revenue CAGR: {latest_ratio['revenue_cagr_5yr']:.2f}%",
    ]

    for item in metrics:
        elements.append(Paragraph(item, styles["Normal"]))

    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Revenue Trend", styles["Heading2"]))

    elements.append(Image(revenue_chart, width=400, height=180))

    elements.append(Paragraph("Net Profit Trend", styles["Heading2"]))

    elements.append(Image(profit_chart, width=400, height=180))

    elements.append(Paragraph("ROE Trend", styles["Heading2"]))

    elements.append(Image(roe_chart, width=400, height=180))

    elements.append(Paragraph("ROCE Trend", styles["Heading2"]))

    elements.append(Image(roce_chart, width=400, height=180))

    # PAGE 2

    elements.append(PageBreak())

    elements.append(Paragraph("Balance Sheet Composition", styles["Heading1"]))

    elements.append(Image(bs_chart, width=450, height=220))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Cash Flow Summary", styles["Heading1"]))

    elements.append(Image(cashflow_chart, width=450, height=220))

    elements.append(Spacer(1, 15))

    pros = proscons[
        (proscons["company_id"] == company_id) & (proscons["type"] == "pro")
    ].head(5)

    cons = proscons[
        (proscons["company_id"] == company_id) & (proscons["type"] == "con")
    ].head(5)

    elements.append(Paragraph("Pros", styles["Heading1"]))

    for _, row in pros.iterrows():

        elements.append(Paragraph(f"• {row['text']}", styles["BodyText"]))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Cons", styles["Heading1"]))

    for _, row in cons.iterrows():

        elements.append(Paragraph(f"• {row['text']}", styles["BodyText"]))

    doc.build(elements)

    print("Created:", pdf_path)


if __name__ == "__main__":

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(
        """
        SELECT id
        FROM companies
        """,
        conn,
    )

    conn.close()

    skipped = []

    generated = 0

    for ticker in companies["id"]:

        try:

            conn = sqlite3.connect(DB_PATH)

            pl = pd.read_sql(
                f"""
                SELECT *
                FROM profitandloss
                WHERE company_id='{ticker}'
                """,
                conn,
            )

            conn.close()

            years_available = pl["year"].dropna().nunique()

            if years_available < 3:

                skipped.append(
                    {"company_id": ticker, "reason": "Less than 3 years data"}
                )

                continue

            generate_tearsheet(ticker)

            generated += 1

        except Exception as e:

            skipped.append({"company_id": ticker, "reason": str(e)})

            print(f"Failed: {ticker}")

    pd.DataFrame(skipped).to_csv("data/output/skipped_tearsheets.csv", index=False)

    print("=" * 60)
    print("Generated:", generated)
    print("Skipped:", len(skipped))
    print("=" * 60)
