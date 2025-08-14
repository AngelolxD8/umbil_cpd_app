# ui.py
import base64
import streamlit as st

LOGO_PATH = "assets/umbil_logo.png"  # keep your file here

def _logo_html() -> str:
    try:
        with open(LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        # Clickable logo → Home
        return f'''
        <a href="./" title="Umbil Home" style="display:inline-block;">
            <img src="data:image/png;base64,{b64}" alt="Umbil logo" style="height:40px;vertical-align:middle;"/>
        </a>
        '''
    except Exception:
        # Fallback text if the file can't be read for any reason
        return '<a href="./" title="Umbil Home" style="text-decoration:none;font-weight:700;">Umbil</a>'

def hide_streamlit_sidebar():
    st.markdown(
        """
        <style>
          /* Hide the default sidebar (including nav) */
          section[data-testid="stSidebar"] {display: none;}
          /* Reduce top padding a bit */
          div.block-container {padding-top: 1rem;}
          /* Simple topbar layout spacing */
          .umbil-topbar {display:flex; align-items:center; justify-content:space-between;}
          .umbil-topbar .nav a {margin-left: 1rem; text-decoration:none; font-weight:600;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def _safe_page_link(target, label, icon=""):
    # Prefer Streamlit's built-in page_link when available
    try:
        st.page_link(target, label=label, icon=icon or None)
    except Exception:
        # Fallback to a button + switch_page for older versions
        if st.button(f"{icon} {label}"):
            try:
                st.switch_page(target)
            except Exception:
                pass

def render_topbar(active="home"):
    hide_streamlit_sidebar()

    # Wrap in a single row container
    st.markdown('<div class="umbil-topbar">', unsafe_allow_html=True)
    col_logo, col_nav = st.columns([1, 3])

    with col_logo:
        st.markdown(_logo_html(), unsafe_allow_html=True)

    with col_nav:
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            _safe_page_link("pages/cpd.py", "CPD Log", "🗂️")        # <-- lowercase
        with c2:
            _safe_page_link("pages/pdp.py", "PDP Goals", "🎯")      # <-- lowercase
        with c3:
            _safe_page_link("pages/settings.py", "Settings", "⚙️")  # <-- lowercase

    st.markdown("</div>", unsafe_allow_html=True)
