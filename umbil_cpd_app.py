import streamlit as st
from datetime import datetime
import pandas as pd
# from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --- CONFIGURATION ---
st.set_page_config(page_title="Umbil – Clinical CPD Assistant", layout="centered")

# --- SESSION STATE ---
if "cpd_log" not in st.session_state:
    st.session_state.cpd_log = []

if "pdp_goals" not in st.session_state:
    st.session_state.pdp_goals = []

# --- UI ---
st.title("🧠 Umbil – Clinical CPD Assistant")
st.markdown("Ask a clinical question, get a concise summary, and log it as CPD.")
st.info("🚧 This is a prototype. AI responses are mocked. Connect OpenAI API for real output.")

# --- INPUT ---
query = st.text_input("Enter your clinical question", placeholder="e.g. What does a high FSH mean in a 42-year-old woman?")

if query:
    # --- Mocked AI Response (replace with real OpenAI API call later) ---
    # chat_completion = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "You are a clinical assistant for UK doctors. Use trusted UK sources (e.g. NICE, CKS, SIGN, BNF) to return clear, responsible, evidence-based summaries."},
    #         {"role": "user", "content": query}
    #     ],
    #     temperature=0.3,
    #     max_tokens=500
    # )
    # response = chat_completion.choices[0].message.content

    response = f"📘 This is a placeholder response for your question:\n\n**{query}**\n\n(Real AI output would appear here.)"

    st.subheader("AI Response:")
    st.code(response, language="markdown")

    # --- Reflection input ---
    reflection = st.text_area("Add a short reflection (optional)", placeholder="e.g. Saw this in clinic today...")

    tags = st.text_input("Add tags (comma-separated)", placeholder="e.g. gynae, hormones, fertility")

    if st.button("Log this as CPD"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.cpd_log.append({
            "Timestamp": timestamp,
            "Query": query,
            "Response": response,
            "Reflection": reflection,
            "Tags": [t.strip().lower() for t in tags.split(',')] if tags else []
        })
        st.success("✅ Logged to CPD!")

    # Count all tags
    from collections import Counter
    all_tags = [tag for entry in st.session_state.cpd_log for tag in entry.get("Tags", [])]
    tag_counts = Counter(all_tags)

    # Suggest PDP if any tag appears 3+ times
    for tag, count in tag_counts.items():
        if count == 3:
    if st.button(f"✅ Add '{tag}' as a PDP goal"):
        st.session_state.pdp_goals.append({
            "Topic": tag,
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success(f"🎯 PDP goal added: **{tag}**")



# --- CPD Log Display ---
if st.session_state.cpd_log:
    st.markdown("---")
    st.subheader("🗂️ My CPD Log")
    
    df = pd.DataFrame(st.session_state.cpd_log)
    df['Tags'] = df['Tags'].apply(lambda x: ' | '.join([f'🏷️ {t}' for t in x]) if isinstance(x, list) else '')
    
    st.dataframe(df)

    # --- Download option ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CPD Log (CSV)", data=csv, file_name="umbil_cpd_log.csv", mime="text/csv")

# --- PDP Goals Display ---
if st.session_state.pdp_goals:
    st.markdown("---")
    st.subheader("🎯 My PDP Goals")

    pdp_df = pd.DataFrame(st.session_state.pdp_goals)
    st.table(pdp_df)

    # --- PDP Download Button ---
    pdp_csv = pdp_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download PDP Goals (CSV)",
        data=pdp_csv,
        file_name="umbil_pdp_goals.csv",
        mime="text/csv"
    )

