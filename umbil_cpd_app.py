import streamlit as st
from datetime import datetime
import pandas as pd
import os
import requests
from dotenv import load_dotenv
from collections import Counter

# --- ENV LOADING ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Umbil – Clinical CPD Assistant", layout="centered")

# --- SESSION STATE ---
if "cpd_log" not in st.session_state:
    st.session_state.cpd_log = []

if "pdp_goals" not in st.session_state:
    st.session_state.pdp_goals = []

# --- UI HEADER ---
st.title("🧠 Umbil – Clinical CPD Assistant")
st.markdown("Ask a clinical question, get a concise summary, and log it as CPD.")

# --- INPUT ---
query = st.text_input("Enter your clinical question", placeholder="e.g. What does a high FSH mean in a 42-year-old woman?")

if query:
    # --- GEMINI API CALL ---
    if GEMINI_API_KEY:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        data = {
            "contents": [
                {
                    "parts": [{"text": f"You're a clinical assistant for UK doctors. Use NICE, CKS, SIGN, and BNF to answer this clearly:\n\n{query}"}]
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, params=params, json=data)
            gemini_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            gemini_text = "⚠️ Error from Gemini API. Please check your API key or try again later."
    else:
        gemini_text = f"📘 This is a placeholder response for your question:\n\n**{query}**\n\n(Real AI output would appear here once API is connected.)"

    # --- DISPLAY RESPONSE ---
    st.subheader("AI Response:")
    st.code(gemini_text, language="markdown")

    # --- Reflection & Tags ---
    reflection = st.text_area("Add a short reflection (optional)", placeholder="e.g. Saw this in clinic today...")
    tags = st.text_input("Add tags (comma-separated)", placeholder="e.g. gynae, hormones, fertility")

    if st.button("Log this as CPD"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.cpd_log.append({
            "Timestamp": timestamp,
            "Query": query,
            "Response": gemini_text,
            "Reflection": reflection,
            "Tags": [t.strip().lower() for t in tags.split(',')] if tags else []
        })
        st.success("✅ Logged to CPD!")

    # --- PDP Suggestions ---
    all_tags = [tag for entry in st.session_state.cpd_log for tag in entry.get("Tags", [])]
    tag_counts = Counter(all_tags)

    for tag, count in tag_counts.items():
        if count == 3:
            if st.button(f"✅ Add '{tag}' as a PDP goal"):
                st.session_state.pdp_goals.append({
                    "Topic": tag,
                    "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success(f"🎯 PDP goal added: **{tag}**")

# --- CPD LOG DISPLAY ---
if st.session_state.cpd_log:
    st.markdown("---")
    st.subheader("🗂️ My CPD Log")

    df = pd.DataFrame(st.session_state.cpd_log)
    df['Tags'] = df['Tags'].apply(lambda x: ' | '.join([f'🏷️ {t}' for t in x]) if isinstance(x, list) else '')
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CPD Log (CSV)", data=csv, file_name="umbil_cpd_log.csv", mime="text/csv")

# --- PDP GOALS DISPLAY ---
if st.session_state.pdp_goals:
    st.markdown("---")
    st.subheader("🎯 My PDP Goals")

    pdp_df = pd.DataFrame(st.session_state.pdp_goals)
    st.table(pdp_df)

    pdp_csv = pdp_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download PDP Goals (CSV)", data=pdp_csv, file_name="umbil_pdp_goals.csv", mime="text/csv")
