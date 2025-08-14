import streamlit as st
import pandas as pd
from ui import render_topbar
from storage import load_pdp

st.set_page_config(page_title="PDP Goals", layout="centered", initial_sidebar_state="collapsed")
render_topbar(active="pdp")

st.title("PDP Goals Overview")

if "pdp_goals" not in st.session_state:
    st.session_state.pdp_goals = load_pdp()

if not st.session_state.pdp_goals:
    st.info("No PDP goals yet. Add them from Home when repeated tags appear.")
else:
    df = pd.DataFrame(st.session_state.pdp_goals)
    st.table(df)
    st.download_button(
        "Download PDP Goals (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="umbil_pdp_goals.csv",
        mime="text/csv",
    )
