import streamlit as st
import plotly.express as px
from utils.loader import load_data
import pandas as pd
import re

def show():
    # =====================
    # LOAD DATA
    # =====================
    df = load_data()

    # =====================
    # DEFINISI URUTAN BULAN
    # =====================
    urutan_bulan = [
        "Januari", "Februari", "Maret", "April",
        "Mei", "Juni", "Juli", "Agustus",
        "September", "Oktober", "November", "Desember"
    ]

    df["TANGGAL"] = pd.Categorical(
        df["TANGGAL"],
        categories=urutan_bulan,
        ordered=True
    )

    # =====================
    # NORMALISASI PIC (SPLIT → EXPLODE)
    # =====================
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

    df_pic = normalisasi_pic(df)

    # =====================
    # SIDEBAR (FILTER)
    # =====================
    st.sidebar.markdown("### ⚙️ Filter Data")

    bulan = st.sidebar.multiselect(
        "🗓️ Bulan",
        urutan_bulan,
        default=[]
    )

    pic = st.sidebar.multiselect(
        "👤 PIC",
        sorted(df_pic["NAMA PIC"].unique())
    )

    # =====================
    # FILTER DATA
    # =====================
    df_f = df_pic.copy()

    if bulan:
        df_f = df_f[df_f["TANGGAL"].isin(bulan)]

    if pic:
        df_f = df_f[df_f["NAMA PIC"].isin(pic)]

    # =====================
    # HEADER
    # =====================
    st.title("📊 REKAPITULASI LAPORAN PERSONEL")

    # =====================
    # KPI PIC UNIK
    # =====================
    st.metric(
        "👥 Jumlah PIC Unik",
        df_f["NAMA PIC"].nunique()
    )

    # =====================
    # REKAP TOTAL PER PIC
    # =====================
    rekap = (
        df_f
        .groupby("NAMA PIC")
        .size()
        .reset_index(name="Jumlah")
        .sort_values("Jumlah", ascending=False)
    )

    # =====================
    # REKAP BULANAN PER PIC
    # =====================
    rekap_bulanan = (
        df_f
        .groupby(["TANGGAL", "NAMA PIC"])
        .size()
        .reset_index(name="Jumlah")
        .sort_values("TANGGAL")
    )

    # =====================
    # VISUALISASI BAR & PIE
    # =====================
    colA, colB = st.columns([2, 1])

    with colA:
        fig_bar = px.bar(
            rekap,
            x="NAMA PIC",
            y="Jumlah",
            color="Jumlah",
            template="plotly_white",
            title="📊 Jumlah Laporan per PIC"
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with colB:
        fig_pie = px.pie(
            rekap,
            names="NAMA PIC",
            values="Jumlah",
            hole=0.45,
            title="🥧 Distribusi Laporan"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # =====================
    # GRAFIK TREN BULANAN
    # =====================
    st.markdown("### 📈 Tren Jumlah Laporan Per Bulan")

    fig_line = px.line(
        rekap_bulanan,
        x="TANGGAL",
        y="Jumlah",
        color="NAMA PIC",
        markers=True,
        template="plotly_white",
        category_orders={"TANGGAL": urutan_bulan},
        title="Tren Jumlah Laporan per Bulan"
    )

    fig_line.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Jumlah Laporan",
        legend_title="PIC"
    )

    st.plotly_chart(fig_line, use_container_width=True)
