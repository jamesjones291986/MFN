#!/usr/bin/env python3
"""
Simple MFN Game Log Downloader
==============================

Minimal manual work approach:
1. You provide: league, year, starting Game ID
2. Script generates: Game ID list for entire season
3. Downloads: All game logs automatically

Usage:
python simple_game_downloader.py --league USFL --year 2018 --starting-id 14077
"""

import pandas as pd
import argparse
from pathlib import Path
from GameLogDownloader import GameLogDownloader
from SeasonCompiler import SeasonCompiler


def create_game_id_list(starting_game_id: int, num_games: int = 256) -> pd.DataFrame:
    """
    Create a simple list of Game IDs for download.
    
    Args:
        starting_game_id: First game ID of the season
        num_games: Number of games in season (default: 256)
    
    Returns:
        DataFrame with Game ID and Captured columns
    """
    games = []
    for i in range(num_games):
        games.append({
            'Game ID': starting_game_id + i,
            'Captured': 0  # 0 = download, 1 = skip
        })
    
    return pd.DataFrame(games)


def download_season_simple(league: str, year: int, starting_game_id: int, 
                          num_games: int = 256) -> None:
    """
    Download an entire season with minimal setup.
    
    Args:
        league: League name (e.g., 'USFL')
        year: Season year (e.g., 2018)
        starting_game_id: First game ID (e.g., 14077)
        num_games: Number of games to download (default: 256)
    """
    print(f"🏈 Downloading {league} {year} season...")
    print(f"📊 Game IDs: {starting_game_id} → {starting_game_id + num_games - 1}")
    
    # Create simple game ID list
    games_df = create_game_id_list(starting_game_id, num_games)
    
    # Save temporary CSV for GameLogDownloader
    temp_csv = f"{league}_{year}_games.csv"
    games_df.to_csv(temp_csv, index=False)
    print(f"📝 Created game list: {temp_csv}")
    
    # Initialize and run downloader
    gdl = GameLogDownloader()
    gdl.set_league_season(league, year)
    
    print(f"⬇️  Starting downloads...")
    success = gdl.download_season(override_path=temp_csv)
    
    if success:
        print(f"✅ Downloads complete!")
        print(f"📁 Game logs saved in: {gdl.root}/{league}/{year}/")
        
        # Clean up temp CSV
        Path(temp_csv).unlink()
        print(f"🧹 Cleaned up {temp_csv}")
        
        print(f"\n🎯 Next steps:")
        print(f"1. Check downloaded game logs in: {gdl.root}/{league}/{year}/")
        print(f"2. Run SeasonCompiler manually if you need feather files")
        print(f"3. Use downloaded logs for scouting analysis")
        
    else:
        print(f"❌ Download failed!")


def main():
    parser = argparse.ArgumentParser(description='Simple MFN Game Log Downloader')
    parser.add_argument('--league', '-l', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--year', '-y', type=int, required=True, help='Season year (e.g., 2018)')
    parser.add_argument('--starting-id', '-s', type=int, required=True, 
                       help='Starting Game ID (e.g., 14077)')
    parser.add_argument('--num-games', '-n', type=int, default=256,
                       help='Number of games in season (default: 256)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Just create the game list, don\'t download')
    
    args = parser.parse_args()
    
    if args.dry_run:
        print(f"🧪 DRY RUN: Creating game list for {args.league} {args.year}")
        games_df = create_game_id_list(args.starting_id, args.num_games)
        output_file = f"{args.league}_{args.year}_games_preview.csv"
        games_df.to_csv(output_file, index=False)
        print(f"📝 Preview saved to: {output_file}")
        print(f"📊 Game IDs: {args.starting_id} → {args.starting_id + args.num_games - 1}")
        print("🎯 Remove --dry-run to start downloading")
    else:
        download_season_simple(args.league, args.year, args.starting_id, args.num_games)


if __name__ == "__main__":
    main()