# MFN Automation Suite

Complete automation solution for MyFootballNow (MFN) game log processing with **zero manual work**.

## 🚀 Key Features

- **Fully Automated Downloads**: Authenticated game log downloads with automatic Excel-to-CSV conversion
- **Zero Manual Work**: No copy-pasting schedules or manual game ID configuration  
- **Simple Game ID Generation**: Creates game lists for any season with just a starting ID
- **Robust Authentication**: Handles MFN login, CSRF tokens, and cross-domain cookies
- **Error Handling**: Comprehensive retry logic and status reporting

## 📁 Project Structure

```
mfn/
├── mfn_automation.py          # Main automation pipeline script
├── authenticated_downloader.py # Handles MFN authentication and downloads
├── simple_game_downloader.py   # Game ID generation utilities
├── util.py                    # Configuration and utilities
├── GameLogDownloader.py       # Original downloader (legacy)
└── ScheduleParser.py          # Manual schedule parsing (legacy)
```

## 🔧 Quick Start

### Prerequisites
```bash
pip install requests pandas openpyxl
```

### Basic Usage
```bash
# Download full season (256 games)
python3 mfn_automation.py \
  --league USFL \
  --year 2018 \
  --starting-id 14077 \
  --username YOUR_USERNAME \
  --password YOUR_PASSWORD

# Download with schedule generation
python3 mfn_automation.py \
  --league USFL \
  --year 2018 \
  --starting-id 14077 \
  --username YOUR_USERNAME \
  --password YOUR_PASSWORD \
  --generate-schedule

# Download specific number of games
python3 mfn_automation.py \
  --league USFL \
  --year 2018 \
  --starting-id 14077 \
  --username YOUR_USERNAME \
  --password YOUR_PASSWORD \
  --num-games 16
```

## 🔍 How It Works

### 1. Authentication Flow
- Logs into MFN website with CSRF token handling
- Establishes authenticated session across main and league subdomains
- Maintains cookies for seamless downloads

### 2. Game Discovery  
- Visits each game's box score page to extract download links
- Automatically discovers correct download URL format (`/download-game/{id}`)
- No manual URL construction or guessing required

### 3. Download & Conversion
- Downloads game logs (ZIP files containing Excel data)
- Automatically extracts and converts Excel files to CSV format
- Cleans up temporary files and maintains organized directory structure

### 4. File Organization
Game logs are saved to: `{Config.root}/{league}/{season}/{game_id}.csv`

Example: `/Users/jamesjones/personal/game_logs/USFL/2018/14077.csv`

## 📊 Output Format

Each CSV contains detailed play-by-play data with 82 columns including:
- Game state (down, distance, field position, score)
- Play details (offensive/defensive formations, yards gained)  
- Player assignments (all 22 positions per play)
- Special teams units and personnel
- Complete game timeline with timestamps

## 🔄 Migration from Manual Process

### Before (Manual)
1. Copy schedules from league page
2. Paste into ScheduleParser.py
3. Parse and format data
4. Configure download_season.py
5. Run downloads with authentication issues

### After (Automated)
1. Run one command with league, year, and starting Game ID
2. Everything else is automatic ✨

## 🛠️ Configuration

Edit `util.py` to modify:
- Output directory (`Config.root`)
- League domain mappings (`Config.domain_map`)  
- File paths and naming conventions

## 🚨 Troubleshooting

### Authentication Issues
- Verify username/password are correct
- Check that account has access to the specific league
- Ensure network connectivity to myfootballnow.com

### Download Failures
- Starting Game ID must be valid for the season
- Some games may not have logs available (pre-season, etc.)
- Check league domain mapping in util.py

### File Permission Errors
- Ensure write permissions to output directory
- Check disk space availability
- Verify Python has access to create/modify files

## 🔮 Future Enhancements

The automation suite is designed for easy extension:

- **Scouting Pipeline Integration**: Automated player performance analysis
- **Best Plays Selection**: AI-powered play recommendation system  
- **Performance Reports**: Automated team and player statistics
- **Real-time Processing**: Live game log processing during seasons

### MFN Data Flow (Legacy)

1. Extraction Layer
   1. Game log CSV downloads (now automated)
   2. Game log page data
2. Transformation Layer
3. Load Layer - Output files
   1. Play events by league-season
   2. Player stats by game
   3. Possession logs by league-season
   4. Aggregate play data by league-season
4. Presentation Layer - Tableau

## 💡 Technical Notes

- Uses requests.Session for persistent authentication
- Handles ZIP file extraction and Excel parsing with pandas/openpyxl
- Robust error handling and status reporting throughout
- Cross-platform compatibility (tested on macOS, should work on Linux/Windows)

## 📝 Example Output

```
🚀 MFN Automation Pipeline Starting
League: USFL, Season: 2018
Games: 14077 to 14332

📋 Step 1: Generating Game ID List
✅ Generated game list: USFL_2018_games.csv
   256 games from ID 14077

⬇️  Step 2: Downloading Game Logs  
🔐 Logging into https://www.myfootballnow.com/login...
✅ Login successful!
🌐 Visiting league domain: https://usflwfl.myfootballnow.com/
✅ League domain session established

Downloading 14077 for USFL...
✅ Converted Excel to CSV: 161 rows, 82 columns
...

📊 Download Summary:
✅ Successful: 256  
❌ Failed: 0
📁 Files saved to: /Users/jamesjones/personal/game_logs/USFL/2018

🎉 MFN Automation Pipeline Completed Successfully!
```

---

**No more manual work. No more copy-pasting. Just one command for complete season automation.**