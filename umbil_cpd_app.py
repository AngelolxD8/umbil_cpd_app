import streamlit as st
from datetime import datetime
import pandas as pd
from collections import Counter

# --- PAGE CONFIG ---
st.set_page_config(page_title="Umbil – Clinical CPD Assistant", layout="wide")

# --- SESSION STATE ---
if "cpd_log" not in st.session_state:
    st.session_state.cpd_log = []

if "pdp_goals" not in st.session_state:
    st.session_state.pdp_goals = []

# --- TOP BAR ---
st.markdown("""
<style>
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 1.1em;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid #e6e6e6;
        background-color: white;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .top-bar a {
        margin-left: 20px;
        text-decoration: none;
        color: #444;
    }
    .top-bar a:hover {
        text-decoration: underline;
    }
</style>
<div class="top-bar">
    <div><strong>U</strong> Umbil</div>
    <div>
        <a href="#">CPD Log</a>
        <a href="#">PDP Goals</a>
        <a href="#">Settings</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("Ask Umbil anything")
    query = st.text_input("Enter a question or topic...", label_visibility="collapsed")

    if query:
        # --- MOCKED RESPONSE (replace with API call if needed) ---
        ai_response = f"""
        **Polycystic ovary syndrome (PCOS)**

        PCOS is a common endocrine disorder involving irregular or absent menstrual cycles, hyperandrogenism, and polycystic ovaries on ultrasound.
        Diagnostic criteria include two of these, after excluding other causes. Management strategies include:

        - Lifestyle modifications: weight control, exercise
        - Pharmacological: combined oral contraceptives, metformin for insulin resistance
        - Fertility treatments: clomifene citrate, letrozole

        Consult NICE/CKS guidance for details.
        """
        st.markdown(ai_response)

        # --- Reflection ---
        reflection = st.text_area("Reflection", placeholder="Reviewed NICE/CKS guidance on PCOS")

        # --- Tags ---
        tags = st.text_input("Tags (comma-separated)", placeholder="PCOS, fertility, hormones")

        # --- Log CPD Entry ---
        if st.button("Log CPD entry"):
            timestamp = datetime.now().strftime("%d %b %Y %I:%M %p")
            st.session_state.cpd_log.append({
                "Timestamp": timestamp,
                "Query": query,
                "Response": ai_response,
                "Reflection": reflection,
                "Tags": [t.strip().lower() for t in tags.split(',')] if tags else []
            })
            st.success("✅ Entry logged!")

with col_right:
    st.subheader("CPD Log")
    if st.session_state.cpd_log:
        last_entry = st.session_state.cpd_log[-1]
        st.markdown(f"**{last_entry['Timestamp']}**")
        for tag in last_entry['Tags']:
            st.markdown(f"`{tag}`")
        if last_entry["Reflection"]:
            st.write("Reflection")
            st.write(last_entry["Reflection"])

        # --- PDP Suggestion ---
        all_tags = [tag for entry in st.session_state.cpd_log for tag in entry.get("Tags", [])]
        tag_counts = Counter(all_tags)
        for tag, count in tag_counts.items():
            if count >= 3:
                st.info(f"You've logged several entries about **{tag}**. Add as PDP goal?")
                if st.button(f"Add '{tag}' as PDP goal"):
                    st.session_state.pdp_goals.append({
                        "Topic": tag,
                        "Created": datetime.now().strftime("%d %b %Y %I:%M %p")
                    })
                    st.success(f"🎯 PDP goal added: {tag}")

    # --- PDP GOALS ---
    if st.session_state.pdp_goals:
        st.markdown("### PDP Goals")
        pdp_df = pd.DataFrame(st.session_state.pdp_goals)
        st.table(pdp_df)

    # --- DOWNLOAD ---
    if st.session_state.cpd_log:
        csv = pd.DataFrame(st.session_state.cpd_log).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CPD Log (CSV)", data=csv, file_name="umbil_cpd_log.csv", mime="text/csv")
