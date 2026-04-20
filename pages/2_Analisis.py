import streamlit as st
import plotly.express as px
import pandas as pd
from utils.loader import load_data, normalisasi_pic, URUTAN_BULAN

# =====================
# LOAD DATA
# =====================
df = load_data()

# =====================
# AMBIL FILTER GLOBAL
# =====================
bulan = st.session_state.get("bulan", [])
pic = st.session_state.get("pic", [])

df["TANGGAL"] = pd.Categorical(
    df["TANGGAL"],
    categories=URUTAN_BULAN,
    ordered=True
)

df_pic = normalisasi_pic(df)

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
st.title("📊 ANALISIS NOTIFIKASI STAKEHOLDER")

# =====================
# TOP 10 STAKEHOLDER
# =====================
top_sh = (
    df_f["SH"]
    .dropna()
    .value_counts()
    .head(10)
    .reset_index()
)

top_sh.columns = ["Stakeholder", "Jumlah Notifikasi"]

# =====================
# KOMPOSISI SEKTOR
# =====================
sektor = (
    df_f["SEKTOR"]
    .dropna()
    .value_counts()
    .reset_index()
)

sektor.columns = ["Sektor", "Jumlah"]

# =====================
# KOMPOSISI IIV vs NON IIV
# =====================
iiv_df = df_f.copy()

iiv_df["Kategori IIV"] = (
    iiv_df["IIV"]
    .astype(str)
    .str.strip()
    .str.lower()
    .apply(lambda x: "IIV" if x == "ya" else "Non IIV")
)

iiv_rekap = (
    iiv_df["Kategori IIV"]
    .value_counts()
    .reset_index()
)

iiv_rekap.columns = ["Kategori", "Jumlah"]

# =====================
# VISUALISASI UTAMA
# =====================
col1, col2 = st.columns([2, 1])

with col1:
    fig_bar = px.bar(
        top_sh,
        x="Stakeholder",
        y="Jumlah Notifikasi",
        color="Jumlah Notifikasi",
        template="plotly_white",
        title="🏆 Top 10 Stakeholder yang Dinotifikasi"
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie_sektor = px.pie(
        sektor,
        names="Sektor",
        values="Jumlah",
        hole=0.45,
        title="🥧 Persentase Notifikasi per Sektor"
    )
    st.plotly_chart(fig_pie_sektor, use_container_width=True)

st.divider()

# =====================
# PIE IIV vs NON IIV
# =====================
fig_pie_iiv = px.pie(
    iiv_rekap,
    names="Kategori",
    values="Jumlah",
    hole=0.45,
    title="🛡️ Persentase IIV vs Non IIV"
)

st.plotly_chart(fig_pie_iiv, use_container_width=True)
