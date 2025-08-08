import streamlit as st
from topbar import top_bar

st.set_page_config(page_title="Settings", layout="wide")
top_bar()

st.title("⚙️ Settings")
st.text_input("OpenRouter API Key", type="password")
st.selectbox("Theme", ["Light", "Dark", "System Default"])
