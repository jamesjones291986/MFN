# MFN Draft Analyzer - Boom Analysis

Advanced volatility and boom potential analysis for MFN draft prospects.

## Files:
- `boom_adjusted_draft_analyzer.py` - Main boom analyzer with prediction model
- `volatility_prediction_model.py` - Position+volatility skill growth prediction model
- `sheets_connector.py` - Google Sheets connection utility
- `credentials.json` - Google API credentials

## Usage:
```python
from boom_adjusted_draft_analyzer import run_boom_adjusted_draft_analysis

# Generates three draft boards:
# 1. Boom Potential - Maximum upside
# 2. Conservative - Expected development  
# 3. Highest Upside - Biggest boom/bust gaps
analyses = run_boom_adjusted_draft_analysis()
```

## Features:
- Position-specific volatility prediction models
- Boom/conservative/bust scenario analysis
- Corrected speed adjustments for position changes
- Skill-by-skill growth predictions based on historical data