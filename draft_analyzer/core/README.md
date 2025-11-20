# MFN Draft Analyzer - Core System

A streamlined draft analysis system for My Football Now (MFN) leagues. Analyzes draft prospects across all positions and creates optimized draft boards.

## 🚀 Quick Start

```bash
# 1. Update data from Google Sheets
python3 update_live_rookies.py

# 2. Run analysis and create your draft tab
python3 multi_position_boom_analyzer.py
```

That's it! Your "Draft-Prioritized Multi-Position Analysis" tab will be created/updated in Google Sheets.

## 📁 Core Files

### Essential Scripts

#### `update_live_rookies.py` ⭐
**Purpose:** Downloads latest draft prospects from Google Sheets  
**What it does:**
- Connects to your Google Sheets draft database
- Finds all rookie/draft-eligible players (Experience = 'R')
- Downloads current and max skill values, volatility, physical stats
- Saves to `live_rookies.csv` for analysis

**When to run:** 
- Before each draft analysis session
- Weekly during draft season  
- After any roster updates in Google Sheets

**Example output:**
```
🔄 UPDATING LIVE ROOKIES DATA
✅ Connected successfully  
✅ Found 324 rookies in 'Player Import'
✅ Successfully updated live_rookies.csv
```

#### `multi_position_boom_analyzer.py` ⭐ 
**Purpose:** Creates your main draft analysis tab
**What it does:**
- Analyzes every prospect at all 21 positions (QB, RB, WR, etc.)
- Uses boom projection model for realistic future ratings
- Applies intelligent filtering (removes low-quality prospects)
- Creates position-prioritized draft board
- Exports to "Draft-Prioritized Multi-Position Analysis" tab in Google Sheets

**Analysis Features:**
- **Multi-position analysis:** Every player tested at every position
- **Speed filtering:** Removes unrealistic 100-speed prospects
- **Position restrictions:** Prevents nonsensical position changes (DT→WR, etc.)
- **Tier-based prioritization:** Skill positions → Premium defense → Linebackers → Offensive line → Specialists
- **Boom projections:** Uses historical data to predict realistic development

**Example output:**
```
🏆 TOP DRAFT PROSPECTS
1   Richard Hamblin    CB   84.3 overall
2   Robert Harris      RB   84.1 overall  
3   Carlos Davila      RB   84.1 overall
4   Charles Clark      QB   82.5 overall
5   Brett Odum         QB   82.3 overall
```

### Supporting Files

#### `proper_boom_projection_model.py`
**Purpose:** Mathematical model for projecting player development
- Uses position-specific algorithms
- Factors in current vs max potential gaps
- Applies volatility-based adjustments
- **Note:** Automatically used by the analyzer (don't run directly)

#### `sheets_connector.py`
**Purpose:** Google Sheets API interface
- Handles authentication
- Manages data import/export
- **Note:** Automatically used by other scripts (don't run directly)

### Data Files

#### `live_rookies.csv`
**Content:** Current draft class data (324+ players)
- All current and max skill values
- Physical attributes (height, weight, speed)
- Volatility ratings
- Position and college information
- **Updated by:** `update_live_rookies.py`

#### `draft_prioritized_analysis.csv`
**Content:** Analysis results from last run
- Complete multi-position analysis for each prospect
- Position ratings, projections, and recommendations
- **Created by:** `multi_position_boom_analyzer.py`

### Configuration

#### `config.py`
**Content:** System settings
- Google Sheets configuration
- Default worksheet names
- API settings

#### `credentials.json`
**Content:** Google Sheets API authentication
- Service account credentials
- Required for Google Sheets access
- **Security:** Keep this file private

## 🎯 Complete Workflow

### First-Time Setup
1. Ensure `credentials.json` is in the core directory
2. Install required packages: `pip install gspread pandas google-auth`

### Regular Usage

#### Weekly Draft Analysis
```bash
# Get latest prospect data
python3 update_live_rookies.py

# Run full analysis  
python3 multi_position_boom_analyzer.py
```

#### Quick Re-analysis (same data)
```bash
# If data hasn't changed, just re-run analysis
python3 multi_position_boom_analyzer.py
```

## 📊 Understanding the Output

### Google Sheets Tab: "Draft-Prioritized Multi-Position Analysis"

**Columns:**
- **Name:** Player name
- **Orig:** Original position 
- **Vol:** Volatility rating (development potential)
- **Best Pos:** Optimal position for this player
- **Best Overall:** Projected rating at best position
- **2nd Pos/3rd Pos:** Alternative position options
- **Speed/Physical:** Key athletic metrics

**Sorting Priority:**
1. **Skill Positions First:** QB, RB, WR, TE, CB, FS, SS (highest draft value)
2. **Premium Defense:** Elite defensive players
3. **Linebackers:** Good value picks
4. **Offensive Line:** Positional needs
5. **Specialists:** Late round/special situations

### Console Output Sections

#### 1. Data Loading
```
✅ Loaded 324 rookies from live_rookies.csv
```

#### 2. Analysis Progress  
```
🔄 Analyzing 324 rookies across all 21 positions...
   Processed 50/324 players...
```

#### 3. Quality Filtering
```
   Filtered out 150 players:
     - K/P specialists below 90 overall
     - DT players below 75 overall
     - Players with unrealistic speed/rating combos
```

#### 4. Top Prospects
```
🏆 TOP DRAFT PROSPECTS (Tier 1: Premium Positions by Overall)
1   Richard Hamblin    CB   84.3 overall
```

#### 5. Position Flexibility
```
🔄 POSITION FLEXIBILITY ANALYSIS
Players with 85+ overall at multiple positions: 6
```

#### 6. Export Confirmation
```
✅ Created new sheet tab: 'Draft-Prioritized Multi-Position Analysis'
```

## ⚠️ Common Issues & Solutions

### "Authentication Error"
- **Problem:** Can't connect to Google Sheets
- **Solution:** Check that `credentials.json` is present and valid

### "No rookies found"  
- **Problem:** `update_live_rookies.py` finds 0 players
- **Solution:** Check that Google Sheets has players with Experience = 'R'

### "Old players in analysis"
- **Problem:** Seeing outdated prospect names
- **Solution:** Run `update_live_rookies.py` first to refresh data

### "Low ratings across the board"
- **Problem:** All prospects show 60-70 overall instead of 80-90s
- **Solution:** This is normal for current draft class vs. historical data

## 🔧 Customization Options

### Modify Filtering Criteria
Edit `multi_position_boom_analyzer.py` lines 200+ to adjust:
- Minimum overall thresholds
- Speed requirements  
- Position restrictions

### Change Export Settings
Edit `multi_position_boom_analyzer.py` lines 400+ to modify:
- Google Sheets tab name
- Column order
- Number of prospects exported

## 🎯 Draft Strategy Integration

### How to Use Results

#### Early Draft (Rounds 1-3)
- Focus on **Skill Positions** section
- Target players with 82+ overall ratings
- Prioritize high-speed prospects (88+ speed)

#### Mid Draft (Rounds 4-6)  
- Look at **Key Defensive** and **Linebackers** sections
- Consider position flexibility (multiple 75+ positions)
- Factor in team needs vs. best player available

#### Late Draft (Rounds 7+)
- **Offensive Line** section for depth
- **Specialists** if you need K/P
- High-volatility prospects (development potential)

#### Position Changes
- Players often project better at different positions
- Trust the analysis - it accounts for physical requirements
- Example: TE → RB for speed, LB → SS for coverage

## 📈 Data Sources

### Google Sheets Integration
- **Sheet ID:** `1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A`
- **Source Worksheet:** "Player Import"  
- **Output Worksheet:** "Draft-Prioritized Multi-Position Analysis"

### Update Frequency
- **Live Data:** Updated when you run `update_live_rookies.py`
- **Historical Model:** Built into `proper_boom_projection_model.py`
- **Weights/Formulas:** Loaded from Google Sheets "Weights" tab

---

## 🤝 Support

For issues:
1. Check that data is current (`update_live_rookies.py`)
2. Verify Google Sheets authentication
3. Review console output for specific errors
4. Check that all core files are present

**File Issues:** All archived scripts are in `../archive/` for reference
- `draft_analyzer.py` - Main analyzer with corrected skill mappings and realistic ratings
- `sheets_connector.py` - Google Sheets connection utility
- `credentials.json` - Google API credentials

## Usage:
```python
from draft_analyzer import FixedMultiPositionAnalyzer

analyzer = FixedMultiPositionAnalyzer("your_sheet_id", verbose=True)
analyzer.load_data()

# Analyze all prospects
for prospect in analyzer.draft_prospects[:10]:
    analysis = analyzer.analyze_player_all_positions_fixed(prospect)
    print(f"{analysis['player_name']}: {analysis['best_current_rating']:.1f} at {analysis['best_position']}")
```

## Features:
- Corrected skill mapping between weights sheet and player data
- Realistic overall ratings (not inflated)
- Position weight and speed adjustments
- Multi-position analysis