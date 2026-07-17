import sqlite3
import pandas as pd
import streamlit as st

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = ROOT / "db" / "nifty100.db"


@st.cache_data(ttl=600)
def get_companies():

    conn = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_company(company_name):

    conn = sqlite3.connect(DATABASE_PATH)

    query = f"""
    SELECT *
    FROM companies
    WHERE company_name='{company_name}'
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_ratios(year=None):

    conn = sqlite3.connect(DATABASE_PATH)

    query = """
    SELECT *
    FROM financial_ratios
    """

    if year:
        query += f" WHERE year={year}"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sectors():

    conn = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = sqlite3.connect(DATABASE_PATH)

    query = f"""
    SELECT *
    FROM profitandloss
    WHERE company_id='{ticker}'
    ORDER BY year
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df