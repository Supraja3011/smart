"""
config.py
Global configuration file of the Smart Complaint Map.
- paths (database, uploads)
- geographic constants
- colors/theme
- Streamlit and open API configuration
"""

import os
import streamlit as st

# DATABASE SQLite
DB_PATH = "complaints.db"

# File where pictures are uploaded
UPLOAD_DIR = "uploads"

# OPEN DATABASE API KEY
OPENAQ_API_KEY = "2ce5f5f19f575442fd61aa19b94b50b0bcfbeef41e821b17173f6427e8c4ddf9"
# WORLD AIR QUALITY INDEX (WAQI) API KEY
WAQI_TOKEN = "dc5fd5b4e7f9ebdab1be25310cff9def54f726c5"

# Geographical Param

# Default position (Lyon)
DEFAULT_LAT = 17.4065
DEFAULT_LON = 78.4772

# Niveau de zoom par défaut pour les cartes
DEFAULT_ZOOM = 13


# Main website colours : light green
PRIMARY_BG = "#f1ffe8"   
PRIMARY_ACCENT = "#d5f5c8"
PRIMARY_BORDER = "#b9e6ae"

# Colours for cards and graphs
COLOR_MAP = {
    "Air quality": "#ff6961",         # soft red
    "Noise": "#5c7cfa",               # blue
    "Heat": "#ffa94d", 
    "Water":"#97d2ff",
    "Cycling / Walking": "#51cf66",   # green
    "Odor": "#9b5de5",                # purple
    "Other": "#6c757d",               # grey
}

# streamlit configuration

def setup():
    st.set_page_config(
        page_title="Smart Complaint Map",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    os.makedirs(UPLOAD_DIR, exist_ok=True)
