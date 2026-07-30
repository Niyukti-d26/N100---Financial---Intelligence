import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT
    year,
    sales
FROM profitandloss
WHERE company_id='TCS'
AND year IS NOT NULL
ORDER BY year
""", conn)

start = df.iloc[0]["sales"]
end = df.iloc[-1]["sales"]
years = len(df) - 1

cagr = ((end / start) ** (1 / years) - 1) * 100

print("Start =", start)
print("End =", end)
print("Years =", years)
print("Revenue CAGR =", round(cagr, 2), "%")

conn.close()