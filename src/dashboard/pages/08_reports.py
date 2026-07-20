import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st

st.title("📄 Reports & Downloads")

st.subheader("Available Reports")

st.info(
    """
    • Screener Export CSV

    • Peer Comparison Analysis

    • Financial Trend Reports

    • Valuation Summary (Coming Soon)

    • Capital Structure Report
    """
)

st.success(
    "Reports module is ready for Sprint 4 integration."
)