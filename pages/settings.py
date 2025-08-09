import streamlit as st
import os
from storage import CPD_FILE, PDP_FILE, save_cpd, save_pdp

st.set_page_config(page_title="Settings", layout="centered")

st.title("⚙️ Settings")

# --- Clear CPD log with confirmation ---
st.subheader("🗂️ CPD Log")
if st.button("🗑️ Clear CPD Log"):
    st.session_state.show_clear_cpd_confirm = True

if st.session_state.get("show_clear_cpd_confirm", False):
    st.warning("Are you sure you want to delete **all CPD log entries**? This cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, clear CPD log"):
            st.session_state.cpd_log = []
            save_cpd([])  # Overwrite CSV with empty file
            if os.path.exists(CPD_FILE):
                os.remove(CPD_FILE)
            st.session_state.show_clear_cpd_confirm = False
            st.success("✅ CPD log cleared from memory and file.")
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.show_clear_cpd_confirm = False

st.markdown("---")

# --- Clear PDP goals with confirmation ---
st.subheader("🎯 PDP Goals")
if st.button("🗑️ Clear PDP Goals"):
    st.session_state.show_clear_pdp_confirm = True

if st.session_state.get("show_clear_pdp_confirm", False):
    st.warning("Are you sure you want to delete **all PDP goals**? This cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, clear PDP goals"):
            st.session_state.pdp_goals = []
            save_pdp([])  # Overwrite CSV with empty file
            if os.path.exists(PDP_FILE):
                os.remove(PDP_FILE)
            st.session_state.show_clear_pdp_confirm = False
            st.success("✅ PDP goals cleared from memory and file.")
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.show_clear_pdp_confirm = False

st.markdown("---")
st.caption("Clearing data will remove it permanently from both memory and disk.")
