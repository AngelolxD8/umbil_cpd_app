# ui.py
import base64
import streamlit as st

LOGO_PATH = "assets/umbil_logo.png"
LOGO_HEIGHT = 76  # change to 88+ if you want it even bigger

def _logo_html(height: int = LOGO_HEIGHT) -> str:
    try:
        with open(LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        # target="_self" ensures same-tab navigation
        return f'''
        <a href="./" target="_self" title="Umbil Home" style="display:inline-block;">
            <img src="data:image/png;base64,{b64}" alt="Umbil logo"
                 style="height:{height}px; vertical-align:middle; cursor:pointer;"/>
        </a>
        '''
    except Exception:
        return '<a href="./" target="_self" title="Umbil Home" style="text-decoration:none;font-weight:700;">Umbil</a>'

def hide_streamlit_sidebar():
    st.markdown(
        """
        <style>
          /* Hide the default sidebar */
          section[data-testid="stSidebar"] { display: none !important; }

          /* More top padding so logo/nav never look clipped */
          div.block-container { padding-top: 3rem; }

          /* Optional: tighten spacing of page_link buttons */
          div[data-baseweb="button"] { margin-right: 0.25rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _safe_page_link(target, label):
    try:
        st.page_link(target, label=label)
    except Exception:
        if st.button(label):
            try:
                st.switch_page(target)
            except Exception:
                pass

def render_topbar(active="home"):
    hide_streamlit_sidebar()

    # layout: [logo] [big spacer] [right-aligned nav]
    col_logo, col_spacer, col_nav = st.columns([2, 8, 3], gap="small")

    with col_logo:
        st.markdown(_logo_html(), unsafe_allow_html=True)

    with col_nav:
        a, b, c = st.columns([1, 1, 1], gap="small")
        with a:
            _safe_page_link("pages/cpd.py", "📂")
        with b:
            _safe_page_link("pages/pdp.py", "🎯")
        with c:
            _safe_page_link("pages/settings.py", "⚙️")
