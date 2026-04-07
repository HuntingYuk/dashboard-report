import streamlit as st
import pandas as pd
import plotly.express as px
import re

# =====================
# AMBIL FILTER GLOBAL DARI SIDEBAR
# =====================
bulan = st.session_state.get("bulan", [])
pic = st.session_state.get("pic", [])

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

.kpi {
    border-radius: 18px;
    padding: 22px;
    color: white;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

.kpi-large {
    padding: 42px;
    min-height: 200px;
}
.kpi-large .kpi-value {
    font-size: 54px;
}

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
    font-size: 28px;
    font-weight: bold;
}

/* KPI COLORS */
.bg-total { background: linear-gradient(135deg,#2563eb,#38bdf8); }
.bg-notif { background: linear-gradient(135deg,#ec4899,#fb7185); }
.bg-analisis { background: linear-gradient(135deg,#f59e0b,#facc15); }
.bg-ca { background: linear-gradient(135deg,#10b981,#34d399); }
.bg-sektor { background: linear-gradient(135deg,#6366f1,#818cf8); }
.bg-sensor { background: linear-gradient(135deg,#0ea5e9,#38bdf8); }
.bg-maintenance { background: linear-gradient(135deg,#14b8a6,#5eead4); }
.bg-log { background: linear-gradient(135deg,#8b5cf6,#a78bfa); }
.bg-data { background: linear-gradient(135deg,#64748b,#94a3b8); }
.bg-web { background: linear-gradient(135deg,#dc2626,#f87171); }
.bg-ancaman { background: linear-gradient(135deg,#7c3aed,#c084fc); }
</style>
""", unsafe_allow_html=True)

# =====================
# LOAD DATA
# =====================
CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vQeydV3v3dnBOuyyp6O8Zu-BKx-2B4W73L7xV4bCt-YU4EAYv6fkSIlgVTpjMYwCA"
    "/pub?gid=1002955304&single=true&output=csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    df["TANGGAL"] = df["TANGGAL"].astype(str).str.capitalize()
    df["JENIS LAPORAN"] = df["JENIS LAPORAN"].astype(str).str.strip()
    df["STATUS"] = df["STATUS"].astype(str)
    return df

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
# NORMALISASI PIC (SUPPORT MULTI PIC)
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
# FILTER DATA (BULAN + PIC)
# =====================
if bulan:
    df = df[df["TANGGAL"].isin(bulan)]

if pic:
    df = df[df["PIC_SPLIT"].isin(pic)]

# Kembalikan ke data unik setelah explode
df = df.drop(columns=["PIC_SPLIT"]).drop_duplicates()

# =====================
# HITUNG KPI
# =====================
total = len(df)

notif = (df["JENIS LAPORAN"] == "Laporan Notifikasi Kerentanan Stakeholder").sum()
analisis = (df["JENIS LAPORAN"] == "Laporan Analisis Kerentanan CVE/Produk").sum()
ca = (df["JENIS LAPORAN"] == "Laporan Compromise Assessment").sum()
sektor = (df["JENIS LAPORAN"] == "Laporan Penelusuran Kerentanan Sektor").sum()
sensor = (df["JENIS LAPORAN"] == "Laporan Koordinasi Pemasangan Sensor Open Source").sum()
maintenance = (df["JENIS LAPORAN"] == "Laporan Pemasangan/Pemeliharaan Sensor Monitoring Open Source").sum()
log = (df["JENIS LAPORAN"] == "Laporan Analisis Log Sensor Monitoring Open Source").sum()
data_dukung = (df["JENIS LAPORAN"] == "Data dukung bahan pimpinan").sum()
web_deface = (df["JENIS LAPORAN"] == "Laporan Notifikasi Web Defacement").sum()
ancaman = (df["JENIS LAPORAN"] == "Laporan Analisis Penelusuran Potensi Ancaman Stakeholder").sum()

# =====================
# HEADER
# =====================
st.markdown(
    "<div class='title-responsive'>🚀 REKAPITULASI LAPORAN THREAT HUNTING</div>",
    unsafe_allow_html=True
)
st.divider()

# =====================
# TOTAL KPI
# =====================
st.markdown(f"""
<div class="kpi kpi-large bg-total">
    <div class="kpi-label">📄 TOTAL LAPORAN</div>
    <div class="kpi-value">{total}</div>
</div>
""", unsafe_allow_html=True)

# =====================
# KPI ROW 1
# =====================
cols1 = st.columns(5)
labels1 = [
    ("🔔 Notifikasi Kerentanan", notif, "bg-notif"),
    ("🧪 Analisis CVE/Produk", analisis, "bg-analisis"),
    ("🛡️ Compromise Assessment", ca, "bg-ca"),
    ("🏭 Kerentanan Sektor", sektor, "bg-sektor"),
    ("📡 Koordinasi Sensor", sensor, "bg-sensor"),
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
# KPI ROW 2
# =====================
cols2 = st.columns(5)
labels2 = [
    ("🛠️ Pemasangan / Pemeliharaan", maintenance, "bg-maintenance"),
    ("📊 Analisis Log", log, "bg-log"),
    ("📑 Data Dukung Pimpinan", data_dukung, "bg-data"),
    ("🌐 Notifikasi Web Defacement", web_deface, "bg-web"),
    ("🎯 Analisis Potensi Ancaman", ancaman, "bg-ancaman"),
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
# STATUS DISTRIBUTION
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

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card-left">', unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:20px; font-weight:700;'>📊 Komposisi Status Laporan</div>",
        unsafe_allow_html=True
    )

    fig = px.pie(
        status_rekap,
        names="STATUS",
        values="Jumlah",
        hole=0.45
    )

    fig.update_traces(textinfo="percent+label")

    fig.update_layout(height=350)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col2:
    st.markdown('<div class="card-right">', unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:20px; font-weight:700; margin-bottom:40px;'>📋 Tabel Status Laporan</div>",
        unsafe_allow_html=True
    )

    st.dataframe(
        status_rekap,
        use_container_width=True,
        hide_index=True,
        height=250
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================
# GRAFIK TAHUNAN
# =====================
st.divider()
st.subheader("📈 Jumlah Laporan per Tahun (2021–2026)")

data_tahunan = pd.DataFrame({
    "Tahun": [2021, 2022, 2023, 2024, 2025, 2026],
    "Jumlah Laporan": [57, 109, 154, 61, 418, total]
})

fig_tahun = px.bar(
    data_tahunan,
    x="Tahun",
    y="Jumlah Laporan",
    text="Jumlah Laporan"
)

fig_tahun.update_traces(textposition="outside")

fig_tahun.add_scatter(
    x=data_tahunan["Tahun"],
    y=data_tahunan["Jumlah Laporan"],
    mode="lines+markers",
    name="Trend",
    line=dict(color="#e11d48", width=4), marker=dict(size=10)
)

st.plotly_chart(fig_tahun, use_container_width=True)
