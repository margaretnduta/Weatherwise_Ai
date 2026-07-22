"""
app/components/sidebar.py
─────────────────────────
Shared sidebar component for WeatherWise AI.
Manages global state (Location/Sub-County, Target Crop, Growth Stage, ML Model selection).
"""

from typing import Any, Dict
import streamlit as st

# Trans Nzoia Sub-Counties list
TRANS_NZOIA_SUBCOUNTIES = [
    "Kitale (Central Trans Nzoia)",
    "Endebess",
    "Cherangany",
    "Kwanza",
    "Saboti",
]

OTHER_KENYA_COUNTIES = [
    "Uasin Gishu",
    "Bungoma",
    "Kakamega",
    "West Pokot",
    "Elgeyo-Marakwet",
    "Nandi",
    "Nakuru",
    "Nairobi",
]

CROPS = ["Maize (Corn)", "Beans", "Wheat", "Potatoes", "Vegetables"]

GROWTH_STAGES = [
    "Planting",
    "Vegetative",
    "Flowering / Tasseling",
    "Maturation / Harvest",
]

ML_MODELS = [
    "Random Forest Classifier (Ensemble)",
    "XGBoost Rainfall Predictor",
]


def render_sidebar() -> Dict[str, Any]:
    """
    Render the shared WeatherWise AI sidebar.

    Returns
    -------
    dict containing:
        - location: str (Selected sub-county or county)
        - crop: str (Selected target crop)
        - growth_stage: str (Selected crop growth stage)
        - ml_model: str (Selected ML model)
        - is_trans_nzoia: bool (True if location is inside Trans Nzoia)
    """
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding-bottom: 10px;">
                <h2 style="color: #38BDF8; margin-bottom: 0px; font-size: 1.6rem;">🌦️ WeatherWise AI</h2>
                <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">Smart Weather Copilot • Hack the Weather 2026</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # 1. Location Selector
        st.subheader("📍 Location Context")

        location_scope = st.radio(
            "Region Focus",
            options=["Trans Nzoia Sub-County", "Other Kenya County"],
            index=0,
            key="location_scope_radio",
        )

        if location_scope == "Trans Nzoia Sub-County":
            selected_location = st.selectbox(
                "Select Sub-County:",
                options=TRANS_NZOIA_SUBCOUNTIES,
                index=0,
                key="subcounty_select",
                help="Trans Nzoia is Kenya's primary maize basket. Select your sub-county for localized weather predictions.",
            )
            is_trans_nzoia = True
        else:
            selected_location = st.selectbox(
                "Select County:",
                options=OTHER_KENYA_COUNTIES,
                index=0,
                key="county_select",
            )
            is_trans_nzoia = False

        st.divider()

        # 2. Agricultural Context
        st.subheader("🌾 Crop & Farming Stage")

        selected_crop = st.selectbox(
            "Target Crop:",
            options=CROPS,
            index=0,
            key="crop_select",
            help="Select the crop you are actively managing or planning.",
        )

        selected_growth_stage = st.selectbox(
            "Growth Stage:",
            options=GROWTH_STAGES,
            index=2 if "Maize" in selected_crop else 0,
            key="growth_stage_select",
            help="Water requirements and heat sensitivity vary greatly by growth stage.",
        )

        st.divider()

        # 3. Model Engine Context
        st.subheader("🤖 Predictive Engine")

        selected_model = st.selectbox(
            "Rainfall Model:",
            options=ML_MODELS,
            index=0,
            key="ml_model_select",
            help="Select machine learning architecture used for precipitation predictions.",
        )

        st.divider()

        # Live Status Card
        st.markdown(
            f"""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 10px 14px; margin-top: 10px;">
                <div style="font-size: 0.78rem; color: #6EE7B7; font-weight: 600;">● CONDUIT WEATHER STREAM: CONNECTED</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Sub-county: <b>{selected_location.split(' ')[0]}</b></div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Target: <b>{selected_crop} ({selected_growth_stage.split(' ')[0]})</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Save to session_state
        config = {
            "location": selected_location,
            "crop": selected_crop,
            "growth_stage": selected_growth_stage,
            "ml_model": selected_model,
            "is_trans_nzoia": is_trans_nzoia,
        }

        st.session_state["weatherwise_config"] = config
        return config
