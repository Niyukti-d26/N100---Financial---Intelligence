import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_sectors
)

st.title("📊 Nifty 100 Analytics Dashboard")

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Average ROE",
        round(companies["roe_percentage"].mean(), 2)
    )

with col2:
    if "debt_to_equity" in ratios.columns:
        st.metric(
            "Median D/E",
            round(ratios["debt_to_equity"].median(), 2)
        )

with col3:
    st.metric(
        "Companies",
        len(companies)
    )

with col4:
    if "revenue_cagr_5yr" in ratios.columns:
        st.metric(
            "Median Revenue CAGR",
            round(
                ratios["revenue_cagr_5yr"].median(),
                2
            )
        )

with col5:
    if "debt_to_equity" in ratios.columns:
        debt_free_count = (
    ratios[
        ratios["debt_to_equity"] <= 0
    ]["company_id"]
    .nunique()
)
        st.metric(
            "Debt Free Companies",
            debt_free_count
        )

st.divider()

st.subheader("Sector Breakdown")

sector_counts = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="count")
)

st.dataframe(
    sector_counts,
    use_container_width=True
)

st.divider()

st.subheader("Top Companies")

top_companies = companies[
    [
        "id",
        "company_name",
        "roe_percentage",
        "roce_percentage"
    ]
].sort_values(
    "roe_percentage",
    ascending=False
)

st.dataframe(
    top_companies.head(10),
    use_container_width=True
)