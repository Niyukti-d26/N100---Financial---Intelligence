import sqlite3

from fastapi import APIRouter, HTTPException

from src.config.settings import DATABASE_PATH

router = APIRouter(tags=["Screener"])


def get_connection():
    """Function: get_connection"""
    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


@router.get("/screener")
def get_screener(
    sector: str | None = None,
    market_cap_category: str | None = None,
    roe_min: float | None = None,
    roce_min: float | None = None,
    debt_to_equity_max: float | None = None,
    score_min: float | None = None,
):
    """Function: get_screener"""
    conn = get_connection()

    if roe_min is not None and roe_min < 0:
        raise HTTPException(status_code=400, detail="roe_min cannot be negative")

    if roce_min is not None and roce_min < 0:
        raise HTTPException(status_code=400, detail="roce_min cannot be negative")

    if debt_to_equity_max is not None and debt_to_equity_max < 0:
        raise HTTPException(
            status_code=400, detail="debt_to_equity_max cannot be negative"
        )

    if score_min is not None and score_min < 0:
        raise HTTPException(status_code=400, detail="score_min cannot be negative")

    query = """
    SELECT

        c.id,
        c.company_name,
        c.company_logo,

        s.broad_sector,
        s.market_cap_category,

        fr.year,
        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.debt_to_equity,
        fr.composite_quality_score

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE fr.year = (

        SELECT MAX(fr2.year)

        FROM financial_ratios fr2

        WHERE fr2.company_id = c.id

    )
    """

    params = []

    if sector:

        query += """
        AND s.broad_sector = ?
        """

        params.append(sector)

    if market_cap_category:

        query += """
        AND s.market_cap_category = ?
        """

        params.append(market_cap_category)

    if roe_min is not None:

        query += """
        AND fr.return_on_equity_pct >= ?
        """

        params.append(roe_min)

    if roce_min is not None:

        query += """
        AND fr.return_on_capital_employed_pct >= ?
        """

        params.append(roce_min)

    if debt_to_equity_max is not None:

        query += """
        AND fr.debt_to_equity <= ?
        """

        params.append(debt_to_equity_max)

    if score_min is not None:

        query += """
        AND fr.composite_quality_score >= ?
        """

        params.append(score_min)

    query += """
    ORDER BY fr.composite_quality_score DESC
    """

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [
        {
            "company_id": r["id"],
            "company_name": r["company_name"],
            "company_logo": r["company_logo"],
            "sector": r["broad_sector"],
            "market_cap_category": r["market_cap_category"],
            "year": r["year"],
            "roe_pct": r["return_on_equity_pct"],
            "roce_pct": r["return_on_capital_employed_pct"],
            "debt_to_equity": r["debt_to_equity"],
            "quality_score": r["composite_quality_score"],
        }
        for r in rows
    ]
