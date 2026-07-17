import pandas as pd
import streamlit as st
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
    companies["company_name"] == selected_company
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

    st.write("### About Company")

    st.write(
        row["about_company"]
        if pd.notna(row["about_company"])
        else "No description available"
    )

    if pd.notna(row["website"]):

        st.write(
            f"Website: {row['website']}"
        )

    ticker = row["id"]

    pl = get_pl(ticker)

    if not pl.empty:

        fig1 = px.bar(
            pl.dropna(subset=["year"]),
            x="year",
            y="sales",
            title="Revenue Trend"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        fig2 = px.line(
            pl.dropna(subset=["year"]),
            x="year",
            y="net_profit",
            title="Net Profit Trend"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:

        st.warning(
            f"No P&L data found for {ticker}"
        )