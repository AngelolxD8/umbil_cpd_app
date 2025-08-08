import streamlit as st
from datetime import datetime
import pandas as pd
from collections import Counter

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Umbil – Clinical CPD Assistant", layout="wide")

# ------------------ SESSION STATE ------------------
if "cpd_log" not in st.session_state:
    st.session_state.cpd_log = []

if "pdp_goals" not in st.session_state:
    st.session_state.pdp_goals = []

if "page" not in st.session_state:
    st.session_state.page = "Home"  # Default page

# ------------------ NAVIGATION BAR ------------------
col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
with col1:
    st.markdown("### **U Umbil**")
with col2:
    if st.button("CPD Log"):
        st.session_state.page = "CPD Log"
with col3:
    if st.button("PDP Goals"):
        st.session_state.page = "PDP Goals"
with col4:
    if st.button("Settings"):
        st.session_state.page = "Settings"

st.markdown("---")

# ------------------ HOME PAGE ------------------
if st.session_state.page == "Home":
    left, right = st.columns([2, 1])

    with left:
        st.header("Ask Umbil anything")
        query = st.text_input("Enter a question or topic...")

        if query:
            # Placeholder response (API integration disabled for now)
            ai_response = f"📘 This is a placeholder answer for:\n\n**{query}**\n\n(Replace with real AI output later.)"

            st.subheader("AI Response")
            st.markdown(ai_response)

            reflection = st.text_area("Reflection (optional)")
            tags = st.text_input("Tags (comma-separated)")

            if st.button("Log as CPD"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.cpd_log.append({
                    "Timestamp": timestamp,
                    "Query": query,
                    "Response": ai_response,
                    "Reflection": reflection,
                    "Tags": [t.strip().lower() for t in tags.split(',')] if tags else []
                })
                st.success("✅ CPD entry logged!")

                # Suggest PDP goal if tag appears 3+ times
                all_tags = [tag for entry in st.session_state.cpd_log for tag in entry.get("Tags", [])]
                tag_counts = Counter(all_tags)
                for tag, count in tag_counts.items():
                    if count >= 3 and tag not in [goal["Topic"] for goal in st.session_state.pdp_goals]:
                        st.info(f"You've logged several entries about **{tag}**. Add as a PDP goal?")
                        if st.button(f"✅ Add '{tag}' as PDP goal"):
                            st.session_state.pdp_goals.append({
                                "Topic": tag,
                                "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            st.success(f"PDP goal '{tag}' added!")

    with right:
        st.subheader("Quick Actions")
        st.write("📥 Download your CPD log or PDP goals anytime.")

        if st.session_state.cpd_log:
            df = pd.DataFrame(st.session_state.cpd_log)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CPD Log (CSV)", data=csv, file_name="cpd_log.csv", mime="text/csv")

        if st.session_state.pdp_goals:
            pdp_df = pd.DataFrame(st.session_state.pdp_goals)
            pdp_csv = pdp_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download PDP Goals (CSV)", data=pdp_csv, file_name="pdp_goals.csv", mime="text/csv")

# ------------------ CPD LOG PAGE ------------------
elif st.session_state.page == "CPD Log":
    st.header("🗂️ My CPD Log")
    if st.session_state.cpd_log:
        df = pd.DataFrame(st.session_state.cpd_log)
        df['Tags'] = df['Tags'].apply(lambda x: ' | '.join([f'🏷️ {t}' for t in x]) if isinstance(x, list) else '')
        st.dataframe(df)
    else:
        st.info("No CPD entries yet.")

# ------------------ PDP GOALS PAGE ------------------
elif st.session_state.page == "PDP Goals":
    st.header("🎯 My PDP Goals")
    if st.session_state.pdp_goals:
        st.table(pd.DataFrame(st.session_state.pdp_goals))
    else:
        st.info("No PDP goals yet.")

# ------------------ SETTINGS PAGE ------------------
elif st.session_state.page == "Settings":
    st.header("⚙️ Settings")
    st.write("Future settings can be added here.")
    st.write("- Change API key")
    st.write("- Export all data")
    st.write("- Clear logs")
