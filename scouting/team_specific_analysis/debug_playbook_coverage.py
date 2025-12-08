#!/usr/bin/env python3
"""
Debug Playbook Coverage
=======================

Check which playbook plays are missing from the analysis and why.
"""

import pandas as pd
import sys
from pathlib import Path
import argparse

# Add paths for imports
sys.path.append('/Users/jamesjones/projects/mfn/scouting')
sys.path.append('/Users/jamesjones/projects/mfn/lineup_analyzer')

from util import Config

try:
    from sheets_connector import LineupSheetsConnector
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False

def debug_playbook_coverage(opponent='MIC', league='USFL', season=2018):
    """Debug what playbook plays are missing and why."""
    
    print(f"🔍 DEBUGGING PLAYBOOK COVERAGE vs {opponent}")
    print("=" * 50)
    
    # Load data
    df = Config.load_feather(league, season)
    print(f"✅ Loaded {len(df)} total plays")
    
    # Load playbook
    playbook_plays = []
    if SHEETS_AVAILABLE:
        try:
            sheets_connector = LineupSheetsConnector(verbose=False)
            sheet_id = Config.GAMEPLAN_SHEET_ID
            spreadsheet = sheets_connector.get_sheet(sheet_id)
            
            playbook_worksheet = spreadsheet.worksheet('standard_playbook')
            playbook_data = playbook_worksheet.get_all_values()
            
            # Find header row
            header_row = None
            for i, row in enumerate(playbook_data):
                if 'Play Name' in row:
                    header_row = i
                    break
            
            if header_row is not None:
                headers = playbook_data[header_row]
                play_col_idx = headers.index('Play Name')
                
                for row in playbook_data[header_row + 1:]:
                    if len(row) > play_col_idx and row[play_col_idx].strip():
                        play_name = row[play_col_idx].strip()
                        # Remove numbering if present
                        if '. ' in play_name:
                            play_name = play_name.split('. ', 1)[1]
                        playbook_plays.append(play_name)
                
                print(f"📋 Loaded {len(playbook_plays)} plays from standard_playbook")
            
        except Exception as e:
            print(f"❌ Error loading playbook: {e}")
            return
    
    # Find opponent games
    opponent_games = df.groupby('Game ID')['HasBall'].unique()
    games_with_opponent = [game_id for game_id, teams in opponent_games.items() 
                          if opponent in teams]
    
    # Filter for plays against opponent's defense
    vs_opponent_defense = df[
        (df['Game ID'].isin(games_with_opponent)) &
        (df['HasBall'] != opponent) &
        (df['HasBall'].notna()) &
        (df['OffensivePlay'].notna()) &
        (~df['OffensivePlay'].isin(['Field Goal', 'Punt', 'Victory', 'Kickoff']))
    ].copy()
    
    print(f"📊 Found {len(vs_opponent_defense)} total offensive plays vs {opponent}")
    
    # Check each playbook play
    print(f"\n📋 PLAYBOOK PLAY ANALYSIS")
    print("=" * 30)
    
    found_plays = 0
    missing_plays = []
    low_attempt_plays = []
    min_attempts = 2
    
    for i, play in enumerate(playbook_plays, 1):
        play_data = vs_opponent_defense[vs_opponent_defense['OffensivePlay'] == play]
        attempts = len(play_data)
        
        if attempts == 0:
            missing_plays.append(play)
            status = "❌ NOT USED"
        elif attempts < min_attempts:
            low_attempt_plays.append((play, attempts))
            status = f"⚠️  {attempts} attempt{'s' if attempts != 1 else ''} (below {min_attempts} min)"
        else:
            found_plays += 1
            avg_yards = play_data['YardsGained'].mean()
            status = f"✅ {attempts} attempts, {avg_yards:.1f} avg yards"
        
        print(f"{i:2d}. {play:<40} {status}")
    
    print(f"\n📊 SUMMARY")
    print("=" * 15)
    print(f"✅ Plays with {min_attempts}+ attempts: {found_plays}")
    print(f"⚠️  Plays with 1-{min_attempts-1} attempts: {len(low_attempt_plays)}")
    print(f"❌ Plays never used vs {opponent}: {len(missing_plays)}")
    print(f"📋 Total playbook plays: {len(playbook_plays)}")
    
    if missing_plays:
        print(f"\n❌ PLAYS NEVER USED vs {opponent}")
        for play in missing_plays:
            print(f"   • {play}")
    
    if low_attempt_plays:
        print(f"\n⚠️  PLAYS WITH LOW ATTEMPTS")
        for play, attempts in low_attempt_plays:
            print(f"   • {play}: {attempts} attempt{'s' if attempts != 1 else ''}")
    
    # Check if we should lower minimum attempts
    total_usable = found_plays + len(low_attempt_plays)
    print(f"\n💡 RECOMMENDATIONS")
    print("=" * 20)
    print(f"   Current threshold: {min_attempts} attempts = {found_plays} plays analyzed")
    print(f"   If threshold = 1: {total_usable} plays would be analyzed")
    
    if len(low_attempt_plays) > 0:
        print(f"\n🔧 Consider lowering --min-attempts to 1 to include {len(low_attempt_plays)} more plays")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Debug playbook coverage against a specific opponent')
    parser.add_argument('--opponent', default='MIC', help='Opponent team abbreviation (e.g., MIC)')
    parser.add_argument('--league', default='USFL', help='League name (e.g., USFL)')
    parser.add_argument('--season', type=int, default=2018, help='Season year (e.g., 2018)')
    
    args = parser.parse_args()
    
    # Pass the parsed arguments to the debug_playbook_coverage function
    debug_playbook_coverage(args.opponent.upper(), args.league, args.season)