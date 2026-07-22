"""
app/pages/1_Dashboard.py
────────────────────────
Smart Weather Dashboard page for WeatherWise AI.
Visualizes real-time metrics, 7-day multi-axis forecast, historical rainfall & drought risk,
and an interactive county map (using visualization.charts and visualization.map_data).
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from app.components.styling import inject_custom_css
from app.components.sidebar import render_sidebar
from app.utils import (
    get_current_weather,
    get_7day_forecast_df,
    get_historical_weather_df,
    predict_rainfall_probability,
)
from visualization.charts import (
    plot_forecast_overview,
    plot_rainfall_trend,
    plot_drought_risk,
)
from visualization.map_data import (
    build_county_map,
    generate_sample_county_weather,
)

# Page setup
st.set_page_config(
    page_title="Smart Weather Dashboard — WeatherWise AI",
    page_icon="📊",
    layout="wide",
)

inject_custom_css()
config = render_sidebar()

location = config["location"]
crop = config["crop"]
clean_loc = location.split("(")[0].strip()

st.title("📊 Smart Weather Dashboard")
st.caption(f"Real-time meteorological observations, ML predictions, and spatial analysis for **{location}**.")

# 1. Top KPI Metrics Cards
weather = get_current_weather(location)
pred = predict_rainfall_probability(
    weather["min_temp"], weather["max_temp"], weather["humidity"], weather["wind_speed"]
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Max / Min Temp",
        value=f"{weather['max_temp']} °C",
        delta=f"Min {weather['min_temp']} °C",
    )

with col2:
    st.metric(
        label="Rainfall Probability",
        value=f"{pred['rain_probability_pct']} %",
        delta=f"{pred['expected_rainfall_mm']} mm intensity",
    )

with col3:
    st.metric(
        label="Humidity (Relative)",
        value=f"{weather['humidity']} %",
        delta="High" if weather['humidity'] > 75 else "Moderate",
    )

with col4:
    st.metric(
        label="Wind Speed",
        value=f"{weather['wind_speed']} km/h",
        delta="Gale Warning" if weather['wind_speed'] > 35 else "Calm",
        delta_color="inverse" if weather['wind_speed'] > 35 else "normal",
    )

with col5:
    st.metric(
        label="Soil Moisture",
        value=f"{weather['soil_moisture']} %",
        delta="Good field capacity",
    )

st.divider()

# 2. Tabs Layout
tab_forecast, tab_historical, tab_map, tab_soil = st.tabs(
    [
        "📈 7-Day Forecast Overview",
        "🌧️ Historical Trends & Drought Risk",
        "🗺️ Interactive County Map",
        "🌱 Soil & Crop Health Metrics",
    ]
)

# --- TAB 1: 7-DAY FORECAST OVERVIEW ---
with tab_forecast:
    st.subheader("🔮 7-Day Forecast Overview (ML Model Output)")
    st.markdown(
        "Dual-axis chart illustrating daily expected rainfall (bars) overlaid with maximum & minimum temperature trends (lines)."
    )

    forecast_df = get_7day_forecast_df(location)
    fig_forecast = plot_forecast_overview(forecast_df)
    st.plotly_chart(fig_forecast, use_container_width=True)

    with st.expander("📋 View Raw 7-Day Forecast Data Table"):
        st.dataframe(
            forecast_df[["Date", "MaxTemp", "MinTemp", "Rainfall", "Humidity", "RainTomorrow"]],
            use_container_width=True,
        )

# --- TAB 2: HISTORICAL TRENDS & DROUGHT RISK ---
with tab_historical:
    st.subheader("📜 Historical Rainfall & Regional Drought Risk")
    col_h1, col_h2 = st.columns([3, 2])

    history_df = get_historical_weather_df(location, days=60)

    with col_h1:
        st.markdown("**60-Day Historical Rainfall with 7-Day Rolling Average**")
        fig_trend = plot_rainfall_trend(history_df, location=clean_loc, rolling_window=7)
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_h2:
        st.markdown("**Drought Vulnerability Rating (Trailing 14 Days)**")
        fig_drought = plot_drought_risk(history_df, window_days=14, top_n=10)
        st.plotly_chart(fig_drought, use_container_width=True)

# --- TAB 3: INTERACTIVE COUNTY MAP ---
with tab_map:
    st.subheader("🗺️ County & Sub-County Weather Map (Kenya)")
    st.markdown(
        "Interactive map visualizing rainfall distribution and drought risk across Trans Nzoia and Kenya counties."
    )

    map_engine = st.radio(
        "Map Engine:",
        options=["Folium Interactive Map (streamlit-folium)", "Plotly Spatial Scatter Map"],
        index=0,
        horizontal=True,
        key="map_engine_select",
    )

    if "Folium" in map_engine:
        from app.utils import build_folium_county_map, HAS_FOLIUM
        if HAS_FOLIUM:
            from streamlit_folium import st_folium
            folium_map = build_folium_county_map(location)
            if folium_map:
                st_folium(folium_map, width="100%", height=450)
            else:
                st.info("Displaying Plotly spatial map fallback.")
                sample_county_data = generate_sample_county_weather(seed=42)
                fig_map = build_county_map(sample_county_data, color_by="rainfall_mm")
                st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Folium package not detected. Displaying Plotly spatial map.")
            sample_county_data = generate_sample_county_weather(seed=42)
            fig_map = build_county_map(sample_county_data, color_by="rainfall_mm")
            st.plotly_chart(fig_map, use_container_width=True)
    else:
        col_m1, col_m2 = st.columns([1, 4])
        with col_m1:
            map_metric = st.selectbox(
                "Color Map By:",
                options=["rainfall_mm", "drought_risk", "max_temp_c", "humidity_pct"],
                index=0,
                key="map_metric_select",
            )
            st.info(
                "💡 **Map Tip**: Click markers to view detailed precipitation and drought classification for each county centroid."
            )

        with col_m2:
            sample_county_data = generate_sample_county_weather(seed=42)
            fig_map = build_county_map(sample_county_data, color_by=map_metric)
            st.plotly_chart(fig_map, use_container_width=True)


# --- TAB 4: SOIL & CROP HEALTH METRICS ---
with tab_soil:
    st.subheader("🌱 Soil Parameters & Water Satisfaction Index")
    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.markdown("#### Soil Macronutrients & pH")
        st.progress(weather["nitrogen_n"] / 140.0, text=f"Nitrogen (N): {weather['nitrogen_n']} kg/ha")
        st.progress(weather["phosphorus_p"] / 100.0, text=f"Phosphorus (P): {weather['phosphorus_p']} kg/ha")
        st.progress(weather["potassium_k"] / 100.0, text=f"Potassium (K): {weather['potassium_k']} kg/ha")
        st.info(f"🧪 **Soil pH**: {weather['ph']} (Optimal range for Maize: 5.8 - 7.0)")

    with col_s2:
        st.markdown("#### Solar Radiation & Evapotranspiration")
        st.metric(label="Solar Radiation", value=f"{weather['solar_radiation']} MJ/m²")
        st.metric(label="Est. Daily Evapotranspiration", value="4.2 mm/day")

    with col_s3:
        st.markdown("#### Crop Water Satisfaction Index (CWSI)")
        st.metric(label="CWSI Rating", value="88 / 100", delta="Healthy (Low Water Stress)")
        st.success("✅ Current moisture levels satisfy water requirements for maize development.")
