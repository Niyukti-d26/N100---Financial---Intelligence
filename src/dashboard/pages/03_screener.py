import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from screener.engine import ScreenerEngine

st.title("🔍 Stock Screener")

engine = ScreenerEngine()

df = engine.df.copy()

st.sidebar.header("Filters")

roe_min = st.sidebar.slider("ROE %", 0.0, 100.0, 15.0)

de_max = st.sidebar.slider("Debt To Equity", 0.0, 10.0, 2.0)

rev_cagr_min = st.sidebar.slider("Revenue CAGR %", -20.0, 100.0, 5.0)

pat_cagr_min = st.sidebar.slider("PAT CAGR %", -20.0, 100.0, 5.0)

pe_max = st.sidebar.slider("PE Ratio", 0.0, 150.0, 50.0)

pb_max = st.sidebar.slider("PB Ratio", 0.0, 30.0, 10.0)

fcf_min = st.sidebar.slider("Free Cash Flow", -10000.0, 100000.0, 0.0)

dividend_min = st.sidebar.slider("Dividend Yield %", 0.0, 15.0, 0.0)

icr_min = st.sidebar.slider("Interest Coverage", 0.0, 100.0, 1.0)

opm_min = st.sidebar.slider("Operating Profit Margin %", 0.0, 100.0, 10.0)

filtered = df[
    (df["return_on_equity_pct"] >= roe_min)
    & (df["debt_to_equity"] <= de_max)
    & (df["revenue_cagr_5yr"] >= rev_cagr_min)
    & (df["pat_cagr_5yr"] >= pat_cagr_min)
    & (df["pe_ratio"] <= pe_max)
    & (df["pb_ratio"] <= pb_max)
    & (df["free_cash_flow_cr"] >= fcf_min)
    & (df["dividend_yield_pct"] >= dividend_min)
    & (df["interest_coverage"] >= icr_min)
    & (df["operating_profit_margin_pct"] >= opm_min)
]

filtered = filtered.sort_values("composite_quality_score", ascending=False)

st.subheader(f"{len(filtered)} companies match your filters")

display_cols = [
    "company_id",
    "broad_sector",
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "composite_quality_score",
]

st.dataframe(filtered[display_cols], use_container_width=True)

csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download CSV", csv, file_name="screener_results.csv", mime="text/csv"
)
