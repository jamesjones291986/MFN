# Target Percentage Analyzer

This tool analyzes the target percentages for offensive plays from either team summary tabs or the standard playbook.

## Features

- **Team Analysis**: Analyzes plays from a specific team's summary tab
- **Standard Playbook Analysis**: Analyzes plays from the standard playbook tab  
- **Terminal Output**: Shows results in the terminal (no Google Sheets export)
- **Target Breakdown**: Shows which positions (WR1, WR2, TE1, etc.) get targeted and at what percentages

## Usage

### Analyze a Specific Team

```bash
python target_percent/analyze_targets.py --team SJS --league USFL --season 2018
```

### Analyze Standard Playbook

```bash
python target_percent/analyze_targets.py --standard-playbook
```

## Example Output

```
🎯 TARGET ANALYSIS: SJS (USFL 2018)
============================================================

📋 Reading plays from summary tab: SJS_USFL_2018_Summary
✅ Found 28 offensive plays in SJS_USFL_2018_Summary

📊 TARGET BREAKDOWN:
Based on 28 offensive plays from SJS
----------------------------------------
   WR1:  45%
   TE1:  32%
   WR2:  18%
   RB1:   4%
   WR3:   1%
```

## Requirements

- Google Sheets integration must be working
- Team summary tabs must exist in the Google Sheet
- Standard playbook tab must exist (for --standard-playbook option)
- MFN-Targets.csv file must be present in the scouting directory

## Files

- `target_analyzer.py` - Main analysis script
- `analyze_targets.py` - Wrapper script for easy execution
- `README.md` - This documentation

## Data Sources

The analyzer pulls play data from:

1. **Team Summary Tabs**: Named like `SJS_USFL_2018_Summary`
2. **Standard Playbook Tab**: Named `standard_playbook`

Target percentage data comes from `MFN-Targets.csv` which contains the historical target distribution for each offensive play.