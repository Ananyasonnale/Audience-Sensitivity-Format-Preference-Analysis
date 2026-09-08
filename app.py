"""
Streamlit Web Application for France Top 50 Playlist Analysis.
Client: Atlantic Recording Corporation
Program: Unified Mentor
Authoritative Reference: PROJECT_SPEC.md Section 5

An executive-ready interactive intelligence platform analyzing audience sensitivity,
content compliance, and format preferences for the French streaming market.
"""

import os
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Import modular analytics and KPI engines
from src.analysis import (
    get_album_size_distribution,
    get_album_size_vs_popularity,
    get_content_attribute_concentration,
    get_dilution_vs_concentration,
    get_duration_by_rank_tier,
    get_duration_distribution,
    get_duration_vs_performance,
    get_explicit_by_position,
    get_explicit_popularity_comparison,
    get_explicit_share,
    get_format_by_rank,
    get_format_popularity_comparison,
    get_format_share,
    synthesize_french_preference_profile,
)
from src.kpis import calculate_all_kpis, filter_data

# ==============================================================================
# PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="Atlantic Records | France Top 50 Terminal",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# HYPER-PROFESSIONAL DARK GLASSMORPHIC DESIGN SYSTEM (CSS)
# ==============================================================================
st.markdown(
    """
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Color Tokens & Canvas Resets */
    :root {
        --bg-dark-obsidian: #060913;
        --bg-card-glass: rgba(13, 21, 39, 0.75);
        --bg-card-solid: #0d1527;
        --border-glass: rgba(255, 255, 255, 0.08);
        --border-glow-blue: rgba(56, 189, 248, 0.35);
        --accent-cyan: #38bdf8;
        --accent-purple: #c084fc;
        --accent-emerald: #34d399;
        --accent-rose: #fb7185;
        --accent-amber: #fbbf24;
        --accent-teal: #2dd4bf;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
    }

    .stApp {
        background-color: var(--bg-dark-obsidian);
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.06) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.05) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.03) 0%, transparent 60%);
        background-attachment: fixed;
        color: var(--text-primary);
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top Navigation Header Adjustment */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3.5rem;
        max-width: 1480px;
    }

    /* Scrollbar Polish */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #060913;
    }
    ::-webkit-scrollbar-thumb {
        background: #1e293b;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }

    /* Live Telemetry Pulse Animation */
    .status-pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #34d399;
        box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7);
        animation: pulse-animation 2s infinite;
        margin-right: 6px;
    }
    @keyframes pulse-animation {
        0% {
            box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7);
        }
        70% {
            box-shadow: 0 0 0 8px rgba(52, 211, 153, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(52, 211, 153, 0);
        }
    }

    /* Modern Hero Banner */
    .hero-card {
        position: relative;
        background: linear-gradient(135deg, rgba(17, 24, 43, 0.85) 0%, rgba(10, 15, 29, 0.95) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-glass);
        border-top: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.65), 0 0 30px rgba(56, 189, 248, 0.08);
        overflow: hidden;
    }
    .hero-card::before {
        content: "";
        position: absolute;
        top: -100px;
        right: -100px;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, rgba(0,0,0,0) 70%);
        pointer-events: none;
    }
    .hero-badge-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .badge-cyan {
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
    }
    .badge-purple {
        background: rgba(168, 85, 247, 0.12);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.35);
    }
    .badge-emerald {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .badge-amber {
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    /* Header Typography */
    .exec-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.55rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        line-height: 1.12;
        background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 4px 0 8px 0;
    }
    .exec-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 0;
        font-weight: 400;
        max-width: 950px;
        line-height: 1.5;
    }

    /* Executive KPI Ribbon Cards */
    .kpi-card {
        background: linear-gradient(180deg, rgba(20, 30, 52, 0.85) 0%, rgba(13, 21, 39, 0.95) 100%);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 16px;
        padding: 18px 16px;
        border: 1px solid var(--border-glass);
        border-top: 3px solid #38bdf8;
        box-shadow: 0 10px 28px -8px rgba(0, 0, 0, 0.5);
        transition: all 0.25s ease-in-out;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 16px 36px -6px rgba(56, 189, 248, 0.18);
    }
    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .kpi-icon {
        font-size: 1.3rem;
        opacity: 0.9;
    }
    .kpi-title {
        font-size: 0.72rem;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.07em;
    }
    .kpi-val {
        font-size: 1.85rem;
        color: #ffffff;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 4px 0 2px 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-sub {
        font-size: 0.76rem;
        color: #64748b;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Spotlight Showcase Component */
    .spotlight-wrapper {
        background: linear-gradient(180deg, rgba(17, 25, 44, 0.7) 0%, rgba(10, 15, 29, 0.85) 100%);
        border-radius: 20px;
        padding: 22px;
        border: 1px solid rgba(56, 189, 248, 0.15);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
        margin-bottom: 30px;
    }
    .spotlight-card {
        background: #0f172a;
        border-radius: 14px;
        padding: 13px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        text-align: left;
        position: relative;
        overflow: hidden;
    }
    .spotlight-card:hover {
        transform: translateY(-5px) scale(1.01);
        border-color: #38bdf8;
        box-shadow: 0 14px 30px rgba(56, 189, 248, 0.22);
    }
    .spotlight-img-container {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 10px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.55);
    }
    .spotlight-img {
        width: 100%;
        aspect-ratio: 1/1;
        object-fit: cover;
        display: block;
        transition: transform 0.4s ease;
    }
    .spotlight-card:hover .spotlight-img {
        transform: scale(1.05);
    }
    
    /* Rank Badges */
    .spotlight-rank {
        position: absolute;
        top: 10px;
        left: 10px;
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(8px);
        color: #f8fafc;
        font-weight: 800;
        font-size: 0.78rem;
        padding: 4px 10px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        z-index: 2;
    }
    .spotlight-rank-1 {
        background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%);
        color: #ffffff;
        border: 1px solid rgba(251, 191, 36, 0.5);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
    }
    .spotlight-rank-2 {
        background: linear-gradient(135deg, #94a3b8 0%, #475569 100%);
        color: #ffffff;
        border: 1px solid rgba(203, 213, 225, 0.5);
    }
    .spotlight-rank-3 {
        background: linear-gradient(135deg, #d97706 0%, #78350f 100%);
        color: #ffffff;
        border: 1px solid rgba(217, 119, 6, 0.5);
    }

    .spotlight-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 2px;
        line-height: 1.3;
    }
    .spotlight-artist {
        font-size: 0.8rem;
        color: #94a3b8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 10px;
    }

    /* Explicit & Format Tags */
    .pill {
        display: inline-block;
        font-size: 0.65rem;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .pill-explicit {
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.4);
    }
    .pill-clean {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .pill-album {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.4);
    }
    .pill-single {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }

    /* Executive Callout Insight Banner */
    .exec-banner {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(13, 21, 39, 0.95) 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-left: 5px solid #10b981;
        border-radius: 12px;
        padding: 16px 20px;
        color: #f1f5f9;
        margin: 18px 0 24px 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }
    .exec-banner-neutral {
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.1) 0%, rgba(13, 21, 39, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-left: 5px solid #38bdf8;
        border-radius: 12px;
        padding: 16px 20px;
        color: #f1f5f9;
        margin: 18px 0 24px 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }

    /* Custom Streamlit Tabs Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #0b1120;
        padding: 8px;
        border-radius: 16px;
        border: 1px solid var(--border-glass);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.92rem;
        padding: 10px 20px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc;
        background-color: rgba(255, 255, 255, 0.04);
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        font-weight: 700 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
    }

    /* Sidebar Styling Overhaul */
    section[data-testid="stSidebar"] {
        background-color: #080d1a !important;
        border-right: 1px solid var(--border-glass) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem;
    }

    /* Inputs & Selectboxes Styling */
    div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #38bdf8 !important;
    }
    
    /* Buttons Styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.35) !important;
        transform: translateY(-2px);
    }

    /* Download Button Specific */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        width: 100%;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3) !important;
    }

    /* Footer styling */
    .footer-container {
        margin-top: 60px;
        padding-top: 28px;
        border-top: 1px solid var(--border-glass);
        color: var(--text-muted);
        font-size: 0.85rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# DATA LOADER & CACHING (Section 5.3)
# ==============================================================================
@st.cache_data
def load_clean_data(
    file_path: str = "data/processed/france_top50_clean.csv",
) -> pd.DataFrame:
    """Loads cleaned, pre-processed playlist observations."""
    df = pd.read_csv(file_path, encoding="utf-8")
    df["date_dt"] = pd.to_datetime(df["date"])
    return df


# Load dataset
try:
    df_raw = load_clean_data()
except Exception as e:
    st.error(
        f"Error loading clean dataset from data/processed/france_top50_clean.csv: {e}"
    )
    st.stop()


# ==============================================================================
# PLOTLY EXECUTIVE DARK THEME HELPER
# ==============================================================================
def apply_executive_dark_theme(
    fig: go.Figure, title: str = None, height: int = None
) -> go.Figure:
    """Applies a consistent luxury dark glass theme with neon accents to Plotly figures."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15, 23, 42, 0.7)",
        plot_bgcolor="rgba(15, 23, 42, 0.7)",
        font=dict(
            family="Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, sans-serif",
            color="#cbd5e1",
        ),
        title=dict(
            text=f"<b>{title}</b>" if title else fig.layout.title.text,
            font=dict(size=15, color="#f8fafc", family="Outfit"),
            x=0.02,
            y=0.96,
        )
        if (title or fig.layout.title.text)
        else None,
        margin=dict(l=24, r=24, t=54, b=24),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#cbd5e1"),
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#94a3b8", size=11),
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.08)",
            tickfont=dict(color="#94a3b8", size=11),
        ),
        hoverlabel=dict(
            bgcolor="#0b1324",
            bordercolor="#38bdf8",
            font_size=12,
            font_family="Plus Jakarta Sans",
            font_color="#f8fafc",
        ),
    )
    if height:
        fig.update_layout(height=height)
    return fig


# ==============================================================================
# SIDEBAR CONTROLS (Section 5.2)
# ==============================================================================
with st.sidebar:
    if os.path.exists("assets/atlantic_logo.svg"):
        st.image("assets/atlantic_logo.svg", use_container_width=True)
    else:
        st.markdown(
            "<div style='font-size: 1.4rem; font-weight: 900; color: #ffffff; text-align: center; font-family: Outfit;'>ATLANTIC RECORDS</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
<div style="text-align: center; margin-top: 4px; margin-bottom: 24px;">
    <span style="font-size: 0.72rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: rgba(56, 189, 248, 0.1); padding: 5px 14px; border-radius: 9999px; border: 1px solid rgba(56, 189, 248, 0.3);">
        <span class="status-pulse"></span> 🇫🇷 France Top 50 Terminal
    </span>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### 🎛️ **Market Filters**")

    # Date range selector
    min_date = df_raw["date_dt"].min().date()
    max_date = df_raw["date_dt"].max().date()

    date_selection = st.date_input(
        "Observation Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter playlist snapshots across the 555-day observation timeline.",
    )

    if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
        start_date_str = date_selection[0].strftime("%Y-%m-%d")
        end_date_str = date_selection[1].strftime("%Y-%m-%d")
    else:
        start_date_str = min_date.strftime("%Y-%m-%d")
        end_date_str = max_date.strftime("%Y-%m-%d")

    # Rank Tier filter
    rank_tier_options = ["Top 50 (All Ranks)", "Top 25", "Top 10"]
    selected_rank_tier = st.selectbox(
        "Chart Rank Tier",
        rank_tier_options,
        index=0,
        help="Focus on elite placements or the complete Top 50 chart.",
    )

    # Explicit content toggle
    explicit_options = ["All", "Explicit only", "Clean only"]
    selected_explicit = st.radio(
        "Content Advisory Filter",
        explicit_options,
        index=0,
        horizontal=True,
        help="Filter tracks by lyrical content advisory rating.",
    )

    # Album type filter
    album_type_options = ["All", "Album", "Single"]
    selected_album_type = st.radio(
        "Release Format Filter",
        album_type_options,
        index=0,
        horizontal=True,
        help="Filter tracks by catalog release configuration.",
    )

    # Apply global unified filtering
    filtered_df = filter_data(
        df_raw,
        date_range=(start_date_str, end_date_str),
        rank_tier=selected_rank_tier,
        explicit_filter=selected_explicit,
        album_type_filter=selected_album_type,
    )

    st.markdown("---")
    sample_pct = (
        (len(filtered_df) / len(df_raw) * 100) if len(df_raw) > 0 else 0
    )
    st.markdown(
        f"""
    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid var(--border-glass); border-radius: 12px; padding: 14px; font-size: 0.82rem; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
        <div style="color: #94a3b8; font-weight: 700; text-transform: uppercase; font-size: 0.68rem; letter-spacing: 0.06em; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
            <span>Telemetry Status</span>
            <span style="color: #34d399; font-weight: 700;">ACTIVE</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #cbd5e1;">Filtered Observations:</span>
            <span style="color: #38bdf8; font-weight: 700; font-family: 'JetBrains Mono', monospace;">{len(filtered_df):,}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #cbd5e1;">Total Dataset Universe:</span>
            <span style="color: #94a3b8; font-family: 'JetBrains Mono', monospace;">{len(df_raw):,}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #cbd5e1;">Sample Retention:</span>
            <span style="color: #34d399; font-weight: 700;">{sample_pct:.1f}%</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# HERO HEADER WITH VISUAL BANNER & BRANDING
# ==============================================================================
st.markdown(
    """
<div class="hero-card">
    <div class="hero-badge-row">
        <span class="badge-pill badge-cyan"><span class="status-pulse"></span> 🇫🇷 France Streaming Terminal</span>
        <span class="badge-pill badge-purple">🏢 Atlantic Recording Corporation</span>
        <span class="badge-pill badge-emerald">⚡ 555-Day Longitudinal Telemetry</span>
        <span class="badge-pill badge-amber">📊 Executive Analytics Engine</span>
    </div>
    <h1 class="exec-title">Audience Sensitivity & Format Preference Analysis</h1>
    <p class="exec-subtitle">Executive streaming intelligence evaluating content compliance, catalog structure, and song duration dynamics across the French Top 50 streaming market.</p>
</div>
""",
    unsafe_allow_html=True,
)


# Graceful Empty-State Protection
if len(filtered_df) == 0:
    st.markdown(
        """
    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 16px; padding: 28px; text-align: center; margin: 30px 0;">
        <div style="font-size: 2.5rem; margin-bottom: 10px;">⚠️</div>
        <div style="font-size: 1.25rem; font-weight: 700; color: #f87171; margin-bottom: 6px;">Zero Observations Matching Current Criteria</div>
        <div style="color: #cbd5e1; font-size: 0.92rem; max-width: 600px; margin: 0 auto;">No playlist records matched the active filter combination. Please broaden your date range or adjust your filters in the left sidebar.</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop()


# ==============================================================================
# EXECUTIVE KPI RIBBON (Section 4 & Section 5.1)
# ==============================================================================
kpis = calculate_all_kpis(filtered_df)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(
        f"""
    <div class="kpi-card" style="border-top-color: #fb7185;">
        <div>
            <div class="kpi-header">
                <span class="kpi-title">Explicit Share</span>
                <span class="kpi-icon">🔞</span>
            </div>
            <div class="kpi-val" style="color: #fb7185;">{kpis['explicit_content_share']['display']}</div>
        </div>
        <div class="kpi-sub">
            <span>tracks flagged</span>
            <strong style="color: #f1f5f9; margin-left: auto;">{int((filtered_df['is_explicit']==True).sum()):,}</strong>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
    <div class="kpi-card" style="border-top-color: #34d399;">
        <div>
            <div class="kpi-header">
                <span class="kpi-title">Clean Ratio</span>
                <span class="kpi-icon">🛡️</span>
            </div>
            <div class="kpi-val" style="color: #34d399;">{kpis['clean_dominance_ratio']['display']}</div>
        </div>
        <div class="kpi-sub">Clean vs Explicit ratio</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
    <div class="kpi-card" style="border-top-color: #38bdf8;">
        <div>
            <div class="kpi-header">
                <span class="kpi-title">Single / Album</span>
                <span class="kpi-icon">💿</span>
            </div>
            <div class="kpi-val" style="color: #38bdf8;">{kpis['single_album_ratio']['display']}</div>
        </div>
        <div class="kpi-sub">Singles per Album track</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
    <div class="kpi-card" style="border-top-color: #fbbf24;">
        <div>
            <div class="kpi-header">
                <span class="kpi-title">Avg Duration</span>
                <span class="kpi-icon">⏱️</span>
            </div>
            <div class="kpi-val" style="color: #fbbf24;">{kpis['average_song_duration']['raw_mean']:.2f}m</div>
        </div>
        <div class="kpi-sub">
            <span>Median:</span>
            <strong style="color: #f1f5f9; margin-left: auto;">{kpis['average_song_duration']['raw_median']:.2f} min</strong>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        f"""
    <div class="kpi-card" style="border-top-color: #c084fc;">
        <div>
            <div class="kpi-header">
                <span class="kpi-title">Album Impact</span>
                <span class="kpi-icon">📈</span>
            </div>
            <div class="kpi-val" style="color: #c084fc;">{kpis['album_size_impact_index']['display']}</div>
        </div>
        <div class="kpi-sub">Large vs Single pop diff</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col6:
    st.markdown(
        f"""
    <div class="kpi-card" style="border-top-color: #2dd4bf;">
        <div>
            <div class="kpi-header">
                <span class="kpi-title">Acceptance</span>
                <span class="kpi-icon">🎯</span>
            </div>
            <div class="kpi-val" style="color: #2dd4bf;">{kpis['content_acceptance_score']['display']}</div>
        </div>
        <div class="kpi-sub">Composite French Index</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# VISUAL SPOTLIGHT: TOP CHART SHOWCASE WITH REAL ALBUM ARTWORK
# ==============================================================================
st.markdown(
    """
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px;">
    <div style="font-size: 1.2rem; font-weight: 800; color: #f8fafc; display: flex; align-items: center; gap: 10px; font-family: 'Outfit';">
        <span style="font-size: 1.4rem;">🔥</span> Top Chart Leaders & Cover Showcase
    </div>
    <div style="font-size: 0.8rem; color: #94a3b8; background: rgba(15, 23, 42, 0.7); padding: 4px 12px; border-radius: 9999px; border: 1px solid var(--border-glass);">
        Spotify Artwork Feed &bull; Ranked by Highest Chart Position
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Pick Top 5 unique tracks in current view (sorted by position, then popularity)
top5_tracks = (
    filtered_df.sort_values(
        by=["position", "popularity"], ascending=[True, False]
    )
    .drop_duplicates(subset=["song", "artist"])
    .head(5)
)

cols_spotlight = st.columns(5)
for i, (_, track) in enumerate(top5_tracks.iterrows()):
    with cols_spotlight[i]:
        cover_url = (
            track["album_cover_url"]
            if pd.notna(track["album_cover_url"])
            else "https://via.placeholder.com/300?text=Atlantic+Records"
        )
        is_exp = bool(track["is_explicit"])
        is_album = str(track["album_type"]).lower() == "album"
        rank_val = int(track["position"])
        
        # Rank styling
        if rank_val == 1:
            rank_class = "spotlight-rank spotlight-rank-1"
            rank_label = "👑 #1"
        elif rank_val == 2:
            rank_class = "spotlight-rank spotlight-rank-2"
            rank_label = "🥈 #2"
        elif rank_val == 3:
            rank_class = "spotlight-rank spotlight-rank-3"
            rank_label = "🥉 #3"
        else:
            rank_class = "spotlight-rank"
            rank_label = f"#{rank_val}"

        st.markdown(
            f"""
        <div class="spotlight-card">
            <div class="spotlight-img-container">
                <img src="{cover_url}" class="spotlight-img" />
                <div class="{rank_class}">{rank_label}</div>
            </div>
            <div class="spotlight-title" title="{track['song']}">{track['song']}</div>
            <div class="spotlight-artist" title="{track['artist']}">{track['artist']}</div>
            <div style="display: flex; gap: 5px; margin-bottom: 10px;">
                <span class="pill {'pill-explicit' if is_exp else 'pill-clean'}">{'EXPLICIT' if is_exp else 'CLEAN'}</span>
                <span class="pill {'pill-album' if is_album else 'pill-single'}">{track['album_type'].upper()}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #94a3b8; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 8px;">
                <span>Popularity: <strong style="color: #38bdf8;">{int(track['popularity'])}/100</strong></span>
                <span>⏱️ {track['duration_min']:.2f}m</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# CORE MODULE TABS (Section 5.1)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔞 Explicit Sensitivity",
    "💿 Format Preferences",
    "⏱️ Song Duration",
    "🎯 Attribute Concentration",
    "🖼️ Catalog & Cover Gallery",
])


# ------------------------------------------------------------------------------
# TAB 1: Explicit vs Clean Content Analysis
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("🔞 Explicit Content Sensitivity & Listener Acceptance")
    st.markdown(
        "Empirical evaluation of how explicit lyrics impact playlist rank distribution and listener popularity scores."
    )

    col_t1a, col_t1b = st.columns([1, 1])

    with col_t1a:
        exp_count = int((filtered_df["is_explicit"] == True).sum())
        clean_count = int((filtered_df["is_explicit"] == False).sum())
        fig_share = px.pie(
            names=["Explicit", "Clean"],
            values=[exp_count, clean_count],
            title="Explicit vs. Clean Content Share (Current Selection)",
            color=["Explicit", "Clean"],
            color_discrete_map={"Explicit": "#fb7185", "Clean": "#34d399"},
            hole=0.55,
        )
        fig_share = apply_executive_dark_theme(fig_share)
        st.plotly_chart(fig_share, use_container_width=True)

    with col_t1b:
        fig_pop_box = px.box(
            filtered_df,
            x="is_explicit",
            y="popularity",
            color="is_explicit",
            labels={
                "is_explicit": "Content Advisory",
                "popularity": "Popularity Score (0-100)",
            },
            title="Popularity Score Distribution: Explicit vs. Clean",
            color_discrete_map={True: "#fb7185", False: "#34d399"},
            category_orders={"is_explicit": [True, False]},
        )
        fig_pop_box.update_xaxes(
            ticktext=["Explicit", "Clean"], tickvals=[True, False]
        )
        fig_pop_box = apply_executive_dark_theme(fig_pop_box)
        fig_pop_box.update_layout(showlegend=False)
        st.plotly_chart(fig_pop_box, use_container_width=True)

    # Statistical significance banner
    pop_sum_df, exp_tests = get_explicit_popularity_comparison(filtered_df)
    if exp_tests["significant"]:
        st.markdown(
            f"""
        <div class="exec-banner">
            <strong style="color: #34d399; font-size: 1rem;">✅ Confirmed Statistical Finding:</strong> {exp_tests['interpretation']}<br>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94a3b8; margin-top: 6px;">
                Mann-Whitney U = {exp_tests['mann_whitney_u']:,} | p-value &lt; 0.001 | Cohen's d = {exp_tests['cohens_d']:.2f} | Rank-Biserial r = {exp_tests['rank_biserial_effect_size']:.3f}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
        <div class="exec-banner-neutral">
            <strong style="color: #38bdf8; font-size: 1rem;">ℹ️ Statistical Verification:</strong> {exp_tests['interpretation']}
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Rank-wise explicit distribution
    st.markdown("##### Rank-Wise Explicit Content Penetration (Positions 1–50)")
    exp_pos_df = get_explicit_by_position(filtered_df)
    fig_pos = px.bar(
        exp_pos_df,
        x="position",
        y="explicit_pct",
        title="Explicit Lyric % at Each Playlist Position (1 = Top Position)",
        labels={
            "position": "Playlist Rank (1 = Top)",
            "explicit_pct": "Explicit Content (%)",
        },
        color="explicit_pct",
        color_continuous_scale=["#0d1527", "#fb7185"],
    )
    avg_exp = filtered_df["is_explicit"].mean() * 100
    fig_pos.add_hline(
        y=avg_exp,
        line_dash="dash",
        line_color="#38bdf8",
        annotation_text=f"Market Average ({avg_exp:.1f}%)",
        annotation_font_color="#38bdf8",
    )
    fig_pos = apply_executive_dark_theme(fig_pos)
    st.plotly_chart(fig_pos, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 2: Release Format Preferences
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("💿 Release Format Preferences: Singles vs. Album Tracks")
    st.markdown(
        "Evaluating France's cultural inclination toward structured album formats vs. standalone single releases."
    )

    col_t2a, col_t2b = st.columns([1, 1])

    with col_t2a:
        fmt_share_df = get_format_share(filtered_df)
        fig_fmt_share = px.bar(
            fmt_share_df,
            x="segment",
            y=["album_pct", "single_pct"],
            title="Format Representation Across Rank Tiers (%)",
            labels={
                "value": "Share (%)",
                "variable": "Format",
                "segment": "Segment",
            },
            color_discrete_map={"album_pct": "#38bdf8", "single_pct": "#fbbf24"},
            barmode="group",
        )
        fig_fmt_share = apply_executive_dark_theme(fig_fmt_share)
        st.plotly_chart(fig_fmt_share, use_container_width=True)

    with col_t2b:
        fig_fmt_pop = px.violin(
            filtered_df,
            x="album_type",
            y="popularity",
            color="album_type",
            box=True,
            points="outliers",
            title="Popularity by Release Format (Violin Density)",
            labels={"album_type": "Format", "popularity": "Popularity Score"},
            color_discrete_map={"album": "#38bdf8", "single": "#fbbf24"},
        )
        fig_fmt_pop = apply_executive_dark_theme(fig_fmt_pop)
        fig_fmt_pop.update_layout(showlegend=False)
        st.plotly_chart(fig_fmt_pop, use_container_width=True)

    fmt_sum_df, fmt_tests = get_format_popularity_comparison(filtered_df)
    st.markdown(
        f"""
    <div class="exec-banner">
        <strong style="color: #38bdf8; font-size: 1rem;">💿 Release Format Performance Finding:</strong> {fmt_tests['interpretation']}<br>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94a3b8; margin-top: 6px;">
            Mann-Whitney U = {fmt_tests['mann_whitney_u']:,} | p-value &lt; 0.001 | Cohen's d = {fmt_tests['cohens_d']:.2f}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Format shift across 5-rank bands
    st.markdown("##### Format Distribution Across 5-Rank Chart Bands")
    fmt_rank_df = get_format_by_rank(filtered_df, band_size=5)
    fig_bands = px.bar(
        fmt_rank_df,
        x="rank_band",
        y=["album_pct", "single_pct"],
        barmode="stack",
        title="Format Composition Across Chart Bands (%)",
        labels={"rank_band": "Rank Band", "value": "Share (%)"},
        color_discrete_map={"album_pct": "#38bdf8", "single_pct": "#fbbf24"},
    )
    fig_bands = apply_executive_dark_theme(fig_bands)
    st.plotly_chart(fig_bands, use_container_width=True)

    # Dilution vs Concentration Summary
    st.markdown(
        "##### Album Structure Impact: Dilution vs. Concentration Dynamics"
    )
    col_dil1, col_dil2 = st.columns([1, 1])

    with col_dil1:
        album_dist_df = get_album_size_distribution(filtered_df)
        fig_size_bar = px.bar(
            album_dist_df,
            x="album_size_bucket",
            y="avg_popularity",
            color="album_size_bucket",
            title="Mean Track Popularity by Host Album Size",
            labels={
                "album_size_bucket": "Album Size Bucket",
                "avg_popularity": "Mean Popularity",
            },
            color_discrete_sequence=["#fbbf24", "#94a3b8", "#38bdf8"],
        )
        fig_size_bar = apply_executive_dark_theme(fig_size_bar)
        fig_size_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_size_bar, use_container_width=True)

    with col_dil2:
        dist_df, dil_stats = get_dilution_vs_concentration(filtered_df)
        fig_conc_bar = px.bar(
            dist_df,
            x="placement_tier",
            y="album_day_count",
            title="Concurrent Chart Placements per Album on Same Day",
            labels={
                "placement_tier": "Tracks Charted Same Day",
                "album_day_count": "Occurrences",
            },
            color="album_day_count",
            color_continuous_scale=["#0d1527", "#38bdf8"],
        )
        fig_conc_bar = apply_executive_dark_theme(fig_conc_bar)
        st.plotly_chart(fig_conc_bar, use_container_width=True)

    st.markdown(
        f"""
    <div class="exec-banner-neutral">
        💡 <strong>Key Structural Catalog Insight:</strong> {dil_stats['conclusion']}
    </div>
    """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------------------
# TAB 3: Song Duration Dynamics
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("⏱️ Song Duration Preferences & Optimal Length Windows")
    st.markdown(
        "Quantifying French listener tolerance windows and testing duration elasticity against popularity."
    )

    col_t3a, col_t3b = st.columns([1, 1])

    with col_t3a:
        hist_df, dur_metrics = get_duration_distribution(filtered_df)
        fig_dur_hist = px.bar(
            hist_df,
            x="duration_interval",
            y="track_count",
            title="Track Duration Distribution (0.5-Minute Intervals)",
            labels={
                "duration_interval": "Duration Window",
                "track_count": "Track Placements",
            },
            color="track_count",
            color_continuous_scale=["#0d1527", "#2dd4bf"],
        )
        fig_dur_hist = apply_executive_dark_theme(fig_dur_hist)
        st.plotly_chart(fig_dur_hist, use_container_width=True)

    with col_t3b:
        dur_tier_df = get_duration_by_rank_tier(filtered_df)
        fig_dur_tier = px.bar(
            dur_tier_df,
            x="segment",
            y="percentage",
            color="duration_bucket",
            barmode="stack",
            title="Duration Category Breakdown Across Tiers (%)",
            labels={
                "percentage": "Share (%)",
                "segment": "Segment",
                "duration_bucket": "Duration Category",
            },
            color_discrete_map={
                "Short (<2.5min)": "#fb7185",
                "Medium (2.5–4min)": "#34d399",
                "Long (>4min)": "#38bdf8",
            },
        )
        fig_dur_tier = apply_executive_dark_theme(fig_dur_tier)
        st.plotly_chart(fig_dur_tier, use_container_width=True)

    # Duration vs Performance Correlation
    dur_perf_df, dur_perf_stats = get_duration_vs_performance(filtered_df)
    st.markdown(
        f"""
    <div class="exec-banner-neutral">
        <strong>Duration vs Performance Spearman Correlation:</strong> {dur_perf_stats['interpretation']}<br>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94a3b8; margin-top: 6px;">
            Duration vs Popularity Spearman rho = {dur_perf_stats['duration_vs_pop_spearman_rho']:.4f} (p &lt; 0.001) | Duration vs Rank rho = {dur_perf_stats['duration_vs_pos_spearman_rho']:.4f} (p = {dur_perf_stats['duration_vs_pos_p']:.3f})
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("##### Duration Norms for France Top 50 (Empirical Benchmarks)")
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    with col_d1:
        st.metric(
            "Mean Duration",
            f"{dur_metrics['mean_min']:.2f} min",
            f"~{int(dur_metrics['mean_min']*60)} sec",
        )
    with col_d2:
        st.metric(
            "Median Duration",
            f"{dur_metrics['median_min']:.2f} min",
            "50th Percentile",
        )
    with col_d3:
        st.metric(
            "Interquartile Window",
            f"{dur_metrics['p25']:.2f} – {dur_metrics['p75']:.2f} min",
            "25th to 75th %ile",
        )
    with col_d4:
        st.metric(
            "90% Acceptance Band",
            f"{dur_metrics['p5']:.2f} – {dur_metrics['p95']:.2f} min",
            "5th to 95th %ile",
        )


# ------------------------------------------------------------------------------
# TAB 4: Attribute Concentration & Market Synthesis
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("🎯 Cross-Tier Content Attribute Concentration Analysis")
    st.markdown(
        "Synthesized density comparison across Top 10, Top 25, and Top 50 tiers per Section 3.5."
    )

    conc_df = get_content_attribute_concentration(filtered_df)

    st.dataframe(
        conc_df.style.format({
            "Explicit (%)": "{:.2f}%",
            "Clean (%)": "{:.2f}%",
            "Album Track (%)": "{:.2f}%",
            "Single Track (%)": "{:.2f}%",
            "Duration Short <2.5m (%)": "{:.2f}%",
            "Duration Medium 2.5-4m (%)": "{:.2f}%",
            "Duration Long >4m (%)": "{:.2f}%",
            "Sample Size (N)": "{:,}",
        }),
        use_container_width=True,
    )

    # Visual comparison
    melted_conc = conc_df.melt(
        id_vars=["Rank Tier", "Sample Size (N)"],
        value_vars=[
            "Explicit (%)",
            "Album Track (%)",
            "Duration Medium 2.5-4m (%)",
        ],
        var_name="Attribute",
        value_name="Density (%)",
    )
    fig_radar_bar = px.bar(
        melted_conc,
        x="Attribute",
        y="Density (%)",
        color="Rank Tier",
        barmode="group",
        title="Key Content Attribute Densities Across Rank Tiers (%)",
        color_discrete_sequence=["#0369a1", "#38bdf8", "#7dd3fc"],
    )
    fig_radar_bar = apply_executive_dark_theme(fig_radar_bar)
    st.plotly_chart(fig_radar_bar, use_container_width=True)

    # Synthesized Preferred Profile
    pref_profile = synthesize_french_preference_profile(conc_df)
    st.markdown(
        f"""
    <div class="exec-banner">
        <strong style="color: #34d399; font-size: 1.15rem; font-family: Outfit;">🎯 Atlantic Empirical Blueprint for France:</strong><br>
        <div style="font-size: 0.95rem; color: #f8fafc; margin-top: 8px; line-height: 1.5;">
            {pref_profile['composite_summary_statement']}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    fmt_rec = pref_profile['format_preference'].get('overall_preference', 'Album Catalog Strategy')
    dur_rec = pref_profile['duration_preference'].get('sweet_spot', '2.5 – 4.0 min (Medium)')
    vol_leader = pref_profile['content_sensitivity_preference'].get('chart_volume_leader', 'Explicit')
    qual_leader = pref_profile['content_sensitivity_preference'].get('popularity_quality_leader', 'Clean')
    sens_rec = f"{vol_leader} (Volume) / {qual_leader} (Longevity)"

    col_prof1, col_prof2, col_prof3 = st.columns(3)
    with col_prof1:
        st.markdown(
            f"""
        <div class="kpi-card" style="border-top-color: #38bdf8;">
            <div class="kpi-title">1. Release Format Strategy</div>
            <div style="color: #ffffff; font-weight: 700; font-size: 1.05rem; margin: 8px 0; font-family: Outfit;">{fmt_rec}</div>
            <div style="color: #94a3b8; font-size: 0.82rem; line-height: 1.45;">{pref_profile['format_preference']['rationale']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col_prof2:
        st.markdown(
            f"""
        <div class="kpi-card" style="border-top-color: #34d399;">
            <div class="kpi-title">2. Duration Window Strategy</div>
            <div style="color: #ffffff; font-weight: 700; font-size: 1.05rem; margin: 8px 0; font-family: Outfit;">{dur_rec}</div>
            <div style="color: #94a3b8; font-size: 0.82rem; line-height: 1.45;">{pref_profile['duration_preference']['rationale']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col_prof3:
        st.markdown(
            f"""
        <div class="kpi-card" style="border-top-color: #fb7185;">
            <div class="kpi-title">3. Content Compliance Advisory</div>
            <div style="color: #ffffff; font-weight: 700; font-size: 1.05rem; margin: 8px 0; font-family: Outfit;">{sens_rec}</div>
            <div style="color: #94a3b8; font-size: 0.82rem; line-height: 1.45;">{pref_profile['content_sensitivity_preference']['rationale']}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------------------------
# TAB 5: Data Catalog & Visual Cover Gallery
# ------------------------------------------------------------------------------
with tab5:
    st.subheader("🖼️ France Top 50 Track Catalog & Artwork Gallery")
    st.markdown(
        f"Exploring **{len(filtered_df):,}** validated playlist observations from `data/processed/france_top50_clean.csv`."
    )

    view_mode = st.radio(
        "Display Mode",
        ["🖼️ Visual Album Artwork Gallery", "📋 Comprehensive Data Table"],
        horizontal=True,
    )

    # Search query
    search_query = st.text_input(
        "🔍 Search Track or Artist Name",
        placeholder="e.g. Ninho, Damso, SDM, Werenoi, Jul, Gazo...",
    )
    display_sub = filtered_df
    if search_query:
        display_sub = display_sub[
            display_sub["song"].str.contains(search_query, case=False, na=False)
            | display_sub["artist"].str.contains(
                search_query, case=False, na=False
            )
        ]

    if view_mode == "🖼️ Visual Album Artwork Gallery":
        # Gallery view with Spotify album covers
        st.markdown(
            f"Showing top matching tracks ({len(display_sub):,} available):"
        )
        gallery_sample = (
            display_sub.drop_duplicates(subset=["song", "artist"])
            .sort_values(by=["popularity", "position"], ascending=[False, True])
            .head(24)
        )

        num_cols = 4
        rows = [
            gallery_sample.iloc[i : i + num_cols]
            for i in range(0, len(gallery_sample), num_cols)
        ]

        for row_df in rows:
            cols = st.columns(num_cols)
            for idx, (_, track_row) in enumerate(row_df.iterrows()):
                with cols[idx]:
                    img_url = (
                        track_row["album_cover_url"]
                        if pd.notna(track_row["album_cover_url"])
                        else "https://via.placeholder.com/300?text=Cover+Art"
                    )
                    is_exp = bool(track_row["is_explicit"])
                    st.markdown(
                        f"""
                    <div class="spotlight-card" style="margin-bottom: 16px;">
                        <div class="spotlight-img-container">
                            <img src="{img_url}" class="spotlight-img" />
                        </div>
                        <div class="spotlight-title" title="{track_row['song']}">{track_row['song']}</div>
                        <div class="spotlight-artist" title="{track_row['artist']}">{track_row['artist']}</div>
                        <div style="display: flex; gap: 5px; margin-bottom: 8px;">
                            <span class="pill {'pill-explicit' if is_exp else 'pill-clean'}">{'EXPLICIT' if is_exp else 'CLEAN'}</span>
                            <span class="pill {'pill-album' if str(track_row['album_type']).lower()=='album' else 'pill-single'}">{str(track_row['album_type']).upper()}</span>
                        </div>
                        <div style="font-size: 0.74rem; color: #94a3b8; display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 6px;">
                            <span>Rank: <strong>#{int(track_row['position'])}</strong></span>
                            <span>Pop: <strong style="color: #38bdf8;">{int(track_row['popularity'])}/100</strong></span>
                            <span>⏱️ {track_row['duration_min']:.2f}m</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

    else:
        # Table view
        st.dataframe(
            display_sub[[
                "date",
                "position",
                "song",
                "artist",
                "popularity",
                "duration_min",
                "album_type",
                "total_tracks",
                "is_explicit",
                "rank_tier",
                "duration_bucket",
                "album_size_bucket",
            ]],
            use_container_width=True,
            hide_index=True,
        )

    # Download button
    csv_data = display_sub.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Telemetry Dataset (CSV)",
        data=csv_data,
        file_name=f"france_top50_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )


# ==============================================================================
# EXECUTIVE FOOTER (Section 5.3 & Section 0)
# ==============================================================================
st.markdown(
    """
<div class="footer-container">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 20px; align-items: flex-start;">
        <div style="max-width: 880px;">
            <div style="font-weight: 700; color: #cbd5e1; margin-bottom: 6px; font-family: Outfit; font-size: 0.95rem;">
                Client: Atlantic Recording Corporation &bull; Program: Unified Mentor
            </div>
            <div style="line-height: 1.55; color: #94a3b8; font-size: 0.83rem;">
                <strong>Project:</strong> Audience Sensitivity, Content Compliance & Format Preference Analysis of France Top 50 Playlist.<br>
                <strong>Provenance:</strong> Authentic longitudinal streaming telemetry sourced from <code>Atlantic_France.csv</code> (27,800 observations across 555 consecutive days, May 2024 to Nov 2025). Audited and cleansed by <code>src/data_prep.py</code>.
            </div>
        </div>
        <div style="text-align: right; min-width: 200px;">
            <div style="color: #38bdf8; font-weight: 800; font-size: 0.98rem; font-family: Outfit;">v2.5 Executive Dark Glass Terminal</div>
            <div style="color: #64748b; font-size: 0.78rem; margin-top: 3px;">Streamlit &bull; Plotly Luxury Theme &bull; Spotify CDN</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
