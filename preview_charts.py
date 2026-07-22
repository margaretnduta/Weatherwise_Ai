"""
preview_charts.py
──────────────────
Standalone test script — lets you see your charts and map render in your
browser WITHOUT running the full Streamlit app or needing any teammate's
code. Just this script + your visualization/ folder + your CSV data.

USAGE (from VSCode terminal, inside your project folder):
    python preview_charts.py

Each chart opens as a separate browser tab. Close tabs between runs if
you re-run the script.
"""

import pandas as pd
import plotly.io as pio
from visualization import charts, map_data

# Force charts to open in your default web browser (VSCode sometimes
# auto-detects a notebook-style renderer instead, which shows raw JSON
# in the terminal rather than opening a tab).
pio.renderers.default = "browser"

# ── 1. Load your real data ──────────────────────────────────────────────
DATA_PATH = "Data/Cleaned/Cleaned_weatherAUS.csv"   # matches the repo's folder structure
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows from {DATA_PATH}")
print("Columns:", list(df.columns))

# ── 2. Rainfall trend ────────────────────────────────────────────────────
sample_location = df["Location"].dropna().unique()[0]
print(f"\nPreviewing rainfall trend for: {sample_location}")
fig1 = charts.plot_rainfall_trend(df, location=sample_location)
fig1.show()

# ── 3. Drought risk ──────────────────────────────────────────────────────
print("\nPreviewing drought risk (last 30 days of data)")
fig2 = charts.plot_drought_risk(df, window_days=30)
fig2.show()

# ── 4. Forecast overview ─────────────────────────────────────────────────
forecast_slice = (
    df[df["Location"] == sample_location]
    .tail(7)[["Date", "MaxTemp", "MinTemp", "Rainfall"]]
)
print(f"\nPreviewing 7-day forecast overview for: {sample_location}")
fig3 = charts.plot_forecast_overview(forecast_slice)
fig3.show()

# ── 5. County-level map ───────────────────────────────────────────────────
print("\nPreviewing county-level map (sample Kenya data)")
county_weather = map_data.generate_sample_county_weather()
fig4 = map_data.build_county_map(county_weather, color_by="drought_risk")
fig4.show()

print("\nAll charts opened in your browser. Done.")