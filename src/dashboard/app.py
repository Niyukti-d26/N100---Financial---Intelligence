import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics", layout="wide", initial_sidebar_state="expanded"
)

st.title("N100 Financial Intelligence Platform")

st.success("Dashboard running successfully.")
