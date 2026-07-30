import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DB_PATH = "db/nifty100.db"


def load_data():
    """Function: load_data"""
    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn,
    )

    sectors = pd.read_sql(
        """
        SELECT company_id,
               broad_sector
        FROM sectors
        """,
        conn,
    )

    conn.close()

    ratios = (
        ratios.dropna(subset=["year"])
        .sort_values(["company_id", "year"])
        .groupby("company_id", as_index=False)
        .tail(1)
    )

    clusters = pd.read_csv("data/output/cluster_labels.csv")

    return ratios, sectors, clusters


def cluster_profiles(ratios, clusters):
    """Function: cluster_profiles"""
    df = ratios.merge(clusters, on="company_id")

    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct",
    ]

    profile = df.groupby("cluster_name")[features].agg(["mean", "median"]).round(2)

    profile.to_csv("data/output/cluster_profiles.csv")

    print("Saved cluster_profiles.csv")


def correlation_heatmap(ratios):
    """Function: correlation_heatmap"""
    cols = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
    ]

    corr = ratios[cols].corr()

    plt.figure(figsize=(10, 8))

    sns.heatmap(corr, annot=True, cmap="coolwarm")

    plt.title("KPI Correlation Matrix")

    plt.tight_layout()

    plt.savefig("reports/correlation_heatmap.png")

    plt.close()

    print("Saved correlation_heatmap.png")


def portfolio_stats(ratios):
    """Function: portfolio_stats"""
    metrics = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
    ]

    rows = []

    for metric in metrics:

        s = ratios[metric].dropna()

        rows.append(
            {
                "metric": metric,
                "P10": s.quantile(0.10),
                "P25": s.quantile(0.25),
                "P50": s.quantile(0.50),
                "P75": s.quantile(0.75),
                "P90": s.quantile(0.90),
                "Mean": s.mean(),
                "Std": s.std(),
            }
        )

    pd.DataFrame(rows).round(2).to_csv("data/output/portfolio_stats.csv", index=False)

    print("Saved portfolio_stats.csv")


def outlier_report(ratios, sectors):
    """Function: outlier_report"""
    df = ratios.merge(sectors, on="company_id")

    metrics = ["return_on_equity_pct", "debt_to_equity", "revenue_cagr_5yr"]

    rows = []

    for sector in df["broad_sector"].unique():

        sub = df[df["broad_sector"] == sector]

        for metric in metrics:

            mean = sub[metric].mean()
            std = sub[metric].std()

            if std == 0:
                continue

            z = (sub[metric] - mean) / std

            flagged = sub[abs(z) > 3]

            for _, r in flagged.iterrows():

                rows.append(
                    {
                        "company_id": r["company_id"],
                        "sector": sector,
                        "metric": metric,
                        "z_score": round((r[metric] - mean) / std, 2),
                    }
                )

    pd.DataFrame(rows).to_csv("data/output/outlier_report.csv", index=False)

    print("Saved outlier_report.csv")


if __name__ == "__main__":

    ratios, sectors, clusters = load_data()

    cluster_profiles(ratios, clusters)

    correlation_heatmap(ratios)

    portfolio_stats(ratios)

    outlier_report(ratios, sectors)

    print("=" * 80)
    print("DAY 37 COMPLETE")
    print("=" * 80)
