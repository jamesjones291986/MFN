#!/usr/bin/env python3
"""
MFN Data Analysis CLI
Main entry point for all MFN data operations
"""

import argparse
import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from util import Config
from GameLogDownloader import GameLogDownloader
from SeasonCompiler import SeasonCompiler
from main import format_df, scout, adj_ev, all_plays, run_best_plays_analysis
from gameplan import generate_gameplan
from personnel_analyzer import create_personnel_gameplan
from season_manager import setup_auto_downloads, check_for_new_seasons, organize_storage
from auto_downloader import auto_download_season
from advanced_gameplan import create_comprehensive_gameplan
from quick_update import quick_update_workflow, update_season_only


def download_league_season(league, season, force=False, partial=False, auto=False):
    """Download game logs for a specific league and season"""
    print(f"Downloading {league} {season} game logs...")
    if force:
        print("  (Force mode: re-downloading existing files)")
    if partial:
        print("  (Partial mode: downloading incomplete season)")
    if auto:
        print("  (Auto-discovery mode: no Google Sheets needed)")
        
        # Use auto-downloader for new seasons
        games_found = auto_download_season(league, season, force)
        
        if games_found:
            print(f"Successfully auto-downloaded {len(games_found)} games for {league} {season}")
            return True
        else:
            print(f'ERROR! No games found for {league} {season}')
            return False
    else:
        # Use traditional method with Google Sheets
        gdl = GameLogDownloader()
        
        if not gdl.set_league_season(league, season):
            print(f'ERROR! {league} {season} not set!')
            return False
            
        if not gdl.download_season():
            print(f'ERROR! {league} {season} not downloaded!')
            return False
            
        print(f"Successfully downloaded {league} {season}")
        return True


def download_all_leagues(force=False):
    """Download all available league seasons"""
    print("Downloading all available league seasons...")
    if force:
        print("  (Force mode: re-downloading existing files)")
        
    gdl = GameLogDownloader()
    success_count = 0
    error_count = 0
    
    for league, seasons in Config.ls_dictionary.items():
        for season in seasons:
            try:
                if not gdl.set_league_season(league, season):
                    print(f'ERROR! {league} {season} not set!')
                    error_count += 1
                    continue
                    
                if not gdl.download_season():
                    print(f'ERROR! {league} {season} not downloaded!')
                    error_count += 1
                    continue
                    
                print(f"✅ Downloaded {league} {season}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Error downloading {league} {season}: {e}")
                error_count += 1
    
    print(f"\n📊 Download Summary:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print("Finished downloading all leagues")


def add_new_league_season(league, season, domain=None, sheet_id=None):
    """Add and download a new league/season not in the config"""
    print(f"Adding new league/season: {league} {season}")
    
    # Try to guess domain if not provided
    if not domain:
        domain = league.lower()
        print(f"  Using guessed domain: {domain}")
    
    # Update the config temporarily (in memory)
    if league not in Config.ls_dictionary:
        Config.ls_dictionary[league] = []
    
    if season not in Config.ls_dictionary[league]:
        Config.ls_dictionary[league].append(season)
    
    if league not in Config.domain_map:
        Config.domain_map[league] = domain
    
    if sheet_id and league not in Config.sheet_lookup:
        Config.sheet_lookup[league] = sheet_id
    
    # Try to download
    try:
        gdl = GameLogDownloader()
        if gdl.set_league_season(league, season):
            if gdl.download_season():
                print(f"✅ Successfully added and downloaded {league} {season}")
                
                # TODO: Save updated config to local file
                print(f"💡 To make this permanent, add to your config.local.yaml:")
                print(f"   leagues:")
                print(f"     {league}:")
                print(f"       seasons: [{season}]")
                print(f"       domain: {domain}")
                if sheet_id:
                    print(f"       sheet_id: {sheet_id}")
                
                return True
            else:
                print(f"❌ Failed to download {league} {season}")
        else:
            print(f"❌ Failed to set up {league} {season} - check domain name")
    except Exception as e:
        print(f"❌ Error adding {league} {season}: {e}")
    
    return False


def compile_season(league, season, schedule_path=None):
    """Compile individual game logs into season dataset"""
    print(f"Compiling {league} {season}...")
    
    if not schedule_path:
        schedule_path = f"{Config.root}/{league}/{league}_{season}.csv"
        
    if not os.path.exists(schedule_path):
        print(f"ERROR! Schedule file not found: {schedule_path}")
        return False
        
    SeasonCompiler.compile(league, season, override_path=schedule_path)
    print(f"Successfully compiled {league} {season}")
    return True


def generate_scouting_report(league, season, team):
    """Generate scouting report for a team"""
    print(f"Generating scouting report for {team} in {league} {season}")
    scout(league, season, team)


def create_gameplan(league, season, opponent, include_personnel=False):
    """Generate gameplan against opponent"""
    if include_personnel:
        print("Generating enhanced gameplan with personnel analysis...")
        # Run both analyses
        basic_gameplan = generate_gameplan(league, season, opponent)
        personnel_gameplan = create_personnel_gameplan(league, season, opponent)
        return {'basic': basic_gameplan, 'personnel': personnel_gameplan}
    else:
        return generate_gameplan(league, season, opponent)


def analyze_best_plays():
    """Run best plays analysis across all data"""
    print("Analyzing best offensive plays...")
    off_play_adj_ev = run_best_plays_analysis()
    
    output_path = f"{Config.root}/best_plays_analysis.csv"
    off_play_adj_ev.to_csv(output_path, index=False)
    print(f"Best plays analysis saved to: {output_path}")
    
    return off_play_adj_ev


def generate_targeting_data():
    """Generate targeting data required for enhanced scouting"""
    print("Generating targeting data...")
    print("This analyzes where teams target their passes by position.")
    
    try:
        # Import and run targets.py logic
        import subprocess
        result = subprocess.run(['python3', 'targets.py'], 
                              capture_output=True, text=True, 
                              cwd='/Users/jamesjones/projects/mfn')
        
        if result.returncode == 0:
            print("✅ Targeting data generated successfully!")
            print("   Enhanced scouting reports will now show pass targeting analysis")
        else:
            print(f"❌ Error generating targeting data:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error running targeting analysis: {e}")
        print("   Try running 'python targets.py' manually in the project directory")


def list_available_leagues():
    """List all available leagues and seasons"""
    print("Available leagues and seasons:")
    for league, seasons in Config.ls_dictionary.items():
        print(f"  {league}: {', '.join(map(str, seasons))}")


def main():
    parser = argparse.ArgumentParser(description='MFN Data Analysis CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Download commands
    download_parser = subparsers.add_parser('download', help='Download game logs')
    download_subparsers = download_parser.add_subparsers(dest='download_type')
    
    # Download specific league/season
    download_season_parser = download_subparsers.add_parser('season', help='Download specific league/season')
    download_season_parser.add_argument('league', help='League name (e.g., qad, xfl, pfl)')
    download_season_parser.add_argument('season', type=int, help='Season year')
    download_season_parser.add_argument('--force', action='store_true', help='Force re-download even if files exist')
    download_season_parser.add_argument('--partial', action='store_true', help='Download partial/incomplete season')
    download_season_parser.add_argument('--auto', action='store_true', help='Auto-discover games (no Google Sheets needed)')
    
    # Download all
    download_all_parser = download_subparsers.add_parser('all', help='Download all available leagues/seasons')
    download_all_parser.add_argument('--force', action='store_true', help='Force re-download even if files exist')
    
    # Add new league/season
    add_parser = download_subparsers.add_parser('add', help='Add and download new league/season not in config')
    add_parser.add_argument('league', help='League name')
    add_parser.add_argument('season', type=int, help='Season year')
    add_parser.add_argument('--domain', help='League domain (e.g., fantasy-league, xfl)')
    add_parser.add_argument('--sheet-id', help='Google Sheet ID for schedule data')
    
    # Compile commands
    compile_parser = subparsers.add_parser('compile', help='Compile season data')
    compile_parser.add_argument('league', help='League name')
    compile_parser.add_argument('season', type=int, help='Season year')
    compile_parser.add_argument('--schedule', help='Path to schedule CSV file')
    
    # Scout command
    scout_parser = subparsers.add_parser('scout', help='Generate scouting report')
    scout_parser.add_argument('league', help='League name')
    scout_parser.add_argument('season', type=int, help='Season year')
    scout_parser.add_argument('team', help='Team name/abbreviation')
    
    # Gameplan command
    gameplan_parser = subparsers.add_parser('gameplan', help='Generate gameplan vs opponent')
    gameplan_parser.add_argument('league', help='League name')
    gameplan_parser.add_argument('season', type=int, help='Season year')
    gameplan_parser.add_argument('opponent', help='Opponent team name/abbreviation')
    gameplan_parser.add_argument('--personnel', action='store_true', help='Include detailed personnel-based analysis')
    
    # Personnel-specific gameplan
    personnel_parser = subparsers.add_parser('personnel', help='Generate personnel-based gameplan')
    personnel_parser.add_argument('league', help='League name')
    personnel_parser.add_argument('season', type=int, help='Season year')
    personnel_parser.add_argument('opponent', help='Opponent team name/abbreviation')
    
    # Comprehensive gameplan (18+ plays)
    comprehensive_parser = subparsers.add_parser('comprehensive', help='Generate comprehensive 18+ play gameplan')
    comprehensive_parser.add_argument('league', help='League name')
    comprehensive_parser.add_argument('season', type=int, help='Season year')
    comprehensive_parser.add_argument('opponent', help='Opponent team name/abbreviation')
    
    # Quick update workflow
    update_parser = subparsers.add_parser('update', help='Download latest + compile + gameplan (all-in-one)')
    update_parser.add_argument('league', help='League name')
    update_parser.add_argument('season', type=int, help='Season year')
    update_parser.add_argument('opponent', nargs='?', help='Opponent team (optional)')
    update_parser.add_argument('--data-only', action='store_true', help='Update data only, no gameplan')
    
    # Analysis commands
    subparsers.add_parser('analyze', help='Run best plays analysis')
    subparsers.add_parser('targets', help='Generate targeting data (required for enhanced scouting)')
    subparsers.add_parser('list', help='List available leagues and seasons')
    
    # Season management commands
    manage_parser = subparsers.add_parser('manage', help='Season and data management')
    manage_subparsers = manage_parser.add_subparsers(dest='manage_type')
    
    # Check for new seasons
    manage_subparsers.add_parser('check', help='Check for new seasons')
    
    # Setup auto-download
    auto_parser = manage_subparsers.add_parser('auto', help='Setup automatic downloads')
    auto_parser.add_argument('leagues', nargs='+', help='Leagues to monitor (e.g., qad xfl pfl)')
    
    # Organize storage
    manage_subparsers.add_parser('organize', help='Organize data storage')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'download':
            if args.download_type == 'season':
                download_league_season(args.league, args.season, 
                                     getattr(args, 'force', False), 
                                     getattr(args, 'partial', False),
                                     getattr(args, 'auto', False))
            elif args.download_type == 'all':
                download_all_leagues(getattr(args, 'force', False))
            elif args.download_type == 'add':
                add_new_league_season(args.league, args.season,
                                    getattr(args, 'domain', None),
                                    getattr(args, 'sheet_id', None))
            else:
                download_parser.print_help()
                
        elif args.command == 'compile':
            compile_season(args.league, args.season, args.schedule)
            
        elif args.command == 'scout':
            generate_scouting_report(args.league, args.season, args.team)
            
        elif args.command == 'gameplan':
            create_gameplan(args.league, args.season, args.opponent, 
                          getattr(args, 'personnel', False))
            
        elif args.command == 'personnel':
            create_personnel_gameplan(args.league, args.season, args.opponent)
            
        elif args.command == 'comprehensive':
            create_comprehensive_gameplan(args.league, args.season, args.opponent)
            
        elif args.command == 'update':
            if getattr(args, 'data_only', False):
                update_season_only(args.league, args.season)
            else:
                quick_update_workflow(args.league, args.season, args.opponent)
            
        elif args.command == 'analyze':
            analyze_best_plays()
            
        elif args.command == 'targets':
            generate_targeting_data()
            
        elif args.command == 'list':
            list_available_leagues()
            
        elif args.command == 'manage':
            if args.manage_type == 'check':
                check_for_new_seasons()
            elif args.manage_type == 'auto':
                setup_auto_downloads(args.leagues)
            elif args.manage_type == 'organize':
                organize_storage()
            else:
                manage_parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())