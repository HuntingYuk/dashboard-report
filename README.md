# 🛡️ SI-THREAT (Sistem Informasi Threat Hunting)

**SI-THREAT** adalah dashboard interaktif berbasis web yang dibangun untuk memonitor, menganalisis, dan melaporkan kegiatan *Threat Hunting* secara *real-time*. Aplikasi ini memvisualisasikan data laporan harian, kinerja personel, serta tren ancaman siber menggunakan data dari spreadsheet terpusat (Google Sheets).

---

## ✨ Fitur Utama

- **🚀 Dashboard Eksekutif**: Ringkasan KPI (Key Performance Indicators) total laporan, notifikasi, analisis, dan kegiatan teknis lainnya.
- **📊 Analisis Personel**: Pelacakan kinerja *Person In Charge* (PIC) dengan grafik tren bulanan dan distribusi tugas.
- **📈 Analisis Ancaman**: Visualisasi distribusi notifikasi ke stakeholder, sektor terdampak, dan kategori insiden (IIV/Non-IIV).
- **📝 Detail Data**: Tabel interaktif untuk eksplorasi data mentah dengan fitur ekspor ke CSV.
- **🎨 Modern UI**: Antarmuka responsif dengan *Dark Mode*, grafik interaktif (Plotly), dan navigasi berbasis menu.

---

## 🛠️ Teknologi yang Digunakan

- **[Python](https://www.python.org/)**: Bahasa pemrograman utama.
- **[Streamlit](https://streamlit.io/)**: Framework untuk membangun aplikasi data interaktif.
- **[Pandas](https://pandas.pydata.org/)**: Manipulasi dan analisis data.
- **[Plotly](https://plotly.com/)**: Pembuatan grafik interaktif.
- **[PyYAML](https://pyyaml.org/)**: Konfigurasi navigasi dinamis.

---

## ⚙️ Persyaratan Sistem

- Python 3.8 atau lebih baru.
- Koneksi internet (untuk mengambil data dari Google Sheets).

---

## 🚀 Instalasi & Menjalankan Aplikasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di lingkungan lokal Anda:

### 1. Clone Repository
```bash
git clone https://github.com/username/si-threat.git
cd si-threat
```

### 2. Buat Virtual Environment (Disarankan)
```bash
# Untuk macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Untuk Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment
Salin file `.env.example` menjadi `.env` dan sesuaikan URL CSV-nya.
```bash
cp .env.example .env
```
> **Catatan:** Pastikan `CSV_URL` di dalam file `.env` mengarah ke link CSV Google Sheets yang valid (Published to Web).

### 5. Jalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

---

## 📂 Struktur Proyek

```
📦 si-threat
 ┣ 📂 views/            # Logika tampilan per halaman
 ┃ ┣ 📜 home.py         # Dashboard utama
 ┃ ┣ 📜 personel.py     # Analisis kinerja personel
 ┃ ┣ 📜 analisis.py     # Analisis stakeholder & sektor
 ┃ ┗ 📜 detail_data.py  # Tabel data mentah
 ┣ 📂 utils/            # Fungsi bantuan (loader, theme)
 ┣ 📜 app.py            # Entry point utama (Routing & Layout)
 ┣ 📜 menu.yml          # Konfigurasi menu navigasi
 ┣ 📜 .env              # Konfigurasi Environment (URL, Secrets)
 ┣ 📜 requirements.txt  # Daftar pustaka Python
 ┗ 📜 README.md         # Dokumentasi proyek
```

---

## 🤝 Kontribusi

Kontribusi selalu diterima! Silakan buat *Pull Request* atau laporkan masalah melalui fitur *Issues*.

---

<div align="center">
  <p>Dibuat dengan ❤️ oleh Tim Threat Hunting</p>
  <p>© 2026 SI-THREAT. All Rights Reserved.</p>
</div>
