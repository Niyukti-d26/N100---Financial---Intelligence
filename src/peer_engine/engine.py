import sqlite3
from pathlib import Path

import pandas as pd

from src.config.settings import DATABASE_PATH


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
        .rank(method="average", pct=True, ascending=True)
        * 100
    )

        return df
    
    def generate_peer_comparison(self):
        metrics = [
        ("return_on_equity_pct", "roe"),
        ("return_on_capital_employed_pct", "roce"),
        ("market_cap_crore", "marketcap"),
        ("pe_ratio", "pe"),
        ("pb_ratio", "pb"),
        ("revenue_cagr_5yr", "revenue"),
        ("pat_cagr_5yr", "pat"),
        ("eps_cagr_5yr", "eps"),
        ("asset_turnover", "asset_turnover"),
    ]

        df = self.df.copy()

        for metric, prefix in metrics:
            df[f"{prefix}_rank"] = (
            df.groupby("peer_group_name")[metric]
            .rank(method="dense", ascending=False)
        )

            df[f"{prefix}_percentile"] = (
            df.groupby("peer_group_name")[metric]
            .rank(method="average", pct=True, ascending=True)
            * 100
        )

        return df

    def close(self):
        self.conn.close()