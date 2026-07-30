import sqlite3

from fastapi import APIRouter, HTTPException

from src.config.settings import DATABASE_PATH

router = APIRouter(tags=["Valuation"])


def get_connection():
    """Function: get_connection"""
    return sqlite3.connect(DATABASE_PATH)


@router.get("/market-cap/{ticker}")
def get_market_cap(ticker: str):
    """Function: get_market_cap"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    ticker = ticker.upper()

    rows = conn.execute(
        """
        SELECT
            company_id,
            year,
            market_cap_crore,
            enterprise_value_crore,
            pe_ratio,
            pb_ratio,
            ev_ebitda,
            dividend_yield_pct
        FROM market_cap
        WHERE company_id = ?
        ORDER BY year
        """,
        (ticker,),
    ).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Company valuation data not found")

    return [dict(row) for row in rows]
