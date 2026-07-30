import sqlite3

from fastapi import APIRouter

from src.config.settings import DATABASE_PATH

router = APIRouter(tags=["Portfolio"])


def get_connection():
    """Function: get_connection"""
    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


@router.get("/portfolio/stats")
def portfolio_stats():
    """Function: portfolio_stats"""
    conn = get_connection()

    total_companies = conn.execute("""
        SELECT COUNT(*)
        FROM companies
        """).fetchone()[0]

    total_sectors = conn.execute("""
        SELECT COUNT(DISTINCT broad_sector)
        FROM sectors
        """).fetchone()[0]

    latest_year = conn.execute("""
        SELECT MAX(year)
        FROM financial_ratios
        """).fetchone()[0]

    avg_roe = conn.execute(
        """
        SELECT AVG(return_on_equity_pct)
        FROM financial_ratios
        WHERE year = ?
        """,
        (latest_year,),
    ).fetchone()[0]

    avg_roce = conn.execute(
        """
        SELECT AVG(return_on_capital_employed_pct)
        FROM financial_ratios
        WHERE year = ?
        """,
        (latest_year,),
    ).fetchone()[0]

    avg_quality = conn.execute(
        """
        SELECT AVG(composite_quality_score)
        FROM financial_ratios
        WHERE year = ?
        """,
        (latest_year,),
    ).fetchone()[0]

    conn.close()

    return {
        "total_companies": total_companies,
        "total_sectors": total_sectors,
        "latest_financial_year": latest_year,
        "average_roe_pct": round(avg_roe, 2) if avg_roe else None,
        "average_roce_pct": round(avg_roce, 2) if avg_roce else None,
        "average_quality_score": round(avg_quality, 2) if avg_quality else None,
    }
