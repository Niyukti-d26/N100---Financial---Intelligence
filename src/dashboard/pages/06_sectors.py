import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_sectors,
    get_ratios
)

st.title("🏭 Sector Analysis")

sectors = get_sectors()
ratios = get_ratios()

sector_summary = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="company_count")
)

st.subheader("Companies per Sector")

fig = px.bar(
    sector_summary,
    x="broad_sector",
    y="company_count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

merged = ratios.merge(
    sectors,
    on="company_id",
    how="left"
)

sector_roe = (
    merged.groupby("broad_sector")
    ["return_on_equity_pct"]
    .mean()
    .reset_index()
)

st.subheader("Average ROE by Sector")

fig = px.bar(
    sector_roe,
    x="broad_sector",
    y="return_on_equity_pct"
)

st.plotly_chart(
    fig,
    use_container_width=True
)