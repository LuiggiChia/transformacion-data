import streamlit as st
import time

st.set_page_config(
    page_icon = "💯"
)

text_placeholder = st.empty()

text = "Transformación de HS y Tácticos"

for i in range(len(text)+1):
    text_placeholder.markdown(f"<h1>{text[:i]}<h1>", unsafe_allow_html=True)
    time.sleep(0.05)