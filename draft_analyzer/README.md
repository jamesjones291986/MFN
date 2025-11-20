# MFN Draft Analyzer

A comprehensive suite of tools for analyzing draft prospects in My Football Now (MFN) leagues, featuring multi-position analysis, boom/bust projections, and volatility-based player development predictions.

## 📁 Project Structure

```
draft_analyzer/
├── core/                   # Main analysis tools
├── boom_analysis/          # Boom/bust prediction models
├── archive/               # Historical analysis tools
└── README.md             # This file
```

## 🚀 Core Analysis Tools

### Main Scripts

#### `live_rookies_analyzer.py` ⭐ **RECOMMENDED**
**Purpose:** Analyzes current draft prospects using live data from CSV
- **Input:** `live_rookies.csv` (current draft class data)
- **Output:** Multi-position analysis with realistic projections
- **Usage:** `python3 live_rookies_analyzer.py`
- **Best for:** Current draft analysis with up-to-date prospect data

#### `main.py`
**Purpose:** Entry point for draft analysis with customizable options
- **Input:** CSV file with draft prospect data
- **Output:** Draft board in multiple formats (CSV, JSON, HTML)
- **Usage:** `python3 main.py --input-file live_rookies.csv --verbose`
- **Options:**
  - `--position`: Filter by specific position
  - `--top-n`: Number of players to include
  - `--format`: Output format (csv/json/html)

#### `update_live_rookies.py` ⭐ **DATA UPDATE**
**Purpose:** Downloads latest draft prospects from Google Sheets
- **Input:** Google Sheets (Player Import worksheet)
- **Output:** Updated `live_rookies.csv` file
- **Usage:** `python3 update_live_rookies.py`
- **Best for:** Keeping draft data current and accurate

#### `draft_analyzer.py`
**Purpose:** Core analyzer with fixed skill mappings
- **Features:** Corrected skill mapping between weights and player data
- **Output:** Multi-position analysis with conservative projections
- **Best for:** Reliable, tested analysis framework

#### `draft_prioritized_analyzer.py`
**Purpose:** Matches format of original "Draft-Prioritized Multi-Position Analysis" tab
- **Features:** Enhanced ratings with volatility and speed bonuses
- **Output:** Google Sheets export matching original tab format
- **Integration:** Boom analysis predictions

### Specialized Analyzers

#### `enhanced_draft_analyzer.py`
**Purpose:** Enhanced analysis with boom/bust predictions
- **Features:** Position eligibility logic, volatility-based projections
- **Output:** Google Sheets export with enhanced metrics

#### `fixed_projection_analyzer.py`
**Purpose:** Uses maximum potential values for projections
- **Features:** Boom-enhanced skill predictions
- **Output:** "Fixed Projection Board" tab in Google Sheets

#### `simple_enhanced_analyzer.py`
**Purpose:** Simplified boom integration with original analyzer logic
- **Features:** Minimal changes to proven analysis methods
- **Output:** Basic enhanced projections

## 📊 Data Sources & Updates

### Current Data
- **`live_rookies.csv`**: Current draft class with detailed skill data 
  - Contains current and max potential values for all skills
  - Includes volatility ratings and physical attributes
  - **Auto-updated** from Google Sheets using `update_live_rookies.py`

### 🔄 Updating Data
To get the latest draft prospects:

```bash
# Update live_rookies.csv with latest data
python3 update_live_rookies.py

# Then run analysis with fresh data
python3 live_rookies_analyzer.py
```

**When to update:**
- Before each new draft analysis
- When new prospects are added to Google Sheets
- Weekly during draft season
- After any data corrections in the sheets

### Google Sheets Integration
- **Sheet ID:** `1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A`
- **Key Worksheets:**
  - `Weights`: Position weight matrices for skill calculations
  - `Player Import`: Historical player data (324 players)
  - `Players Cur/Max`: Current and maximum skill values
  - `MaxDraft/CurFormulas`: Calculated position ratings

## 🔮 Boom Analysis System

### `boom_analysis/volatility_prediction_model.py`
**Purpose:** Predicts player development patterns using historical data
- **Training Data:** 678 real MFN players (322 pre-draft, 356 post-draft)
- **Analysis:** Position-specific volatility patterns by skill level
- **Output:** Boom/bust predictions with confidence intervals

### Key Features
- **Position-Specific Analysis:** Different volatility patterns by position and skill
- **Historical Patterns:** Based on real player development data
- **Skill-Level Groupings:** Very Low (0-20), Low (21-40), Medium (41-60), High (61-80), Very High (81-100)
- **Boom/Bust Calculations:** Maximum positive and negative skill changes observed

## ⚙️ Configuration

### `config.py`
- Google Sheets API configuration
- Authentication settings
- Default sheet IDs and worksheet names

### `sheets_connector.py`
- Google Sheets API interface
- Authentication handling
- Data import/export functions

## 🎯 Analysis Methods

### Multi-Position Analysis
Each player is analyzed at all 20 positions:
- **Offensive:** QB, RB, FB, TE, WR, LT, LG, C, RG, RT
- **Defensive:** LDE, DT, RDE, LLB, MLB, RLB, LCB, SS, FS, RCB

### Skill Mapping System
Correctly maps position weights to player skills:
```python
'Max Speed': 'MaxSpeed'
'Ball Carrying': 'BallSecurity'  
'Break Tackle': 'BreakTackle'
'M2M Coverage': 'ManCoverage'
'Zone coverage': 'ZoneCoverage'
# ... and 35+ other mappings
```

### Rating Calculations
1. **Current Rating:** Based on current skill values
2. **Max Potential:** Based on maximum skill ceiling
3. **Conservative Projection:** Volatility-adjusted realistic projection
4. **Boom Projection:** Enhanced projection using historical boom patterns

### Speed Adjustments
- Players analyzed at optimal weight for each position
- Speed adjusted based on weight difference (-1 speed per 9.5 lbs)
- Position weight targets (e.g., QB: 225, LT: 315, WR: 200)

## 📈 Draft Strategy Integration

### Position Prioritization
1. **Speed-qualified skill positions** (88+ speed): WR, RB, TE, FS, SS, QB
2. **Speed-qualified premium positions**: QB, LT, RT, LG, RG, C
3. **Non-speed-qualified skill positions**
4. **All other positions by rating**

### Volatility Analysis
- **High Volatility (80+):** High risk/reward players with boom potential
- **Medium Volatility (40-79):** Developmental prospects
- **Low Volatility (0-39):** Safe, predictable players

## 🛠️ Setup & Usage

### Prerequisites
```bash
pip install gspread pandas google-auth google-auth-oauthlib google-auth-httplib2
```

### Authentication
1. Place `credentials.json` (Google Sheets API) in the core directory
2. Run any script to complete OAuth flow
3. `token.json` will be created automatically

### Quick Start
```bash
# Analyze current draft class
python3 live_rookies_analyzer.py

# Full analysis with options
python3 main.py --input-file live_rookies.csv --top-n 50 --verbose

# Export to Google Sheets
python3 draft_prioritized_analyzer.py
```

## 📝 Output Formats

### Console Output
- Ranked draft boards with key metrics
- Position-by-position analysis
- Boom/bust percentages
- Player profiles and classifications

### Google Sheets Export
- **"Enhanced Draft-Prioritized Analysis"**: Main output tab
- **"Fixed Projection Board"**: Max potential analysis
- **"Simple Enhanced Analysis"**: Basic enhanced metrics

### CSV Export
- Structured data for further analysis
- Compatible with external tools
- Customizable column selection

## 🔍 Debugging & Validation

### Test Scripts
- `check_existing_tabs.py`: Analyze Google Sheets structure
- `quick_test.py`: Basic functionality testing

### Validation Features
- Skill mapping verification
- Position eligibility logic
- Rating calculation auditing
- Historical comparison tools

## 📚 Historical Context

### Archive Directory
Contains previous analysis iterations and research:
- Historical boom analysis models
- Experimental projection methods
- Detailed volatility studies
- Player development research

### Key Learnings
1. **Skill Mapping Critical:** Incorrect mappings produce unrealistic results
2. **Position Eligibility:** Defensive players shouldn't move to offensive line
3. **Speed Qualification:** 88+ speed threshold for skill position value
4. **Volatility Impact:** High volatility = high boom potential but also high bust risk

## 🎲 Advanced Features

### Boom Analysis Integration
- Historical pattern recognition
- Position-specific volatility modeling
- Skill-level impact analysis
- Confidence interval predictions

### Enhanced Projections
- Multi-factor volatility bonuses
- Speed qualification bonuses
- Position-specific adjustments
- Risk/reward classifications

### Strategic Insights
- Player profiles and archetypes
- Draft timing recommendations
- Position scarcity analysis
- Development trajectory predictions

---

## 🤝 Contributing

When adding new features:
1. Follow existing code patterns
2. Update this README
3. Add appropriate error handling
4. Test with live_rookies.csv data
5. Validate against historical results

## 📞 Support

For issues or questions:
1. Check the archive for similar implementations
2. Verify Google Sheets authentication
3. Ensure CSV data format matches expected structure
4. Test with known working data (live_rookies.csv)