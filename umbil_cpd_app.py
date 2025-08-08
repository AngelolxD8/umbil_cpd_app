
import streamlit as st
from datetime import datetime
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --- CONFIGURATION ---
st.set_page_config(page_title="Umbil – Clinical CPD Assistant", layout="centered")

# --- SESSION STATE ---
if "cpd_log" not in st.session_state:
    st.session_state.cpd_log = []

# --- UI ---
st.title("🧠 Umbil – Clinical CPD Assistant")
st.markdown("Ask a clinical question, get a concise summary, and log it as CPD.")

# --- INPUT ---
query = st.text_input("Enter your clinical question", placeholder="e.g. What does a high FSH mean in a 42-year-old woman?")

if query:
    # Mock GPT output (replace with real API later)
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a clinical assistant for UK doctors. Use trusted UK sources (e.g. NICE, CKS, SIGN, BNF) to return clear, responsible, evidence-based summaries."},
            {"role": "user", "content": query}
    ],
    temperature=0.3,
    max_tokens=500
)

    response = chat_completion.choices[0].message.content


    st.subheader("AI Response:")
    
    st.code(response, language="markdown")

    # Reflection input
    reflection = st.text_area("Add a short reflection (optional)", placeholder="e.g. Saw this in clinic today...")

    if st.button("Log this as CPD"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.cpd_log.append({
            "Timestamp": timestamp,
            "Query": query,
            "Response": response,
            "Reflection": reflection
        })
        st.success("✅ Logged to CPD!")

# --- CPD Log Display ---
if st.session_state.cpd_log:
    st.markdown("---")
    st.subheader("🗂️ My CPD Log")
    df = pd.DataFrame(st.session_state.cpd_log)
    st.dataframe(df)

    # Allow export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CPD Log (CSV)", data=csv, file_name="umbil_cpd_log.csv", mime="text/csv")
