from fastapi import APIRouter, HTTPException
import sqlite3

from src.config.settings import DATABASE_PATH


router = APIRouter(
    tags=["Documents"]
)


def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn


@router.get("/companies/{ticker}/documents")
def documents(ticker: str):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            company_id,
            year,
            annual_report
        FROM documents
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (ticker.upper(),)
    ).fetchall()

    conn.close()

    if not rows:

        raise HTTPException(
            status_code=404,
            detail="Documents not found"
        )

    return [
        dict(r)
        for r in rows
    ]