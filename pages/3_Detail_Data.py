import streamlit as st
import pandas as pd
import re
from utils.loader import load_data, URUTAN_BULAN

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

df["TANGGAL"] = pd.Categorical(
    df["TANGGAL"],
    categories=URUTAN_BULAN,
    ordered=True
)

# =====================
# NORMALISASI PIC (PAKAI KOLOM TERPISAH AGAR NAMA PIC ASLI TETAP)
# =====================
df["PIC_SPLIT"] = (
    df["NAMA PIC"]
    .astype(str)
    .str.lower()
    .apply(lambda x: re.split(r"[;,/]", x))
)

df = df.explode("PIC_SPLIT")
df["PIC_SPLIT"] = df["PIC_SPLIT"].str.strip()
df = df[df["PIC_SPLIT"] != ""]

# =====================
# FILTER DATA
# =====================
if bulan:
    df = df[df["TANGGAL"].isin(bulan)]

if pic:
    df = df[df["PIC_SPLIT"].isin(pic)]

df_final = df.drop(columns=["PIC_SPLIT"]).drop_duplicates()

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
