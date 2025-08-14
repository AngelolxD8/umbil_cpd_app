# ui.py
import base64
import streamlit as st

LOGO_PATH = "assets/umbil_logo.png"
LOGO_HEIGHT = 76  # tweak if you want bigger/smaller

def _logo_html(height: int = LOGO_HEIGHT) -> str:
    try:
        with open(LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
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

          /* Give the top area breathing room so nothing looks clipped */
          div.block-container { padding-top: 3rem; }

          /* Make nav buttons sit on one line */
          button[kind], div[data-baseweb="button"] button {
            white-space: nowrap;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _nav_button(label: str, target: str, key: str):
    if st.button(label, key=key):
        try:
            st.switch_page(target)
        except Exception:
            pass

def render_topbar(active="home"):
    hide_streamlit_sidebar()

    # [logo] [big spacer] [wide right nav]
    # Make the right column wider so labels don't squish.
    col_logo, col_spacer, col_nav = st.columns([2, 6, 8], gap="small")

    with col_logo:
        st.markdown(_logo_html(), unsafe_allow_html=True)

    with col_nav:
        # three equal columns for nav buttons
        a, b, c = st.columns([1, 1, 1], gap="small")
        with a:
            _nav_button("📁 CPD Log", "pages/cpd.py", "nav_cpd")
        with b:
            _nav_button("🎯 PDP Goals", "pages/pdp.py", "nav_pdp")
        with c:
            _nav_button("⚙️ Settings", "pages/settings.py", "nav_settings")
