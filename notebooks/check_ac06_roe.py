import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")


df = pd.read_sql(
    """
    SELECT
        c.id AS company_id,
        c.roe_percentage AS company_roe,
        f.return_on_equity_pct AS ratio_roe
    FROM companies c
    JOIN financial_ratios f
    ON c.id = f.company_id
    WHERE f.year = 2024
    LIMIT 5
    """,
    conn
)


df["difference"] = abs(
    df["company_roe"] - df["ratio_roe"]
)

df["difference_pct"] = (
    df["difference"] / df["company_roe"]
) * 100


print(df)

print("\nMaximum Difference %:")
print(df["difference_pct"].max())


conn.close()