# WeatherWise AI

An AI-powered weather decision-support platform that turns raw weather data into practical, crop-specific farming advice for smallholder farmers in Kenya.

Built for **Hack the Weather 2026 Hackathon**.

---

## Problem

Farmers have access to weather forecasts, but not actionable, localized recommendations. Knowing it will rain 20% of the time doesn't tell a farmer in Trans Nzoia whether to plant, irrigate, or wait. **WeatherWise AI** closes that gap by converting weather data into direct farming actions.

## Solution

WeatherWise AI combines:
- **Rainfall Prediction** — ML model (Random Forest/XGBoost) forecasting rainfall probability and intensity
- **Recommendation Engine** — rule-based logic converting forecasts into farming actions (plant, irrigate, fertilize, spray, harvest)
- **AI Weather Copilot** — LLM + RAG assistant answering natural-language farming questions
- **Smart Alerts** — real-time notifications for drought, heavy rainfall, wind, and heat stress
- **Interactive Dashboard** — weather trends, crop risk levels, and county-level risk maps

## Core Features

| Feature | Description |
|---|---|
| 🌤 Weather Summary | Real-time temperature, rainfall, humidity, wind, UV index |
| 📊 Weather Trends | Historical + forecasted rainfall charts |
| 🌽 Crop Health & Drought Risk | Predicted stress/drought risk levels |
| 🤖 AI Recommendations | Personalized planting/irrigation/fertilizing advice |
| 🚨 Smart Alerts | Notifications for extreme weather events |
| 🗺️ Interactive Weather Map | County-level risk visualization |
| 💬 AI Weather Copilot | Natural-language Q&A on farming decisions |

## Tech Stack

- **Language:** Python
- **ML:** scikit-learn, XGBoost
- **AI Copilot:** LLM + RAG (LangChain, ChromaDB)
- **Visualization:** Plotly, Folium
- **App/UI:** Streamlit
- **Prototyping:** Jupyter Notebooks

## Project Structure

```
weatherwise-ai/
├── data/                  # raw, processed, and sample weather data
├── notebooks/             # exploration & prototyping (ML + visualization)
├── models/                # finalized rainfall model, recommendation engine, copilot
├── visualization/         # chart and map-building functions
├── app/                   # Streamlit app (Home.py + multi-page UI)
├── tests/                 # unit tests
└── scripts/               # demo scripts, sample data seeding
```

## Team

| Track | Members |
|---|---|
| ML / Models | Margaret, Martina, Janet, Dennis |
| Visualization | Terry, Ann |
| UI/UX (Streamlit) | Wilfred, Lorna |

## Getting Started

```bash
# 1. Clone the repo
git clone <repo-url>
cd weatherwise-ai

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env          # then fill in API keys

# 5. Run the app
streamlit run app/Home.py
```

## Example

> **Farmer:** "Should I irrigate today?"
> **WeatherWise AI:** "Rainfall is expected within the next 24 hours. Irrigation is not recommended today as natural rainfall will provide sufficient soil moisture."

## Roadmap Status

See the team task checklist for the current build status across ML, Visualization, and UI/UX (Day-by-day, Jul 21 – Jul 27).

## License

Built for hackathon purposes — Hack the Weather 2026.
