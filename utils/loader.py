import os
import streamlit as st
import pandas as pd
import re
from dotenv import load_dotenv

load_dotenv()

CSV_URL = os.getenv("CSV_URL")

@pd.api.extensions.register_dataframe_accessor("clean")
def _(_): pass  # dummy agar editor tidak error (opsional)

@st.cache_data(ttl=300)
def load_data():
    if not CSV_URL:
        raise RuntimeError("CSV_URL environment variable is not set. Set it in .env (local) or via secret (k8s).")
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    df["TANGGAL"] = df["TANGGAL"].astype(str).str.strip().str.capitalize()
    df["NAMA PIC"] = df["NAMA PIC"].astype(str).str.strip()
    df["JENIS LAPORAN"] = df["JENIS LAPORAN"].astype(str).str.strip()
    df["SEKTOR"] = df["SEKTOR"].astype(str).str.strip()
    df["SH"] = df["SH"].astype(str).str.strip()
    df["SUBSEKTOR"] = df["SUBSEKTOR"].astype(str).str.strip()
    df["IIV"] = df["IIV"].astype(str).str.strip()
    df["STATUS"] = df["STATUS"].astype(str).str.strip()
    df["ARSIP"] = df["ARSIP"].astype(str).str.strip()
    return df


URUTAN_BULAN = [
    "Januari", "Februari", "Maret", "April",
    "Mei", "Juni", "Juli", "Agustus",
    "September", "Oktober", "November", "Desember"
]


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
