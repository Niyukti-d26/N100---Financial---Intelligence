import sqlite3

from fastapi import APIRouter, HTTPException

from src.config.settings import DATABASE_PATH

router = APIRouter(tags=["Sectors"])


def get_connection():
    """Function: get_connection"""
    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ---------------------------------------------------------
# ALL SECTORS SUMMARY
# ---------------------------------------------------------


@router.get("/sectors")
def get_all_sectors():
    """Function: get_all_sectors"""
    conn = get_connection()

    rows = conn.execute("""
        SELECT
            s.broad_sector,
            COUNT(DISTINCT s.company_id) AS company_count,
            ROUND(AVG(fr.return_on_equity_pct), 2) AS average_roe,
            ROUND(AVG(fr.debt_to_equity), 2) AS average_de
        FROM sectors s

        LEFT JOIN financial_ratios fr
        ON s.company_id = fr.company_id

        GROUP BY s.broad_sector

        ORDER BY s.broad_sector
        """).fetchall()

    conn.close()

    return [
        {
            "sector": row["broad_sector"],
            "company_count": row["company_count"],
            "average_roe_pct": row["average_roe"],
            "average_debt_to_equity": row["average_de"],
        }
        for row in rows
    ]


# ---------------------------------------------------------
# SECTOR COMPANIES
# ---------------------------------------------------------


@router.get("/sectors/{sector_name}/companies")
def get_sector_companies(sector_name: str):
    """Function: get_sector_companies"""
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            c.company_name,
            s.company_id,
            s.broad_sector,
            s.sub_sector,
            s.index_weight_pct,
            s.market_cap_category,

            fr.year,
            fr.return_on_equity_pct,
            fr.return_on_capital_employed_pct,
            fr.debt_to_equity,
            fr.composite_quality_score

        FROM sectors s

        JOIN companies c
        ON s.company_id = c.id

        LEFT JOIN financial_ratios fr
        ON s.company_id = fr.company_id

        WHERE s.broad_sector = ?

        AND fr.year = (
            SELECT MAX(fr2.year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = s.company_id
        )

        ORDER BY s.index_weight_pct DESC
        """,
        (sector_name,),
    ).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Sector not found")

    return {
        "sector": sector_name,
        "company_count": len(rows),
        "companies": [dict(row) for row in rows],
    }
