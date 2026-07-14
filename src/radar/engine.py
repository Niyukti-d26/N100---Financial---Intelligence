import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.config.settings import DATABASE_PATH


class RadarEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE_PATH)

        self.output_dir = Path("reports/radar_charts")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.df = self.load_data()

    def load_data(self):
        ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
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
        peers,
        on="company_id",
        how="left",
    )

        latest_year = df["year"].max()

        df = df[
        df["year"] == latest_year
    ].copy()

        return df

    def get_metrics(self):
        return [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "fcf_conversion_pct",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "composite_quality_score",
    ]

    def get_company(self, company_id):
        return self.df[
        self.df["company_id"] == company_id
    ].iloc[0]

    def plot_radar(self, company_id):
        metrics = self.get_metrics()

        company = self.get_company(company_id)

        peer_group = company["peer_group_name"]

        if pd.isna(peer_group):
            peer_average = self.df[metrics].mean()

        else:
            peer_average = (
            self.df[
                self.df["peer_group_name"] == peer_group
            ][metrics]
            .mean()
        )

        company_values = company[metrics].fillna(0).tolist()

        peer_values = peer_average.fillna(0).tolist()

        labels = [
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "Revenue CAGR",
        "Composite",
    ]

        angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False,
    ).tolist()

        company_values += company_values[:1]
        peer_values += peer_values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(
        figsize=(7, 7),
        subplot_kw={"polar": True},
    )

        ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company_id,
    )

        ax.fill(
        angles,
        company_values,
        alpha=0.25,
    )

        ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average",
    )

        ax.set_xticks(angles[:-1])

        ax.set_xticklabels(labels)

        ax.set_title(f"{company_id} Radar Chart")

        ax.legend(loc="upper right")

        output_file = (
        self.output_dir /
        f"{company_id}_radar.png"
    )

        plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

        plt.close(fig)

        return output_file

    def generate_all(self):
        for company_id in self.df["company_id"].unique():
            try:
               self.plot_radar(company_id)

            except Exception as e:
                print(f"Skipped {company_id}: {e}")

        print("All radar charts generated.")

    def close(self):
       self.conn.close()