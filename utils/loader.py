import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()

CSV_URL = os.getenv("CSV_URL")

@pd.api.extensions.register_dataframe_accessor("clean")
def _(_): pass  # dummy agar editor tidak error (opsional)

def load_data():
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