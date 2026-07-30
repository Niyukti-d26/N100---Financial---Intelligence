import os
import sqlite3

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from src.config.settings import DATABASE_PATH

router = APIRouter(tags=["Companies"])


def get_connection():
    """Function: get_connection"""
    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# ALL COMPANIES
# =========================================================


@router.get("/companies")
def get_companies(search: str | None = None):
    """Function: get_companies"""
    conn = get_connection()

    query = """
    SELECT
        company_name,
        company_logo,
        roce_percentage,
        roe_percentage

    FROM companies

    WHERE 1=1
    """

    params = []

    if search:

        query += """
        AND company_name LIKE ?
        """

        params.append(f"%{search}%")

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [
        {
            "company_name": r["company_name"],
            "company_logo": r["company_logo"],
            "roce_pct": r["roce_percentage"],
            "roe_pct": r["roe_percentage"],
        }
        for r in rows
    ]


# =========================================================
# P&L HISTORY
# =========================================================


@router.get("/companies/{ticker}/pl")
def get_profit_loss(ticker: str):
    """Function: get_profit_loss"""
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# =========================================================
# BALANCE SHEET
# =========================================================


@router.get("/companies/{ticker}/bs")
def get_balance_sheet(ticker: str):
    """Function: get_balance_sheet"""
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year
        """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# =========================================================
# CASH FLOW
# =========================================================


@router.get("/companies/{ticker}/cashflow")
def get_cashflow(ticker: str):
    """Function: get_cashflow"""
    conn = get_connection()

    rows = conn.execute(
        """

    SELECT

    company_id,


    CASE

        WHEN year LIKE 'Mar-%'
        THEN CAST('20' || substr(year,5,2) AS INTEGER)


        WHEN year LIKE 'Mar %'
        THEN CAST(substr(year,5,4) AS INTEGER)


        ELSE CAST(year AS INTEGER)

    END AS year,


    operating_activity,
    investing_activity,
    financing_activity,
    net_cash_flow


    FROM cashflow


    WHERE company_id=?
    AND year IS NOT NULL


    GROUP BY year


    ORDER BY year ASC


    """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# =========================================================
# FINANCIAL RATIOS
# =========================================================


@router.get("/companies/{ticker}/ratios")
def get_ratios(ticker: str, year: int | None = None):
    """Function: get_ratios"""
    conn = get_connection()

    query = """

    SELECT *

    FROM financial_ratios

    WHERE company_id=?

    """

    params = [ticker.upper()]

    if year:

        query += " AND year=?"

        params.append(year)

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# =========================================================
# COMPANY PROFILE
# =========================================================


@router.get("/companies/{ticker}")
def get_company_profile(ticker: str):
    """Function: get_company_profile"""
    conn = get_connection()

    ticker = ticker.upper()

    company = conn.execute(
        """
        SELECT *

        FROM companies

        WHERE id=?

        """,
        (ticker,),
    ).fetchone()

    if not company:

        raise HTTPException(status_code=404, detail="Company not found")

    latest = conn.execute(
        """
        SELECT *

        FROM financial_ratios

        WHERE company_id=?

        ORDER BY year DESC

        LIMIT 1

        """,
        (ticker,),
    ).fetchone()

    sector = conn.execute(
        """
        SELECT *

        FROM sectors

        WHERE company_id=?

        """,
        (ticker,),
    ).fetchone()

    conn.close()

    return {
        "company": dict(company),
        "latest_kpis": dict(latest) if latest else None,
        "sector": dict(sector) if sector else None,
    }


# =========================================================
# PDF TEARSHEET
# =========================================================


@router.get("/companies/{ticker}/tearsheet")
def get_tearsheet(ticker: str):
    """Function: get_tearsheet"""
    path = f"reports/tearsheets/{ticker.upper()}.pdf"

    if not os.path.exists(path):

        raise HTTPException(status_code=404, detail="Tearsheet not generated")

    return FileResponse(path, media_type="application/pdf")
