import pandas as pd
from pathlib import Path

from src.config.settings import PROCESSED_DATA_DIR, OUTPUT_DIR


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


datasets = {}
failures = []


def load_data():

    for file in PROCESSED_DATA_DIR.glob("*.csv"):

        datasets[file.stem] = pd.read_csv(file)


def add_failure(dataset, rule, severity, row_id, message):

    failures.append(
        {
            "dataset": dataset,
            "rule": rule,
            "severity": severity,
            "row": row_id,
            "message": message,
        }
    )
def dq01_primary_key():

    print("\nRunning DQ-01 : Primary Key Check")

    for dataset_name, df in datasets.items():

        if "id" not in df.columns:
            continue

        duplicate_rows = df[df["id"].duplicated()]

        for _, row in duplicate_rows.iterrows():

            add_failure(
                dataset_name,
                "DQ-01",
                "CRITICAL",
                row["id"],
                "Duplicate Primary Key",
            )

    print("DQ-01 Completed") 
def dq02_company_year():

    print("\nRunning DQ-02 : Company-Year Uniqueness")

    tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
    ]

    for table in tables:

        if table not in datasets:
            continue

        df = datasets[table]

        if "company_id" not in df.columns:
            continue

        if "year" not in df.columns:
            continue

        duplicates = df[
            df.duplicated(
                subset=["company_id", "year"],
                keep=False,
            )
        ]

        for _, row in duplicates.iterrows():

            add_failure(
                table,
                "DQ-02",
                "CRITICAL",
                row["id"],
                f"Duplicate record for {row['company_id']} ({row['year']})",
            )

    print("DQ-02 Completed")
def dq03_foreign_key():

    print("\nRunning DQ-03 : Foreign Key Integrity")

    company_ids = set(
        datasets["companies"]["id"]
        .astype(str)
        .str.strip()
    )

    child_tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "analysis",
        "documents",
        "prosandcons",
        "peer_groups",
        "sectors",
        "stock_prices",
    ]

    for table in child_tables:

        if table not in datasets:
            continue

        df = datasets[table]

        if "company_id" not in df.columns:
            continue

        invalid_rows = df[
            ~df["company_id"]
            .astype(str)
            .str.strip()
            .isin(company_ids)
        ]

        for _, row in invalid_rows.iterrows():

            add_failure(
                table,
                "DQ-03",
                "CRITICAL",
                row["id"],
                f"Invalid company_id : {row['company_id']}",
            )

    print("DQ-03 Completed")
def dq04_balance_sheet():

    print("\nRunning DQ-04 : Balance Sheet Validation")

    if "balancesheet" not in datasets:
        return

    df = datasets["balancesheet"]

    required_columns = [
        "id",
        "company_id",
        "year",
        "total_assets",
        "total_liabilities",
    ]

    for column in required_columns:

        if column not in df.columns:
            print(f"Missing column : {column}")
            return

    df = df.copy()

    df["total_assets"] = pd.to_numeric(
        df["total_assets"],
        errors="coerce",
    )

    df["total_liabilities"] = pd.to_numeric(
        df["total_liabilities"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "total_assets",
            "total_liabilities",
        ]
    )

    tolerance = df["total_assets"] * 0.01

    invalid = df[
        abs(
            df["total_assets"]
            - df["total_liabilities"]
        )
        > tolerance
    ]

    for _, row in invalid.iterrows():

        add_failure(
            "balancesheet",
            "DQ-04",
            "WARNING",
            row["id"],
            (
                f"{row['company_id']} ({int(row['year'])}) : "
                f"Assets={row['total_assets']} "
                f"Liabilities={row['total_liabilities']}"
            ),
        )

    print("DQ-04 Completed")
def dq05_opm():

    print("\nRunning DQ-05 : Operating Profit Margin Check")

    if "profitandloss" not in datasets:
        return

    df = datasets["profitandloss"].copy()

    required_columns = [
        "id",
        "company_id",
        "year",
        "sales",
        "operating_profit",
        "opm_percentage",
    ]

    for column in required_columns:

        if column not in df.columns:
            print(f"Missing column : {column}")
            return

    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df["operating_profit"] = pd.to_numeric(df["operating_profit"], errors="coerce")
    df["opm_percentage"] = pd.to_numeric(df["opm_percentage"], errors="coerce")

    df = df.dropna()

    df = df[df["sales"] != 0]

    df["calculated_opm"] = (
        df["operating_profit"] / df["sales"]
    ) * 100

    df = df[
    (df["opm_percentage"] >= -100) &
    (df["opm_percentage"] <= 100)
    ]
    invalid = df[
        abs(
            df["calculated_opm"] -
            df["opm_percentage"]
        ) > 1
    ]

    for _, row in invalid.iterrows():

        add_failure(
            "profitandloss",
            "DQ-05",
            "WARNING",
            row["id"],
            (
                f"{row['company_id']} ({int(row['year'])}) "
                f"Expected={row['calculated_opm']:.2f}% "
                f"Found={row['opm_percentage']:.2f}%"
            ),
        )

    print("DQ-05 Completed")
def dq06_positive_sales():

    print("\nRunning DQ-06 : Positive Sales Check")

    if "profitandloss" not in datasets:
        return

    df = datasets["profitandloss"].copy()

    if "sales" not in df.columns:
        return

    df["sales"] = pd.to_numeric(
        df["sales"],
        errors="coerce",
    )

    invalid = df[df["sales"] < 0]

    for _, row in invalid.iterrows():

        add_failure(
            "profitandloss",
            "DQ-06",
            "WARNING",
            row["id"],
            f"{row['company_id']} ({int(row['year'])}) Negative Sales",
        )

    print("DQ-06 Completed")
def dq07_tax_percentage():

    print("\nRunning DQ-07 : Tax Percentage Check")

    if "profitandloss" not in datasets:
        return

    df = datasets["profitandloss"].copy()

    required = [
        "id",
        "company_id",
        "year",
        "tax_percentage",
    ]

    for col in required:
        if col not in df.columns:
            return

    df["tax_percentage"] = pd.to_numeric(
        df["tax_percentage"],
        errors="coerce",
    )

    invalid = df[
        (df["tax_percentage"] < 0) |
        (df["tax_percentage"] > 100)
    ]

    for _, row in invalid.iterrows():

        add_failure(
            "profitandloss",
            "DQ-07",
            "WARNING",
            row["id"],
            f"{row['company_id']} ({int(row['year'])}) Invalid Tax Percentage"
        )

    print("DQ-07 Completed")
def dq08_net_profit():

    print("\nRunning DQ-08 : Net Profit Check")

    if "profitandloss" not in datasets:
        return

    df = datasets["profitandloss"].copy()

    required = [
        "id",
        "company_id",
        "year",
        "net_profit",
        "profit_before_tax",
    ]

    for col in required:
        if col not in df.columns:
            return

    df["net_profit"] = pd.to_numeric(
        df["net_profit"],
        errors="coerce",
    )

    df["profit_before_tax"] = pd.to_numeric(
        df["profit_before_tax"],
        errors="coerce",
    )

    invalid = df[
        df["net_profit"] > df["profit_before_tax"]
    ]

    for _, row in invalid.iterrows():

        year = (
            "Unknown"
            if pd.isna(row["year"])
            else int(row["year"])
        )

        add_failure(
            "profitandloss",
            "DQ-08",
            "WARNING",
            row["id"],
            f"{row['company_id']} ({year}) Net Profit exceeds Profit Before Tax",
        )

    print("DQ-08 Completed")
def dq09_dividend_payout():

    print("\nRunning DQ-09 : Dividend Payout Check")

    if "profitandloss" not in datasets:
        return

    df = datasets["profitandloss"].copy()

    if "dividend_payout" not in df.columns:
        return

    df["dividend_payout"] = pd.to_numeric(
        df["dividend_payout"],
        errors="coerce",
    )

    invalid = df[
        (df["dividend_payout"] < 0)
        | (df["dividend_payout"] > 100)
    ]

    for _, row in invalid.iterrows():

        year = (
            "Unknown"
            if pd.isna(row["year"])
            else int(row["year"])
        )

        add_failure(
            "profitandloss",
            "DQ-09",
            "WARNING",
            row["id"],
            f"{row['company_id']} ({year}) Invalid Dividend Payout",
        )

    print("DQ-09 Completed")
def dq10_eps_check():

    print("\nRunning DQ-10 : EPS Validation")

    if "profitandloss" not in datasets:
        return

    df = datasets["profitandloss"].copy()

    required = [
        "id",
        "company_id",
        "year",
        "eps",
        "net_profit",
    ]

    for col in required:
        if col not in df.columns:
            return

    df["eps"] = pd.to_numeric(
        df["eps"],
        errors="coerce",
    )

    df["net_profit"] = pd.to_numeric(
        df["net_profit"],
        errors="coerce",
    )

    invalid = df[
        (df["net_profit"] != 0)
        & (df["eps"] == 0)
    ]

    for _, row in invalid.iterrows():

        year = (
            "Unknown"
            if pd.isna(row["year"])
            else int(row["year"])
        )

        add_failure(
            "profitandloss",
            "DQ-10",
            "WARNING",
            row["id"],
            f"{row['company_id']} ({year}) EPS is zero while Net Profit is non-zero",
        )

    print("DQ-10 Completed")
def dq11_cashflow():

    print("\nRunning DQ-11 : Cash Flow Validation")

    if "cashflow" not in datasets:
        return

    df = datasets["cashflow"].copy()

    cols = [
        "id",
        "company_id",
        "year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow",
    ]

    for col in cols:
        if col not in df.columns:
            return

    for col in cols[3:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    calculated = (
        df["operating_activity"]
        + df["investing_activity"]
        + df["financing_activity"]
    )

    invalid = df[
        abs(calculated - df["net_cash_flow"]) > 1
    ]

    for _, row in invalid.iterrows():

        year = "Unknown" if pd.isna(row["year"]) else int(row["year"])

        add_failure(
            "cashflow",
            "DQ-11",
            "WARNING",
            row["id"],
            f"{row['company_id']} ({year}) Net Cash Flow mismatch",
        )

    print("DQ-11 Completed")
def dq12_website():

    print("\nRunning DQ-12 : Website URL Check")

    if "companies" not in datasets:
        return

    df = datasets["companies"].copy()

    invalid = df[
        ~df["website"].astype(str).str.startswith(("http://", "https://"))
    ]

    for _, row in invalid.iterrows():

        add_failure(
            "companies",
            "DQ-12",
            "WARNING",
            row["id"],
            "Invalid Website URL",
        )

    print("DQ-12 Completed")
def dq13_annual_report():

    print("\nRunning DQ-13 : Annual Report URL Check")

    if "documents" not in datasets:
        return

    df = datasets["documents"].copy()

    invalid = df[
        ~df["annual_report"].astype(str).str.startswith(("http://", "https://"))
    ]

    for _, row in invalid.iterrows():

        add_failure(
            "documents",
            "DQ-13",
            "WARNING",
            row["id"],
            "Invalid Annual Report URL",
        )

    print("DQ-13 Completed")
def dq14_market_cap():

    print("\nRunning DQ-14 : Market Cap Check")

    if "market_cap" not in datasets:
        return

    df = datasets["market_cap"].copy()

    df["market_cap_crore"] = pd.to_numeric(
        df["market_cap_crore"],
        errors="coerce",
    )

    invalid = df[
        df["market_cap_crore"] <= 0
    ]

    for _, row in invalid.iterrows():

        add_failure(
            "market_cap",
            "DQ-14",
            "WARNING",
            row["id"],
            "Invalid Market Cap",
        )

    print("DQ-14 Completed")
def dq15_stock_prices():

    print("\nRunning DQ-15 : Stock Price Validation")

    if "stock_prices" not in datasets:
        return

    df = datasets["stock_prices"].copy()

    cols = [
        "open_price",
        "high_price",
        "low_price",
        "close_price",
    ]

    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    invalid = df[
        (df["high_price"] < df["low_price"])
    ]

    for _, row in invalid.iterrows():

        add_failure(
            "stock_prices",
            "DQ-15",
            "WARNING",
            row["id"],
            "High Price lower than Low Price",
        )

    print("DQ-15 Completed")
def dq16_roe():

    print("\nRunning DQ-16 : ROE Validation")

    if "companies" not in datasets:
        return

    df = datasets["companies"].copy()

    df["roe_percentage"] = pd.to_numeric(
        df["roe_percentage"],
        errors="coerce",
    )

    invalid = df[
        (df["roe_percentage"] < -100)
        | (df["roe_percentage"] > 100)
    ]

    for _, row in invalid.iterrows():

        add_failure(
            "companies",
            "DQ-16",
            "WARNING",
            row["id"],
            "Invalid ROE Percentage",
        )

    print("DQ-16 Completed")
def run_validation():

    load_data()

    dq01_primary_key()
    dq02_company_year()
    dq03_foreign_key()
    dq04_balance_sheet()
    dq05_opm()
    dq06_positive_sales()
    dq07_tax_percentage()
    dq08_net_profit()
    dq09_dividend_payout()
    dq10_eps_check()
    dq11_cashflow()
    dq12_website()
    dq13_annual_report()
    dq14_market_cap()
    dq15_stock_prices()
    dq16_roe()

    report = pd.DataFrame(failures)

    report.to_csv(
        OUTPUT_DIR / "validation_failures.csv",
        index=False,
    )

    print()

    print("=" * 50)

    print(report)

    print()

    print(f"Total Issues : {len(report)}")


if __name__ == "__main__":

    run_validation()