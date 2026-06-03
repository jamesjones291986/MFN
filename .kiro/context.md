# MFN Analytics Suite

Tools for MyFootballNow (MFN) online football simulation league. Opponent scouting, draft analysis, lineup/gameplan optimization.

## Structure

- `scouting/` — Core analytics: opponent tendency analysis, gameplan generation, schedule processing
  - `main.py` / `run_analysis.py` — Entry points for scouting reports
  - `gameplan_generator/` — Generates offensive/defensive gameplans from scouting data
  - `team_specific_analysis/` — Per-opponent breakdowns
  - Reference CSVs: `MFN Global Reference - DefPlays.csv`, `OffPlays.csv`
- `draft_analyzer/` — Draft value/pick analysis
- `lineup_analyzer/` — Roster optimization
- `other_scripts/` — Misc utilities

## Current Branch: automation-workflow

Active development on automating the scouting/gameplan workflow.

## Key Concepts

- Game logs downloaded from MFN site, parsed into structured data
- Scouting analyzes opponent play-calling tendencies (down/distance, formation, play type frequencies)
- Gameplans output specific defensive/offensive play calls to counter tendencies
- Season data compiled from individual game logs

## Tech Stack

Python, pandas, CSV-based data, Google Sheets integration
