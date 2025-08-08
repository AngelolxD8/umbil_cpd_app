import streamlit as st
import pandas as pd
from storage import load_pdp  # this reads the CSV

st.set_page_config(page_title="PDP Goals", layout="centered")

st.write("✅ PDP Goals page loaded")  # Debug check

st.title("🎯 PDP Goals Overview")

# Load from session state or CSV
if "pdp_goals" not in st.session_state:
    st.session_state.pdp_goals = load_pdp()

# Show table or message
if not st.session_state.pdp_goals:
    st.info("No PDP goals yet. Add them from the Home page when you log CPD with repeated tags.")
else:
    pdp_df = pd.DataFrame(st.session_state.pdp_goals)
    st.table(pdp_df)

    pdp_csv = pdp_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download PDP Goals (CSV)",
        data=pdp_csv,
        file_name="umbil_pdp_goals.csv",
        mime="text/csv"
    )
