import sqlite3
from pathlib import Path

import pandas as pd

from config.settings import DATABASE_PATH


class PeerEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE_PATH)

        self.df = self.load_data()

    def load_data(self):

        ratios = pd.read_sql(
            """
            SELECT *
            FROM financial_ratios
            """,
            self.conn,
        )

        market = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                market_cap_crore,
                pe_ratio,
                pb_ratio,
                dividend_yield_pct
            FROM market_cap
            """,
            self.conn,
        )

        peers = pd.read_sql(
            """
            SELECT
                company_id,
                peer_group_name,
                is_benchmark
            FROM peer_groups
            """,
            self.conn,
        )

        df = ratios.merge(
            market,
            on=["company_id", "year"],
            how="left",
        )

        df = df.merge(
            peers,
            on="company_id",
            how="left",
        )

        latest_year = df["year"].max()

        df = df[
            df["year"] == latest_year
        ].copy()

        return df

    def get_data(self):
        return self.df.copy()
    
    def rank_metric(self, metric, rank_column):
        df = self.df.copy()

        df[rank_column] = (
        df.groupby("peer_group_name")[metric]
        .rank(method="dense", ascending=False)
    )

        return df
    
    def percentile_metric(self, metric, percentile_column):
        df = self.df.copy()

        df[percentile_column] = (
        df.groupby("peer_group_name")[metric]
        .rank(method="average", pct=True, ascending=False)
        * 100
    )

        return df
    
    def generate_peer_comparison(self):
        metrics = [
    ("return_on_equity_pct", "roe"),
    ("return_on_capital_employed_pct", "roce"),
    ("net_profit_margin_pct", "npm"),
    ("debt_to_equity", "de"),
    ("free_cash_flow_cr", "fcf"),
    ("pat_cagr_5yr", "pat"),
    ("revenue_cagr_5yr", "revenue"),
    ("eps_cagr_5yr", "eps"),
    ("interest_coverage", "icr"),
    ("asset_turnover", "asset_turnover"),
]

        df = self.df.copy()

        for metric, prefix in metrics:
            ascending = False

            if metric == "debt_to_equity":
             ascending = True

            df[f"{prefix}_rank"] = (
            df.groupby("peer_group_name")[metric]
           .rank(
            method="dense",
            ascending=ascending,
        )
    )

            df[f"{prefix}_percentile"] = (
        df.groupby("peer_group_name")[metric]
        .rank(
            method="average",
            pct=True,
            ascending=False,
        )
        * 100
    )

        return df
    
    def save_peer_percentiles(self):
        df = self.generate_peer_comparison()

        records = []

        metrics = [
        ("roe", "return_on_equity_pct"),
        ("roce", "return_on_capital_employed_pct"),
        ("npm", "net_profit_margin_pct"),
        ("de", "debt_to_equity"),
        ("fcf", "free_cash_flow_cr"),
        ("revenue", "revenue_cagr_5yr"),
        ("pat", "pat_cagr_5yr"),
        ("eps", "eps_cagr_5yr"),
        ("icr", "interest_coverage"),
        ("asset_turnover", "asset_turnover"),
    ]

        for _, row in df.iterrows():
            if pd.isna(row["peer_group_name"]):
               continue

            for prefix, metric in metrics:

                records.append({
                "company_id": row["company_id"],
                "peer_group_name": row["peer_group_name"],
                "metric": metric,
                "value": row[metric],
                "percentile_rank": row[f"{prefix}_percentile"],
                "year": row["year"],
            })

        output = pd.DataFrame(records)

        output.to_sql(
        "peer_percentiles",
        self.conn,
        if_exists="replace",
        index=False,
    )

        return output
    
    def get_company_peer_data(self, company_id):
        df = self.generate_peer_comparison()

        company = df[df["company_id"] == company_id]

        if company.empty:
            return "Company not found"

        if company["peer_group_name"].isna().all():
            return "No peer group assigned"
   
        return company

    def close(self):
        self.conn.close()