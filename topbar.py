import streamlit as st

def top_bar():
    # Create a horizontal top bar
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

    # Big "🧠 Umbil" text on the left that links back to Home
    with col1:
        st.markdown(
            """
            <a href="/" style="text-decoration: none; font-size: 2rem; font-weight: bold; color: black;">
                🧠 Umbil
            </a>
            """,
            unsafe_allow_html=True
        )

    # Navigation buttons on the right
    with col2:
        if st.button("📂 CPD Log"):
            st.switch_page("pages/1_CPD_Log.py")

    with col3:
        if st.button("🎯 PDP Goals"):
            st.switch_page("pages/2_PDP_Goals.py")

    with col4:
        if st.button("⚙️ Settings"):
            st.switch_page("pages/3_Settings.py")
