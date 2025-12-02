#!/usr/bin/env python3
"""
Automated Scouting Pipeline for MFN
===================================

This script automates the scouting workflow:
1. Auto-loads teams from schedule processing
2. Runs defensive scouting for all teams
3. Runs offensive scouting for all teams  
4. Saves structured results for best plays analysis
5. Eliminates manual copy/paste between scripts

Usage:
python automated_scouting.py --league USFL --year 2018
"""

import pandas as pd
import argparse
import json
import pickle
from pathlib import Path
from typing import Dict, List, Any
from main import format_df
from util import Config


def load_teams_from_file(teams_file: str) -> List[str]:
    """Load team list from automated schedule processor output."""
    teams_path = Path(teams_file)
    if not teams_path.exists():
        raise FileNotFoundError(f"Teams file not found: {teams_file}")
    
    teams = []
    with open(teams_path, 'r') as f:
        for line in f:
            team = line.strip()
            if team:
                teams.append(team)
    
    return teams


def load_season_data(league: str, year: str) -> pd.DataFrame:
    """Load and format season data from feather file."""
    file_name = f"{league}_{year}.feather"
    
    try:
        df = format_df(Config.load_specific_feather(file_name)).reset_index(drop=True)
        print(f"✅ Loaded {len(df)} plays from {file_name}")
        return df
    except Exception as e:
        raise Exception(f"Could not load {file_name}: {e}")


def run_defensive_scouting(df: pd.DataFrame, teams: List[str], league: str, season: str,
                          threshold_percentage: float = 7.0) -> Dict[str, Any]:
    """
    Run defensive scouting analysis for all teams.
    
    Returns dictionary with defensive play usage by team and personnel.
    """
    print(f"🛡️  Running defensive scouting for {len(teams)} teams...")
    
    all_results = {}
    
    for team in teams:
        print(f"   Scouting defense: {team}")
        team_results = {}
        
        for personnel in df.OffPersonnel.unique():
            if pd.isna(personnel):
                continue
                
            # Filter for this team's defensive plays in this personnel
            filtered_df = df.loc[
                df.DefTeam.eq(team) &
                df.League.eq(league) &
                df.OffPersonnel.eq(personnel) &
                df.Season.astype(str).eq(season)
            ]
            
            if len(filtered_df) == 0:
                continue
            
            # Get top defensive plays and percentages
            grouped_data = filtered_df.groupby('DefensivePlay').size().sort_values(ascending=False)
            percentages = grouped_data / grouped_data.sum() * 100
            
            # Store plays above threshold
            significant_plays = percentages[percentages >= threshold_percentage]
            if len(significant_plays) > 0:
                team_results[personnel] = significant_plays.to_dict()
        
        if team_results:
            all_results[team] = team_results
    
    return all_results


def run_offensive_scouting(df: pd.DataFrame, teams: List[str], league: str, season: str,
                          threshold_percentage: float = 10.0) -> Dict[str, Any]:
    """
    Run offensive scouting analysis for all teams.
    
    Returns dictionary with offensive play usage by team and personnel.
    """
    print(f"⚡ Running offensive scouting for {len(teams)} teams...")
    
    all_results = {}
    
    for team in teams:
        print(f"   Scouting offense: {team}")
        team_results = {}
        
        for personnel in df.OffPersonnel.unique():
            if pd.isna(personnel):
                continue
                
            # Filter for this team's offensive plays in this personnel
            filtered_df = df.loc[
                df.HasBall.eq(team) &  # Team with the ball = offensive team
                df.League.eq(league) &
                df.OffPersonnel.eq(personnel) &
                df.Season.astype(str).eq(season)
            ]
            
            if len(filtered_df) == 0:
                continue
            
            # Get top offensive plays and percentages
            grouped_data = filtered_df.groupby('OffensivePlay').size().sort_values(ascending=False)
            percentages = grouped_data / grouped_data.sum() * 100
            
            # Store plays above threshold
            significant_plays = percentages[percentages >= threshold_percentage]
            if len(significant_plays) > 0:
                team_results[personnel] = significant_plays.to_dict()
        
        if team_results:
            all_results[team] = team_results
    
    return all_results


def create_combined_analysis(def_results: Dict, off_results: Dict, 
                           threshold: float = 7.0) -> pd.DataFrame:
    """
    Create combined analysis similar to the original scripts' output.
    
    This mimics the DataFrame creation from the original def_scouting.py
    """
    data_to_append = []
    
    # Process defensive results
    for team, personnel_results in def_results.items():
        for personnel, play_percentages in personnel_results.items():
            for play, usage_pct in play_percentages.items():
                if usage_pct >= threshold:
                    data_to_append.append({
                        'Team': team,
                        'Side': 'Defense',
                        'Personnel': personnel,
                        'Play': play,
                        'Usage': usage_pct
                    })
    
    # Process offensive results  
    for team, personnel_results in off_results.items():
        for personnel, play_percentages in personnel_results.items():
            for play, usage_pct in play_percentages.items():
                if usage_pct >= threshold:
                    data_to_append.append({
                        'Team': team,
                        'Side': 'Offense',
                        'Personnel': personnel,
                        'Play': play,
                        'Usage': usage_pct
                    })
    
    return pd.DataFrame(data_to_append)


def save_results(def_results: Dict, off_results: Dict, output_prefix: str) -> None:
    """Save scouting results in multiple formats for different uses."""
    
    # Save raw results as JSON (human readable)
    with open(f"{output_prefix}_defensive_scouting.json", 'w') as f:
        json.dump(def_results, f, indent=2)
    
    with open(f"{output_prefix}_offensive_scouting.json", 'w') as f:
        json.dump(off_results, f, indent=2)
    
    # Save as pickle (for Python programs)  
    with open(f"{output_prefix}_defensive_scouting.pkl", 'wb') as f:
        pickle.dump(def_results, f)
    
    with open(f"{output_prefix}_offensive_scouting.pkl", 'wb') as f:
        pickle.dump(off_results, f)
    
    # Create combined analysis DataFrame
    combined_df = create_combined_analysis(def_results, off_results)
    combined_df.to_csv(f"{output_prefix}_scouting_summary.csv", index=False)
    
    print(f"✅ Saved scouting results:")
    print(f"   📄 {output_prefix}_defensive_scouting.json")
    print(f"   📄 {output_prefix}_offensive_scouting.json") 
    print(f"   🐍 {output_prefix}_defensive_scouting.pkl")
    print(f"   🐍 {output_prefix}_offensive_scouting.pkl")
    print(f"   📊 {output_prefix}_scouting_summary.csv")


def generate_team_specific_reports(def_results: Dict, off_results: Dict, 
                                 teams_to_scout: List[str], output_dir: str = "scouting_reports") -> None:
    """Generate individual scouting reports for specific teams."""
    
    reports_path = Path(output_dir)
    reports_path.mkdir(exist_ok=True)
    
    for team in teams_to_scout:
        report_lines = []
        report_lines.append(f"=== SCOUTING REPORT: {team} ===\n")
        
        # Defensive tendencies
        if team in def_results:
            report_lines.append("🛡️  DEFENSIVE TENDENCIES:")
            for personnel, plays in def_results[team].items():
                report_lines.append(f"\n  {personnel} Personnel:")
                for play, pct in sorted(plays.items(), key=lambda x: x[1], reverse=True):
                    report_lines.append(f"    • {play}: {pct:.1f}%")
        
        # Offensive tendencies  
        if team in off_results:
            report_lines.append("\n⚡ OFFENSIVE TENDENCIES:")
            for personnel, plays in off_results[team].items():
                report_lines.append(f"\n  {personnel} Personnel:")
                for play, pct in sorted(plays.items(), key=lambda x: x[1], reverse=True):
                    report_lines.append(f"    • {play}: {pct:.1f}%")
        
        # Save team report
        report_file = reports_path / f"{team}_scouting_report.txt"
        with open(report_file, 'w') as f:
            f.write('\n'.join(report_lines))
    
    print(f"📁 Generated individual reports in {output_dir}/")


def main():
    parser = argparse.ArgumentParser(description='Automated MFN Scouting Pipeline')
    parser.add_argument('--league', '-l', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--year', '-y', required=True, help='Season year (e.g., 2018)')
    parser.add_argument('--teams-file', help='Teams file (auto-detected if not provided)')
    parser.add_argument('--def-threshold', type=float, default=7.0, help='Defensive usage threshold % (default: 7.0)')
    parser.add_argument('--off-threshold', type=float, default=10.0, help='Offensive usage threshold % (default: 10.0)')
    parser.add_argument('--output-prefix', help='Output file prefix (auto-generated if not provided)')
    parser.add_argument('--scout-teams', nargs='*', help='Generate detailed reports for specific teams')
    
    args = parser.parse_args()
    
    # Auto-detect teams file if not provided
    if args.teams_file:
        teams_file = args.teams_file
    else:
        teams_file = f"{args.league}_{args.year}_teams.txt"
    
    # Auto-generate output prefix if not provided
    if args.output_prefix:
        output_prefix = args.output_prefix
    else:
        output_prefix = f"{args.league}_{args.year}"
    
    try:
        # Load teams
        print(f"📋 Loading teams from {teams_file}")
        teams = load_teams_from_file(teams_file)
        print(f"✅ Loaded {len(teams)} teams: {', '.join(teams[:5])}{'...' if len(teams) > 5 else ''}")
        
        # Load season data
        print(f"📊 Loading season data for {args.league} {args.year}")
        df = load_season_data(args.league, args.year)
        
        # Run defensive scouting
        def_results = run_defensive_scouting(df, teams, args.league, args.year, args.def_threshold)
        print(f"✅ Defensive scouting complete - analyzed {len(def_results)} teams")
        
        # Run offensive scouting  
        off_results = run_offensive_scouting(df, teams, args.league, args.year, args.off_threshold)
        print(f"✅ Offensive scouting complete - analyzed {len(off_results)} teams")
        
        # Save results
        save_results(def_results, off_results, output_prefix)
        
        # Generate team-specific reports if requested
        if args.scout_teams:
            generate_team_specific_reports(def_results, off_results, args.scout_teams)
        
        print("\n🎯 Next steps:")
        print(f"1. Review scouting summary: {output_prefix}_scouting_summary.csv")
        print(f"2. Use results in automated best plays analysis")
        print(f"3. Individual team reports available if --scout-teams was used")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())