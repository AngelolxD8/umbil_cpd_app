# Home.py
import os
from datetime import datetime
from collections import Counter

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI  # ✅ new import

from ui import render_topbar
from storage import load_cpd, save_cpd, load_pdp, save_pdp

# Must be the first Streamlit call
st.set_page_config(
    page_title="Umbil – Clinical CPD Assistant",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown("""
    <style>
        .splash {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: #0E1117;  /* dark background */
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            font-size: 2em;
            z-index: 9999;
            opacity: 1;
            transition: opacity 0.8s ease;
        }
        .splash h1 {
            font-size: 3em;
            margin-bottom: 0.5em;
            color: #2B6CB0;
        }
        .splash p {
            font-size: 1.2em;
            opacity: 0.8;
        }
        .splash.fade-out {
            opacity: 0;
            pointer-events: none;
        }
    </style>

    <div class="splash" id="splash">
        <h1>🧠 Umbil</h1>
        <p>Clinical CPD Assistant is loading...</p>
    </div>

    <script>
        const interval = setInterval(function() {
            const appRoot = document.querySelector('.main');
            if (appRoot) {
                const splash = document.getElementById("splash");
                if (splash) {
                    splash.classList.add("fade-out");
                    setTimeout(() => splash.remove(), 1000);
                }
                clearInterval(interval);
            }
        }, 100);
    </script>
""", unsafe_allow_html=True)

render_topbar(active="home")  # top bar + hide sidebar

# --- Load API key ---
def load_openai_key() -> str | None:
    try:
        key = st.secrets["OPENAI_API_KEY"]  # Streamlit secrets if available
    except Exception:
        key = None
    if not key:
        load_dotenv()
        key = os.getenv("OPENAI_API_KEY")
    return key.strip().strip('"').strip("'") if key else None

OPENAI_API_KEY = load_openai_key()
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# --- Call OpenAI ---
def get_openai_response(query: str) -> str:
    if not client:
        return f"📘 Placeholder response for:\n\n**{query}**\n\n(Connect OpenAI API to get real answers.)"
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a clinical assistant for UK doctors. Use NICE, CKS, SIGN, and BNF to answer clinical questions clearly and accurately.",
                },
                {"role": "user", "content": query},
            ],
            temperature=0.3,
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Request failed: {e}"

# --- State ---
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
        ai_response = get_openai_response(query)

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
