import streamlit as st
import requests
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from datetime import datetime

# ================= CONFIG =================
AQI_TOKEN = "82cd855d311f9a9a038fc56bcb242deb941da170"

HYD_LAT, HYD_LON = 17.3850, 78.4867
HYD_LAT_MIN, HYD_LAT_MAX = 17.1, 17.7
HYD_LON_MIN, HYD_LON_MAX = 78.1, 78.9

# ================= SESSION STATE (LAST KNOWN AQI) =================
if "last_aqi_value" not in st.session_state:
    st.session_state.get["last_aqi_value"] = None
    st.session_state["last_aqi_time"] = None

# ================= AQI UTILS =================
def get_aqi_info(aqi):
    if aqi is None:
        return "Unavailable", "#9e9e9e"
    aqi = int(aqi)
    if aqi <= 50: return "Good", "#4CAF50"
    elif aqi <= 100: return "Moderate", "#FBC02D"
    elif aqi <= 150: return "Unhealthy (Sensitive)", "#FF9800"
    elif aqi <= 200: return "Unhealthy", "#E53935"
    elif aqi <= 300: return "Very Unhealthy", "#8E24AA"
    else: return "Hazardous", "#7E0023"

# ================= DATA FETCH =================
@st.cache_data(ttl=300)
def fetch_hyderabad_stations():
    url = (
        "https://api.waqi.info/map/bounds/"
        f"?latlng={HYD_LAT_MIN},{HYD_LON_MIN},{HYD_LAT_MAX},{HYD_LON_MAX}"
        f"&token={AQI_TOKEN}"
    )
    r = requests.get(url, timeout=15)
    data = r.json()

    if data.get("status") != "ok":
        return [], "WAQI API error"

    stations = []
    for s in data["data"]:
        aqi_raw = s.get("aqi")
        aqi = None if aqi_raw in ("-", None) else int(aqi_raw)

        stations.append({
            "name": s["station"]["name"],
            "lat": s["lat"],
            "lon": s["lon"],
            "aqi": aqi
        })

    return stations, None

# ================= UI =================
def render():
    st.set_page_config(page_title="Hyderabad AQI", layout="wide")

    st.markdown("""
        <style>
        .aqi-card {
            background: white;
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Hyderabad Real-Time Air Quality")

    with st.sidebar:
        st.header("Controls")
        if st.button("🔄 Refresh AQI"):
            st.cache_data.clear()
            st.rerun()

        st.caption("Data source: **WAQI (CPCB + global stations)**")
        st.caption("Note: Indian AQI may pause at night.")

    stations, error = fetch_hyderabad_stations()

    if error:
        st.error(error)
        return

    if not stations:
        st.warning("No stations returned by API.")
        return

    # ===== City AQI (average of valid AQIs) =====
    valid_aqis = [s["aqi"] for s in stations if s["aqi"] is not None]

    if valid_aqis:
        avg_aqi = int(sum(valid_aqis) / len(valid_aqis))
        label, color = get_aqi_info(avg_aqi)

        # Store last known AQI
        st.session_state["last_aqi_value"] = avg_aqi
        st.session_state["last_aqi_time"] = datetime.now()

        value_display = avg_aqi
        time_label = "Updated " + datetime.now().strftime("%H:%M")

    else:
        # FALLBACK TO LAST KNOWN AQI
        if st.session_state["last_aqi_value"] is not None:
            value_display = st.session_state["last_aqi_value"]
            label, color = get_aqi_info(value_display)
            last_time = st.session_state["last_aqi_time"].strftime("%d %b %Y, %H:%M")
            time_label = f"Last updated {last_time}"
        else:
            value_display = "--"
            label, color = "Temporarily Unavailable", "#9e9e9e"
            time_label = "Live data unavailable"

    st.markdown(f"""
        <div class="aqi-card">
            <p style="color:#666">Average AQI in Hyderabad</p>
            <h1 style="color:{color};font-size:64px">{value_display}</h1>
            <h3 style="color:{color}">{label}</h3>
            <p style="font-size:13px;color:#777">
                Stations detected: {len(stations)} · {time_label}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ===== MAP =====
    col_map, col_list = st.columns([2, 1])

    with col_map:
        st.subheader("🗺️ AQI Map – Hyderabad")

        m = folium.Map(
            location=[HYD_LAT, HYD_LON],
            zoom_start=11,
            tiles="cartodbpositron"
        )

        heat_data = [
            [s["lat"], s["lon"], s["aqi"]]
            for s in stations if s["aqi"] is not None
        ]

        if heat_data:
            HeatMap(heat_data, radius=25, blur=20).add_to(m)

        for s in stations:
            label_s, color_s = get_aqi_info(s["aqi"])
            popup = f"{s['name']}<br>AQI: {s['aqi'] if s['aqi'] else 'N/A'} ({label_s})"

            folium.CircleMarker(
                location=[s["lat"], s["lon"]],
                radius=9,
                popup=popup,
                color="white",
                weight=1,
                fill=True,
                fill_color=color_s,
                fill_opacity=0.85
            ).add_to(m)

        st_folium(m, width="100%", height=520)

    # ===== STATION LIST =====
    with col_list:
        st.subheader("📍 Monitoring Stations")

        for s in stations[:10]:
            label_s, color_s = get_aqi_info(s["aqi"])
            aqi_text = s["aqi"] if s["aqi"] else "N/A"

            st.markdown(f"""
                <div style="border-left:5px solid {color_s};padding-left:10px;margin-bottom:12px">
                    <b>{s['name'].split(',')[0]}</b><br>
                    AQI: <b style="color:{color_s}">{aqi_text}</b> — {label_s}
                </div>
            """, unsafe_allow_html=True)

    st.caption(
        "⚠️live sensor data is unavailable during nights/early mornings."
    )

# ================= RUN =================
if __name__ == "__main__":
    render()
