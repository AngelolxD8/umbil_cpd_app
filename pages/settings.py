import os
import streamlit as st
from ui import render_topbar
from storage import CPD_FILE, PDP_FILE, save_cpd, save_pdp

st.set_page_config(page_title="Settings", layout="centered", initial_sidebar_state="collapsed")
render_topbar(active="settings")

st.title("Settings")

st.subheader("CPD Log")
if st.button("Clear CPD Log"):
    st.session_state.show_clear_cpd_confirm = True

if st.session_state.get("show_clear_cpd_confirm", False):
    st.warning("Delete all CPD log entries? This cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, clear CPD log"):
            st.session_state.cpd_log = []
            save_cpd([])
            if os.path.exists(CPD_FILE):
                os.remove(CPD_FILE)
            st.session_state.show_clear_cpd_confirm = False
            st.success("CPD log cleared.")
    with col2:
        if st.button("Cancel"):
            st.session_state.show_clear_cpd_confirm = False

st.subheader("PDP Goals")
if st.button("Clear PDP Goals"):
    st.session_state.show_clear_pdp_confirm = True

if st.session_state.get("show_clear_pdp_confirm", False):
    st.warning("Delete all PDP goals? This cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, clear PDP goals"):
            st.session_state.pdp_goals = []
            save_pdp([])
            if os.path.exists(PDP_FILE):
                os.remove(PDP_FILE)
            st.session_state.show_clear_pdp_confirm = False
            st.success("PDP goals cleared.")
    with col2:
        if st.button("Cancel"):
            st.session_state.show_clear_pdp_confirm = False

st.caption("Clearing data removes it permanently from both memory and disk.")

st.subheader("Appearance")
st.text("Theme: to be added")
