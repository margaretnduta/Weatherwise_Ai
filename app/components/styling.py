"""
app/components/styling.py
─────────────────────────
Custom CSS and theme tweaks for WeatherWise AI.
Injects modern glassmorphism, responsive card grids, metric typography,
alert badges, and dark/light harmonized aesthetics into Streamlit pages.
"""

import streamlit as st


def inject_custom_css() -> None:
    """Inject custom CSS rules into the active Streamlit runtime."""
    st.markdown(
        """
        <style>
        /* Import Inter & Outfit Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3, h4, .main-header-title {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700;
        }

        /* Glassmorphism Card Container */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.28);
        }

        /* Weather Metric Styling */
        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 14px 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        div[data-testid="stMetricValue"] > div {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.9rem;
            color: #38BDF8;
        }

        div[data-testid="stMetricLabel"] > div {
            font-size: 0.88rem;
            font-weight: 500;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Alert Badges */
        .badge-critical {
            background-color: rgba(239, 68, 68, 0.2);
            color: #FCA5A5;
            border: 1px solid rgba(239, 68, 68, 0.4);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        .badge-warning {
            background-color: rgba(245, 158, 11, 0.2);
            color: #FDE047;
            border: 1px solid rgba(245, 158, 11, 0.4);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        .badge-advisory {
            background-color: rgba(16, 185, 129, 0.2);
            color: #6EE7B7;
            border: 1px solid rgba(16, 185, 129, 0.4);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        /* Recommendation Box Styling */
        .rec-box {
            background: rgba(30, 41, 59, 0.7);
            border-left: 4px solid #10B981;
            padding: 14px 18px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 12px;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .rec-box-warning {
            background: rgba(30, 41, 59, 0.7);
            border-left: 4px solid #F59E0B;
            padding: 14px 18px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 12px;
            font-size: 0.95rem;
        }

        .rec-box-alert {
            background: rgba(30, 41, 59, 0.7);
            border-left: 4px solid #EF4444;
            padding: 14px 18px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 12px;
            font-size: 0.95rem;
        }

        /* Hackathon Header Banner */
        .hackathon-banner {
            background: linear-gradient(135deg, #065F46 0%, #0F766E 50%, #0284C7 100%);
            color: #FFFFFF;
            padding: 24px 30px;
            border-radius: 20px;
            margin-bottom: 25px;
            box-shadow: 0 10px 25px -5px rgba(6, 95, 70, 0.4);
        }

        .hackathon-banner h1 {
            color: #FFFFFF !important;
            margin-bottom: 6px;
            font-size: 2.2rem;
        }

        .hackathon-banner p {
            color: #E0F2FE;
            font-size: 1.05rem;
            margin-bottom: 0;
        }

        /* Quick Prompt Pill Buttons */
        .prompt-pill {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 8px 16px;
            margin: 4px;
            display: inline-block;
            font-size: 0.85rem;
            color: #E2E8F0;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .prompt-pill:hover {
            background: rgba(14, 165, 233, 0.25);
            border-color: #38BDF8;
            color: #FFFFFF;
        }

        /* Custom Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.5);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.3);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(148, 163, 184, 0.5);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
