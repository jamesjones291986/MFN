# MFN Gameplan Generator

An automated system for generating data-driven defensive gameplans for My Football Now (MFN) leagues.

## 🏈 What It Does

This tool analyzes team offensive tendencies and recommends the best defensive plays to call against them using historical MFN data.

### Key Features
- **Automated Tendency Analysis**: Finds what plays each team calls frequently by formation
- **Data-Driven Recommendations**: Uses 1.7M+ historical plays to determine effective counters
- **Formation-Based Strategy**: Organizes recommendations by personnel groupings (113, 122, etc.)
- **Comprehensive Coverage**: Can generate gameplans for individual teams or entire leagues

## 📁 Project Structure

```
gameplan_generator/
├── gameplan.py              # Main entry point
├── README.md               # This file
├── src/                    # Core functionality
│   └── automated_gameplan_generator.py
├── examples/              # Usage examples
│   └── gameplan_demo.py
├── docs/                  # Documentation
│   └── GAMEPLAN_USAGE.md
└── outputs/              # Generated gameplan files
```

## 🚀 Quick Start

### Generate a Gameplan for One Team
```bash
cd gameplan_generator
python3 gameplan.py --league USFL --season 2011 --team SJS
```

### Generate Gameplans for All Teams
```bash
python3 gameplan.py --league USFL --season 2011 --all-teams
```

### Run the Demo
```bash
python3 examples/gameplan_demo.py
```

## 📖 Documentation

- **[Usage Guide](docs/GAMEPLAN_USAGE.md)** - Comprehensive usage instructions
- **[Examples](examples/)** - Sample scripts and demonstrations

## 🎯 Output Example

```
DEFENSIVE GAMEPLAN: SJS (USFL 2011)
============================================================

113 FORMATION (1RB/1TE/3WR)
----------------------------------------

SJS's Offensive Tendencies:
  • Shotgun Normal HB Flare           63.9% (156 plays)
  • Singleback Slot Strong HB Counter 13.9% (34 plays)

Best Pass Defense (Top 10):
  1. 3-4 Normal OLBs Blitz           ANY/A: 0.84
  2. 3-4 Normal Man Cover 1          ANY/A: 1.14

Best Run Defense (Top 10):
  1. Goal Line Attack #1             YPP: -2.33
  2. Goal Line Attack #3             YPP: -2.26
```

## 🔧 Requirements

- Python 3.7+
- pandas, numpy
- Access to MFN feather data files (in `../feathers/`)
- Access to MFN utility functions (in `../`)

## 💡 Tips

1. **Focus on high-frequency formations** (15%+ usage) for primary gameplan
2. **Use ANY/A for pass defense** (lower is better)
3. **Use YPP for run defense** (lower is better)
4. **Select 3-5 plays per formation** for manageable in-game execution

## 🎮 Integration with MFN

1. Run the generator for your next opponent
2. Review their formation usage and tendencies
3. Select defensive plays based on recommendations
4. Create your in-game defensive gameplan
5. Practice the plays in MFN before the game

## 📊 Data Sources

The system analyzes:
- **1.7M+ historical plays** from multiple MFN leagues
- **Formation/personnel data** for situational analysis
- **Play-by-play results** for effectiveness metrics
- **Expected value calculations** for advanced analytics

---

*Created for the MFN community to automate scouting and gameplan creation.*