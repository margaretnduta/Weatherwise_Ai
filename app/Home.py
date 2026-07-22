"""
app/Home.py
───────────
WeatherWise AI — Main Landing Page / Entrypoint
Hack the Weather 2026 Hackathon Entry
Targeting Trans Nzoia County, Kenya (Kenya's Maize Granary)
"""

import sys
import os

# Add parent directory to sys.path so modules like visualization can be imported cleanly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.components.styling import inject_custom_css
from app.components.sidebar import render_sidebar
from app.utils import (
    get_current_weather,
    predict_rainfall_probability,
    smart_alerts,
)

# 1. Page Configuration
st.set_page_config(
    page_title="WeatherWise AI — Smart Weather Copilot",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inject Custom CSS & Sidebar
inject_custom_css()
config = render_sidebar()

location = config["location"]
crop = config["crop"]
growth_stage = config["growth_stage"]

# 3. Main Header Banner
st.markdown(
    """
    <div class="hackathon-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                    🏆 Hack the Weather 2026 Hackathon
                </span>
                <h1 style="margin-top: 10px; font-size: 2.3rem;">WeatherWise AI</h1>
                <p>Localized Predictive Weather Intelligence & AI Decision Copilot for Trans Nzoia Farmers</p>
            </div>
            <div style="text-align: right; background: rgba(0,0,0,0.2); padding: 12px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15);">
                <div style="font-size: 0.8rem; color: #7DD3FC; text-transform: uppercase; font-weight: 600;">Target Region</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #FFFFFF;">Trans Nzoia County</div>
                <div style="font-size: 0.78rem; color: #E0F2FE;">"Kenya's Granary" (Kitale)</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 4. Ticker Metrics Bar
weather = get_current_weather(location)
pred = predict_rainfall_probability(
    weather["min_temp"], weather["max_temp"], weather["humidity"], weather["wind_speed"]
)
active_alerts = smart_alerts(pred["rain_prediction"], weather["max_temp"], weather["wind_speed"])

col_t1, col_t2, col_t3, col_t4 = st.columns(4)
with col_t1:
    st.metric(
        label=f"Active Location ({location.split(' ')[0]})",
        value=f"{weather['max_temp']} °C",
        delta=f"Min {weather['min_temp']} °C",
    )
with col_t2:
    st.metric(
        label="Rainfall Probability",
        value=f"{pred['rain_probability_pct']} %",
        delta=f"~{pred['expected_rainfall_mm']} mm expected",
    )
with col_t3:
    st.metric(
        label="Soil Moisture (Topsoil)",
        value=f"{weather['soil_moisture']} %",
        delta="Optimal for Maize" if weather['soil_moisture'] > 50 else "Irrigation needed",
    )
with col_t4:
    st.metric(
        label="Active Weather Alerts",
        value=f"{len(active_alerts)} Alerts",
        delta="High Priority" if len(active_alerts) > 1 else "Normal",
        delta_color="inverse" if len(active_alerts) > 1 else "normal",
    )

st.write("")

# 5. Core Platform Features Grid
st.markdown("### 🚀 Core Platform Modules")
st.markdown(
    "WeatherWise AI moves beyond standard weather apps by translating raw meteorological data into proactive, actionable agricultural decisions."
)

col_f1, col_f2 = st.columns(2)

with col_f1:
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="color: #38BDF8; margin-top: 0;">📊 1. Smart Weather Dashboard</h3>
            <p style="color: #CBD5E1; font-size: 0.95rem;">
                Explore real-time conditions, 7-day multi-metric forecasts (Rainfall, Min/Max Temp, Humidity),
                historical drought risk trends, and an interactive county-level map for Trans Nzoia and Kenya.
            </p>
            <span style="color: #34D399; font-weight: 600; font-size: 0.88rem;">Features:</span> Plotly charts • County scatter-mapbox • Soil moisture depth profiles
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="glass-card">
            <h3 style="color: #38BDF8; margin-top: 0;">🤖 2. AgriCopilot AI Chat (LLM + RAG)</h3>
            <p style="color: #CBD5E1; font-size: 0.95rem;">
                Natural-language conversational assistant trained on Trans Nzoia weather forecasts, soil pH profiles,
                and agronomic management rules. Ask questions in plain English or Swahili context.
            </p>
            <span style="color: #34D399; font-weight: 600; font-size: 0.88rem;">Features:</span> RAG context retrieval • Instant localized decision support • Model transparency
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_f2:
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="color: #38BDF8; margin-top: 0;">🌾 3. Smart Crop Advisor</h3>
            <p style="color: #CBD5E1; font-size: 0.95rem;">
                Location- and growth-stage-specific recommendations telling farmers exactly when to plant, irrigate,
                top-dress fertilizer, spray pesticides, and manage fungal blight risk.
            </p>
            <span style="color: #34D399; font-weight: 600; font-size: 0.88rem;">Features:</span> Rule & ML advisory engine • What-If Scenario Matrix • Soil nutrient tracker
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="glass-card">
            <h3 style="color: #38BDF8; margin-top: 0;">⚡ 4. Smart Weather Alerts</h3>
            <p style="color: #CBD5E1; font-size: 0.95rem;">
                Real-time warnings for extreme downpours, dry spells, heat stress, and high winds, complete with
                practical step-by-step mitigation actions to safeguard crops.
            </p>
            <span style="color: #34D399; font-weight: 600; font-size: 0.88rem;">Features:</span> Severity filters • Cause analysis • Emergency action steps
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# 6. Technical Architecture Summary
with st.expander("🛠️ View System Architecture & Conduit Weather Data Integration", expanded=False):
    st.markdown(
        f"""
        - **Machine Learning Models**: Random Forest Ensemble & XGBoost trained on precipitation, temperature, wind, and humidity indices.
        - **Data Pipeline**: Ingests weather station data, satellite grid observations, and agricultural parameters (`N, P, K, pH`).
        - **Active Configuration**:
          - Location: **{location}**
          - Selected Crop: **{crop}**
          - Growth Stage: **{growth_stage}**
          - Active Engine: **{config['ml_model']}**
        """
    )
