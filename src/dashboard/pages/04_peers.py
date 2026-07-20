import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from peer_engine.engine import PeerEngine

st.title("🤝 Peer Comparison")

engine = PeerEngine()

df = engine.generate_peer_comparison()

peer_groups = sorted(
    df["peer_group_name"]
    .dropna()
    .unique()
)

selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups
)

group_df = df[
    df["peer_group_name"]
    == selected_group
].copy()

companies = sorted(
    group_df["company_id"]
    .unique()
)

selected_company = st.selectbox(
    "Select Company",
    companies
)

company_row = group_df[
    group_df["company_id"]
    == selected_company
].iloc[0]

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "interest_coverage",
    "asset_turnover"
]

peer_avg = (
    group_df[metrics]
    .mean()
)

company_values = [
    company_row[m]
    for m in metrics
]

peer_values = [
    peer_avg[m]
    for m in metrics
]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=metrics,
        fill="toself",
        name=selected_company
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=metrics,
        fill="toself",
        name="Peer Average"
    )
)

fig.update_layout(
    title=f"{selected_company} vs Peer Average",
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    showlegend=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Peer Group Comparison")

display_cols = [
    "company_id",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "composite_quality_score",
    "is_benchmark"
]

peer_table = (
    group_df[display_cols]
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
)

def highlight_benchmark(row):

    if row["is_benchmark"] == 1:
        return [
            "background-color: gold"
        ] * len(row)

    return [""] * len(row)

st.dataframe(
    peer_table
    .style
    .apply(
        highlight_benchmark,
        axis=1
    ),
    use_container_width=True
)