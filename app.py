import streamlit as st
import yaml
import importlib
from utils.theme import apply_theme

# =====================
# CONFIG & STYLE
# =====================
st.set_page_config(
    page_title="Dashboard Laporan TH",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(apply_theme(dark=True), unsafe_allow_html=True)

# =====================
# LOAD MENU
# =====================
with open("menu.yml", "r") as f:
    config = yaml.safe_load(f)

# =====================
# SIDEBAR NAVIGATION
# =====================
st.sidebar.title("🛡️ SI-THREAT")
st.sidebar.caption("Sistem Informasi Threat Hunting")
st.sidebar.divider()

# Extract menu titles for the radio button
menu_titles = [item["title"] for item in config["menu"]]
icons = [item["icon"] for item in config["menu"]]

# Create a mapping for easy lookup
menu_map = {item["title"]: item for item in config["menu"]}

# Custom Format for Radio Button (Adding Icons)
def format_func(option):
    return f"{menu_map[option]['icon']}  {option}"

selected_menu = st.sidebar.radio(
    "Navigasi",
    menu_titles,
    format_func=format_func,
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.markdown("### ℹ️ Info")
st.sidebar.info(
    """
    **Versi 1.1**
    
    Dashboard ini menggunakan data 
    real-time dari Google Sheets.
    """
)

# =====================
# DYNAMIC LOADER
# =====================
if selected_menu:
    item = menu_map[selected_menu]
    module_name = item["module"]
    func_name = item["function"]
    
    # Import module dynamically
    module = importlib.import_module(module_name)
    
    # Get the function and call it
    func = getattr(module, func_name)
    func()
