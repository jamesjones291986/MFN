# MFN Data Analysis Tool

A comprehensive Python toolkit for analyzing game data from My Football Now (MFN) online football simulation leagues.

## Features

- **Automated Data Collection**: Download game logs from multiple MFN leagues
- **Data Processing**: Compile and transform raw game data into analyzable formats
- **Advanced Analytics**: Calculate expected values, analyze play effectiveness, and generate insights
- **Scouting Reports**: Generate detailed team analysis for competitive advantage
- **Best Plays Analysis**: Identify optimal offensive and defensive strategies
- **Multi-League Support**: Analyze data across QAD, XFL, USFL, PFL, and other leagues

## Quick Start

### 1. Installation

```bash
# Clone or download the project
cd mfn

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy and customize the configuration file:

```bash
cp config.yaml config.local.yaml
```

Edit `config.local.yaml` to match your local paths:

```yaml
data:
  root_dir: /your/path/to/game_logs
  feathers_dir: /your/path/to/MFN/feathers
  global_files_dir: /your/path/to/game_logs
```

### 3. Basic Usage

```bash
# List available leagues and seasons
python mfn_cli.py list

# Download data for a specific league/season
python mfn_cli.py download season qad 2049

# Download all available data (takes a while!)
python mfn_cli.py download all

# Generate scouting report
python mfn_cli.py scout qad 2049 TeamName

# Generate gameplan vs opponent
python mfn_cli.py gameplan qad 2049 OpponentTeam

# Generate PERSONNEL-BASED gameplan (advanced)
python mfn_cli.py personnel qad 2049 OpponentTeam

# Check for new seasons automatically
python mfn_cli.py manage check

# Setup auto-downloads for new seasons
python mfn_cli.py manage auto qad xfl pfl

# Run best plays analysis
python mfn_cli.py analyze
```

## Detailed Usage

### Data Collection

The tool supports downloading game logs from multiple MFN leagues:

```bash
# Download specific league/season
python mfn_cli.py download season <league> <season>

# Examples:
python mfn_cli.py download season qad 2049
python mfn_cli.py download season xfl 2048
python mfn_cli.py download season pfl 2029

# Download partial/incomplete seasons (for ongoing seasons)
python mfn_cli.py download season qad 2050 --partial

# Force re-download existing data
python mfn_cli.py download season qad 2049 --force

# Add new league/season not in config
python mfn_cli.py download add newleague 2025 --domain newleague-domain
```

**Supported Leagues:**
- `qad`: QAD Fantasy League (2043-2049)
- `xfl`: XFL (2043-2048) 
- `paydirt`: Paydirt (1996-2002)
- `USFL`: USFL/WFL (2002-2011)
- `moguls`: Moguls (2042-2047)
- `norig`: NORIG (2028-2032)
- `pfl`: PFL (2026-2029)
- `lol`: LOL (2117-2120)
- `nba`: NBA League (2000-2001)

### Data Processing

After downloading, compile the raw game logs into analysis-ready datasets:

```bash
python mfn_cli.py compile <league> <season> --schedule /path/to/schedule.csv
```

### Scouting Reports

Generate detailed team analysis including:
- Offensive play frequency and tendencies
- Defensive scheme preferences  
- Down and distance patterns
- Formation usage

```bash
python mfn_cli.py scout qad 2049 "TeamName"
```

### Best Plays Analysis

Analyze play effectiveness across all data using expected value calculations:

```bash
python mfn_cli.py analyze
```

This generates CSV files with:
- Adjusted expected value by play type
- Yards per play statistics
- Success rates and efficiency metrics
- Situational effectiveness (down, distance, field position)

## Advanced Usage

### Custom Analysis Scripts

For specialized analysis, you can use the core modules directly:

```python
from util import Config
from main import format_df, adj_ev, scout

# Load all season data
df = format_df(Config.load_all_seasons())

# Calculate adjusted expected value for offensive plays
results = adj_ev(df, 'OffensivePlay', ['Inside Run', 'Outside Run', 'Short Pass'], 'desc')

# Generate scouting report
scout('qad', 2049, 'TeamName')
```

### Configuration Options

Key settings in `config.yaml`:

```yaml
analysis:
  target_version: "0.4.6"          # Game version to analyze
  min_play_count: 20               # Minimum plays for statistical significance
  pass_threshold: 7                # Threshold for defensive pass analysis
  run_threshold: 6                 # Threshold for defensive run analysis
```

## File Structure

```
mfn/
├── mfn_cli.py              # Main CLI interface
├── config.yaml             # Base configuration
├── config.local.yaml       # Your local settings (create this)
├── config_manager.py       # Configuration management
├── requirements.txt        # Python dependencies
├── util.py                 # Core utilities and data loading
├── main.py                 # Primary analysis functions
├── GameLogDownloader.py    # Download game logs from MFN
├── SeasonCompiler.py       # Compile individual games into seasons
├── ScheduleParser.py       # Parse schedule data
├── best_offense.py         # Offensive strategy analysis
├── best_defense.py         # Defensive strategy analysis
├── targets.py              # Pass targeting analysis
├── feathers/               # Processed season data (Feather format)
└── files/                  # Reference files and exports
```

## Data Flow

1. **Extraction**: Download CSV game logs from MFN league sites
2. **Compilation**: Combine individual game files into season datasets
3. **Transformation**: Process raw data with play types, expected values, etc.
4. **Analysis**: Generate insights, rankings, and recommendations
5. **Export**: Save results to CSV/Feather for visualization tools like Tableau

## Output Files

The tool generates several types of output files:

- **Season Data**: `{league}_{season}.feather` - Complete processed season data
- **Best Plays**: `best_plays_analysis.csv` - Optimal play recommendations  
- **Scouting**: Console output with team tendencies and patterns
- **Targets**: `targets.csv` - Pass targeting frequency by play and receiver
- **Custom Analysis**: Various CSV exports from specialized scripts

## Troubleshooting

### Common Issues

**Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Path Issues**: Verify your `config.local.yaml` has correct paths to your data directories

**Missing Data**: Run `python mfn_cli.py download all` to ensure you have the necessary game logs

**Google Sheets Errors**: If using sheets integration, ensure `credentials.json` is in the project root

### Performance Tips

- Use Feather format files when possible (much faster than CSV)
- Filter data to specific game versions for consistency  
- Consider running analysis on subsets of data for faster iteration

## Contributing

This is a personal analysis tool, but improvements are welcome:

1. Add error handling and logging
2. Implement caching for faster repeated analysis  
3. Add more visualization outputs
4. Extend support for additional leagues
5. Optimize memory usage for large datasets

## License

Personal use tool - modify as needed for your MFN analysis needs.