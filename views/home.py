import streamlit as st
import pandas as pd
import plotly.express as px
from utils.loader import load_data

def show():
    # =====================
    # SIDEBAR
    # =====================
    # Note: Global sidebar elements can be here or in app.py. 
    # Since specific pages have their own filters, we can keep them here.
    
    st.sidebar.markdown(
        "<h4 style='font-size:14px; font-weight:600;'>⚙️ Filter Data</h4>",
        unsafe_allow_html=True
    )

    bulan = st.sidebar.multiselect(
        "🗓️ Bulan",
        [
            "Januari","Februari","Maret","April","Mei","Juni",
            "Juli","Agustus","September","Oktober","November","Desember"
        ],
        default=[]
    )

    # =====================
    # GLOBAL STYLE
    # =====================
    st.markdown("""
    <style>
    .title-responsive {
        font-weight: 800;
        font-size: clamp(26px, 3.5vw, 42px);
        white-space: nowrap;
    }

    /* KPI BASE */
    .kpi {
        border-radius: 18px;
        padding: 22px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }

    /* TOTAL */
    .kpi-large {
        padding: 42px;
        min-height: 200px;
    }
    .kpi-large .kpi-value {
        font-size: 54px;
    }

    /* SMALL KPI */
    .kpi-small {
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .kpi-label {
        font-size: 13px;
        opacity: 0.9;
    }

    .kpi-value {
        font-size: 34px;
        font-weight: bold;
    }

    /* COLORS */
    .bg-total { background: linear-gradient(135deg,#2563eb,#38bdf8); }
    .bg-notif { background: linear-gradient(135deg,#ec4899,#fb7185); }
    .bg-analisis { background: linear-gradient(135deg,#f59e0b,#facc15); }
    .bg-ca { background: linear-gradient(135deg,#10b981,#34d399); }
    .bg-sektor { background: linear-gradient(135deg,#6366f1,#818cf8); }
    .bg-sensor { background: linear-gradient(135deg,#0ea5e9,#38bdf8); }
    .bg-maintenance { background: linear-gradient(135deg,#14b8a6,#5eead4); }
    .bg-log { background: linear-gradient(135deg,#8b5cf6,#a78bfa); }
    .bg-data { background: linear-gradient(135deg,#64748b,#94a3b8); }
    </style>
    """, unsafe_allow_html=True)

    # =====================
    # LOAD DATA
    # =====================
    df = load_data()

    # =====================
    # FILTER BULAN
    # =====================
    if bulan:
        df = df[df["TANGGAL"].isin(bulan)]

    # =====================
    # HITUNG JENIS LAPORAN
    # =====================
    def hitung(k):
        return df["JENIS LAPORAN"].str.contains(k, case=False, na=False).sum()

    total = len(df)

    data = {
        "notif": hitung("Notifikasi"),
        "analisis": hitung("Analisis"),
        "ca": hitung("Compromise"),
        "sektor": hitung("Sektor"),
        "sensor": hitung("Koordinasi"),
        "maintenance": hitung("Pemasangan|Pemeliharaan"),
        "log": hitung("Log"),
        "data": hitung("Data")
    }

    # =====================
    # HEADER
    # =====================
    st.markdown(
        "<div class='title-responsive'>🚀 REKAPITULASI LAPORAN THREAT HUNTING</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # =====================
    # TOTAL LAPORAN
    # =====================
    st.markdown(f"""
    <div class="kpi kpi-large bg-total">
        <div class="kpi-label">📄 TOTAL LAPORAN</div>
        <div class="kpi-value">{total}</div>
    </div>
    """, unsafe_allow_html=True)

    # =====================
    # BARIS 1 KPI
    # =====================
    cols1 = st.columns(4)
    labels1 = [
        ("🔔 Notifikasi", data["notif"], "bg-notif"),
        ("🧪 Analisis CVE/Produk", data["analisis"], "bg-analisis"),
        ("🛡️ Compromise Assessment", data["ca"], "bg-ca"),
        ("🏭 Kerentanan Sektor", data["sektor"], "bg-sektor")
    ]

    for col, (label, val, bg) in zip(cols1, labels1):
        with col:
            st.markdown(f"""
            <div class="kpi kpi-small {bg}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    # =====================
    # BARIS 2 KPI
    # =====================
    cols2 = st.columns(4)
    labels2 = [
        ("📡 Koordinasi Sensor", data["sensor"], "bg-sensor"),
        ("🛠️ Pemasangan / Pemeliharaan", data["maintenance"], "bg-maintenance"),
        ("📊 Analisis Log", data["log"], "bg-log"),
        ("📑 Data Dukung Pimpinan", data["data"], "bg-data")
    ]

    for col, (label, val, bg) in zip(cols2, labels2):
        with col:
            st.markdown(f"""
            <div class="kpi kpi-small {bg}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    # =====================
    # 🔥 STATUS LAPORAN (PIE)
    # =====================
    st.divider()
    st.subheader("📌 Distribusi Status Laporan")

    status_rekap = (
        df[df["STATUS"].notna() & (df["STATUS"] != "")]
        .groupby("STATUS")
        .size()
        .reset_index(name="Jumlah")
        .sort_values("Jumlah", ascending=False)
    )

    colA, colB = st.columns([2, 1])

    with colA:
        fig = px.pie(
            status_rekap,
            names="STATUS",
            values="Jumlah",
            hole=0.45,
            title="📊 Komposisi Status Laporan"
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with colB:
        st.dataframe(
            status_rekap,
            width="stretch",
            hide_index=True
        )
