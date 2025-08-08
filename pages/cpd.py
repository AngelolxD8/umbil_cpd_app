import streamlit as st
import pandas as pd

st.set_page_config(page_title="CPD Log", layout="centered")

st.write("✅ CPD log page loaded")  # Debug test

st.title("🗂️ CPD Log Overview")

# Ensure CPD log exists
if "cpd_log" not in st.session_state:
    st.session_state.cpd_log = []

if not st.session_state.cpd_log:
    st.info("No CPD entries logged yet. Go to the Home page to add some!")
else:
    df = pd.DataFrame(st.session_state.cpd_log)
    df['Tags'] = df['Tags'].apply(
        lambda x: ' | '.join([f'🏷️ {t}' for t in x]) if isinstance(x, list) else ''
    )
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download CPD Log (CSV)",
        data=csv,
        file_name="umbil_cpd_log.csv",
        mime="text/csv"
    )
