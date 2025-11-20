#!/usr/bin/env python3
"""
MFN Complete Automation Script
==============================

Fully automated workflow for MFN game log processing with zero manual work.

This script provides:
1. Simple Game ID generation for any season
2. Authenticated game log downloads
3. Ready for scouting pipeline integration

Usage:
python mfn_automation.py --league USFL --year 2018 --starting-id 14077 --username YOUR_USERNAME --password YOUR_PASSWORD
"""

import argparse
import os
import sys
from pathlib import Path

# Import our custom modules
from simple_game_downloader import create_game_id_list
from authenticated_downloader import AuthenticatedGameLogDownloader


def main():
    parser = argparse.ArgumentParser(description='Complete MFN Automation Pipeline')
    parser.add_argument('--league', '-l', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--year', '-y', type=int, required=True, help='Season year (e.g., 2018)')
    parser.add_argument('--starting-id', '-s', type=int, required=True, 
                       help='Starting Game ID (e.g., 14077)')
    parser.add_argument('--num-games', '-n', type=int, default=256,
                       help='Number of games in season (default: 256)')
    parser.add_argument('--username', '-u', required=True, help='MFN username')
    parser.add_argument('--password', '-p', required=True, help='MFN password')
    parser.add_argument('--generate-schedule', action='store_true',
                       help='Generate a schedule CSV file')
    parser.add_argument('--download-only', action='store_true',
                       help='Skip schedule generation, only download games')
    
    args = parser.parse_args()
    
    print(f"🚀 MFN Automation Pipeline Starting")
    print(f"League: {args.league}, Season: {args.year}")
    print(f"Games: {args.starting_id} to {args.starting_id + args.num_games - 1}")
    print()
    
    # Step 1: Generate schedule/game list if requested
    if args.generate_schedule and not args.download_only:
        print("📋 Step 1: Generating Game ID List")
        schedule_path = f"{args.league}_{args.year}_games.csv"
        
        game_list = create_game_id_list(args.starting_id, args.num_games)
        game_list.to_csv(schedule_path, index=False)
        
        print(f"✅ Generated game list: {schedule_path}")
        print(f"   {len(game_list)} games from ID {args.starting_id}")
        print()
    
    # Step 2: Download all game logs
    print("⬇️  Step 2: Downloading Game Logs")
    
    downloader = AuthenticatedGameLogDownloader(
        league=args.league,
        season=args.year,
        username=args.username,
        password=args.password
    )
    
    # Authenticate
    if not downloader.login():
        print("❌ Authentication failed")
        return 1
    
    # Download all games
    success = downloader.download_season(args.starting_id, args.num_games)
    
    if not success:
        print("❌ Download failed")
        return 1
    
    print("✅ All downloads completed!")
    print()
    
    # Step 3: Future integration points
    print("🔮 Next Steps (Future Automation):")
    print("   - Scouting pipeline integration")
    print("   - Best plays selection automation")
    print("   - Performance analysis reports")
    print()
    
    print("🎉 MFN Automation Pipeline Completed Successfully!")
    return 0


if __name__ == "__main__":
    exit(main())