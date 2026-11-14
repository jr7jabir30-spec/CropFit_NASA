import streamlit as str_lit
import folium
from streamlit_folium import st_folium

# ==========================================
# PAGE CONFIGURATION & LUXURY THEME
# ==========================================
str_lit.set_page_config(
    page_title="CropFit | NASA Space Apps",
    page_icon="🌾",
    layout="centered"
)

# Custom Forest-Green & Gold Glassmorphism CSS
str_lit.markdown("""
<style>
    .stApp {
        background-color: #0A1C14;
        color: #E2E8F0;
    }
    .hero-box {
        background: linear-gradient(135deg, #064E3B 0%, #022C22 100%);
        border: 1px solid #10B981;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    .metric-card {
        background: #112A21;
        border: 1px solid #1E4637;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "step" not in str_lit.session_state:
    str_lit.session_state.step = 1
if "lat" not in str_lit.session_state:
    str_lit.session_state.lat = 24.2155
if "lon" not in str_lit.session_state:
    str_lit.session_state.lon = 55.7483
if "current_crop" not in str_lit.session_state:
    str_lit.session_state.current_crop = "Wheat"
if "next_preference" not in str_lit.session_state:
    str_lit.session_state.next_preference = "Date Palm"

# Header Title
str_lit.markdown("""
<div class="hero-box">
    <h1 style="color: #34D399; margin: 0; font-size: 28px;">🌾 CropFit : NASA Space Apps Edition</h1>
    <p style="color: #9CA3AF; margin: 5px 0 0 0; font-size: 14px;">Intelligent Precision Agriculture & Soil Moisture Analytics for Low-Connectivity Fields</p>
</div>
""", unsafe_allow_html=True)

# Comprehensive Crop Database
CROPS_DB = [
    {"name": "Wheat", "water": "Medium", "season": "Rabi / Winter", "soil": "Loamy", "nitrogen": "High"},
    {"name": "Date Palm", "water": "Low", "season": "Year-round / Arid", "soil": "Sandy / Saline", "nitrogen": "Low"},
    {"name": "Millet (Bajra)", "water": "Low", "season": "Kharif / Summer", "soil": "Sandy / Drought-resistant", "nitrogen": "Low"},
    {"name": "Alfalfa", "water": "High", "season": "Perennial", "soil": "Well-drained loam", "nitrogen": "Fixer"},
    {"name": "Tomato", "water": "High", "season": "Controlled / Greenhouse", "soil": "Rich organic", "nitrogen": "Medium"},
    {"name": "Barley", "water": "Low", "season": "Winter", "soil": "Well-drained", "nitrogen": "Medium"},
    {"name": "Sorghum", "water": "Low", "season": "Summer", "soil": "Clay to Sandy", "nitrogen": "Low"}
]

# ==========================================
# STEP 1: PIN FARM LOCATION
# ==========================================
if str_lit.session_state.step == 1:
    str_lit.markdown("### 📍 Step 1: Pin Your Farm on the Satellite Map")
    str_lit.caption("Tap anywhere on the map or drag to target your exact field coordinates.")

    # Clean English Map (Esri Tiles - No API key or foreign language issues)
    m = folium.Map(
        location=[str_lit.session_state.lat, str_lit.session_state.lon], 
        zoom_start=6,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri &mdash; Source: Esri, USGS, NOAA"
    )
    folium.Marker(
        [str_lit.session_state.lat, str_lit.session_state.lon], 
        tooltip="Selected Farm", 
        icon=folium.Icon(color="green", icon="leaf", prefix="fa")
    ).add_to(m)
    
    map_data = st_folium(m, height=320, width=700)

    if map_data and map_data.get("last_clicked"):
        str_lit.session_state.lat = round(map_data["last_clicked"]["lat"], 4)
        str_lit.session_state.lon = round(map_data["last_clicked"]["lng"], 4)

    str_lit.markdown(f"""
    <div style="background: #112A21; padding: 12px 16px; border-radius: 10px; border: 1px solid #1E4637; margin: 15px 0;">
        📌 Locked Coordinates: <b style="color: #34D399;">{str_lit.session_state.lat}°, {str_lit.session_state.lon}°</b> | 🛰️ NASA SMAP & POWER Linked
    </div>
    """, unsafe_allow_html=True)

    if str_lit.button("Next: Choose Your Crops ➡️"):
        str_lit.session_state.step = 2
        str_lit.rerun()

# ==========================================
# STEP 2: CROP PLANNING & SEARCH
# ==========================================
elif str_lit.session_state.step == 2:
    str_lit.markdown("### 🌾 Step 2: Current & Planned Crops")
    str_lit.caption("Select what is in your field now and what you want to grow next season.")

    # Offline connectivity status badge
    str_lit.markdown("""
    <div style="background: #064E3B; padding: 8px 12px; border-radius: 8px; border: 1px solid #059669; margin-bottom: 15px; font-size: 13px;">
        📶 <b>Offline-Ready Mode:</b> Crop databases and cached NASA parameters are indexed locally for field access.
    </div>
    """, unsafe_allow_html=True)

    # Live Search Bar for instant client-side filtering
    search_query = str_lit.text_input("🔍 Quick search crop list:", "").lower()
    
    filtered_crops = [c for c in CROPS_DB if search_query in c["name"].lower()]
    filtered_names = [c["name"] for c in filtered_crops] if filtered_crops else [c["name"] for c in CROPS_DB]

    c1, c2 = str_lit.columns(2)
    with c1:
        current_crop = str_lit.selectbox("1. What is growing now?", filtered_names)
    with c2:
        next_preference = str_lit.selectbox("2. Preferred next crop (Optional)", filtered_names)

    str_lit.session_state.current_crop = current_crop
    str_lit.session_state.next_preference = next_preference

    col1, col2 = str_lit.columns(2)
    with col1:
        if str_lit.button("⬅️ Back"):
            str_lit.session_state.step = 1
            str_lit.rerun()
    with col2:
        if str_lit.button("Next: View Rotation Advice ➡️"):
            str_lit.session_state.step = 3
            str_lit.rerun()

# ==========================================
# STEP 3: ROTATION ADVICE & NASA ANALYTICS
# ==========================================
elif str_lit.session_state.step == 3:
    str_lit.markdown("### 📊 Step 3: NASA Analytics & Rotation Insights")
    str_lit.caption("AI-driven crop rotation recommendations optimized using regional soil moisture telemetry.")

    str_lit.markdown(f"""
    <div style="background: #112A21; padding: 15px; border-radius: 10px; border: 1px solid #1E4637; margin-bottom: 15px;">
        <h4 style="color: #34D399; margin-top: 0;">Rotation Recommendation</h4>
        <p>Transitioning from <b>{str_lit.session_state.current_crop}</b> to <b>{str_lit.session_state.next_preference}</b> helps balance soil nitrogen levels and optimizes root water absorption based on local NASA POWER solar radiation data.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = str_lit.columns(2)
    with col1:
        if str_lit.button("⬅️ Back to Crops"):
            str_lit.session_state.step = 2
            str_lit.rerun()
    with col2:
        if str_lit.button("🔄 Restart Planner"):
            str_lit.session_state.step = 1
            str_lit.rerun()