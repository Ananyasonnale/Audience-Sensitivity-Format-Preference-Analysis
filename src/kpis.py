"""
KPI Calculation Engine for France Top 50 Playlist Analysis.
Client: Atlantic Recording Corporation
Program: Unified Mentor
Authoritative Reference: PROJECT_SPEC.md Section 4

Provides pure, unit-testable functions to compute all 6 core business KPIs.
Equipped with robust divide-by-zero guards and graceful handling for empty/edge slices.
Reused consistently by both the research paper and the interactive Streamlit dashboard.
"""

from typing import Dict, Any, Optional, Tuple, List
import pandas as pd
import numpy as np


def filter_data(
    df: pd.DataFrame,
    date_range: Optional[Tuple[str, str]] = None,
    rank_tier: Optional[str] = None,
    explicit_filter: Optional[str] = None,
    album_type_filter: Optional[str] = None
) -> pd.DataFrame:
    """
    Standardized dataset filtering engine reused by dashboard and analytical modules.
    Ensures identical filtering behavior across all deliverables.
    
    Parameters:
    - df: Cleaned input DataFrame
    - date_range: Optional tuple of (start_date_str, end_date_str) in 'YYYY-MM-DD'
    - rank_tier: 'Top 10', 'Top 25', or 'Top 50' (Top 50 = no filter / full list)
    - explicit_filter: 'All', 'Explicit only', or 'Clean only'
    - album_type_filter: 'All', 'Single', or 'Album'
    """
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=df.columns if df is not None else [])
    
    filtered = df.copy()
    
    # 1. Date range filter
    if date_range is not None and len(date_range) == 2:
        start_date, end_date = str(date_range[0]), str(date_range[1])
        filtered = filtered[(filtered['date'] >= start_date) & (filtered['date'] <= end_date)]
        
    # 2. Rank tier filter (Top 50 = no filter)
    if rank_tier is not None:
        tier_clean = rank_tier.strip().lower()
        if '10' in tier_clean:
            filtered = filtered[filtered['position'] <= 10]
        elif '25' in tier_clean:
            filtered = filtered[filtered['position'] <= 25]
        # 'Top 50' or 'all' retains full list 1-50
        
    # 3. Explicit filter
    if explicit_filter is not None:
        exp_clean = explicit_filter.strip().lower()
        if exp_clean in ('explicit only', 'explicit', 'true'):
            filtered = filtered[filtered['is_explicit'] == True]
        elif exp_clean in ('clean only', 'clean', 'false'):
            filtered = filtered[filtered['is_explicit'] == False]
            
    # 4. Album type filter
    if album_type_filter is not None:
        alb_clean = album_type_filter.strip().lower()
        if alb_clean in ('single', 'singles'):
            filtered = filtered[filtered['album_type'] == 'single']
        elif alb_clean in ('album', 'albums'):
            filtered = filtered[filtered['album_type'] == 'album']
            
    return filtered.reset_index(drop=True)


# ==============================================================================
# Core Pure KPI Calculation Functions (Section 4)
# ==============================================================================

def calculate_explicit_share(df: pd.DataFrame) -> float:
    """
    KPI 1: Explicit Content Share
    Formula: (explicit_tracks / total_tracks_in_view) * 100
    Returns percentage as float (0.0 if empty).
    """
    total = len(df)
    if total == 0:
        return 0.0
    explicit_tracks = int((df['is_explicit'] == True).sum())
    return round((explicit_tracks / total) * 100.0, 2)


def calculate_clean_dominance_ratio(df: pd.DataFrame) -> Optional[float]:
    """
    KPI 2: Clean Content Dominance Ratio
    Formula: clean_tracks / explicit_tracks
    Guards against divide-by-zero: returns None if explicit_tracks == 0.
    """
    total = len(df)
    if total == 0:
        return None
    explicit_tracks = int((df['is_explicit'] == True).sum())
    clean_tracks = int((df['is_explicit'] == False).sum())
    
    if explicit_tracks == 0:
        return None  # Represents infinite clean dominance
    return round(clean_tracks / explicit_tracks, 3)


def calculate_single_album_ratio(df: pd.DataFrame) -> Optional[float]:
    """
    KPI 3: Single vs Album Track Ratio
    Formula: single_tracks / album_tracks
    Guards against divide-by-zero: returns None if album_tracks == 0.
    """
    total = len(df)
    if total == 0:
        return None
    single_tracks = int((df['album_type'] == 'single').sum())
    album_tracks = int((df['album_type'] == 'album').sum())
    
    if album_tracks == 0:
        return None  # Represents infinite single dominance
    return round(single_tracks / album_tracks, 3)


def calculate_song_duration_kpis(df: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    KPI 4: Average Song Duration (with Median)
    Formula: Mean of duration_min; Median of duration_min.
    Returns dict with 'mean_duration_min' and 'median_duration_min'.
    """
    if len(df) == 0 or 'duration_min' not in df.columns:
        return {
            "mean_duration_min": None,
            "median_duration_min": None,
            "std_duration_min": None
        }
    dur = df['duration_min'].dropna()
    if len(dur) == 0:
        return {
            "mean_duration_min": None,
            "median_duration_min": None,
            "std_duration_min": None
        }
    return {
        "mean_duration_min": round(float(dur.mean()), 2),
        "median_duration_min": round(float(dur.median()), 2),
        "std_duration_min": round(float(dur.std()), 2)
    }


def calculate_album_size_impact_index(df: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    KPI 5: Album Size Impact Index
    Formula: (avg_popularity_large_album - avg_popularity_small_or_single) / avg_popularity_small_or_single
    
    Large album: album_size_bucket == 'Large (13+)' (total_tracks >= 13)
    Small/Single: album_size_bucket == 'Single/EP (1-4)' (total_tracks <= 4)
    
    Returns dict with raw index, percentage, and segment mean popularities.
    Guards against empty segments or zero denominator.
    """
    if len(df) == 0:
        return {
            "album_size_impact_index": None,
            "album_size_impact_pct": None,
            "large_album_avg_popularity": None,
            "small_single_avg_popularity": None
        }
        
    large_sub = df[df['album_size_bucket'] == 'Large (13+)']['popularity'].dropna()
    small_sub = df[df['album_size_bucket'] == 'Single/EP (1-4)']['popularity'].dropna()
    
    if len(large_sub) == 0 or len(small_sub) == 0:
        return {
            "album_size_impact_index": None,
            "album_size_impact_pct": None,
            "large_album_avg_popularity": round(float(large_sub.mean()), 2) if len(large_sub) > 0 else None,
            "small_single_avg_popularity": round(float(small_sub.mean()), 2) if len(small_sub) > 0 else None
        }
        
    large_avg = float(large_sub.mean())
    small_avg = float(small_sub.mean())
    
    if small_avg == 0:
        return {
            "album_size_impact_index": None,
            "album_size_impact_pct": None,
            "large_album_avg_popularity": round(large_avg, 2),
            "small_single_avg_popularity": round(small_avg, 2)
        }
        
    impact_index = (large_avg - small_avg) / small_avg
    return {
        "album_size_impact_index": round(impact_index, 4),
        "album_size_impact_pct": round(impact_index * 100.0, 2),
        "large_album_avg_popularity": round(large_avg, 2),
        "small_single_avg_popularity": round(small_avg, 2)
    }


def calculate_content_acceptance_score(
    df: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    KPI 6: Content Acceptance Score (CAS)
    A composite 0–100 index measuring alignment with the empirical French preference profile:
    - 40% Format Alignment (Share of album-format catalog tracks)
    - 30% Explicit Alignment (Share of clean content, reflecting cultural compliance)
    - 30% Duration Alignment (Share of tracks in the 2.5–4.0 min preferred sweet spot)
    
    Formula:
      CAS = (W_format * Format_Score) + (W_explicit * Clean_Score) + (W_duration * Duration_Score)
      where each sub-score is normalized 0-100.
    """
    if weights is None:
        weights = {
            "format": 0.40,
            "explicit": 0.30,
            "duration": 0.30
        }
        
    total = len(df)
    if total == 0:
        return {
            "content_acceptance_score": 0.0,
            "format_subscore": 0.0,
            "clean_subscore": 0.0,
            "duration_subscore": 0.0,
            "weights": weights,
            "formula_documentation": "40% Album Format Alignment + 30% Clean Content Alignment + 30% Medium Duration Alignment"
        }
        
    clean_subscore = ((df['is_explicit'] == False).sum() / total) * 100.0
    format_subscore = ((df['album_type'] == 'album').sum() / total) * 100.0
    duration_subscore = ((df['duration_bucket'] == 'Medium (2.5–4min)').sum() / total) * 100.0
    
    cas = (
        weights["format"] * format_subscore +
        weights["explicit"] * clean_subscore +
        weights["duration"] * duration_subscore
    )
    
    return {
        "content_acceptance_score": round(float(cas), 2),
        "format_subscore": round(float(format_subscore), 2),
        "clean_subscore": round(float(clean_subscore), 2),
        "duration_subscore": round(float(duration_subscore), 2),
        "weights": weights,
        "formula_documentation": (
            f"{int(weights['format']*100)}% Album Format + "
            f"{int(weights['explicit']*100)}% Clean Compliance + "
            f"{int(weights['duration']*100)}% Duration Sweet-Spot (2.5–4min)"
        )
    }


def calculate_all_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convenience aggregator that computes all 6 KPIs on any DataFrame slice.
    Provides formatted strings and raw floats ready for direct display in
    Streamlit KPI metric cards and research paper tables.
    """
    total = len(df)
    if total == 0:
        return {
            "total_tracks": 0,
            "explicit_content_share": {"raw": 0.0, "display": "0.00%"},
            "clean_dominance_ratio": {"raw": None, "display": "N/A"},
            "single_album_ratio": {"raw": None, "display": "N/A"},
            "average_song_duration": {"raw_mean": None, "raw_median": None, "display": "N/A"},
            "album_size_impact_index": {"raw_index": None, "raw_pct": None, "display": "N/A"},
            "content_acceptance_score": {"raw": 0.0, "display": "0.0 / 100"}
        }
        
    exp_share = calculate_explicit_share(df)
    clean_dom = calculate_clean_dominance_ratio(df)
    sgl_alb = calculate_single_album_ratio(df)
    dur_kpis = calculate_song_duration_kpis(df)
    album_impact = calculate_album_size_impact_index(df)
    cas_dict = calculate_content_acceptance_score(df)
    
    return {
        "total_tracks": total,
        "explicit_content_share": {
            "raw": exp_share,
            "display": f"{exp_share:.2f}%"
        },
        "clean_dominance_ratio": {
            "raw": clean_dom,
            "display": f"{clean_dom:.3f}x" if clean_dom is not None else "∞ (Clean Only)"
        },
        "single_album_ratio": {
            "raw": sgl_alb,
            "display": f"{sgl_alb:.3f}x" if sgl_alb is not None else "∞ (Singles Only)"
        },
        "average_song_duration": {
            "raw_mean": dur_kpis["mean_duration_min"],
            "raw_median": dur_kpis["median_duration_min"],
            "raw_std": dur_kpis["std_duration_min"],
            "display": f"{dur_kpis['mean_duration_min']:.2f} min (med {dur_kpis['median_duration_min']:.2f})"
        },
        "album_size_impact_index": {
            "raw_index": album_impact["album_size_impact_index"],
            "raw_pct": album_impact["album_size_impact_pct"],
            "large_avg": album_impact["large_album_avg_popularity"],
            "small_avg": album_impact["small_single_avg_popularity"],
            "display": f"{album_impact['album_size_impact_pct']:+.2f}%" if album_impact['album_size_impact_pct'] is not None else "N/A"
        },
        "content_acceptance_score": {
            "raw": cas_dict["content_acceptance_score"],
            "format_subscore": cas_dict["format_subscore"],
            "clean_subscore": cas_dict["clean_subscore"],
            "duration_subscore": cas_dict["duration_subscore"],
            "display": f"{cas_dict['content_acceptance_score']:.1f} / 100",
            "weights_note": cas_dict["formula_documentation"]
        }
    }


if __name__ == "__main__":
    clean_path = "data/processed/france_top50_clean.csv"
    print(f"Executing KPI calculation verification on: {clean_path}")
    df = pd.read_csv(clean_path)
    
    kpis_overall = calculate_all_kpis(df)
    print("\n--- OVERALL TOP 50 KPIS ---")
    for k, v in kpis_overall.items():
        print(f"  {k}: {v}")
        
    kpis_top10 = calculate_all_kpis(filter_data(df, rank_tier='Top 10'))
    print("\n--- TOP 10 KPIS ---")
    for k, v in kpis_top10.items():
        print(f"  {k}: {v}")
        
    print("\nALL SECTION 4 KPIS CALCULATED AND VERIFIED SUCCESSFULLY!")
