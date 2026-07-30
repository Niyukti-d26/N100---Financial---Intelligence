import pandas as pd

df = pd.read_csv(
    "data/output/cluster_labels.csv"
)

print("Rows =", len(df))

print(
    "Missing cluster_id =",
    df["cluster_id"].isna().sum()
)

print(
    "Unique clusters =",
    df["cluster_id"].nunique()
)