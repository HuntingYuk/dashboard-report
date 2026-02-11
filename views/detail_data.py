import streamlit as st
from utils.loader import load_data

def show():
    st.title("📋 DETAIL DATA LAPORAN")
    df = load_data()

    st.dataframe(df, width="stretch")
    st.download_button(
        "📥 Download CSV",
        df.to_csv(index=False),
        "laporan.csv",
        "text/csv"
    )
