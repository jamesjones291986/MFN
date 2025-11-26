# MFN Season Download Module

Streamlined tool for downloading complete MFN (My Football Now) seasons with minimal setup.

## Features

- **Simple Game ID Generation**: Automatically creates game ID lists for any season
- **Authenticated Downloads**: Handles MFN website authentication seamlessly  
- **Multiple File Formats**: Supports CSV, ZIP, and Excel file downloads with automatic conversion
- **Progress Tracking**: Real-time download progress and error reporting
- **Robust Error Handling**: Continues downloading even if some games fail

## Quick Start

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure paths:** Edit `config.py` to set your desired download directories

### Basic Usage

Download a complete season:

```bash
python season_downloader.py --league USFL --year 2018 --starting-id 14077 --username YOUR_USERNAME --password YOUR_PASSWORD
```

### Command Line Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--league` | `-l` | ✅ | League name (e.g., USFL, xfl, qad) |
| `--year` | `-y` | ✅ | Season year (e.g., 2018) |
| `--starting-id` | `-s` | ✅ | First game ID of the season |
| `--username` | `-u` | ✅ | MFN username |
| `--password` | `-p` | ✅ | MFN password |
| `--num-games` | `-n` | ❌ | Number of games (default: 256) |
| `--generate-schedule` | | ❌ | Create a CSV file with game IDs |
| `--test-single` | | ❌ | Download only 1 game for testing |

## Examples

### Download Full Season
```bash
python season_downloader.py -l USFL -y 2018 -s 14077 -u myusername -p mypassword
```

### Test Single Game
```bash
python season_downloader.py -l USFL -y 2018 -s 14077 -u myusername -p mypassword --test-single
```

### Custom Number of Games
```bash
python season_downloader.py -l USFL -y 2018 -s 14077 -u myusername -p mypassword -n 128
```

### Generate Schedule File
```bash
python season_downloader.py -l USFL -y 2018 -s 14077 -u myusername -p mypassword --generate-schedule
```

## Supported Leagues

The tool supports multiple MFN leagues:

| League | Domain | Example Seasons |
|--------|--------|-----------------|
| USFL | usflwfl.myfootballnow.com | 2002-2011, 2017-2018 |
| XFL | xfl.myfootballnow.com | 2043-2048 |
| QAD | fantasy-league.myfootballnow.com | 2043-2049 |
| Paydirt | paydirt.myfootballnow.com | 1996-2002 |
| Moguls | moguls.myfootballnow.com | 2042-2047 |
| Norig | norig.myfootballnow.com | 2028-2032 |
| PFL | pfl.myfootballnow.com | 2026-2029 |
| LOL | lol.myfootballnow.com | 2117-2120 |
| NBA | nba-league.myfootballnow.com | 2000-2001 |

## Configuration

### File Paths

Edit `config.py` to customize where files are saved:

```python
class Config:
    # Base directory for downloaded game logs
    root = r'/Users/jamesjones/personal/game_logs'
    
    # Directory for compiled season feather files
    seasons = r'/Users/jamesjones/personal/MFN/feathers'
```

### Finding Game IDs

To find the starting game ID for a season:

1. Go to your league's website
2. Navigate to any game from the season you want
3. Look at the URL: `https://usflwfl.myfootballnow.com/box/14077`
4. The number at the end (14077) is a game ID
5. Use the earliest game ID from that season as your starting ID

## Output

### Directory Structure

Downloaded files are organized as:
```
/game_logs/
├── USFL/
│   ├── 2018/
│   │   ├── 14077.csv
│   │   ├── 14078.csv
│   │   └── ...
│   └── 2017/
└── xfl/
    └── 2043/
```

### Download Summary

The tool provides a summary after completion:
```
📊 Download Summary:
✅ Successful: 248
❌ Failed: 8
📁 Files saved to: /Users/jamesjones/personal/game_logs/USFL/2018
```

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify your username and password are correct
   - Check that your account has access to the specified league

2. **No Games Found (404 errors)**
   - Verify the starting game ID is correct for that season
   - Check that the season year matches the league's available seasons

3. **Download Failures**
   - Network issues may cause intermittent failures
   - Failed files are automatically removed and reported
   - Re-run the script to retry failed downloads

### Debug Mode

Use `--test-single` to test your configuration with just one game:

```bash
python season_downloader.py -l USFL -y 2018 -s 14077 -u myusername -p mypassword --test-single
```

## Integration

This module is designed to be the first step in a larger MFN analysis pipeline:

1. **Download Season** ← You are here
2. **Compile to Feather** (coming soon)
3. **Scouting Analysis** (coming soon)
4. **Performance Reports** (coming soon)

## Dependencies

- `pandas`: Data manipulation and CSV handling
- `requests`: HTTP requests and authentication
- `openpyxl`: Excel file support for some league formats