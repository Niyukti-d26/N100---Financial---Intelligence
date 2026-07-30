import time
import sqlite3

from fastapi import APIRouter

from src.config.settings import DATABASE_PATH


router = APIRouter(
    tags=["Health"]
)


START_TIME = time.time()



@router.get("/health")
def health_check():
    """
    API health status.
    """

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "financial_ratios",
        "market_cap",
        "stock_prices",
    ]


    counts = {}

    for table in tables:

        count = conn.execute(
            f"""
            SELECT COUNT(*)
            FROM {table}
            """
        ).fetchone()[0]

        counts[table] = count


    conn.close()


    return {

        "status": "ok",

        "db_row_counts": counts,

        "uptime_seconds":
            round(
                time.time() - START_TIME,
                2
            ),

        "version": "1.0.0"

    }