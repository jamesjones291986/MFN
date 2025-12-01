#!/usr/bin/env python3
"""
Target Percentage Analyzer
===========================

Analyzes target percentages for plays from team summary tabs or standard playbook.

Usage:
    # Analyze a specific team's summary tab
    python target_analyzer.py --team SJS --league USFL --season 2018
    
    # Analyze the standard playbook
    python target_analyzer.py --standard-playbook

Features:
- Reads plays from Google Sheets (team summary tabs or standard playbook)
- Applies target percentage analysis using MFN-Targets.csv
- Outputs results to terminal only (no Google Sheets export)
"""

import argparse
import csv
import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append('/Users/jamesjones/projects/mfn/scouting')
sys.path.append('/Users/jamesjones/projects/mfn/lineup_analyzer')

try:
    from sheets_connector import LineupSheetsConnector
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False
    print("⚠️  Google Sheets connector not available.")
    print("📦 Missing packages: gspread, google-auth, google-auth-oauthlib, google-auth-httplib2")
    print("💡 Install with: pip install gspread google-auth google-auth-oauthlib google-auth-httplib2")
    sys.exit(1)

from util import Config


class TargetAnalyzer:
    """Analyzes target percentages for offensive plays."""
    
    def __init__(self, sheets_id: str = None):
        """Initialize the target analyzer."""
        # Use provided sheets_id or default from config
        if sheets_id:
            self.sheets_id = sheets_id
        else:
            self.sheets_id = getattr(Config, 'GAMEPLAN_SHEET_ID', None)
        
        if not self.sheets_id:
            raise ValueError("No Google Sheets ID provided. Check Config.GAMEPLAN_SHEET_ID")
        
        # Initialize Google Sheets connector
        try:
            self.sheets_connector = LineupSheetsConnector(verbose=False)
            print(f"✅ Connected to Google Sheets: {self.sheets_id}")
        except Exception as e:
            raise ValueError(f"Failed to connect to Google Sheets: {e}")
        
        # Load targets data
        self.targets_file = "/Users/jamesjones/projects/mfn/scouting/MFN-Targets.csv"
        if not os.path.exists(self.targets_file):
            raise ValueError(f"Targets file not found: {self.targets_file}")
    
    def get_target_totals(self, play_names: List[str]) -> List[Tuple[str, int]]:
        """
        Calculate target percentages for a list of offensive plays.
        
        Args:
            play_names: List of offensive play names
            
        Returns:
            List of tuples (target_position, total_percentage) sorted by percentage desc
        """
        totals = {}
        
        with open(self.targets_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # If the play matches any in our list
                if row['OffensivePlay'] in play_names:
                    target = row['target']
                    # Remove % sign and convert to int
                    percentage = int(float(row['tgt %'].replace('%', '')))
                    
                    if target in totals:
                        totals[target] += percentage
                    else:
                        totals[target] = percentage
        
        # Sort by total percentage descending
        sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        return sorted_totals
    
    def get_plays_from_team_summary(self, team: str, league: str, season: int) -> Dict[str, List[str]]:
        """
        Get offensive plays from a team's summary tab, grouped by formation.
        
        Args:
            team: Team abbreviation (e.g., SJS)
            league: League name (e.g., USFL)  
            season: Season year (e.g., 2018)
            
        Returns:
            Dict mapping formation names to lists of offensive play names
        """
        try:
            # Get the spreadsheet
            spreadsheet = self.sheets_connector.get_sheet(self.sheets_id)
            
            # Construct summary tab name
            summary_tab_name = f"{team}_{league}_{season}_Summary"
            
            print(f"📋 Reading plays from summary tab: {summary_tab_name}")
            
            # Get the worksheet
            worksheet = spreadsheet.worksheet(summary_tab_name)
            
            # Get all data
            all_values = worksheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                raise ValueError(f"No data found in {summary_tab_name}")
            
            # Find the "Offensive Play" and "Personnel" columns
            headers = all_values[0]
            try:
                play_col_index = headers.index("Offensive Play")
            except ValueError:
                # Try alternative column names
                if "OffensivePlay" in headers:
                    play_col_index = headers.index("OffensivePlay")
                else:
                    raise ValueError(f"'Offensive Play' column not found in {summary_tab_name}. Available columns: {headers}")
            
            # Try to find Personnel column for formation grouping
            personnel_col_index = None
            try:
                personnel_col_index = headers.index("Personnel")
            except ValueError:
                pass
            
            # Group plays by formation
            formation_plays = {}
            total_plays = 0
            
            for row in all_values[1:]:
                if len(row) > play_col_index and row[play_col_index].strip():
                    play_name = row[play_col_index].strip()
                    
                    # Get formation/personnel info
                    if personnel_col_index and len(row) > personnel_col_index and row[personnel_col_index].strip():
                        formation = row[personnel_col_index].strip()
                    else:
                        # If no personnel column, try to infer from play name
                        formation = self._infer_formation_from_play_name(play_name)
                    
                    if formation not in formation_plays:
                        formation_plays[formation] = []
                    formation_plays[formation].append(play_name)
                    total_plays += 1
            
            print(f"✅ Found {total_plays} offensive plays in {summary_tab_name} across {len(formation_plays)} formations")
            return formation_plays
            
        except Exception as e:
            raise ValueError(f"Error reading team summary tab: {e}")
    
    def _infer_formation_from_play_name(self, play_name: str) -> str:
        """Infer formation type from play name."""
        play_lower = play_name.lower()
        
        if 'shotgun' in play_lower:
            if '5 wide' in play_lower:
                return 'Shotgun 5 Wide'
            elif '4 wide' in play_lower:
                return 'Shotgun 4 Wide' 
            elif '3 wide' in play_lower or '2 rb 3 wr' in play_lower:
                return 'Shotgun 2RB 3WR'
            else:
                return 'Shotgun Normal'
        elif 'singleback' in play_lower:
            if 'big' in play_lower:
                return 'Singleback Big'
            elif '4 wide' in play_lower:
                return 'Singleback 4 Wide'
            else:
                return 'Singleback Normal'
        elif 'i formation' in play_lower:
            if '3wr' in play_lower or '3 wr' in play_lower:
                return 'I Formation 3WR'
            elif 'twin wr' in play_lower:
                return 'I Formation Twin WR'
            elif 'power' in play_lower:
                return 'I Formation Power'
            else:
                return 'I Formation Normal'
        elif 'strong i' in play_lower:
            if 'big' in play_lower:
                return 'Strong I Big'
            else:
                return 'Strong I Normal'
        elif 'weak i' in play_lower:
            return 'Weak I Normal'
        elif 'split backs' in play_lower:
            return 'Split Backs 3 Wide'
        elif 'empty' in play_lower:
            return 'Empty 4 Wide'
        elif 'goal line' in play_lower:
            return 'Goal Line'
        else:
            return 'Unknown Formation'
    
    def get_plays_from_standard_playbook(self) -> Dict[str, List[str]]:
        """
        Get offensive plays from the standard playbook tab, grouped by formation.
        
        Returns:
            Dict mapping formation names to lists of offensive play names
        """
        try:
            # Get the spreadsheet
            spreadsheet = self.sheets_connector.get_sheet(self.sheets_id)
            
            print(f"📋 Reading plays from standard_playbook tab")
            
            # Get the worksheet
            worksheet = spreadsheet.worksheet('standard_playbook')
            
            # Get all data
            all_values = worksheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                raise ValueError("No data found in standard_playbook tab")
            
            # Debug: Show first few rows to understand structure
            print(f"🔍 First 5 rows of standard_playbook:")
            for i, row in enumerate(all_values[:5]):
                print(f"  Row {i}: {row}")
            
            # Look for the proper header row and data
            header_row_idx = None
            for i, row in enumerate(all_values):
                if 'Play Name' in row:
                    header_row_idx = i
                    break
            
            if header_row_idx is not None:
                headers = all_values[header_row_idx]
                play_col_index = headers.index('Play Name')
                
                # Try to find Formation column
                formation_col_index = None
                try:
                    formation_col_index = headers.index('Formation')
                except ValueError:
                    pass
                
                # Group plays by formation
                formation_plays = {}
                total_plays = 0
                
                for row in all_values[header_row_idx + 1:]:
                    if len(row) > play_col_index and row[play_col_index].strip():
                        play_name = row[play_col_index].strip()
                        # Remove numbering prefix (e.g., "1. " from "1. I Formation Twin WR Hard Slants")
                        if '. ' in play_name:
                            play_name = play_name.split('. ', 1)[1]
                        
                        # Get formation info
                        if formation_col_index and len(row) > formation_col_index and row[formation_col_index].strip():
                            formation = row[formation_col_index].strip()
                        else:
                            # Infer formation from play name
                            formation = self._infer_formation_from_play_name(play_name)
                        
                        if formation not in formation_plays:
                            formation_plays[formation] = []
                        formation_plays[formation].append(play_name)
                        total_plays += 1
                
                print(f"✅ Found {total_plays} offensive plays in standard_playbook across {len(formation_plays)} formations")
                return formation_plays
            
            # Fallback: try to find a proper header row
            headers = all_values[0]
            print(f"🔍 Available columns in standard_playbook: {headers}")
            try:
                play_col_index = headers.index("Offensive Play")
            except ValueError:
                # Try alternative column names
                if "OffensivePlay" in headers:
                    play_col_index = headers.index("OffensivePlay")
                else:
                    raise ValueError(f"'Offensive Play' column not found in standard_playbook. Available columns: {headers}")
            
            # Extract play names (skip header row)
            plays = []
            for row in all_values[1:]:
                if len(row) > play_col_index and row[play_col_index].strip():
                    plays.append(row[play_col_index].strip())
            
            print(f"✅ Found {len(plays)} offensive plays in standard_playbook")
            return plays
            
        except Exception as e:
            raise ValueError(f"Error reading standard playbook: {e}")
    
    def analyze_team_targets(self, team: str, league: str, season: int):
        """Analyze target percentages for a specific team."""
        print(f"🎯 TARGET ANALYSIS: {team} ({league} {season})")
        print("=" * 60)
        
        # Get plays from team summary, grouped by formation
        formation_plays = self.get_plays_from_team_summary(team, league, season)
        
        if not formation_plays:
            print("⚠️  No plays found for analysis")
            return
        
        # Analyze targets for each formation
        total_plays = sum(len(plays) for plays in formation_plays.values())
        print(f"\n📊 TARGET BREAKDOWN BY FORMATION:")
        print(f"Based on {total_plays} offensive plays from {team}")
        print("=" * 60)
        
        for formation, plays in formation_plays.items():
            if not plays:
                continue
                
            print(f"\n{formation}:")
            target_totals = self.get_target_totals(plays)
            
            if target_totals:
                for position, total_percentage in target_totals:
                    print(f"  Total for {position} is {total_percentage}")
            else:
                print("  ⚠️  No target data found for these plays")
            
        print("")  # Extra line at end
    
    def analyze_standard_playbook_targets(self):
        """Analyze target percentages for the standard playbook."""
        print(f"🎯 TARGET ANALYSIS: Standard Playbook")
        print("=" * 60)
        
        # Get plays from standard playbook, grouped by formation
        formation_plays = self.get_plays_from_standard_playbook()
        
        if not formation_plays:
            print("⚠️  No plays found for analysis")
            return
        
        # Analyze targets for each formation
        total_plays = sum(len(plays) for plays in formation_plays.values())
        print(f"\n📊 TARGET BREAKDOWN BY FORMATION:")
        print(f"Based on {total_plays} offensive plays from standard playbook")
        print("=" * 60)
        
        for formation, plays in formation_plays.items():
            if not plays:
                continue
                
            print(f"\n{formation}:")
            target_totals = self.get_target_totals(plays)
            
            if target_totals:
                for position, total_percentage in target_totals:
                    print(f"  Total for {position} is {total_percentage}")
            else:
                print("  ⚠️  No target data found for these plays")
            
        print("")  # Extra line at end


def main():
    """Main function to run the target analyzer."""
    parser = argparse.ArgumentParser(description='Analyze target percentages for offensive plays')
    parser.add_argument('--team', help='Team abbreviation (e.g., SJS)')
    parser.add_argument('--league', help='League name (e.g., USFL)')
    parser.add_argument('--season', type=int, help='Season year (e.g., 2018)')
    parser.add_argument('--standard-playbook', action='store_true', help='Analyze standard playbook instead of team')
    parser.add_argument('--sheets-id', help='Google Sheets ID (optional)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.standard_playbook:
        if args.team or args.league or args.season:
            print("Error: Cannot use --team, --league, or --season with --standard-playbook")
            return 1
    else:
        if not args.team or not args.league or not args.season:
            print("Error: Must specify --team, --league, and --season (or use --standard-playbook)")
            return 1
    
    try:
        # Initialize analyzer
        analyzer = TargetAnalyzer(sheets_id=args.sheets_id)
        
        # Run analysis
        if args.standard_playbook:
            analyzer.analyze_standard_playbook_targets()
        else:
            analyzer.analyze_team_targets(args.team, args.league, args.season)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())