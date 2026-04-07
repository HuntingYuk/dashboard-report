import streamlit as st
import pandas as pd
import re
from utils.loader import load_data


def normalisasi_pic(df):
    df = df.copy()

    df["NAMA PIC"] = (
        df["NAMA PIC"]
        .astype(str)
        .str.lower()
        .apply(lambda x: re.split(r"[;,/]", x))
    )

    df = df.explode("NAMA PIC")
    df["NAMA PIC"] = df["NAMA PIC"].str.strip()
    df = df[df["NAMA PIC"] != ""]

    return df


def render_sidebar():

    df = load_data()
    df_pic = normalisasi_pic(df)

    urutan_bulan = [
        "Januari", "Februari", "Maret", "April",
        "Mei", "Juni", "Juli", "Agustus",
        "September", "Oktober", "November", "Desember"
    ]

    st.sidebar.markdown("## ⚙️ Filter Data")

    bulan = st.sidebar.multiselect(
        "🗓️ Bulan",
        urutan_bulan,
        default=st.session_state.get("bulan", [])
    )

    pic = st.sidebar.multiselect(
        "👤 PIC",
        sorted(df_pic["NAMA PIC"].unique()),
        default=st.session_state.get("pic", [])
    )

    # Simpan ke session_state agar bisa dipakai semua page
    st.session_state["bulan"] = bulan
    st.session_state["pic"] = pic

    # Spacer agar turun ke bawah
    st.sidebar.markdown("---")
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
