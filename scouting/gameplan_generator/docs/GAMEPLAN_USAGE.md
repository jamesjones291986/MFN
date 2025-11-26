# Automated Gameplan Generator Usage Guide

## Overview

The Automated Gameplan Generator analyzes team offensive tendencies and recommends the best defensive plays to call against them, using historical MFN data for accuracy.

## What It Does

1. **Analyzes Team Tendencies**: Finds what plays each team calls frequently by formation/personnel
2. **Finds Counter-Plays**: Uses 1.7M+ historical plays to determine which defensive plays are most effective
3. **Generates Gameplans**: Provides top defensive recommendations organized by formation
4. **Handles All Teams**: Can generate gameplans for entire leagues at once

## Quick Start

### Single Team Gameplan
```bash
python3 automated_gameplan_generator.py --league USFL --season 2011 --team SJS
```

### All Teams in League/Season
```bash
python3 automated_gameplan_generator.py --league USFL --season 2011 --all-teams
```

### Custom Settings
```bash
python3 automated_gameplan_generator.py --league USFL --season 2011 --team SJS \
    --threshold 2.5 \
    --top-plays 20 \
    --output my_gameplan.txt
```

## Parameters

- `--league`: League name (USFL, qad, xfl, etc.)
- `--season`: Season year
- `--team`: Specific team acronym (optional if using --all-teams)
- `--all-teams`: Generate for all teams in league/season
- `--threshold`: Minimum percentage for plays to be considered (default: 2.0%)
- `--top-plays`: Number of defensive plays to recommend (default: 30)
- `--output`: Custom output file path

## Output Format

The gameplan shows:

### Team Tendencies by Formation
```
113 FORMATION (1RB/1TE/3WR)
SJS's Offensive Tendencies:
  • Shotgun Normal HB Flare           63.9% (156 plays)
  • Singleback Slot Strong HB Counter 13.9% (34 plays)
```

### Defensive Recommendations
```
Best Pass Defense (Top 10):
  1. 3-4 Normal OLBs Blitz           ANY/A: 0.84
  2. 3-4 Normal Man Cover 1          ANY/A: 1.14

Best Run Defense (Top 10):
  1. Goal Line Attack #1             YPP: -2.33
  2. Goal Line Attack #3             YPP: -2.26

Best Overall Defense (Top 15):
  1. 3-4 Normal OLBs Blitz           YPP: 3.42
  2. 3-4 Normal Man Cover 1          YPP: 3.58
```

## Formation Codes

- **113**: 1RB/1TE/3WR (most common passing formation)
- **122**: 1RB/2TE/2WR (balanced formation)
- **212**: 2RB/1TE/2WR (I-Formation variants)
- **221**: 2RB/2TE/1WR (power running)
- **203**: 2RB/3WR (spread running)
- **311**: 3RB/1TE/1WR (power formations)
- **104**: 1RB/4WR (spread passing)
- **105**: 5WR (empty backfield)

## Understanding Metrics

### ANY/A (Adjusted Net Yards per Attempt)
- Lower is better for defense
- Accounts for passing yards, TDs, INTs, sacks
- Negative values = defense is winning

### YPP (Yards Per Play)
- Lower is better for defense
- Simple average of yards gained per play
- Negative values = defense is causing losses

## Tips for Usage

### Gameplan Creation Workflow
1. Run script for opponent team
2. Review their top formations and plays
3. Focus on formations they use 15%+ of the time
4. Select 3-5 defensive plays per formation for your gameplan
5. Practice these plays in-game

### Selecting Defensive Plays
- **High-frequency formations**: Use top 3-5 recommended plays
- **Low-frequency formations**: Pick 1-2 plays you're comfortable with
- **Goal line situations**: Always include Goal Line Attack plays
- **Passing downs**: Focus on plays with good ANY/A ratings
- **Running downs**: Focus on plays with low YPP against runs

### Advanced Usage
```python
from automated_gameplan_generator import GameplanGenerator

# Custom analysis
generator = GameplanGenerator(min_play_threshold=4.0, top_plays_limit=25)
gameplan = generator.generate_team_gameplan('USFL', 2011, 'SJS')

# Access raw data for custom analysis
tendencies = generator.analyze_team_tendencies('USFL', 2011, 'SJS')
counters = generator.find_counter_plays(['Shotgun Normal HB Flare'], '1RB/1TE/3WR')
```

## File Locations

- Script: `/Users/jamesjones/projects/mfn/scouting/automated_gameplan_generator.py`
- Demo: `/Users/jamesjones/projects/mfn/scouting/gameplan_demo.py`
- Data: `/Users/jamesjones/projects/mfn/scouting/feathers/`

## Available Leagues & Seasons

The script works with any league/season combination in your feathers directory:
- USFL: 2002-2011, 2017-2018
- qad: 2043-2049
- xfl: 2043-2048
- paydirt: 1996-2002
- moguls: 2042-2047
- And more...

## Troubleshooting

### "No data found" errors
- Check that the league/season/team combination exists
- Verify feather files are in the correct directory
- Ensure team acronym is correct (case-sensitive)

### Memory issues
- The script loads 1.7M+ historical plays for analysis
- Consider using smaller `--top-plays` values for faster processing
- For all-teams analysis, run during off-peak times

### No significant tendencies
- Lower the `--threshold` parameter (try 1.5 or 1.0)
- Some teams may not have enough data or consistent tendencies

## Example Workflow

```bash
# Step 1: Scout your next opponent
python3 automated_gameplan_generator.py --league USFL --season 2011 --team DAL --threshold 3.0

# Step 2: Review the gameplan file
cat gameplan_USFL_2011_DAL.txt

# Step 3: Create your defensive gameplan in-game based on the recommendations
# Step 4: Focus on the formations they use most frequently
```

This tool automates what used to be hours of manual analysis, giving you data-driven defensive recommendations for every opponent!