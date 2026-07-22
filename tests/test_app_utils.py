"""
tests/test_app_utils.py
───────────────────────
Unit tests for Phase 1 of WeatherWise AI Streamlit Application.
Verifies utils bridge, recommendation algorithms, weather data generators,
and component imports.
"""

import pytest
import pandas as pd
from app.utils import (
    planting_advisor,
    irrigation_advisor,
    fertilizer_advisor,
    spraying_advisor,
    disease_risk_advisor,
    smart_alerts,
    generate_recommendations,
    predict_rainfall_probability,
    get_current_weather,
    get_7day_forecast_df,
    get_historical_weather_df,
    generate_copilot_response,
    load_ml_models,
)
from app.components.sidebar import TRANS_NZOIA_SUBCOUNTIES, CROPS, GROWTH_STAGES


def test_subcounty_list():
    """Verify Trans Nzoia sub-counties are properly configured."""
    assert "Kitale (Central Trans Nzoia)" in TRANS_NZOIA_SUBCOUNTIES
    assert "Endebess" in TRANS_NZOIA_SUBCOUNTIES
    assert "Cherangany" in TRANS_NZOIA_SUBCOUNTIES
    assert "Kwanza" in TRANS_NZOIA_SUBCOUNTIES
    assert "Saboti" in TRANS_NZOIA_SUBCOUNTIES


def test_recommendation_logic():
    """Test recommendation engine logic matching Notebooks/Recommendation engine.ipynb."""
    # Test planting advisor
    plant_yes = planting_advisor(rain_prediction=1, rainfall_amount=20.0)
    assert any("favorable" in msg for msg in plant_yes)
    plant_no = planting_advisor(rain_prediction=0, rainfall_amount=2.0)
    assert any("Wait" in msg for msg in plant_no)

    # Test irrigation advisor
    irr_delay = irrigation_advisor(rain_prediction=1, max_temp=25.0)
    assert any("Delay" in msg for msg in irr_delay)
    irr_hot = irrigation_advisor(rain_prediction=0, max_temp=34.0)
    assert any("Increase" in msg for msg in irr_hot)

    # Test fertilizer advisor
    fert_delay = fertilizer_advisor(rain_prediction=1)
    assert any("Delay" in msg for msg in fert_delay)

    # Test spraying advisor
    spray_wind = spraying_advisor(wind_speed=40.0)
    assert any("Avoid" in msg for msg in spray_wind)

    # Test disease risk advisor
    fungal = disease_risk_advisor(humidity=90.0, temperature=24.0)
    assert any("fungal" in msg.lower() for msg in fungal)

    # Test smart alerts
    alerts = smart_alerts(rain_prediction=1, max_temp=36.0, wind_speed=40.0)
    assert len(alerts) == 3


def test_generate_recommendations_pipeline():
    """Test combined recommendation pipeline."""
    recs = generate_recommendations(
        crop_name="maize",
        rain_prediction=1,
        rainfall_amount=25.0,
        temperature=28.0,
        humidity=88.0,
        wind_speed=18.0,
    )
    assert isinstance(recs, list)
    assert len(recs) >= 6


def test_predict_rainfall_probability():
    """Test rainfall probability prediction and model fallback."""
    pred = predict_rainfall_probability(
        min_temp=14.0, max_temp=26.0, humidity=80.0, wind_speed=15.0
    )
    assert "rain_prediction" in pred
    assert "rain_probability_pct" in pred
    assert "expected_rainfall_mm" in pred
    assert 0 <= pred["rain_probability_pct"] <= 100


def test_weather_data_generators():
    """Test weather data frame generation."""
    weather = get_current_weather("Kitale")
    assert weather["location"] == "Kitale"
    assert "max_temp" in weather
    assert "soil_moisture" in weather

    forecast_df = get_7day_forecast_df("Kitale")
    assert isinstance(forecast_df, pd.DataFrame)
    assert len(forecast_df) == 7
    assert "Rainfall" in forecast_df.columns
    assert "MaxTemp" in forecast_df.columns

    history_df = get_historical_weather_df("Kitale", days=30)
    assert isinstance(history_df, pd.DataFrame)
    assert len(history_df) == 30


def test_copilot_response():
    """Test AgriCopilot AI natural language engine."""
    response = generate_copilot_response(
        user_query="When should I plant maize?",
        chat_history=[],
        location="Kitale",
        crop="Maize",
        growth_stage="Planting",
    )
    assert isinstance(response, str)
    assert "Planting" in response or "Maize" in response
