import sqlite3

dbs = [
    "data/nifty100.db",
    "db/nifty100.db"
]

for db in dbs:

    print("\n" + "=" * 60)
    print(db)

    conn = sqlite3.connect(db)

    tables = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """).fetchall()

    for t in tables:
        print(t[0])

    conn.close()