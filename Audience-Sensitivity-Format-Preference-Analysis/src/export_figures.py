"""
Figure Generation Engine for France Top 50 Research Paper Deliverable.
Client: Atlantic Recording Corporation
Program: Unified Mentor
Authoritative Reference: PROJECT_SPEC.md Section 6.1

Generates high-resolution (300 DPI) publication-quality figures corresponding
to each analytical subsection in Section 3 and saves them to deliverables/figures/.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.analysis import (
    get_explicit_share,
    get_explicit_popularity_comparison,
    get_format_share,
    get_format_by_rank,
    get_format_popularity_comparison,
    get_album_size_distribution,
    get_dilution_vs_concentration,
    get_duration_distribution,
    get_duration_by_rank_tier,
    get_content_attribute_concentration
)

# Output directory
FIGURES_DIR = "deliverables/figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Aesthetic palette
COLOR_NAVY = "#1e3a8a"
COLOR_BLUE = "#3b82f6"
COLOR_RED = "#ef4444"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f97316"
COLOR_SLATE = "#64748b"
COLOR_BG = "#f8fafc"

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8


def export_figure_1(df: pd.DataFrame):
    """Figure 1: Explicit Content Sensitivity & Popularity Disparity."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    
    # Panel A: Share by Tier
    share_df = get_explicit_share(df)
    tiers = ['Top 10 (1-10)', 'Top 25 (1-25)', 'Overall (Top 50)']
    sub_share = share_df[share_df['segment'].isin(tiers)].copy()
    sub_share = sub_share.set_index('segment').reindex(tiers).reset_index()
    
    y = np.arange(len(tiers))
    height = 0.35
    
    ax1.barh(y - height/2, sub_share['explicit_pct'], height, label='Explicit Content', color=COLOR_RED, alpha=0.9)
    ax1.barh(y + height/2, sub_share['clean_pct'], height, label='Clean Content', color=COLOR_GREEN, alpha=0.9)
    
    for i in range(len(tiers)):
        ax1.text(sub_share['explicit_pct'].iloc[i] + 1, y[i] - height/2, f"{sub_share['explicit_pct'].iloc[i]:.1f}%", va='center', fontsize=9, fontweight='bold', color=COLOR_RED)
        ax1.text(sub_share['clean_pct'].iloc[i] + 1, y[i] + height/2, f"{sub_share['clean_pct'].iloc[i]:.1f}%", va='center', fontsize=9, fontweight='bold', color=COLOR_GREEN)
        
    ax1.set_yticks(y)
    ax1.set_yticklabels(tiers, fontsize=10, fontweight='bold')
    ax1.set_xlabel("Content Share (%)", fontsize=10, fontweight='bold')
    ax1.set_title("(A) Explicit vs. Clean Content Share Across Tiers", fontsize=11, fontweight='bold', pad=10)
    ax1.set_xlim(0, 80)
    ax1.legend(loc='lower right', frameon=True, facecolor='white')
    ax1.grid(axis='x', linestyle='--', alpha=0.4)
    
    # Panel B: Popularity Comparison
    exp_pop = df[df['is_explicit'] == True]['popularity']
    cln_pop = df[df['is_explicit'] == False]['popularity']
    
    bp = ax2.boxplot(
        [exp_pop, cln_pop],
        tick_labels=['Explicit Tracks', 'Clean Tracks'],
        patch_artist=True,
        widths=0.45,
        medianprops=dict(color='black', linewidth=1.5),
        showmeans=True,
        meanprops=dict(marker='o', markeredgecolor='black', markerfacecolor='white', markersize=6)
    )
    bp['boxes'][0].set_facecolor('#fca5a5')
    bp['boxes'][1].set_facecolor('#a7f3d0')
    
    ax2.text(1, exp_pop.mean() + 2, f"Mean: {exp_pop.mean():.2f}\n(Med: {exp_pop.median():.1f})", ha='center', fontsize=9, fontweight='bold', color='#991b1b')
    ax2.text(2, cln_pop.mean() + 2, f"Mean: {cln_pop.mean():.2f}\n(Med: {cln_pop.median():.1f})", ha='center', fontsize=9, fontweight='bold', color='#065f46')
    
    ax2.set_ylabel("Popularity Score (0–100)", fontsize=10, fontweight='bold')
    ax2.set_title("(B) Listener Popularity by Lyric Sensitivity\n(Mann-Whitney U: p < 0.001, Cohen's d = -0.69)", fontsize=11, fontweight='bold', pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig1_explicit_sensitivity.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Exported: {out_path}")


def export_figure_2(df: pd.DataFrame):
    """Figure 2: Release Format Preferences (Singles vs Album Tracks)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    
    # Panel A: Format share across tiers
    fmt_df = get_format_share(df)
    tiers = ['Top 10 (1-10)', 'Top 25 (1-25)', 'Overall (Top 50)']
    sub_fmt = fmt_df[fmt_df['segment'].isin(tiers)].copy()
    sub_fmt = sub_fmt.set_index('segment').reindex(tiers).reset_index()
    
    x = np.arange(len(tiers))
    width = 0.35
    ax1.bar(x - width/2, sub_fmt['album_pct'], width, label='Album Tracks', color=COLOR_BLUE, alpha=0.9)
    ax1.bar(x + width/2, sub_fmt['single_pct'], width, label='Singles', color=COLOR_ORANGE, alpha=0.9)
    
    for i in range(len(tiers)):
        ax1.text(x[i] - width/2, sub_fmt['album_pct'].iloc[i] + 1, f"{sub_fmt['album_pct'].iloc[i]:.1f}%", ha='center', fontsize=9, fontweight='bold', color=COLOR_BLUE)
        ax1.text(x[i] + width/2, sub_fmt['single_pct'].iloc[i] + 1, f"{sub_fmt['single_pct'].iloc[i]:.1f}%", ha='center', fontsize=9, fontweight='bold', color=COLOR_ORANGE)
        
    ax1.set_xticks(x)
    ax1.set_xticklabels(['Top 10', 'Top 25', 'Overall (Top 50)'], fontsize=10, fontweight='bold')
    ax1.set_ylabel("Format Share (%)", fontsize=10, fontweight='bold')
    ax1.set_title("(A) Album vs. Single Format Composition", fontsize=11, fontweight='bold', pad=10)
    ax1.set_ylim(0, 70)
    ax1.legend(loc='upper right', frameon=True, facecolor='white')
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    
    # Panel B: Format progression across 5-rank bands
    rank_fmt = get_format_by_rank(df, band_size=5)
    r_labels = [f"{i+1}-{i+5}" for i in range(0, 50, 5)]
    r_x = np.arange(len(r_labels))
    
    ax2.plot(r_x, rank_fmt['album_pct'], marker='o', linewidth=2.5, color=COLOR_BLUE, label='Album Tracks (%)')
    ax2.plot(r_x, rank_fmt['single_pct'], marker='s', linewidth=2.5, color=COLOR_ORANGE, label='Singles (%)')
    ax2.axhline(50, linestyle=':', color=COLOR_SLATE, alpha=0.6)
    
    ax2.set_xticks(r_x)
    ax2.set_xticklabels(r_labels, rotation=45, fontsize=9)
    ax2.set_xlabel("Playlist Rank Band", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Share (%)", fontsize=10, fontweight='bold')
    ax2.set_title("(B) Shift in Release Format Composition by Rank Band", fontsize=11, fontweight='bold', pad=10)
    ax2.legend(loc='center right', frameon=True, facecolor='white')
    ax2.grid(True, linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig2_format_preferences.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Exported: {out_path}")


def export_figure_3(df: pd.DataFrame):
    """Figure 3: Album Structure Dilution vs. Concentration Dynamics."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    
    # Panel A: Track Popularity by Album Size Bucket
    size_df = get_album_size_distribution(df)
    order = ['Single/EP (1-4)', 'Standard (5-12)', 'Large (13+)']
    size_df = size_df.set_index('album_size_bucket').reindex(order).reset_index()
    
    bars = ax1.bar(size_df['album_size_bucket'], size_df['avg_popularity'], color=[COLOR_ORANGE, COLOR_SLATE, COLOR_BLUE], width=0.5, alpha=0.9)
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.2f}", ha='center', fontsize=10, fontweight='bold')
        
    ax1.set_ylabel("Mean Track Popularity", fontsize=10, fontweight='bold')
    ax1.set_title("(A) Popularity Dilution in Larger Host Albums\n(Spearman rho = -0.350, p < 0.001)", fontsize=11, fontweight='bold', pad=10)
    ax1.set_ylim(0, 95)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    
    # Annotate dilution gap
    ax1.annotate(
        "-10.83% Dilution",
        xy=(2, 72.32), xytext=(1.2, 85),
        arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
        fontsize=9, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="#fee2e2", ec=COLOR_RED)
    )
    
    # Panel B: Concurrent Album Chart Placements
    dist_df, dil_stats = get_dilution_vs_concentration(df)
    ax2.bar(dist_df['placement_tier'], dist_df['album_day_count'], color=COLOR_NAVY, width=0.5, alpha=0.85)
    
    for i, row in dist_df.iterrows():
        ax2.text(i, row['album_day_count'] + 150, f"{row['album_day_count']:,}\n({row['pct_of_album_days']:.1f}%)", ha='center', fontsize=9, fontweight='bold')
        
    ax2.set_ylabel("Distinct Daily Album Placements", fontsize=10, fontweight='bold')
    ax2.set_title("(B) Concentration: Multi-Track Daily Chart Invasions\n(1,779 days with >= 2 tracks; Peak = 18 concurrent tracks)", fontsize=11, fontweight='bold', pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    ax2.set_ylim(0, max(dist_df['album_day_count']) * 1.2)
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig3_album_structure_dilution_concentration.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Exported: {out_path}")


def export_figure_4(df: pd.DataFrame):
    """Figure 4: Song Duration Preference Distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    
    # Panel A: Overall Duration Histogram
    dur_data = df['duration_min']
    n, bins, patches = ax1.hist(dur_data, bins=35, range=(1.0, 5.5), color=COLOR_BLUE, alpha=0.7, edgecolor='white')
    
    # Highlight 2.5 - 4.0 sweet spot
    for b_left, p in zip(bins[:-1], patches):
        if 2.5 <= b_left < 4.0:
            p.set_facecolor(COLOR_GREEN)
            p.set_alpha(0.85)
            
    ax1.axvline(dur_data.mean(), color=COLOR_NAVY, linestyle='-', linewidth=2, label=f"Mean ({dur_data.mean():.2f} min)")
    ax1.axvline(dur_data.median(), color=COLOR_ORANGE, linestyle='--', linewidth=2, label=f"Median ({dur_data.median():.2f} min)")
    
    ax1.set_xlabel("Song Duration (Minutes)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Track Occurrences", fontsize=10, fontweight='bold')
    ax1.set_title("(A) Track Duration Distribution\n(Green = 2.5–4.0 Min Preferred Window: 81.9% of Tracks)", fontsize=11, fontweight='bold', pad=10)
    ax1.legend(loc='upper right', frameon=True, facecolor='white')
    ax1.grid(True, linestyle='--', alpha=0.4)
    
    # Panel B: Breakdown by rank tier
    tier_dur = get_duration_by_rank_tier(df)
    sub_dur = tier_dur[tier_dur['segment'].isin(['Top 10 (1-10)', 'Top 25 (1-25)', 'Overall (Top 50)'])].copy()
    
    pivot_dur = sub_dur.pivot(index='segment', columns='duration_bucket', values='percentage').reindex(['Top 10 (1-10)', 'Top 25 (1-25)', 'Overall (Top 50)'])
    
    y = np.arange(len(pivot_dur))
    p_short = pivot_dur['Short (<2.5min)']
    p_med = pivot_dur['Medium (2.5–4min)']
    p_long = pivot_dur['Long (>4min)']
    
    ax2.barh(y, p_short, label='Short (<2.5m)', color='#fca5a5', alpha=0.9)
    ax2.barh(y, p_med, left=p_short, label='Medium (2.5-4m)', color=COLOR_GREEN, alpha=0.9)
    ax2.barh(y, p_long, left=p_short+p_med, label='Long (>4m)', color='#93c5fd', alpha=0.9)
    
    for i in range(len(pivot_dur)):
        ax2.text(p_short.iloc[i]/2, y[i], f"{p_short.iloc[i]:.1f}%", va='center', ha='center', fontsize=8, fontweight='bold')
        ax2.text(p_short.iloc[i] + p_med.iloc[i]/2, y[i], f"{p_med.iloc[i]:.1f}%", va='center', ha='center', fontsize=9, fontweight='bold', color='white')
        ax2.text(p_short.iloc[i] + p_med.iloc[i] + p_long.iloc[i]/2, y[i], f"{p_long.iloc[i]:.1f}%", va='center', ha='center', fontsize=8, fontweight='bold')
        
    ax2.set_yticks(y)
    ax2.set_yticklabels(['Top 10', 'Top 25', 'Overall (Top 50)'], fontsize=10, fontweight='bold')
    ax2.set_xlabel("Composition Share (%)", fontsize=10, fontweight='bold')
    ax2.set_title("(B) Duration Category Breakdown by Rank Tier", fontsize=11, fontweight='bold', pad=10)
    ax2.legend(loc='lower right', frameon=True, facecolor='white')
    ax2.set_xlim(0, 100)
    ax2.grid(axis='x', linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig4_duration_dynamics.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Exported: {out_path}")


def export_figure_5(df: pd.DataFrame):
    """Figure 5: Cross-Tier Attribute Concentration Matrix."""
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    
    conc_df = get_content_attribute_concentration(df)
    tiers = conc_df['Rank Tier'].tolist()
    
    attributes = ['Explicit (%)', 'Clean (%)', 'Album Track (%)', 'Single Track (%)', 'Duration Medium 2.5-4m (%)']
    labels = ['Explicit', 'Clean', 'Album Format', 'Single Format', 'Medium Duration (2.5-4m)']
    
    x = np.arange(len(labels))
    width = 0.25
    
    rects1 = ax.bar(x - width, conc_df[conc_df['Rank Tier'] == 'Top 10'][attributes].iloc[0], width, label='Top 10', color=COLOR_NAVY)
    rects2 = ax.bar(x, conc_df[conc_df['Rank Tier'] == 'Top 25'][attributes].iloc[0], width, label='Top 25', color=COLOR_BLUE)
    rects3 = ax.bar(x + width, conc_df[conc_df['Rank Tier'] == 'Top 50'][attributes].iloc[0], width, label='Top 50 (Overall)', color='#93c5fd')
    
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, h + 1, f"{h:.1f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')
            
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold')
    ax.set_ylabel("Density / Concentration (%)", fontsize=10, fontweight='bold')
    ax.set_title("Cross-Tier Content Attribute Concentration Profile (France Top 50)", fontsize=12, fontweight='bold', pad=12)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right', frameon=True, facecolor='white')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    out_path = os.path.join(FIGURES_DIR, "fig5_attribute_concentration.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Exported: {out_path}")


def run_all_exports(clean_path: str = "data/processed/france_top50_clean.csv"):
    df = pd.read_csv(clean_path)
    export_figure_1(df)
    export_figure_2(df)
    export_figure_3(df)
    export_figure_4(df)
    export_figure_5(df)
    print("All 5 publication figures successfully exported to deliverables/figures/!")


if __name__ == "__main__":
    run_all_exports()
