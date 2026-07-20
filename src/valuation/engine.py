import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = ROOT / "db" / "nifty100.db"


class ValuationEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE_PATH)

    def generate_valuation(self):

        market = pd.read_sql(
            """
            SELECT *
            FROM market_cap
            """,
            self.conn
        )

        cashflow = pd.read_sql(
            """
            SELECT *
            FROM cashflow
            """,
            self.conn
        )

        latest_year = market["year"].max()

        market = market[
            market["year"] == latest_year
        ]

        cashflow = cashflow[
            cashflow["year"] == latest_year
        ]

        # Remove duplicate company rows
        market = market.drop_duplicates(
            subset=["company_id"]
        )

        cashflow = cashflow.drop_duplicates(
            subset=["company_id"]
        )

        df = market.merge(
            cashflow,
            on=["company_id", "year"],
            how="left"
        )

        # Replace missing cash flow values
        df["net_cash_flow"] = (
            df["net_cash_flow"]
            .fillna(0)
        )

        # FCF Yield
        df["fcf_yield_pct"] = (
            df["net_cash_flow"]
            /
            df["market_cap_crore"]
        ) * 100

        df["fcf_yield_pct"] = (
            df["fcf_yield_pct"]
            .round(2)
        )

        # Valuation Label
        def pe_flag(pe):

            if pd.isna(pe):
                return "Unknown"

            if pe < 15:
                return "Undervalued"

            elif pe <= 30:
                return "Fair Value"

            else:
                return "Overvalued"

        df["valuation_label"] = (
            df["pe_ratio"]
            .apply(pe_flag)
        )

        return df

    def close(self):

        self.conn.close()