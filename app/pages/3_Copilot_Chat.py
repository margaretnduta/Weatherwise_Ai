"""
app/pages/3_Copilot_Chat.py
───────────────────────────
AgriCopilot AI Chat Interface for WeatherWise AI.
Natural-language chat interface (LLM + RAG) interpreting weather forecasts,
ML predictions, and localized Trans Nzoia agronomic knowledge.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import time
import streamlit as st
from app.components.styling import inject_custom_css
from app.components.sidebar import render_sidebar
from app.utils import (
    get_current_weather,
    predict_rainfall_probability,
    generate_copilot_response,
)

# Page configuration
st.set_page_config(
    page_title="AgriCopilot AI Chat — WeatherWise AI",
    page_icon="🤖",
    layout="wide",
)

inject_custom_css()
config = render_sidebar()

location = config["location"]
crop = config["crop"]
growth_stage = config["growth_stage"]

st.title("🤖 AgriCopilot AI Weather Chat")
st.caption(
    "Ask any question about weather forecasts, planting windows, fertilizer timing, or pest risks in plain English."
)

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"Habari! 👋 I am your **WeatherWise AgriCopilot** for **{location}**.\n\n"
                f"I am actively monitoring weather patterns for **{crop}** ({growth_stage} stage). "
                f"How can I assist your farming operations today?"
            ),
        }
    ]

# Layout: Chat Column (main) & Active RAG Context Card (side)
col_chat, col_context = st.columns([3, 1])

with col_context:
    st.markdown("### 📌 Active RAG Context")
    weather = get_current_weather(location)
    pred = predict_rainfall_probability(
        weather["min_temp"], weather["max_temp"], weather["humidity"], weather["wind_speed"]
    )

    st.markdown(
        f"""
        <div class="glass-card" style="font-size: 0.88rem;">
            <div style="color: #38BDF8; font-weight: 700; margin-bottom: 6px;">📍 Location Profile</div>
            <div>Region: <b>{location.split(' ')[0]}</b></div>
            <div>Target Crop: <b>{crop}</b></div>
            <div>Stage: <b>{growth_stage}</b></div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
            <div style="color: #38BDF8; font-weight: 700; margin-bottom: 6px;">🌧️ ML Model State</div>
            <div>Rain Prob: <b>{pred['rain_probability_pct']}%</b></div>
            <div>Expected: <b>{pred['expected_rainfall_mm']} mm</b></div>
            <div>Max Temp: <b>{weather['max_temp']} °C</b></div>
            <div>Soil Humidity: <b>{weather['humidity']}%</b></div>
            <div>Soil pH: <b>{weather['ph']}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 💡 Quick Prompts")
    prompt_1 = f"Should I apply fertilizer in {location.split(' ')[0]} this week?"
    prompt_2 = f"What is the rainfall forecast for {crop}?"
    prompt_3 = "Is there a fungal disease or armyworm risk?"

    if st.button("🌱 Fertilizer timing?", use_container_width=True):
        st.session_state["prompt_input"] = prompt_1
    if st.button("🌦️ 5-Day Rain forecast?", use_container_width=True):
        st.session_state["prompt_input"] = prompt_2
    if st.button("🐛 Pest & Disease risk?", use_container_width=True):
        st.session_state["prompt_input"] = prompt_3

with col_chat:
    # Render existing message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Determine user prompt from input box or prompt button
    user_prompt = st.chat_input("Ask AgriCopilot a farming or weather question...")
    if "prompt_input" in st.session_state and st.session_state["prompt_input"]:
        user_prompt = st.session_state.pop("prompt_input")

    if user_prompt:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Conduit weather stream & ML model predictions..."):
                response_text = generate_copilot_response(
                    user_query=user_prompt,
                    chat_history=st.session_state.messages[:-1],
                    location=location,
                    crop=crop,
                    growth_stage=growth_stage,
                )
                time.sleep(0.3)
                st.markdown(response_text)

        # Append Assistant Response
        st.session_state.messages.append({"role": "assistant", "content": response_text})
