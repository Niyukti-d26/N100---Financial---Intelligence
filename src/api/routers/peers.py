from fastapi import APIRouter, HTTPException
import sqlite3

from src.config.settings import DATABASE_PATH


router = APIRouter(
    tags=["Peers"]
)


def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn


@router.get("/peers/{group_name}")
def get_peers(group_name: str):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            p.peer_group_name,
            p.company_id,
            p.is_benchmark,
            c.company_name
        FROM peer_groups p
        JOIN companies c
        ON p.company_id = c.id
        WHERE p.peer_group_name = ?
        """,
        (group_name,)
    ).fetchall()

    conn.close()

    if not rows:

        raise HTTPException(
            status_code=404,
            detail="Peer group not found"
        )

    return {
        "peer_group": group_name,
        "companies": [
            dict(r)
            for r in rows
        ]
    }

@router.get("/companies/{ticker}/peers/compare")
def compare_company_peers(ticker: str):

    conn = get_connection()

    ticker = ticker.upper()


    # Get company details
    company = conn.execute(
        """
        SELECT
            id,
            company_name
        FROM companies
        WHERE id = ?
        """,
        (ticker,)
    ).fetchone()


    if not company:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )


    # Find peer group
    peer_group = conn.execute(
        """
        SELECT
            peer_group_name
        FROM peer_groups
        WHERE company_id = ?
        LIMIT 1
        """,
        (ticker,)
    ).fetchone()


    if not peer_group:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Peer group not found"
        )


    group_name = peer_group["peer_group_name"]


    # Get peer companies
    peers = conn.execute(
        """
        SELECT
            p.company_id,
            c.company_name
        FROM peer_groups p
        JOIN companies c
            ON p.company_id = c.id
        WHERE p.peer_group_name = ?
        """,
        (group_name,)
    ).fetchall()


    conn.close()


    return {
        "company_id": ticker,
        "company_name": company["company_name"],
        "peer_group": group_name,
        "peer_companies": [
            dict(row)
            for row in peers
        ]
    }