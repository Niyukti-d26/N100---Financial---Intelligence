import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

st.title("💰 Capital Structure")

DB = ROOT.parent / "db" / "nifty100.db"

conn = sqlite3.connect(DB)

bs = pd.read_sql(
    """
    SELECT *
    FROM balancesheet
    """,
    conn,
)

conn.close()

company = st.selectbox("Select Company", sorted(bs["company_id"].unique()))

data = bs[bs["company_id"] == company]

fig = px.line(
    data,
    x="year",
    y=["equity_capital", "borrowings"],
    markers=True,
    title="Equity vs Borrowings",
)

st.plotly_chart(fig, use_container_width=True)

fig = px.line(data, x="year", y="total_assets", markers=True, title="Total Assets")

st.plotly_chart(fig, use_container_width=True)
