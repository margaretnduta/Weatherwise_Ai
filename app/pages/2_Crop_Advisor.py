"""
app/pages/2_Crop_Advisor.py
───────────────────────────
Smart Crop Advisor page for WeatherWise AI.
Generates proactive, location- and crop-specific recommendations based on agricultural rules
and ML predictions (implementing logic from Notebooks/Recommendation engine.ipynb).
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
    generate_recommendations,
    planting_advisor,
    irrigation_advisor,
    fertilizer_advisor,
    spraying_advisor,
    disease_risk_advisor,
)

# Page configuration
st.set_page_config(
    page_title="Smart Crop Advisor — WeatherWise AI",
    page_icon="🌾",
    layout="wide",
)

inject_custom_css()
config = render_sidebar()

location = config["location"]
crop = config["crop"]
growth_stage = config["growth_stage"]

st.title("🌾 Smart Crop Advisor")
st.caption(
    f"Proactive decision engine generating customized farming recommendations for **{crop}** in **{location}** ({growth_stage} stage)."
)

weather = get_current_weather(location)
pred = predict_rainfall_probability(
    weather["min_temp"], weather["max_temp"], weather["humidity"], weather["wind_speed"]
)

# 1. Main Advisory Summary Banner
recs = generate_recommendations(
    crop,
    pred["rain_prediction"],
    pred["expected_rainfall_mm"],
    weather["max_temp"],
    weather["humidity"],
    weather["wind_speed"],
)

st.markdown(
    f"""
    <div class="glass-card" style="border-left: 6px solid #10B981;">
        <h3 style="color: #38BDF8; margin-top: 0;">📋 Executive Action Summary</h3>
        <p style="color: #E2E8F0; font-size: 1.05rem;">
            Current conditions in <b>{location}</b> indicate <b>{pred['rain_probability_pct']}% chance of rain</b> (~{pred['expected_rainfall_mm']} mm).
            Below are prioritized field activity guidance cards tailored for <b>{crop}</b> at the <b>{growth_stage}</b> stage.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# 2. Categorized Advisory Cards (2x2 Grid)
col_card1, col_card2 = st.columns(2)

with col_card1:
    # Planting & Seeding Card
    plant_recs = planting_advisor(pred["rain_prediction"], pred["expected_rainfall_mm"])
    st.markdown("### 🌱 1. Planting & Land Preparation")
    for r in plant_recs:
        st.markdown(f'<div class="rec-box">{r}</div>', unsafe_allow_html=True)
    st.caption("ℹ️ *Maize in Trans Nzoia requires at least 10-15mm rain post-sowing for uniform germination.*")

    st.write("")

    # Fertilizer & Soil Nutrients Card
    fert_recs = fertilizer_advisor(pred["rain_prediction"])
    st.markdown("### 🌿 2. Fertilizer Application (CAN / DAP)")
    for r in fert_recs:
        box_class = "rec-box-warning" if "Delay" in r else "rec-box"
        st.markdown(f'<div class="{box_class}">{r}</div>', unsafe_allow_html=True)
    st.caption("ℹ️ *Avoid top-dressing CAN before heavy downpours to prevent nitrogen leaching into subsoil.*")

with col_card2:
    # Irrigation & Water Management Card
    irr_recs = irrigation_advisor(pred["rain_prediction"], weather["max_temp"])
    st.markdown("### 💧 3. Irrigation Scheduling")
    for r in irr_recs:
        st.markdown(f'<div class="rec-box">{r}</div>', unsafe_allow_html=True)
    st.caption("ℹ️ *Save pumping fuel costs by utilizing ML precipitation probability.*")

    st.write("")

    # Spraying & Pest Control Card
    spray_recs = spraying_advisor(weather["wind_speed"])
    disease_recs = disease_risk_advisor(weather["humidity"], weather["max_temp"])
    st.markdown("### 🚜 4. Spraying & Disease Control")
    for r in spray_recs:
        box_class = "rec-box-alert" if "Avoid" in r else "rec-box"
        st.markdown(f'<div class="{box_class}">{r}</div>', unsafe_allow_html=True)
    for r in disease_recs:
        box_class = "rec-box-warning" if "High" in r else "rec-box"
        st.markdown(f'<div class="{box_class}">{r}</div>', unsafe_allow_html=True)

st.divider()

# 3. Interactive "What-If" Scenario Simulator
st.subheader("🧪 Interactive What-If Recommendation Simulator")
st.markdown("Adjust hypothetical weather conditions below to see how the decision engine dynamically updates field recommendations.")

sim_col1, sim_col2, sim_col3, sim_col4 = st.columns(4)

with sim_col1:
    sim_rain_pred = st.selectbox("Rainfall Forecasted?", options=["Yes (1)", "No (0)"], index=0)
    sim_rain_flag = 1 if "Yes" in sim_rain_pred else 0

with sim_col2:
    sim_rain_mm = st.slider("Expected Rain (mm)", min_value=0.0, max_value=60.0, value=20.0, step=1.0)

with sim_col3:
    sim_temp = st.slider("Max Temp (°C)", min_value=15.0, max_value=40.0, value=28.0, step=0.5)

with sim_col4:
    sim_wind = st.slider("Wind Speed (km/h)", min_value=5.0, max_value=50.0, value=22.0, step=1.0)

simulated_recs = generate_recommendations(
    crop_name=crop,
    rain_prediction=sim_rain_flag,
    rainfall_amount=sim_rain_mm,
    temperature=sim_temp,
    humidity=weather["humidity"],
    wind_speed=sim_wind,
)

st.markdown("#### ⚡ Simulated Decision Output:")
for s_rec in simulated_recs:
    st.markdown(f"- {s_rec}")
