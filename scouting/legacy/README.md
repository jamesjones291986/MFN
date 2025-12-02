# Legacy Scripts

This directory contains scripts that have been superseded by the new **gameplan generator** and **target analyzer** systems.

## Scripts Moved and Their Replacements

### **Gameplan Generation (Superseded by `gameplan_generator/`)**

- **`automated_scouting.py`** → Replaced by `gameplan_generator/gameplan.py`
  - Old: Manual scouting pipeline with hardcoded logic
  - New: Comprehensive automated gameplan generation with Google Sheets integration

- **`best_defense.py`** → Replaced by `gameplan_generator/automated_gameplan_generator.py`
  - Old: Hardcoded defensive formations and play recommendations
  - New: Dynamic defensive analysis using historical data and adj_ev calculations

- **`best_offense.py`** → Replaced by `gameplan_generator/automated_gameplan_generator.py`
  - Old: Hardcoded offensive formations against specific defenses
  - New: Dynamic offensive counter-analysis based on opponent tendencies

- **`def_scouting.py`** → Replaced by `gameplan_generator/automated_gameplan_generator.py`
  - Old: Manual defensive scouting with hardcoded team lists
  - New: Automated defensive analysis with comprehensive team tendency detection

- **`off_scouting.py`** → Replaced by `gameplan_generator/automated_gameplan_generator.py`
  - Old: Manual offensive scouting with hardcoded team lists
  - New: Automated offensive analysis with comprehensive team tendency detection

### **Target Analysis (Superseded by `gameplan_generator/target_percent/`)**

- **`target_percent.py`** → Replaced by `gameplan_generator/target_percent/target_analyzer.py`
  - Old: Hardcoded play dictionaries with manual analysis
  - New: Dynamic analysis pulling plays from Google Sheets team tabs or standard playbook

- **`targets.py`** → Replaced by `gameplan_generator/target_percent/target_analyzer.py`
  - Old: Basic target analysis functionality
  - New: Comprehensive target percentage analysis with formation grouping

### **Download Systems (Superseded by `season_download/`)**

- **`simple_game_downloader.py`** → Replaced by `season_download/season_downloader.py`
  - Old: Basic game download functionality
  - New: Comprehensive season download with authentication, error handling, and feather compilation

- **`authenticated_downloader.py`** → Replaced by `season_download/season_downloader.py`
  - Old: Basic authenticated download functionality
  - New: Robust authentication with session management and automatic retries

### **Development/Testing Scripts**

- **`test.py`** → No longer needed
  - Development testing script, functionality moved to proper test suites

- **`test_def.py`** → No longer needed
  - Defense-specific testing script, functionality integrated into main gameplan generator

## Key Improvements in New Systems

### **Gameplan Generator Advantages:**
- ✅ **Dynamic Analysis**: Uses real historical data instead of hardcoded values
- ✅ **Google Sheets Integration**: Automatic export and summary tab creation
- ✅ **Comprehensive Coverage**: Handles all personnel groups and formations automatically
- ✅ **Smart Filtering**: Automatically excludes special teams and victory formations
- ✅ **Statistical Rigor**: Uses adj_ev calculations and proper thresholds
- ✅ **Scalable**: Can generate gameplans for any team/league/season combination

### **Target Analyzer Advantages:**
- ✅ **Dynamic Data Sources**: Pulls from Google Sheets instead of hardcoded plays
- ✅ **Formation Grouping**: Properly organizes target analysis by formation
- ✅ **Multiple Modes**: Can analyze individual teams or standard playbook
- ✅ **Clean Interface**: Terminal-only output with clear formatting
- ✅ **Extensible**: Easy to add new data sources or analysis methods

## Migration Date
These scripts were moved to legacy on: **December 1, 2025**

## Preservation Notice
These scripts are preserved for:
- Historical reference
- Understanding legacy analysis methods
- Potential code salvaging if specific functionality is needed
- Educational purposes to show evolution of the analysis system

**Note**: These scripts may have dependencies that are no longer maintained in the main codebase.