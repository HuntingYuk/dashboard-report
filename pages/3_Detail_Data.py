import streamlit as st
from utils.loader import load_data
import pandas as pd
import re

st.title("📋 DETAIL DATA LAPORAN")

# =====================
# LOAD DATA
# =====================
df = load_data()

# =====================
# AMBIL FILTER GLOBAL
# =====================
bulan = st.session_state.get("bulan", [])
pic = st.session_state.get("pic", [])

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
# NORMALISASI PIC (AGAR BISA FILTER MULTI PIC)
# =====================
def normalisasi_pic(df):
    df = df.copy()

    df["NAMA PIC_SPLIT"] = (
        df["NAMA PIC"]
        .astype(str)
        .str.lower()
        .apply(lambda x: re.split(r"[;,/]", x))
    )

    df = df.explode("NAMA PIC_SPLIT")
    df["NAMA PIC_SPLIT"] = df["NAMA PIC_SPLIT"].str.strip()
    df = df[df["NAMA PIC_SPLIT"] != ""]

    return df

df_pic = normalisasi_pic(df)

# =====================
# FILTER DATA
# =====================
df_f = df_pic.copy()

if bulan:
    df_f = df_f[df_f["TANGGAL"].isin(bulan)]

if pic:
    df_f = df_f[df_f["NAMA PIC_SPLIT"].isin(pic)]

# =====================
# KEMBALIKAN KE FORMAT AWAL (HAPUS DUPLIKAT SETELAH EXPLODE)
# =====================
df_final = df_f.drop(columns=["NAMA PIC_SPLIT"]).drop_duplicates()

# =====================
# TAMPILKAN DATA
# =====================
st.dataframe(df_final, use_container_width=True)

# =====================
# DOWNLOAD BUTTON (DATA SUDAH TERFILTER)
# =====================
st.download_button(
    "📥 Download CSV",
    df_final.to_csv(index=False),
    "laporan_filtered.csv",
    "text/csv"
)
