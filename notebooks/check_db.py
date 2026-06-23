import sqlite3

conn = sqlite3.connect("db/nifty100.db")

print("Companies in DB:")
print(conn.execute("SELECT COUNT(*) FROM companies").fetchone())

print("\nStock Prices in DB:")
print(conn.execute("SELECT COUNT(*) FROM stock_prices").fetchone())

print("\nSample Companies:")
for row in conn.execute("SELECT id FROM companies LIMIT 10"):
    print(row)

conn.close()