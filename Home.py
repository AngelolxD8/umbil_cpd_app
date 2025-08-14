# Home.py
import os
from datetime import datetime
from collections import Counter

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

from ui import render_topbar
from storage import load_cpd, save_cpd, load_pdp, save_pdp

# Must be the first Streamlit call
st.set_page_config(
    page_title="Umbil – Clinical CPD Assistant",
    layout="centered",
    initial_sidebar_state="collapsed",
)
render_topbar(active="home")  # top bar + hide sidebar

# Secrets / env (safe even if secrets.toml is missing)
load_dotenv()  # read .env if present
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # 1) env / .env
if not OPENROUTER_API_KEY:
    try:
        # 2) Streamlit secrets (only if a secrets.toml exists)
        OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        OPENROUTER_API_KEY = None  # run without a key (shows placeholder answers)

# ---------- OpenRouter helper + request ----------
def _app_referer() -> str:
    # Use local dev URL unless you set APP_URL in your env
    return os.getenv("APP_URL", "http://localhost:8501")

def get_openrouter_response(query: str) -> str:
    if not OPENROUTER_API_KEY:
        return "📘 Placeholder response (no OpenRouter key configured)."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": _app_referer(),  # recommended by OpenRouter
        "X-Title": "UmbilCPD",
    }
    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a clinical assistant for UK doctors. Use NICE, CKS, SIGN, and BNF "
                    "to answer clinical questions clearly and accurately."
                ),
            },
            {"role": "user", "content": query},
        ],
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]

        if r.status_code == 401:
            return (
                "⚠️ OpenRouter returned 401 (unauthorized). Double-check that:\n"
                "• The key is an **OpenRouter** key (starts with `sk-or-v1-`).\n"
                "• It’s saved as `OPENROUTER_API_KEY` in `.env` or `.streamlit/secrets.toml` (no quotes/spaces).\n"
                "• You restarted the app after editing `.env`.\n\n"
                f"Server said: {r.text}"
            )
        return f"⚠️ Error: {r.status_code} – {r.text}"
    except Exception as e:
        return f"⚠️ Request failed: {e}"
# --------------------------------------------------

# Load persisted state
if "cpd_log" not in st.session_state:
    st.session_state.cpd_log = load_cpd()
if "pdp_goals" not in st.session_state:
    st.session_state.pdp_goals = load_pdp()

# --- Two-column layout ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.title("Ask Umbil anything")
    st.caption("Concise, evidence-based answers for UK clinical practice (NICE, CKS, SIGN, BNF).")

    query = st.text_input(
        "Enter your clinical question",
        placeholder="e.g. What are the red flag features of cauda equina?",
    )

    if query:
        ai_response = (
            get_openrouter_response(query)
            if OPENROUTER_API_KEY
            else f"📘 Placeholder response for:\n\n**{query}**\n\n(Connect API to get real answers.)"
        )

        st.subheader("AI Response")
        st.code(ai_response, language="markdown")

        reflection = st.text_area("Add a short reflection (optional)", placeholder="e.g. Saw this in clinic today…")
        tags = st.text_input("Add tags (comma-separated)", placeholder="e.g. neuro, red flags, back pain")

        if st.button("Log this as CPD"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                "Timestamp": timestamp,
                "Query": query,
                "Response": ai_response,
                "Reflection": reflection,
                "Tags": [t.strip().lower() for t in tags.split(",")] if tags else [],
            }
            st.session_state.cpd_log.append(entry)
            save_cpd(st.session_state.cpd_log)
            st.success("Logged to CPD.")

        # PDP suggestions from repeated tags
        all_tags = [tag for e in st.session_state.cpd_log for tag in e.get("Tags", [])]
        for tag, count in Counter(all_tags).items():
            if count == 3:
                if st.button(f"Add '{tag}' as a PDP goal"):
                    goal = {"Topic": tag, "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    st.session_state.pdp_goals.append(goal)
                    save_pdp(st.session_state.pdp_goals)
                    st.success(f"PDP goal added: {tag}")

with right_col:
    if st.session_state.cpd_log:
        st.subheader("My CPD Log (recent)")
        df = pd.DataFrame(st.session_state.cpd_log)
        df["Tags"] = df["Tags"].apply(lambda x: " | ".join([f"🏷️ {t}" for t in x]) if isinstance(x, list) else "")
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "Download CPD Log (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="umbil_cpd_log.csv",
            mime="text/csv",
        )

    if st.session_state.pdp_goals:
        st.subheader("My PDP Goals")
        gdf = pd.DataFrame(st.session_state.pdp_goals)
        st.table(gdf)
        st.download_button(
            "Download PDP Goals (CSV)",
            data=gdf.to_csv(index=False).encode("utf-8"),
            file_name="umbil_pdp_goals.csv",
            mime="text/csv",
        )
