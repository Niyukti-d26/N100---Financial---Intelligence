import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

from dashboard.utils.db import get_companies, get_pl

st.title("📈 Financial Trends")

companies = get_companies()

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_row = companies[
    companies["company_name"] == selected_company
]

if company_row.empty:
    st.error("Company not found")
    st.stop()

ticker = company_row.iloc[0]["id"]

ROOT_DB = Path(__file__).resolve().parents[3]
DATABASE_PATH = ROOT_DB / "db" / "nifty100.db"

conn = sqlite3.connect(DATABASE_PATH)

pl = get_pl(ticker)

bs = pd.read_sql(
    f"""
    SELECT *
    FROM balancesheet
    WHERE company_id='{ticker}'
    ORDER BY year
    """,
    conn
)

cf = pd.read_sql(
    f"""
    SELECT *
    FROM cashflow
    WHERE company_id='{ticker}'
    ORDER BY year
    """,
    conn
)

conn.close()

pl = pl.dropna(subset=["year"])

st.subheader("Revenue Trend")

fig = px.line(
    pl,
    x="year",
    y="sales",
    markers=True,
    title="Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Net Profit Trend")

fig = px.line(
    pl,
    x="year",
    y="net_profit",
    markers=True,
    title="Net Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("EPS Trend")

fig = px.bar(
    pl,
    x="year",
    y="eps",
    title="Earnings Per Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Operating Profit Trend")

fig = px.line(
    pl,
    x="year",
    y="operating_profit",
    markers=True,
    title="Operating Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

if not bs.empty:

    st.subheader("Balance Sheet Overview")

    fig = px.line(
        bs,
        x="year",
        y=[
            "total_assets",
            "total_liabilities"
        ],
        markers=True,
        title="Assets vs Liabilities"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

if not cf.empty:

    st.subheader("Cash Flow Trend")

    fig = px.bar(
        cf,
        x="year",
        y="net_cash_flow",
        title="Net Cash Flow"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.line(
        cf,
        x="year",
        y=[
            "operating_activity",
            "investing_activity",
            "financing_activity"
        ],
        markers=True,
        title="Cash Flow Components"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )