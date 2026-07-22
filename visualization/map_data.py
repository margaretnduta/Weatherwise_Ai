"""
map_data.py
───────────
County-level map preparation for WeatherWise AI's Interactive Weather Map.

You currently don't have a Kenya counties GeoJSON/shapefile or per-county
live weather data, so this module ships with:

  1. A built-in lat/lon centroid lookup for all 47 Kenyan counties, so you
     can plot points on a map with zero extra downloads.
  2. `merge_weather_onto_counties()` — attaches a weather DataFrame
     (any source: your model output, an API, or a CSV) onto the county
     centroids by matching a county-name column.
  3. `generate_sample_county_weather()` — produces realistic-looking demo
     data so the map/dashboard renders today, before real per-county data
     is wired up. Swap this out once you have live data — the plotting
     function doesn't care where the numbers came from.
  4. `build_county_map()` — returns a Plotly scatter-mapbox Figure colored
     by rainfall or drought risk, ready for `st.plotly_chart()`.

If you later obtain an official counties GeoJSON (e.g. from the Kenya
Open Data portal or geoBoundaries), you can switch `build_county_map()`
to `px.choropleth_mapbox()` using that file — the merge step below still
works the same way, you'd just join on the GeoJSON's county-name property
instead of plotting centroids.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ── Kenya county centroids (approximate, WGS84 lat/lon) ───────────────────
# Source: publicly available county centroid coordinates, Kenya's 47 counties.
KENYA_COUNTY_CENTROIDS = {
    "Mombasa": (-4.0435, 39.6682),
    "Kwale": (-4.1816, 39.4606),
    "Kilifi": (-3.5107, 39.9093),
    "Tana River": (-1.6500, 40.0333),
    "Lamu": (-2.2717, 40.9020),
    "Taita Taveta": (-3.3167, 38.4833),
    "Garissa": (-0.4569, 39.6583),
    "Wajir": (1.7471, 40.0629),
    "Mandera": (3.9366, 41.8670),
    "Marsabit": (2.3284, 37.9899),
    "Isiolo": (0.3556, 37.5820),
    "Meru": (0.0463, 37.6559),
    "Tharaka-Nithi": (-0.2971, 37.7986),
    "Embu": (-0.5310, 37.4500),
    "Kitui": (-1.3667, 38.0167),
    "Machakos": (-1.5177, 37.2634),
    "Makueni": (-1.8039, 37.6244),
    "Nyandarua": (-0.1833, 36.5167),
    "Nyeri": (-0.4167, 36.9500),
    "Kirinyaga": (-0.6667, 37.3833),
    "Murang'a": (-0.7167, 37.1500),
    "Kiambu": (-1.1714, 36.8356),
    "Turkana": (3.1167, 35.6000),
    "West Pokot": (1.6167, 35.3833),
    "Samburu": (1.2154, 36.9576),
    "Trans Nzoia": (1.0500, 34.9500),
    "Uasin Gishu": (0.5167, 35.2833),
    "Elgeyo-Marakwet": (0.8000, 35.5000),
    "Nandi": (0.1833, 35.1167),
    "Baringo": (0.4667, 35.9667),
    "Laikipia": (0.4000, 36.7833),
    "Nakuru": (-0.3031, 36.0800),
    "Narok": (-1.0833, 35.8667),
    "Kajiado": (-1.8500, 36.7833),
    "Kericho": (-0.3667, 35.2833),
    "Bomet": (-0.7833, 35.3417),
    "Kakamega": (0.2827, 34.7519),
    "Vihiga": (0.0833, 34.7167),
    "Bungoma": (0.5667, 34.5667),
    "Busia": (0.4600, 34.1116),
    "Siaya": (0.0607, 34.2881),
    "Kisumu": (-0.0917, 34.7680),
    "Homa Bay": (-0.5167, 34.4500),
    "Migori": (-1.0634, 34.4731),
    "Kisii": (-0.6773, 34.7796),
    "Nyamira": (-0.5633, 34.9358),
    "Nairobi": (-1.2921, 36.8219),
}


def get_county_centroids() -> pd.DataFrame:
    """Return the county centroid lookup as a tidy DataFrame."""
    return pd.DataFrame(
        [{"County": c, "lat": lat, "lon": lon} for c, (lat, lon) in KENYA_COUNTY_CENTROIDS.items()]
    )


def merge_weather_onto_counties(
    weather_df: pd.DataFrame,
    county_col: str = "County",
) -> pd.DataFrame:
    """
    Left-join county centroids onto a weather DataFrame.

    `weather_df` can come from anywhere (your ML model's per-county
    output, a weather API response you've reshaped, or a CSV) as long as
    it has one row per county with a county-name column.

    Unmatched county names (typos, alternate spellings) are kept in the
    output with NaN lat/lon so you can spot and fix them rather than
    silently dropping rows.
    """
    centroids = get_county_centroids()
    merged = weather_df.merge(
        centroids, left_on=county_col, right_on="County", how="left"
    )
    unmatched = merged[merged["lat"].isna()][county_col].unique()
    if len(unmatched) > 0:
        print(f"[map_data] Warning: no centroid match for: {list(unmatched)}")
    return merged


def generate_sample_county_weather(seed: int = 42) -> pd.DataFrame:
    """
    Demo data generator: plausible rainfall/temperature/drought-risk values
    per county, for wiring up the map UI before live data is available.

    Replace calls to this function with real data — e.g. the output of
    your rainfall-prediction model aggregated to county level, or a merge
    of Kenyan station data mapped to counties.
    """
    rng = np.random.default_rng(seed)
    counties = list(KENYA_COUNTY_CENTROIDS.keys())

    # Arid/semi-arid northern counties get a drier baseline than the rest.
    arid_counties = {
        "Turkana", "Marsabit", "Wajir", "Mandera", "Garissa",
        "Isiolo", "Samburu", "West Pokot", "Tana River", "Kajiado",
    }

    rows = []
    for county in counties:
        is_arid = county in arid_counties
        rainfall_mm = rng.uniform(0, 15) if is_arid else rng.uniform(5, 60)
        max_temp = rng.uniform(28, 38) if is_arid else rng.uniform(20, 30)
        min_temp = max_temp - rng.uniform(8, 14)
        humidity = rng.uniform(20, 45) if is_arid else rng.uniform(40, 85)

        if rainfall_mm < 5:
            risk = "Severe"
        elif rainfall_mm < 20:
            risk = "Moderate"
        elif rainfall_mm < 40:
            risk = "Low"
        else:
            risk = "None"

        rows.append(
            {
                "County": county,
                "rainfall_mm": round(rainfall_mm, 1),
                "max_temp_c": round(max_temp, 1),
                "min_temp_c": round(min_temp, 1),
                "humidity_pct": round(humidity, 1),
                "drought_risk": risk,
            }
        )

    return pd.DataFrame(rows)


# ── Map figure ──────────────────────────────────────────────────────────
_RISK_COLOR_SCALE = {
    "None": "#2e7d32",
    "Low": "#9e9d24",
    "Moderate": "#ef6c00",
    "Severe": "#c62828",
}


def build_county_map(
    county_weather_df: pd.DataFrame,
    color_by: str = "rainfall_mm",
    county_col: str = "County",
) -> go.Figure:
    """
    Build an interactive county-level map.

    Parameters
    ----------
    county_weather_df : one row per county, must include lat/lon (call
        `merge_weather_onto_counties()` first if it doesn't already), and
        the column named in `color_by`.
    color_by : either a numeric column (e.g. "rainfall_mm", "max_temp_c")
        for a continuous color scale, or "drought_risk" for a categorical
        risk-level color scale.
    county_col : name of the county-name column, used for marker labels.
    """
    data = county_weather_df.copy()
    if "lat" not in data.columns or "lon" not in data.columns:
        data = merge_weather_onto_counties(data, county_col=county_col)
    data = data.dropna(subset=["lat", "lon"])

    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No county data available to map.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
        )
        return fig

    fig = go.Figure()

    if color_by == "drought_risk":
        for risk, color in _RISK_COLOR_SCALE.items():
            subset = data[data["drought_risk"] == risk]
            if subset.empty:
                continue
            fig.add_trace(
                go.Scattermapbox(
                    lat=subset["lat"],
                    lon=subset["lon"],
                    mode="markers",
                    marker=dict(size=16, color=color),
                    text=subset[county_col],
                    name=risk,
                    hovertemplate="<b>%{text}</b><br>Drought risk: " + risk + "<extra></extra>",
                )
            )
        legend_title = "Drought risk"
    else:
        fig.add_trace(
            go.Scattermapbox(
                lat=data["lat"],
                lon=data["lon"],
                mode="markers",
                marker=dict(
                    size=16,
                    color=data[color_by],
                    colorscale="YlGnBu",
                    showscale=True,
                    colorbar=dict(title=color_by),
                ),
                text=data[county_col],
                hovertemplate=f"<b>%{{text}}</b><br>{color_by}: " + "%{marker.color}<extra></extra>",
            )
        )
        legend_title = None

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=0.2, lon=37.5),  # roughly the center of Kenya
            zoom=5.2,
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        title=f"County-Level Weather Map — {color_by.replace('_', ' ').title()}",
        legend_title=legend_title,
    )
    return fig