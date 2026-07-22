"""
app/pages/4_Alerts.py
──────────────────────
Smart Alerts Panel for WeatherWise AI.
Real-time UI notifications for adverse weather conditions (heavy rain, high winds, heat stress)
complete with actionable mitigation advice.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from app.components.styling import inject_custom_css
from app.components.sidebar import render_sidebar
from app.utils import (
    get_current_weather,
    predict_rainfall_probability,
    smart_alerts,
)

# Page configuration
st.set_page_config(
    page_title="Smart Weather Alerts — WeatherWise AI",
    page_icon="⚡",
    layout="wide",
)

inject_custom_css()
config = render_sidebar()

location = config["location"]
crop = config["crop"]
growth_stage = config["growth_stage"]

st.title("⚡ Smart Weather Alerts Panel")
st.caption(
    f"Real-time hazard warnings and actionable mitigation protocols for **{location}**."
)

weather = get_current_weather(location)
pred = predict_rainfall_probability(
    weather["min_temp"], weather["max_temp"], weather["humidity"], weather["wind_speed"]
)
alerts_list = smart_alerts(pred["rain_prediction"], weather["max_temp"], weather["wind_speed"])

# 1. Alert Summary Ticker
col_a1, col_a2, col_a3 = st.columns(3)

with col_a1:
    st.metric(
        label="Total Active Alerts",
        value=f"{len(alerts_list)} Active",
        delta="Requires Attention" if len(alerts_list) > 0 else "Normal",
        delta_color="inverse" if len(alerts_list) > 0 else "normal",
    )

with col_a2:
    st.metric(
        label="Highest Severity",
        value="WARNING" if pred["rain_prediction"] == 1 or weather["wind_speed"] > 35 else "ADVISORY",
        delta="Action Required",
    )

with col_a3:
    st.metric(
        label="SMS Broadcast Status",
        value="ACTIVE",
        delta="Subscribed: 1,420 Farmers",
    )

st.divider()

# 2. Alert Severity Filter
filter_severity = st.radio(
    "Filter Alerts by Severity:",
    options=["All Alerts", "Critical / High", "Warning", "Advisory / Normal"],
    horizontal=True,
    index=0,
)

st.write("")

# 3. Dynamic Alert Cards Feed
st.markdown("### 🔔 Live Hazard Warnings & Mitigation Protocols")

# Alert 1: Heavy Rain & Flash Flood Risk
if pred["rain_prediction"] == 1 and (filter_severity in ["All Alerts", "Critical / High", "Warning"]):
    st.markdown(
        f"""
        <div class="glass-card" style="border-left: 6px solid #EF4444;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge-critical">CRITICAL HAZARD</span>
                <span style="color: #94A3B8; font-size: 0.8rem;">Issued: Just now • Ref #WW-RAIN-2026</span>
            </div>
            <h3 style="color: #FCA5A5; margin-top: 10px; margin-bottom: 6px;">🌧️ Heavy Rainfall & Flash Flood Risk Expected</h3>
            <p style="color: #E2E8F0; font-size: 0.95rem;">
                <b>Location</b>: {location} | <b>Expected Volume</b>: ~{pred['expected_rainfall_mm']} mm | <b>Rain Probability</b>: {pred['rain_probability_pct']}%
            </p>
            <div style="background: rgba(15,23,42,0.6); padding: 14px; border-radius: 10px; margin-top: 10px;">
                <div style="color: #38BDF8; font-weight: 700; margin-bottom: 6px;">🛡️ Required Farmer Action Protocol:</div>
                <ul style="color: #CBD5E1; font-size: 0.9rem; margin-bottom: 0;">
                    <li>Clear drainage furrows and trenches around <b>{crop}</b> fields to prevent waterlogging and root rot.</li>
                    <li>Suspend all planned nitrogen fertilizer applications (CAN/Urea) until after rainfall subsides.</li>
                    <li>Move harvested grain sacks off bare ground onto elevated wooden pallets.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Alert 2: High Wind Gusts Warning
if weather["wind_speed"] > 25 and (filter_severity in ["All Alerts", "Warning"]):
    st.markdown(
        f"""
        <div class="glass-card" style="border-left: 6px solid #F59E0B;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge-warning">WARNING</span>
                <span style="color: #94A3B8; font-size: 0.8rem;">Issued: 15 mins ago • Ref #WW-WIND-882</span>
            </div>
            <h3 style="color: #FDE047; margin-top: 10px; margin-bottom: 6px;">💨 High Wind Speed & Lodging Risk</h3>
            <p style="color: #E2E8F0; font-size: 0.95rem;">
                <b>Location</b>: {location} | <b>Sustained Wind</b>: {weather['wind_speed']} km/h
            </p>
            <div style="background: rgba(15,23,42,0.6); padding: 14px; border-radius: 10px; margin-top: 10px;">
                <div style="color: #38BDF8; font-weight: 700; margin-bottom: 6px;">🛡️ Required Farmer Action Protocol:</div>
                <ul style="color: #CBD5E1; font-size: 0.9rem; margin-bottom: 0;">
                    <li>Do <b>NOT</b> apply foliar pesticide or herbicide sprays today due to severe spray drift risk.</li>
                    <li>Inspect tall maize stalks at the <b>{growth_stage}</b> stage for root lodging risk.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Alert 3: Fungal Blight / Heat Stress Risk
if filter_severity in ["All Alerts", "Advisory / Normal"]:
    st.markdown(
        f"""
        <div class="glass-card" style="border-left: 6px solid #10B981;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge-advisory">AGRICULTURAL ADVISORY</span>
                <span style="color: #94A3B8; font-size: 0.8rem;">Issued: Today • Ref #WW-BLIGHT-104</span>
            </div>
            <h3 style="color: #6EE7B7; margin-top: 10px; margin-bottom: 6px;">🦠 Fungal Leaf Blight Monitoring Advisory</h3>
            <p style="color: #E2E8F0; font-size: 0.95rem;">
                <b>Humidity Level</b>: {weather['humidity']}% | <b>Temperature</b>: {weather['max_temp']} °C
            </p>
            <div style="background: rgba(15,23,42,0.6); padding: 14px; border-radius: 10px; margin-top: 10px;">
                <div style="color: #38BDF8; font-weight: 700; margin-bottom: 6px;">🛡️ Recommended Farmer Protocol:</div>
                <ul style="color: #CBD5E1; font-size: 0.9rem; margin-bottom: 0;">
                    <li>Scout maize crops for grey leaf spots or cigar-shaped lesions on lower leaves.</li>
                    <li>Ensure crop row spacing allows good airflow to reduce canopy humidity.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# 4. Emergency Notification Simulator & SMS Dispatcher
st.subheader("📱 Farmer SMS Alert Broadcast Simulator")
with st.expander("Broadcast Alert via SMS to Trans Nzoia Farmer Cooperative", expanded=False):
    sms_text = st.text_area(
        "Edit SMS Broadcast Message:",
        value=f"WEATHERWISE ALERT ({location.split(' ')[0]}): Rain expected ({pred['rain_probability_pct']}% chance). Suspend CAN fertilizer spreading today. - WeatherWise AI",
        height=100,
    )
    if st.button("📡 Dispatch SMS Alert Now", use_container_width=False):
        st.success("✅ SMS Alert successfully broadcasted to 1,420 registered farmers in Trans Nzoia!")
