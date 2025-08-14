import streamlit as st
import pandas as pd
from ui import render_topbar
from storage import load_cpd

st.set_page_config(page_title="CPD Log", layout="centered", initial_sidebar_state="collapsed")
render_topbar(active="cpd")

st.title("CPD Log Overview")

if "cpd_log" not in st.session_state:
    st.session_state.cpd_log = load_cpd()

if not st.session_state.cpd_log:
    st.info("No CPD entries yet. Go to Home to add some.")
else:
    df = pd.DataFrame(st.session_state.cpd_log)
    df["Tags"] = df["Tags"].apply(lambda x: " | ".join([f"🏷️ {t}" for t in x]) if isinstance(x, list) else "")
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "Download CPD Log (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="umbil_cpd_log.csv",
        mime="text/csv",
    )
