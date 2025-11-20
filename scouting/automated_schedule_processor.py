#!/usr/bin/env python3
"""
Automated Schedule Processor for MFN
=====================================

This script automates the schedule processing workflow:
1. Parses schedule data from text input
2. Auto-detects or prompts for season year
3. Auto-generates Game IDs
4. Creates properly formatted CSV output
5. Extracts team lists for scouting automation

Usage:
- Place schedule text in the `schedule_text` variable below, OR
- Pass schedule via command line argument, OR  
- Read from file

Output: CSV ready for Google Sheets import
"""

import re
import csv
import sys
import argparse
from typing import List, Dict, Tuple, Optional
from pathlib import Path


def extract_season_year(schedule_text: str) -> Optional[int]:
    """
    Try to auto-detect season year from schedule text.
    Looks for patterns like "2024 Season", "Season 2024", etc.
    """
    # Common year patterns in schedule headers
    year_patterns = [
        r'(?i)season\s+(\d{4})',
        r'(?i)(\d{4})\s+season',
        r'(?i)(\d{4})\s+schedule',
        r'(?i)schedule\s+(\d{4})',
    ]
    
    for pattern in year_patterns:
        match = re.search(pattern, schedule_text)
        if match:
            year = int(match.group(1))
            # Sanity check: reasonable year range
            if 2000 <= year <= 2050:
                return year
    
    return None


def get_starting_game_id(league: str, season_year: int) -> int:
    """
    Get the starting Game ID for a given league and season.
    
    Since preseason game counts have changed over time, we maintain
    a manual lookup table of known starting Game IDs for each season.
    """
    league_configs = {
        'USFL': {
            # Manual lookup: year -> first regular season game ID
            # Add entries as needed: season_year: first_game_id
            1974: 65,
            1975: 398,
            1976: 731,
            1985: 3616,
            1995: 6786,
            2018: 14077,
            # Add more seasons here as you discover the Game IDs
        }
        # Add other leagues here as needed
    }
    
    if league not in league_configs:
        print(f"Warning: No Game ID config for league '{league}'")
        return None
        
    season_lookup = league_configs[league]
    
    if season_year in season_lookup:
        return season_lookup[season_year]
    else:
        print(f"Warning: No Game ID configured for {league} {season_year}")
        print(f"Available seasons: {sorted(season_lookup.keys())}")
        return None


def parse_schedule_to_csv(schedule_text: str, season_year: int, 
                         starting_game_id: int = None, 
                         league: str = None,
                         season_type: str = "Regular") -> List[Dict]:
    """
    Parse schedule text into CSV-ready format.
    
    Expected format:
    Week 1
    TeamA 24 @ TeamB 17
    TeamC 14 @ TeamD 21 (OT)
    
    Returns list of game dictionaries ready for CSV export.
    """
    games = []
    current_week = None
    
    # Get starting Game ID if not provided
    if starting_game_id is None:
        starting_game_id = get_starting_game_id(league, season_year)
        if starting_game_id is None:
            print(f"❌ No Game ID configured for {league} {season_year}")
            print(f"💡 Add the starting Game ID to the config or use --starting-id parameter")
            return []
        print(f"🎯 Using configured starting Game ID: {starting_game_id}")
    
    game_id = starting_game_id
    
    lines = schedule_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for week header
        week_match = re.match(r'Week\s+(\d+)', line)
        if week_match:
            current_week = int(week_match.group(1))
            continue
            
        # Skip if no week context yet
        if current_week is None:
            continue
            
        # Parse game line: "TeamA Score @ TeamB Score (OT)"
        # Clean up line - remove overtime indicator
        clean_line = re.sub(r'\s*\(OT\)\s*', '', line)
        
        # Try to parse: Team Score @ Team Score
        game_match = re.match(r'(.+?)\s+(\d+)\s*@\s*(.+?)\s+(\d+)\s*$', clean_line)
        
        if game_match:
            away_team = game_match.group(1).strip()
            away_score = int(game_match.group(2))
            home_team = game_match.group(3).strip()
            home_score = int(game_match.group(4))
            
            # Determine winner
            if home_score > away_score:
                winner = 'H'
                at_team = away_team
            elif away_score > home_score:
                winner = 'A' 
                at_team = away_team
            else:
                winner = 'T'  # Tie
                at_team = away_team
            
            # Clean team names (remove spaces for consistency)
            away_team_clean = away_team.replace(' ', '')
            home_team_clean = home_team.replace(' ', '')
            at_team_clean = at_team.replace(' ', '')
            
            game_data = {
                'Season': season_year,
                'Type': season_type,
                'Week': current_week,
                'Away Team': away_team_clean,
                'A Score': away_score,
                'Home Team': home_team_clean,
                'H Score': home_score,
                'Game ID': game_id,
                'Captured': 0,
                'Force Refresh': 0,
                'Win': winner,
                'AT': at_team_clean
            }
            
            games.append(game_data)
            game_id += 1
        else:
            # Could not parse this line, warn user
            print(f"Warning: Could not parse game line: '{line}'")
    
    return games


def extract_all_teams(games: List[Dict]) -> List[str]:
    """Extract unique team list from games for scouting automation."""
    teams = set()
    for game in games:
        teams.add(game['Away Team'])
        teams.add(game['Home Team'])
    return sorted(list(teams))


def save_to_csv(games: List[Dict], output_file: str) -> None:
    """Save games to CSV file."""
    if not games:
        print("No games to save!")
        return
        
    fieldnames = ['Season', 'Type', 'Week', 'Away Team', 'A Score', 'Home Team', 
                  'H Score', 'Game ID', 'Captured', 'Force Refresh', 'Win', 'AT']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(games)
    
    print(f"✅ Saved {len(games)} games to {output_file}")


def update_download_season_config(league: str, year: int, csv_path: str) -> None:
    """Update download_season.py with the new configuration."""
    download_script = Path('download_season.py')
    
    if not download_script.exists():
        print(f"Warning: {download_script} not found - cannot auto-update")
        return
    
    # Read current content
    content = download_script.read_text()
    
    # Update league and year
    content = re.sub(r"league\s*=\s*['\"][^'\"]*['\"]", f"league = '{league}'", content)
    content = re.sub(r"year\s*=\s*['\"][^'\"]*['\"]", f"year = '{year}'", content)
    
    # Update path
    path_line = f"path = '{csv_path}'"
    content = re.sub(r"path\s*=\s*.*", path_line, content)
    
    # Write back
    download_script.write_text(content)
    print(f"✅ Updated download_season.py with league='{league}', year='{year}'")


def main():
    parser = argparse.ArgumentParser(description='Automated MFN Schedule Processor')
    parser.add_argument('--input', '-i', help='Input schedule file')
    parser.add_argument('--output', '-o', help='Output CSV file') 
    parser.add_argument('--league', '-l', default='USFL', help='League name (default: USFL)')
    parser.add_argument('--year', '-y', type=int, help='Season year (auto-detected if not provided)')
    parser.add_argument('--starting-id', type=int, help='Starting Game ID (auto-detected if not provided)')
    parser.add_argument('--update-download', action='store_true', help='Auto-update download_season.py')
    
    args = parser.parse_args()
    
    # Get schedule text
    if args.input:
        schedule_text = Path(args.input).read_text()
        print(f"📖 Reading schedule from {args.input}")
    else:
        # Use the example schedule from ScheduleParser.py for testing
        # In practice, you'd paste your schedule here or read from clipboard
        schedule_text = """Week 1
Hornets 3 @ Bulls 17   
Blazers 6 @ Wheels 20   
Maulers 14 @ Renegades 16   
Stars 23 @ Wranglers 6   
Panthers 13 @ Gamblers 27   
SaberCats 39 @ Showboats 50   
Invaders 0 @ Storm 19   
Federals 10 @ VooDoo 42   
Breakers 0 @ Steamer 17   
(NY) Stars 7 @ Outlaws 20   
Bell 22 @ Generals 0   
Sun 7 @ Gunslingers 44   
Thunderbolts 3 @ Gold 20   
Blitz 6 @ Hawaiians 34   
Stallions 9 @ Express 26   
Force 7 @ Bandits 17   
Week 2
Bulls 37 @ Bandits 20   
Wranglers 3 @ Panthers 33"""
        print("📖 Using example schedule (replace with your actual schedule)")
    
    # Auto-detect or get season year
    if args.year:
        season_year = args.year
        print(f"📅 Using provided season year: {season_year}")
    else:
        detected_year = extract_season_year(schedule_text)
        if detected_year:
            season_year = detected_year
            print(f"📅 Auto-detected season year: {season_year}")
        else:
            # Prompt user
            try:
                season_year = int(input("Enter season year (e.g., 2024): "))
            except (ValueError, KeyboardInterrupt):
                print("❌ Invalid year or cancelled")
                return
    
    # Parse schedule
    print("🔄 Processing schedule...")
    games = parse_schedule_to_csv(schedule_text, season_year, args.starting_id, args.league)
    
    if not games:
        print("❌ No games found in schedule!")
        return
    
    print(f"✅ Parsed {len(games)} games across {max(g['Week'] for g in games)} weeks")
    
    # Extract teams for scouting
    teams = extract_all_teams(games)
    print(f"🏈 Found {len(teams)} unique teams: {', '.join(teams[:5])}{'...' if len(teams) > 5 else ''}")
    
    # Determine output path
    if args.output:
        output_file = args.output
    else:
        output_file = f"{args.league}_{season_year}_schedule.csv"
    
    # Save CSV
    save_to_csv(games, output_file)
    
    # Update download_season.py if requested
    if args.update_download:
        csv_path = Path(output_file).absolute()
        update_download_season_config(args.league, season_year, str(csv_path))
    
    # Save teams list for scouting automation
    teams_file = f"{args.league}_{season_year}_teams.txt"
    with open(teams_file, 'w') as f:
        for team in teams:
            f.write(f"{team}\n")
    print(f"📝 Saved team list to {teams_file} (for scouting automation)")
    
    print("\n🎯 Next steps:")
    print(f"1. Review {output_file} and import to Google Sheets")
    print(f"2. Run: python download_season.py (if --update-download was used)")
    print(f"3. Use teams from {teams_file} for automated scouting")


if __name__ == "__main__":
    main()