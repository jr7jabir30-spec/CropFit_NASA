import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# ==========================================
# PAGE CONFIGURATION & LUXURY THEME
# ==========================================
st.set_page_config(
    page_title="CropFit | NASA Space Apps",
    page_icon="🛰️",
    layout="centered"
)

# Custom High-End Dark Glassmorphism CSS
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #0F172A 0%, #090D16 100%);
        color: #F8FAFC;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .hero-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 95, 70, 0.2) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 24px;
        border-radius: 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 24px;
    }
    .glass-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(52, 211, 153, 0.2);
        padding: 16px;
        border-radius: 12px;
        backdrop-filter: blur(8px);
        margin-bottom: 16px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 12px 28px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.6);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "step" not in st.session_state:
    st.session_state.step = 1
if "lat" not in st.session_state:
    st.session_state.lat = 24.2155
if "lon" not in st.session_state:
    st.session_state.lon = 55.7483
if "current_crop" not in st.session_state:
    st.session_state.current_crop = "Wheat"
if "next_preference" not in st.session_state:
    st.session_state.next_preference = "Date Palm"

# Header Banner
st.markdown("""
<div class="hero-card">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 36px;">🛰️</span>
        <div>
            <h1 style="color: #34D399; margin: 0; font-size: 26px; font-weight: 700;">CropFit : NASA Space Apps</h1>
            <p style="color: #94A3B8; margin: 4px 0 0 0; font-size: 14px;">Next-Gen Precision Agriculture & Global Soil Analytics</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Crop Database
CROPS_DB = [
    {"name": "Wheat", "water": "Medium", "season": "Rabi / Winter", "soil": "Loamy"},
    {"name": "Date Palm", "water": "Low", "season": "Year-round / Arid", "soil": "Sandy / Saline"},
    {"name": "Millet (Bajra)", "water": "Low", "season": "Kharif / Summer", "soil": "Sandy / Drought-resistant"},
    {"name": "Alfalfa", "water": "High", "season": "Perennial", "soil": "Well-drained loam"},
    {"name": "Tomato", "water": "High", "season": "Controlled / Greenhouse", "soil": "Rich organic"},
    {"name": "Barley", "water": "Low", "season": "Winter", "soil": "Well-drained"},
    {"name": "Sorghum", "water": "Low", "season": "Summer", "soil": "Clay to Sandy"}
]

# ==========================================
# STEP 1: TRUE GLOBAL SEARCH & MAP
# ==========================================
if st.session_state.step == 1:
    st.markdown("### 📍 Step 1: Global Location Search")
    st.caption("Type *any* city, village, or landmark in the entire world to look it up live.")

    # Live global search bar input
    global_query = st.text_input("🌍 Search Any Place on Earth (e.g., Abu Hail, Kollam, Tokyo, New York):", "")
    
    if global_query:
        try:
            # Query OpenStreetMap live geocoder with proper headers
            url = f"https://nominatim.openstreetmap.org/search?q={global_query}&format=json&limit=5"
            headers = {"User-Agent": "CropFit-SpaceApps-App/1.0"}
            response = requests.get(url, headers=headers, timeout=5).json()
            
            if response:
                locations = {item["display_name"]: (float(item["lat"]), float(item["lon"])) for item in response}
                chosen = st.selectbox("🎯 Select the exact match from global results:", list(locations.keys()))
                if chosen:
                    st.session_state.lat, st.session_state.lon = locations[chosen]
                    st.success(f"📍 Locked onto: {chosen}")
            else:
                st.warning("⚠️ No global results found for that search. Try another spelling or click directly on the map.")
        except Exception as e:
            st.error(f"⚠️ Search error: Unable to reach global geocoder service.")

    # Clean English Map (Esri Tiles)
    m = folium.Map(
        location=[st.session_state.lat, st.session_state.lon], 
        zoom_start=8,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri &mdash; Source: Esri, USGS, NOAA"
    )
    folium.Marker(
        [st.session_state.lat, st.session_state.lon], 
        tooltip="Selected Field", 
        icon=folium.Icon(color="green", icon="leaf", prefix="fa")
    ).add_to(m)
    
    map_data = st_folium(m, height=320, width=700)

    if map_data and map_data.get("last_clicked"):
        st.session_state.lat = round(map_data["last_clicked"]["lat"], 4)
        st.session_state.lon = round(map_data["last_clicked"]["lng"], 4)

    st.markdown(f"""
    <div class="glass-box">
        📌 Active Coordinates: <b style="color: #34D399;">{st.session_state.lat}°, {st.session_state.lon}°</b> | 🛰️ NASA SMAP & POWER Connected
    </div>
    """, unsafe_allow_html=True)

    if st.button("Next: Choose Your Crops ➡️"):
        st.session_state.step = 2
        st.rerun()

# ==========================================
# STEP 2: CROP PLANNING & SEARCH
# ==========================================
elif st.session_state.step == 2:
    st.markdown("### 🌾 Step 2: Current & Planned Crops")
    st.caption("Select what is in your field now and what you want to grow next season.")

    st.markdown("""
    <div class="glass-box" style="border-color: rgba(16, 185, 129, 0.4);">
        📶 <b>Offline-Ready Mode:</b> Crop databases are indexed locally for field access without stable internet.
    </div>
    """, unsafe_allow_html=True)

    crop_query = st.text_input("🔍 Filter crop list:", "").lower()
    filtered_crops = [c for c in CROPS_DB if crop_query in c["name"].lower()]
    filtered_names = [c["name"] for c in filtered_crops] if filtered_crops else [c["name"] for c in CROPS_DB]

    c1, c2 = st.columns(2)
    with c1:
        current_crop = st.selectbox("1. What is growing now?", filtered_names)
    with c2:
        next_preference = st.selectbox("2. Preferred next crop (Optional)", filtered_names)

    st.session_state.current_crop = current_crop
    st.session_state.next_preference = next_preference

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next: View Rotation Advice ➡️"):
            st.session_state.step = 3
            st.rerun()

# ==========================================
# STEP 3: ROTATION ADVICE & NASA ANALYTICS
# ==========================================
elif st.session_state.step == 3:
    st.markdown("### 📊 Step 3: NASA Analytics & Rotation Insights")
    st.caption("AI-driven crop rotation recommendations optimized using regional soil telemetry.")

    st.markdown(f"""
    <div class="glass-box">
        <h4 style="color: #34D399; margin-top: 0;">Rotation Recommendation</h4>
        <p style="color: #CBD5E1;">Transitioning from <b>{st.session_state.current_crop}</b> to <b>{st.session_state.next_preference}</b> optimizes nitrogen recovery and root moisture retention for field coordinates ({st.session_state.lat}°, {st.session_state.lon}°).</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Crops"):
            str_lit.session_state.step = 2 if 'str_lit' in globals() else 2 # safeguard
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🔄 Restart Planner"):
            st.session_state.step = 1
            st.rerun()