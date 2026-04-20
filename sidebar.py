import streamlit as st
from utils.loader import load_data, normalisasi_pic, URUTAN_BULAN


def render_sidebar():

    df = load_data()
    df_pic = normalisasi_pic(df)

    st.sidebar.markdown("## ⚙️ Filter Data")

    bulan = st.sidebar.multiselect(
        "🗓️ Bulan",
        URUTAN_BULAN,
        default=st.session_state.get("bulan", [])
    )

    pic = st.sidebar.multiselect(
        "👤 PIC",
        sorted(df_pic["NAMA PIC"].unique()),
        default=st.session_state.get("pic", [])
    )

    st.session_state["bulan"] = bulan
    st.session_state["pic"] = pic

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    st.sidebar.markdown(
        f"""
    <style>
    [data-testid="stSidebar"] {{
        position: relative;
    }}

    .sidebar-footer {{
        position: fixed;
        bottom: 10px;
        left: 10px;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: gray;
        opacity: 0.8;
    }}
    </style>

    <div class="sidebar-footer">
        Threat Hunting Dashboard<br>
        <b>Version {1.2} Tahun 2026</b>
    </div>
    """,
        unsafe_allow_html=True
    )
    return bulan, pic
