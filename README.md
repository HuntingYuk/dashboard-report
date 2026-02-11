# 🛡️ SI-THREAT (Threat Hunting Information System)

**SI-THREAT** is an interactive web-based dashboard designed to monitor, analyze, and report *Threat Hunting* activities in real-time. This application visualizes daily report data, personnel performance, and cyber threat trends using centralized data from Google Sheets.

---

## ✨ Key Features

- **🚀 Executive Dashboard**: Comprehensive summary of KPIs (Key Performance Indicators) for total reports, notifications, analysis, and other technical activities.
- **📊 Personnel Analysis**: Track *Person In Charge* (PIC) performance with monthly trend charts and task distribution.
- **📈 Threat Analysis**: Visual breakdown of stakeholder notifications, impacted sectors, and incident categories (IIV/Non-IIV).
- **📝 Detailed Data**: Interactive table for exploring raw data with CSV export functionality.
- **🎨 Modern UI**: Responsive interface featuring *Dark Mode*, interactive charts (Plotly), and menu-based navigation.

---

## 🛠️ Tech Stack

- **[Python](https://www.python.org/)**: Primary programming language.
- **[Streamlit](https://streamlit.io/)**: Framework for building interactive data apps.
- **[Pandas](https://pandas.pydata.org/)**: Data manipulation and analysis.
- **[Plotly](https://plotly.com/)**: Interactive graphing library.
- **[PyYAML](https://pyyaml.org/)**: Dynamic navigation configuration.

---

## ⚙️ System Requirements

- Python 3.8 or newer.
- Internet connection (required to fetch data from Google Sheets).

---

## 🚀 Installation & Running

Follow these steps to run the application in your local environment:

### 1. Clone Repository
```bash
git clone https://github.com/username/si-threat.git
cd si-threat
```

### 2. Create Virtual Environment (Recommended)
```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the `.env.example` file to `.env` and configure your CSV URL.
```bash
cp .env.example .env
```
> **Note:** Ensure `CSV_URL` in the `.env` file points to a valid Google Sheets CSV link (Published to Web).

### 5. Run Application
```bash
streamlit run app.py
```
The application will automatically open in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```
📦 si-threat
 ┣ 📂 views/            # View logic per page
 ┃ ┣ 📜 home.py         # Main dashboard
 ┃ ┣ 📜 personel.py     # Personnel performance analysis
 ┃ ┣ 📜 analisis.py     # Stakeholder & sector analysis
 ┃ ┗ 📜 detail_data.py  # Raw data table
 ┣ 📂 utils/            # Helper functions (loader, theme)
 ┣ 📜 app.py            # Main entry point (Routing & Layout)
 ┣ 📜 menu.yml          # Navigation menu configuration
 ┣ 📜 .env              # Environment Configuration (URL, Secrets)
 ┣ 📜 requirements.txt  # Python dependencies list
 ┗ 📜 README.md         # Project documentation
```

---

## 🤝 Contribution

Contributions are always welcome! Feel free to create a *Pull Request* or report issues via the *Issues* feature.

---

<div align="center">
  <p>Made with ❤️ by Threat Hunting Team</p>
  <p>© 2026 SI-THREAT. All Rights Reserved.</p>
</div>
