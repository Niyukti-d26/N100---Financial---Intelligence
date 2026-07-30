import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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

    conn.close()

    cashflow = pd.read_excel("data/output/cashflow_intelligence.xlsx")

    ratios = ratios.dropna(subset=["year"])

    ratios = ratios.sort_values(["company_id", "year"])

    ratios = ratios.groupby("company_id", as_index=False).tail(1)

    print("Rows:", len(ratios))
    print("Companies:", ratios["company_id"].nunique())

    cashflow = cashflow.drop_duplicates(subset=["company_id"])

    df = ratios.merge(
        cashflow[["company_id", "fcf_cagr_5yr"]], on="company_id", how="left"
    )

    print("Rows after merge:", len(df))

    print("Unique companies:", df["company_id"].nunique())

    return df


def prepare_features(df):
    """Function: prepare_features"""
    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
    ]

    cluster_df = df[["company_id"] + features].copy()

    for col in features:

        cluster_df[col] = cluster_df[col].fillna(cluster_df[col].median())

    return cluster_df


def create_elbow_plot(X):
    """Function: create_elbow_plot"""
    inertias = []

    for k in range(2, 11):

        model = KMeans(n_clusters=k, random_state=42, n_init=10)

        model.fit(X)

        inertias.append(model.inertia_)

    plt.figure(figsize=(7, 4))

    plt.plot(range(2, 11), inertias, marker="o")

    plt.title("KMeans Elbow Plot")
    plt.xlabel("Clusters")
    plt.ylabel("Inertia")

    plt.tight_layout()

    plt.savefig("reports/elbow_plot.png")

    plt.close()


def run_clustering(df):
    """Function: run_clustering"""
    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
    ]

    scaler = StandardScaler()

    X = scaler.fit_transform(df[features])

    create_elbow_plot(X)

    model = KMeans(n_clusters=5, random_state=42, n_init=10)

    df["cluster_id"] = model.fit_predict(X)

    return df, model, X


def assign_cluster_names(df):
    """Function: assign_cluster_names"""
    mapping = {
        0: "High Quality Compounders",
        1: "Defensive Dividend Payers",
        2: "Emerging Growth",
        3: "Value Cyclicals",
        4: "Turnaround Candidates",
    }

    df["cluster_name"] = df["cluster_id"].map(mapping)

    return df


def add_distance_from_centroid(df, model, X):
    """Function: add_distance_from_centroid"""
    distances = []

    for i, row in enumerate(X):

        cid = model.labels_[i]

        center = model.cluster_centers_[cid]

        distance = (((row - center) ** 2).sum()) ** 0.5

        distances.append(round(distance, 4))

    df["distance_from_centroid"] = distances

    return df


def save_output(df):
    """Function: save_output"""
    output = df[["company_id", "cluster_id", "cluster_name", "distance_from_centroid"]]

    output.to_csv("data/output/cluster_labels.csv", index=False)

    print("=" * 80)
    print("DAY 36 COMPLETE")
    print("Companies:", len(output))
    print("Saved: data/output/cluster_labels.csv")
    print("Saved: reports/elbow_plot.png")
    print("=" * 80)


if __name__ == "__main__":

    df = load_data()

    df = prepare_features(df)

    df, model, X = run_clustering(df)

    df = assign_cluster_names(df)

    df = add_distance_from_centroid(df, model, X)

    save_output(df)
