import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT DISTINCT peer_group_name
FROM peer_percentiles
ORDER BY peer_group_name
""", conn)

print(df)
print()
print("Peer Groups =", len(df))

conn.close()