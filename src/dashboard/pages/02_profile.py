import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils.db import (
    get_companies,
    get_pl
)

st.title("🏢 Company Profile")

companies = get_companies()

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company = companies[
    companies["company_name"]
    == selected_company
]

if company.empty:

    st.error("Company not found")

else:

    row = company.iloc[0]

    st.header(row["company_name"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "ROE %",
            row["roe_percentage"]
        )

    with col2:
        st.metric(
            "ROCE %",
            row["roce_percentage"]
        )

    st.divider()

    st.subheader("About Company")

    about_text = row["about_company"]

    if pd.isna(about_text):
        about_text = "No description available"

    st.write(about_text)

    website = row["website"]

    if pd.notna(website):
        st.write(f"Website: {website}")

    ticker = row["id"]

    pl = get_pl(ticker)

    if not pl.empty:

        pl = pl.dropna(
            subset=["year"]
        )

        st.divider()

        revenue_fig = px.bar(
            pl,
            x="year",
            y="sales",
            title="Revenue Trend"
        )

        st.plotly_chart(
            revenue_fig,
            use_container_width=True
        )

        profit_fig = px.line(
            pl,
            x="year",
            y="net_profit",
            title="Net Profit Trend"
        )

        st.plotly_chart(
            profit_fig,
            use_container_width=True
        )

    else:

        st.warning(
            f"No P&L data found for {ticker}"
        )