# DATASET PROVENANCE & SOURCING NOTES

**File:** `data/raw/france_top50.csv`  
**Client:** Atlantic Recording Corporation  
**Program:** Unified Mentor  
**Project:** Audience Sensitivity, Content Compliance & Format Preference Analysis of France Top 50 Playlist  
**Date Sourced:** September 2026 (Historical range: 2024-05-18 to 2025-11-27)

---

## 1. Provenance & Sourcing Logic

In accordance with **Section 1.2 (Data sourcing logic)** of `PROJECT_SPEC.md`:

```
IF a file matching data/*.csv (or data/raw/*.csv) already exists with these columns:
    → use it as-is, proceed to Section 2 (Data Validation)
ELSE:
    → generate a synthetic dataset that mimics 90 consecutive days of a real
      France Top 50 (Spotify-style) playlist, saved to data/raw/france_top50.csv
```

- **Source File:** An authentic client dataset (`Atlantic_France.csv`) was provided directly at the workspace root during project handoff.
- **Action Taken:** Per the sourcing condition above, because the real dataset already exists and contains all 10 authoritative columns matching Section 1.1, the file was ingested and copied to `data/raw/france_top50.csv` as-is.
- **Synthetic Status:** **Not Synthetic (Real Data)**. No synthetic generation was required or performed. Real Spotify/Atlantic streaming playlist observations are utilized throughout this project.

---

## 2. Schema Verification

The ingested dataset strictly complies with the schema defined in Section 1.1 of `PROJECT_SPEC.md`:

| Column | Observed Type | Section 1.1 Specified Type | Status | Description |
|---|---|---|---|---|
| `date` | `object` (`DD-MM-YYYY`) | date | Compliant | Date of playlist snapshot |
| `position` | `int64` (1–50) | int (1–50) | Compliant | Playlist rank |
| `song` | `object` (string) | string | Compliant | Song title |
| `artist` | `object` (string) | string | Compliant | Artist(s) name |
| `popularity` | `int64` (0–100) | int (0–100) | Compliant | Track popularity score |
| `duration_ms` | `int64` | int | Compliant | Duration in milliseconds |
| `album_type` | `object` (categorical) | categorical | Compliant | Release format (`album`, `single`, `compilation`) |
| `total_tracks` | `int64` | int | Compliant | Track count of host album |
| `is_explicit` | `bool` | boolean | Compliant | Explicit lyric indicator |
| `album_cover_url` | `object` (URL) | string (URL) | Compliant | Authentic CDN artwork URL (`https://i.scdn.co/...`) |

---

## 3. Preliminary Profile & Quality Observations

A preliminary audit of `data/raw/france_top50.csv` reveals the following baseline metrics:

- **Total Records:** 27,800 rows
- **Unique Dates:** 555 distinct daily snapshots
- **Temporal Coverage:** 18-05-2024 (May 18, 2024) to 27-11-2025 (November 27, 2025)
- **Snapshot Integrity:**
  - 554 dates have exactly 50 entries.
  - 1 date (`01-03-2025`) contains 100 entries (double capture anomaly to be reconciled during Section 2 Data Validation).
- **Format Breakdown:**
  - `album`: 14,695 tracks (52.86%)
  - `single`: 13,096 tracks (47.11%)
  - `compilation`: 9 tracks (0.03%) — to be standardized in Section 2
- **Explicit Content Distribution:**
  - `True` (Explicit): 15,640 tracks (56.26%)
  - `False` (Clean): 12,160 tracks (43.74%)
- **Track Popularity:**
  - Minimum: 0
  - Maximum: 100
  - Mean: 76.65
- **Track Duration:**
  - Minimum: 0 ms (corrupted edge case)
  - Maximum: 547,413 ms (~9.12 min)
  - Mean: 185,474.8 ms (~3.09 min / 3:05)
- **Missing Value Count:**
  - Exactly 1 row with missing `song` title (`index 13001`, date `02-02-2025`, position `2`, artist `Lavern`, `duration_ms = 0`, `popularity = 0`), which will be quarantined to `data/processed/excluded_rows.csv` during Section 2.

---

## 4. Next Step Handoff

With the folder structure created and raw dataset acquired and documented, the project is ready for **Section 2: Data Validation & Preparation** (`src/data_prep.py`).
