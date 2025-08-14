# ui.py
import base64
import streamlit as st

# tweak these if you want later
LOGO_PATH = "assets/umbil_logo.png"
LOGO_HEIGHT = 76  # "much bigger" – try 76–88 if you want even bigger

def _logo_html(height: int = LOGO_HEIGHT) -> str:
    try:
        with open(LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f'''
        <a href="./" title="Umbil Home" style="display:inline-block;">
            <img src="data:image/png;base64,{b64}" alt="Umbil logo"
                 style="height:{height}px; vertical-align:middle;"/>
        </a>
        '''
    except Exception:
        return '<a href="./" title="Umbil Home" style="text-decoration:none;font-weight:700;">Umbil</a>'

def hide_streamlit_sidebar():
    st.markdown(
        """
        <style>
          /* Hide the default sidebar */
          section[data-testid="stSidebar"] { display: none !important; }

          /* Extra top padding so the logo/nav never look cut off */
          div.block-container { padding-top: 3.0rem; }

          /* Make page_link widgets sit closer together */
          div[data-baseweb="button"] { margin-right: 0.25rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _safe_page_link(target, label, icon=""):
    try:
        st.page_link(target, label=label, icon=icon or None)
    except Exception:
        if st.button(f"{icon} {label}"):
            try:
                st.switch_page(target)
            except Exception:
                pass

def render_topbar(active="home"):
    hide_streamlit_sidebar()

    # Three columns: big logo on the left, a wide spacer in the middle,
    # a narrow right column for nav (so the buttons hug the right side).
    # Adjust [2, 8, 3] if you want even further right: e.g. [2, 9, 2]
    col_logo, col_spacer, col_nav = st.columns([2, 8, 3], gap="small")

    with col_logo:
        st.markdown(_logo_html(), unsafe_allow_html=True)

    with col_nav:
        # 3 mini-columns inside the right-most column for the three links
        a, b, c = st.columns([1, 1, 1], gap="small")
        with a:
            _safe_page_link("pages/cpd.py", "CPD Log", "CPD Log🗂️")
        with b:
            _safe_page_link("pages/pdp.py", "PDP Goals", "PDP Goals🎯")
        with c:
            _safe_page_link("pages/settings.py", "Settings", "Settings⚙️")
