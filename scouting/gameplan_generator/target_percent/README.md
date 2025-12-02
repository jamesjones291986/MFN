# Target Percentage Analyzer

This tool analyzes the target percentages for offensive plays from either team summary tabs or the standard playbook.

## Features

- **Team Analysis**: Analyzes plays from a specific team's summary tab
- **Standard Playbook Analysis**: Analyzes plays from the standard playbook tab  
- **Terminal Output**: Shows results in the terminal (no Google Sheets export)
- **Target Breakdown**: Shows which positions (WR1, WR2, TE1, etc.) get targeted and at what percentages
- **Formation Grouping**: Groups results by formation like the original target_percent.py script

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

📊 TARGET BREAKDOWN BY FORMATION:
Based on 30 offensive plays from SJS
============================================================

2RB/1TE/2WR:
  Total for TE1 is 149
  Total for WR1 is 114
  Total for WR2 is 107
  Total for RB1 is 66
  Total for FB1 is 55

1RB/1TE/3WR:
  Total for RB1 is 135
  Total for WR2 is 98
  Total for WR3 is 67
  Total for TE1 is 59
  Total for WR1 is 32
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