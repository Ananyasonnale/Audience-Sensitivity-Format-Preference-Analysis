# DATA VALIDATION & AUDIT REPORT

**Client:** Atlantic Recording Corporation  
**Program:** Unified Mentor  
**Project:** Audience Sensitivity, Content Compliance & Format Preference Analysis of France Top 50 Playlist  
**Module:** `src/data_prep.py`  
**Generated On:** September 2026

---

## 1. Executive Summary & Definition of Done

This report documents the end-to-end execution of **Section 2 (Data Validation & Preparation)** of `PROJECT_SPEC.md`. Every transformation is fully audited, repeatable, and preserves dataset integrity without silent imputation.

| Metric | Value |
|---|---|
| **Total Rows In (Raw)** | 27,800 |
| **Duplicate Snapshot Entries Removed** | 50 |
| **Corrupted / Invalid Records Excluded** | 1 |
| **Total Rows Excluded to `excluded_rows.csv`** | 51 |
| **Final Clean Row Count** | **27,749** |
| **Clean Date Span** | 2024-05-18 to 2025-11-27 (555 days) |

---

## 2. Row Count & Date Integrity Audit

- **Total Distinct Dates:** 555 daily chart snapshots.
- **Dates with exactly 50 rows:** 554
- **Anomalous Dates Detected:** 1
  - **Date `01-03-2025`:** Contained 100 rows (2 complete sets of positions 1–50).
  - *Investigation:* Audit revealed an overlapping snapshot capture. Block 1 (rows 14350–14399) replicated the previous day's rankings (`28-02-2025`), while Block 2 (rows 14400–14449) captured the updated daily progression aligning with `02-03-2025`.
  - *Resolution:* Position deduplication retaining the latest complete chart snapshot (`keep='last'`) successfully removed the 50 stale duplicate positions.

---

## 3. Duplicate Analysis & Deduplication

- **Duplicate `(date, position)` pairs detected:** 100 rows.
- **Duplicate `(date, song, artist)` pairs detected:** 96 rows.
- **Deduplication Strategy:** Dropped stale duplicate snapshot rows by `(date, position)` keeping `'last'`.
- **Duplicate rows removed:** 50 rows.
- **Remaining duplicates:**
  - Remaining duplicate `(date, position)`: 0
  - Remaining duplicate `(date, song, artist)`: 0

---

## 4. Missing Values & Excluded Records

In accordance with strict compliance rules: *never silently impute `popularity`, `is_explicit`, or `album_type`.*

### Missing Value Scan (Pre-Imputation):
| Column | Missing Count |
|---|---|
| `date` | 0 |
| `position` | 0 |
| `song` | 1 |
| `artist` | 0 |
| `popularity` | 0 |
| `duration_ms` | 0 |
| `album_type` | 0 |
| `total_tracks` | 0 |
| `is_explicit` | 0 |
| `album_cover_url` | 0 |

### Excluded Rows Breakdown:
Total quarantined rows saved to `data/processed/excluded_rows.csv`: **51**.

| Row Index / Date | Position | Artist / Track | Reason for Exclusion |
|---|---|---|---|
| `01-03-2025` | 1 | Werenoi - Pyramide | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 2 | Jungeli & Imen Es & Alonzo - Petit génie | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 3 | Pierre Garnier - Ceux qu'on était | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 4 | Favé - FLASHBACK | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 5 | Dadju & Tayc - I love you | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 6 | Benson Boone - Beautiful Things | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 7 | Gazo & Tiakola - MAMI WATA | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 8 | Werenoi - Tu connais | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 9 | Teddy Swims - Lose Control | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 10 | iñigo quintero - Si No Estás | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 11 | Werenoi - Maudit | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 12 | Dua Lipa - Houdini | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 13 | Werenoi - Laboratoire | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 14 | Soolking & Gazo - Casanova | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 15 | Zola & Koba LaD - Temps en temps | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 16 | Tate McRae - greedy | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 17 | Werenoi - Chemin d'or | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 18 | Booba - Dolce Camara | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 19 | SANTA - Popcorn Salé | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 20 | Kaaris - Panama | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 21 | Ofenbach & Norma Jean Martine - Overdrive (feat. Norma Jean Martine) | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 22 | Werenoi - 16.02.2024 | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 23 | KeBlack - LAISSE MOI | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 24 | Heuss L'enfoiré - Saiyan | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 25 | Werenoi - Dans un verre | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 26 | Beyoncé - TEXAS HOLD 'EM | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 27 | Jeck - Parapluie | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 28 | David Guetta & Kim Petras - When We Were Young (The Logical Song) | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 29 | SDM - Bolide allemand | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 30 | PLK - Ça mène à rien | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 31 | Werenoi - La League | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 32 | Kenya Grace - Strangers | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 33 | Loreen - Is It Love | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 34 | PLK - Faut pas | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 35 | GIMS - LOCO | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 36 | Sia - Gimme Love | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 37 | KeBlack - Aucune attache | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 38 | Kalash Criminel - ENCORE LES PROBLÈMES | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 39 | Werenoi - Solitaire | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 40 | Jul - J'fais plaisir à la zone | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 41 | Tam Sir - Coup du marteau | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 42 | Zaho de Sagazan - La symphonie des éclairs | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 43 | Corneille & Aya Nakamura & Trinix - Avec classe (feat. Aya Nakamura & Trinix) | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 44 | Aya Nakamura - Hypé | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 45 | Kygo & Ava Max - Whatever | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 46 | YG Marley - Praise Jah In The Moonlight | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 47 | Taylor Swift - Cruel Summer | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 48 | Slimane - Mon amour | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 49 | Yamê - Bécane - A COLORS SHOW | Duplicate (date, position) snapshot entry |
| `01-03-2025` | 50 | Werenoi - Vulgaire | Duplicate (date, position) snapshot entry |
| `02-02-2025` | 2 | Lavern - nan | Missing song title (NaN); Corrupted duration (0 ms <= 0) |

*Note:* Row index `13001` (`02-02-2025`, position 2, artist `Lavern`) contained a `NaN` track title, `0` popularity, and `0 ms` duration. It was quarantined to protect the analytical integrity of track-level metrics.

---

## 5. Standardization Decisions

### 5.1 Album Type Standardization
- Applied lowercasing and whitespace stripping.
- Raw distribution: `{'album': 14670, 'single': 13071, 'compilation': 9}`
- **Mapping Decisions:**
  - `single` $\rightarrow$ `single`
  - `album` $\rightarrow$ `album`
  - `compilation` (9 rows) $\rightarrow$ `album`: Tracks from multi-track compilations (e.g., holiday and catalog collections with 13–119 tracks) represent full-length multi-track releases and are mapped to `album` per Section 2 specification.
- Final distribution: `{'album': 14679, 'single': 13071}`
- Unmapped formats: 0

### 5.2 Explicit Flag Validation
- Parsed boolean inputs (`True`, `False`, strings, binary digits).
- Raw distribution: `{'True': 15613, 'False': 12137}`
- Unparseable values: 0 (none required defaulting).
- Clean distribution: `15613` Explicit (56.27%), `12137` Clean (43.74%).

### 5.3 Duration Conversion
- Added `duration_min = duration_ms / 60000.0`, rounded to 2 decimal places.
- Retained original `duration_ms`.
- Mean song duration: `3.09 min` (~185 seconds).
- Median song duration: `3.0 min`.

---

## 6. Type Enforcement & Domain Range Audit

- `date`: Converted from `DD-MM-YYYY` to ISO-8601 `YYYY-MM-DD`.
- `position`: Enforced `int` in domain `[1, 50]`. Observed range: `1–50`.
- `popularity`: Enforced `int` in domain `[0, 100]`. Observed range: `0–100`.
- `total_tracks`: Enforced `int >= 1`. Observed range: `1–119`.
- Out-of-bounds range violations: 0.

---

## 7. Feature Engineering (Derived Columns)

authoritative derived features required by downstream analytics and dashboard modules:

### 7.1 `rank_tier`
- `Top 10` (position $\le$ 10): 5,549 rows
- `Top 25` (11 $\le$ position $\le$ 25): 8,325 rows
- `Top 50` (26 $\le$ position $\le$ 50): 13,875 rows

### 7.2 `duration_bucket`
- `Short (<2.5min)`: 3,517 rows
- `Medium (2.5–4min)`: 22,732 rows
- `Long (>4min)`: 1,500 rows

### 7.3 `album_size_bucket`
- `Single/EP (1-4)`: 12,379 rows
- `Standard (5-12)`: 4,301 rows
- `Large (13+)`: 11,069 rows

---

## 8. Verification Sign-Off

- [x] Clean dataset written to `data/processed/france_top50_clean.csv`.
- [x] Quarantined records logged in `data/processed/excluded_rows.csv`.
- [x] Audit report verified in `data/processed/validation_report.md`.
- [x] Zero unresolved null values in critical columns.
- [x] Ready for downstream analytics in Section 3 (`src/analysis.py`).
