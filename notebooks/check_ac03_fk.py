import sqlite3

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

result = conn.execute(
    """
    PRAGMA foreign_key_check;
    """
).fetchall()


print("Foreign key violations =", len(result))

if len(result) == 0:
    print("PASS")
else:
    print(result[:10])


conn.close()