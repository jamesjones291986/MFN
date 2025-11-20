# MFN Lineup Analyzer

Automated position assignment and free agent analysis tools for My Football Now (MFN) leagues.

## Setup

### Prerequisites
- Python 3.11+
- Virtual environment (recommended)
- Google Service Account credentials

### Installation

1. **Activate the virtual environment:**
   ```bash
   cd /Users/jamesjones/projects/mfn
   source venv/bin/activate
   cd lineup_analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets access:**
   - Place your `credentials.json` file in the `lineup_analyzer` directory
   - Ensure your Google Service Account has access to your MFN spreadsheet

## Tools

### 1. Lineup Analyzer (`lineup_analyzer.py`)

Automatically assigns optimal positions to your current roster based on a priority system.

**Features:**
- Assigns 53 roster spots using position priority (WR1 → RB1 → WR2 → TE1, etc.)
- Applies realistic position movement restrictions
- Shows position-specific key skills
- Exports results to Google Sheets

**Usage:**
```bash
python3 lineup_analyzer.py
```

**Google Sheet Requirements:**
- `Player Import` tab: Your current roster data
- `MaxFormulas` tab: Position ratings for all players

### 2. Free Agent Analyzer (`free_agent_analyzer.py`)

Analyzes large pools of available players and identifies the top 5 at each position.

**Features:**
- Analyzes 19 positions (all except K and P)
- Shows top 5 players per position based on position-specific ratings
- Allows duplicates (versatile players appear in multiple lists)
- Exports organized results to Google Sheets

**Usage:**
```bash
python3 free_agent_analyzer.py
```

**Google Sheet Requirements:**
- `Player Import` tab: Free agent player data
- `MaxFormulas` tab: Position ratings for all players

## Configuration

Both tools use the same Google Sheet ID (currently hardcoded):
```
12D_Kxx1hqPgsJ9qQtkY_zAYigGtUnz7F9uznpKK131s
```

### Position Analysis

**Lineup Analyzer Positions:**
- Offense: QB, RB, FB, WR, TE, LT, LG, C, RG, RT
- Defense: LDE, DT, RDE, SLB, MLB, WLB, CB, FS, SS
- Special Teams: K, P

**Free Agent Analyzer Positions:**
- Same as above, excluding K and P (19 positions total)

### Key Skills by Position
- **QB:** Pass Accuracy
- **Skill Positions (RB, FB, WR, TE):** Speed
- **Offensive Line:** Pass Blocking
- **Defensive Line/LB:** Speed (except DT: Strength)
- **Secondary:** Speed
- **Kicker:** Kick Accuracy
- **Punter:** Punt Strength

## Output

Both tools generate:
1. **Console output** with detailed analysis
2. **Google Sheets export** with formatted results and section headers

### Export Tabs
- Lineup Analyzer: `"Optimal Lineup"`
- Free Agent Analyzer: `"Free Agent Analysis"`

## Troubleshooting

### Common Issues

1. **Import errors (numpy/pandas):**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Google Sheets access denied:**
   - Verify `credentials.json` is in the correct location
   - Check that your service account has access to the spreadsheet

3. **Missing data columns:**
   - Ensure your spreadsheet has `Player Import` and `MaxFormulas` tabs
   - Verify column names match expected format

### Dependencies

- `pandas`: Data manipulation and analysis
- `gspread`: Google Sheets API integration
- `google-auth`: Google authentication
- `google-auth-oauthlib`: OAuth2 authentication
- `google-auth-httplib2`: HTTP transport adapter