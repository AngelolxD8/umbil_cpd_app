import streamlit as st
from datetime import datetime
import pandas as pd
import os
import requests
from dotenv import load_dotenv
from collections import Counter

# --- ENV LOADING ---
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ✅ Debugging: Show whether the API key is loaded (only temporarily)
st.write("🔑 OpenRouter API Key Found:", OPENROUTER_API_KEY is not None)

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

# --- Function to get AI Response ---
def get_openrouter_response(query):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://umbil.com",  # or your dev domain
        "X-Title": "UmbilCPD"
    }
    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a clinical assistant for UK doctors. Use NICE, CKS, SIGN, and BNF to answer clinical questions clearly and accurately."
            },
            {"role": "user", "content": query}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"⚠️ Request failed: {str(e)}"

# --- INPUT ---
query = st.text_input("Enter your clinical question", placeholder="e.g. What does a high FSH mean in a 42-year-old woman?")

if query:
    if OPENROUTER_API_KEY:
        ai_response = get_openrouter_response(query)
    else:
        ai_response = f"📘 This is a placeholder response for your question:\n\n**{query}**\n\n(Real AI output would appear here once API is connected.)"

    st.subheader("AI Response:")
    st.code(ai_response, language="markdown")

    # --- Reflection & Tags ---
    reflection = st.text_area("Add a short reflection (optional)", placeholder="e.g. Saw this in clinic today...")
    tags = st.text_input("Add tags (comma-separated)", placeholder="e.g. gynae, hormones, fertility")

    if st.button("Log this as CPD"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.cpd_log.append({
            "Timestamp": timestamp,
            "Query": query,
            "Response": ai_response,
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
