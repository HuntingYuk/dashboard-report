import streamlit as st
from sidebar import render_sidebar

st.set_page_config(
    page_title="Dashboard Laporan TH",
    layout="wide"
)

render_sidebar()

pg = st.navigation([
    st.Page("pages/0_Home.py", title="Home", icon="🏠"),
    st.Page("pages/1_Personel.py", title="Personel", icon="👨‍💼"),
    st.Page("pages/2_Analisis.py", title="Analisis", icon="📈"),
    st.Page("pages/3_Detail_Data.py", title="Detail Data", icon="💿"),
])

pg.run()
