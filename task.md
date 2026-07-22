# Task Tracker: WeatherWise AI Streamlit Application

Comprehensive task tracking list for **WeatherWise AI** (Hack the Weather 2026 Hackathon) — Trans Nzoia County Smart Agricultural Weather Copilot.

> **Strict Boundary Constraint**: ONLY create and edit files within the `app/` subdirectory (plus unit tests for `app/`). Do NOT edit any existing folders (`models/`, `Data/`, `visualization/`, `Notebooks/`).
> **Workflow Constraint**: After completing each phase, run unit tests to verify functionality, and commit changes via Git before proceeding to the next phase.

---

## Task Checklist

### Phase 1: Architecture & Utilities Foundation
- [x] **Create `app/components/styling.py`**
  - [x] Implement custom CSS injection function (`inject_custom_css`)
  - [x] Style metric cards, alert badges (Critical, Warning, Advisory), glassmorphism cards
  - [x] Style chat message bubbles and sidebar navigation
- [x] **Create `app/components/sidebar.py`**
  - [x] Build unified Streamlit sidebar (`render_sidebar`)
  - [x] Add Trans Nzoia Sub-County selector (Kitale / Central, Endebess, Cherangany, Kwanza, Saboti) and broader Kenya counties
  - [x] Add Crop selector (Maize/Corn, Beans, Wheat, Potatoes, Vegetables)
  - [x] Add Growth Stage selector (Planting, Vegetative, Flowering/Tasseling, Maturation/Harvest)
  - [x] Add ML Model toggle selector (Random Forest Ensemble vs XGBoost Rainfall Model)
  - [x] Store configuration state in `st.session_state`
- [x] **Create `app/utils.py` (Core Bridge to Existing Codebase)**
  - [x] Wire up imports from `visualization.charts` (`plot_rainfall_trend`, `plot_drought_risk`, `plot_forecast_overview`, `compute_drought_risk`)
  - [x] Wire up imports from `visualization.map_data` (`build_county_map`, `generate_sample_county_weather`, `merge_weather_onto_counties`, `KENYA_COUNTY_CENTROIDS`)
  - [x] Implement exact advisory decision logic from `Notebooks/Recommendation engine.ipynb` (`planting_advisor`, `irrigation_advisor`, `fertilizer_advisor`, `spraying_advisor`, `disease_risk_advisor`, `crop_advisor`, `smart_alerts`, `generate_recommendations`)
  - [x] Implement `load_ml_models()` to load `models/rainfall_prediction_model.pkl` and `models/crop_recommendation_model.pkl` with graceful fallbacks
  - [x] Implement data loaders for real-time Trans Nzoia weather context and 7-day forecast data
  - [x] Implement AgriCopilot AI assistant engine (`generate_copilot_response`) with RAG context
- [x] **Phase 1 Verification & Commit**
  - [x] Write and run Phase 1 unit tests (`tests/test_app_utils.py` or `python -m pytest`)
  - [x] Perform Git commit: `"feat(app): implement core styling, sidebar, and utils bridge"`

---

### Phase 2: Core Application Pages
- [ ] **Create `app/Home.py` (Landing Page)**
  - [ ] Configure `st.set_page_config` with page icon, title, and wide layout
  - [ ] Inject custom styling and sidebar controls
  - [ ] Implement landing header & Hack the Weather 2026 project banner
  - [ ] Display Trans Nzoia County agricultural overview and key metrics ticker
  - [ ] Render interactive feature cards with direct navigation links to pages
- [ ] **Create `app/pages/1_Dashboard.py` (Smart Weather Dashboard)**
  - [ ] Render top KPI metric cards (Current Temp, 24h Rainfall, Soil Moisture, Drought Risk)
  - [ ] Build Tab 1: 7-Day Trend & Forecast Overview (using `visualization.charts.plot_forecast_overview`)
  - [ ] Build Tab 2: Historical Rainfall & Drought Risk (using `plot_rainfall_trend` & `plot_drought_risk`)
  - [ ] Build Tab 3: Interactive County & Sub-County Map (using `visualization.map_data.build_county_map`)
- [ ] **Create `app/pages/2_Crop_Advisor.py` (Smart Crop Advisor)**
  - [ ] Integrate advisory recommendations engine from `utils.get_recommendations`
  - [ ] Render recommendation cards by category (Planting, Irrigation, Fertilizer, Spraying, Disease Risk)
  - [ ] Implement interactive "What-If" Scenario Simulator for rainfall & temperature impact
  - [ ] Render optimal planting window calendar & soil nutrient status (N, P, K, pH)
- [ ] **Create `app/pages/3_Copilot_Chat.py` (AgriCopilot AI Chat Interface)**
  - [ ] Implement chat conversation UI with `st.chat_message` and `st.chat_input`
  - [ ] Maintain chat history in `st.session_state.messages`
  - [ ] Render active context sidebar panel (Selected Sub-county, Target Crop, Growth Stage, Active Risk Factors)
  - [ ] Add clickable quick-prompt pills for common farmer questions
  - [ ] Stream AI responses referencing weather forecasts and ML model outputs
- [ ] **Create `app/pages/4_Alerts.py` (Smart Alerts Panel)**
  - [ ] Render real-time alert feed using `smart_alerts()` outputs
  - [ ] Add severity filters (All, Critical, Warning, Advisory)
  - [ ] Render detailed alert cards with alert cause, affected sub-county, and step-by-step mitigation actions
  - [ ] Add notification preference toggle simulator
- [ ] **Phase 2 Verification & Commit**
  - [ ] Run compilation and unit tests across all pages (`app/Home.py` and `app/pages/*.py`)
  - [ ] Perform Git commit: `"feat(app): implement Home, Dashboard, Crop Advisor, Copilot Chat, and Alerts pages"`

---

### Phase 3: System Testing & Final Delivery
- [ ] **End-to-End Verification**
  - [ ] Run full test suite with `pytest`
  - [ ] Verify Streamlit compilation (`python -m py_compile app/Home.py app/utils.py app/components/*.py app/pages/*.py`)
- [ ] **Phase 3 Final Commit**
  - [ ] Perform final Git commit: `"chore(app): finalize WeatherWise AI Streamlit application"`
