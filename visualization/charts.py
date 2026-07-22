"""
charts.py
─────────
Chart-building functions consumed by the Streamlit app (WeatherWise AI).

Every function returns a Plotly Figure — call it and pass straight into
`st.plotly_chart(fig, use_container_width=True)` in your Streamlit page.

DATA CONTRACT
-------------
These functions are written against the column schema of weatherAUS.csv
(and its cleaned version, Cleaned_weatherAUS.csv, which has the same
columns):

    Date, Location, MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine,
    WindGustDir, WindGustSpeed, WindDir9am, WindDir3pm,
    WindSpeed9am, WindSpeed3pm, Humidity9am, Humidity3pm,
    Pressure9am, Pressure3pm, Cloud9am, Cloud3pm,
    Temp9am, Temp3pm, RainToday, RainTomorrow

`Location` currently holds Australian town names — when you swap in real
Kenya county/station data, keep the same column names (or edit the
COLUMN MAP constants below) and everything here keeps working unchanged.

If your rainfall-prediction model instead outputs a forecast table
(e.g. next 7 days with a predicted rainfall/probability), pass that
into `plot_forecast_overview()` — see its docstring for the expected shape.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Column map: change these if your CSV uses different header names ──────
COL_DATE = "Date"
COL_LOCATION = "Location"
COL_RAINFALL = "Rainfall"
COL_MIN_TEMP = "MinTemp"
COL_MAX_TEMP = "MaxTemp"
COL_HUMIDITY_AM = "Humidity9am"
COL_HUMIDITY_PM = "Humidity3pm"
COL_WIND_GUST = "WindGustSpeed"

# Drought-risk thresholds (mm of rainfall over the trailing window).
# Tune these once you have Kenya-specific agronomic thresholds.
DROUGHT_THRESHOLDS = {
    "Severe": 5,     # < 5mm over window  -> severe drought risk
    "Moderate": 20,  # < 20mm over window -> moderate drought risk
    "Low": 40,       # < 40mm over window -> low drought risk
    # >= 40mm -> "None"
}

RISK_COLORS = {
    "None": "#2e7d32",
    "Low": "#9e9d24",
    "Moderate": "#ef6c00",
    "Severe": "#c62828",
}


def _prep(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure Date is datetime and sorted; return a copy so we never mutate caller data."""
    out = df.copy()
    out[COL_DATE] = pd.to_datetime(out[COL_DATE], errors="coerce")
    out = out.dropna(subset=[COL_DATE]).sort_values(COL_DATE)
    return out


def _filter_location(df: pd.DataFrame, location: str | None) -> pd.DataFrame:
    if location and COL_LOCATION in df.columns:
        return df[df[COL_LOCATION] == location]
    return df


# ────────────────────────────────────────────────────────────────────────
# 1. RAINFALL TREND
# ────────────────────────────────────────────────────────────────────────
def plot_rainfall_trend(
    df: pd.DataFrame,
    location: str | None = None,
    date_range: tuple | None = None,
    rolling_window: int = 7,
) -> go.Figure:
    """
    Historical rainfall trend with a rolling average overlay.

    Parameters
    ----------
    df : DataFrame with at least [Date, Rainfall] (and Location, if filtering).
    location : optional county/station name to filter to.
    date_range : optional (start, end) tuple of date-like values to slice to.
    rolling_window : days used for the smoothed trend line.
    """
    data = _prep(df)
    data = _filter_location(data, location)

    if date_range:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        data = data[(data[COL_DATE] >= start) & (data[COL_DATE] <= end)]

    if data.empty:
        return _empty_fig("No rainfall data available for this selection.")

    data = data.groupby(COL_DATE, as_index=False)[COL_RAINFALL].mean()
    data["rolling_avg"] = data[COL_RAINFALL].rolling(rolling_window, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=data[COL_DATE],
            y=data[COL_RAINFALL],
            name="Daily rainfall (mm)",
            marker_color="#4fc3f7",
            opacity=0.6,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data[COL_DATE],
            y=data["rolling_avg"],
            name=f"{rolling_window}-day rolling avg",
            line=dict(color="#01579b", width=2.5),
            mode="lines",
        )
    )

    title = "Rainfall Trend"
    if location:
        title += f" — {location}"

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Rainfall (mm)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(orientation="h", y=1.1),
    )
    return fig


# ────────────────────────────────────────────────────────────────────────
# 2. DROUGHT RISK
# ────────────────────────────────────────────────────────────────────────
def compute_drought_risk(df: pd.DataFrame, window_days: int = 14) -> pd.DataFrame:
    """
    Compute a drought-risk category per location, based on total rainfall
    over the most recent `window_days` days of data available.

    Returns a DataFrame: [Location, total_rainfall_mm, risk_level]
    """
    data = _prep(df)
    if data.empty or COL_LOCATION not in data.columns:
        return pd.DataFrame(columns=[COL_LOCATION, "total_rainfall_mm", "risk_level"])

    cutoff = data[COL_DATE].max() - pd.Timedelta(days=window_days)
    recent = data[data[COL_DATE] >= cutoff]

    summary = (
        recent.groupby(COL_LOCATION, as_index=False)[COL_RAINFALL]
        .sum()
        .rename(columns={COL_RAINFALL: "total_rainfall_mm"})
    )

    def classify(mm: float) -> str:
        if mm < DROUGHT_THRESHOLDS["Severe"]:
            return "Severe"
        if mm < DROUGHT_THRESHOLDS["Moderate"]:
            return "Moderate"
        if mm < DROUGHT_THRESHOLDS["Low"]:
            return "Low"
        return "None"

    summary["risk_level"] = summary["total_rainfall_mm"].apply(classify)
    return summary.sort_values("total_rainfall_mm")


def plot_drought_risk(df: pd.DataFrame, window_days: int = 14, top_n: int = 15) -> go.Figure:
    """
    Horizontal bar chart of drought risk by location, colored by risk level.
    Shows the `top_n` locations with the lowest rainfall (highest risk) first.
    """
    summary = compute_drought_risk(df, window_days=window_days)
    if summary.empty:
        return _empty_fig("No data available to compute drought risk.")

    summary = summary.head(top_n)

    fig = go.Figure()
    for risk in ["Severe", "Moderate", "Low", "None"]:
        subset = summary[summary["risk_level"] == risk]
        if subset.empty:
            continue
        fig.add_trace(
            go.Bar(
                x=subset["total_rainfall_mm"],
                y=subset[COL_LOCATION],
                name=risk,
                orientation="h",
                marker_color=RISK_COLORS[risk],
            )
        )

    fig.update_layout(
        title=f"Drought Risk — trailing {window_days} days",
        xaxis_title="Total rainfall (mm)",
        yaxis_title="",
        template="plotly_white",
        barmode="stack",
        legend_title="Risk level",
        yaxis=dict(autorange="reversed"),
    )
    return fig


# ────────────────────────────────────────────────────────────────────────
# 3. FORECAST OVERVIEW
# ────────────────────────────────────────────────────────────────────────
def plot_forecast_overview(forecast_df: pd.DataFrame) -> go.Figure:
    """
    Multi-metric forecast chart (e.g. next 7 days from your ML model).

    Expected columns (rename to match, or edit constants at top of file):
        Date, MaxTemp, MinTemp, Rainfall, Humidity  (Humidity optional)

    If you only have a probability + expected rainfall (no temps yet),
    pass a DataFrame with just [Date, Rainfall] and this still renders
    the rainfall panel with an empty (but labeled) temperature panel.
    """
    if forecast_df is None or forecast_df.empty:
        return _empty_fig("No forecast data available.")

    data = forecast_df.copy()
    data[COL_DATE] = pd.to_datetime(data[COL_DATE], errors="coerce")
    data = data.dropna(subset=[COL_DATE]).sort_values(COL_DATE)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if COL_RAINFALL in data.columns:
        fig.add_trace(
            go.Bar(
                x=data[COL_DATE],
                y=data[COL_RAINFALL],
                name="Expected rainfall (mm)",
                marker_color="#4fc3f7",
                opacity=0.7,
            ),
            secondary_y=False,
        )

    if COL_MAX_TEMP in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data[COL_DATE],
                y=data[COL_MAX_TEMP],
                name="Max temp (°C)",
                line=dict(color="#e65100", width=2),
                mode="lines+markers",
            ),
            secondary_y=True,
        )

    if COL_MIN_TEMP in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data[COL_DATE],
                y=data[COL_MIN_TEMP],
                name="Min temp (°C)",
                line=dict(color="#0277bd", width=2, dash="dot"),
                mode="lines+markers",
            ),
            secondary_y=True,
        )

    fig.update_layout(
        title="7-Day Forecast Overview",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.15),
    )
    fig.update_yaxes(title_text="Rainfall (mm)", secondary_y=False)
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=True)
    return fig


# ────────────────────────────────────────────────────────────────────────
# helpers
# ────────────────────────────────────────────────────────────────────────
def _empty_fig(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color="gray"),
    )
    fig.update_layout(
        template="plotly_white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig