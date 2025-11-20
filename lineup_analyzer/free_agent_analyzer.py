#!/usr/bin/env python3
"""
MFN Free Agent Analyzer - Top 5 Players Per Position
Analyzes large pool of available players and finds top 5 at each position.
"""

import pandas as pd
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from sheets_connector import LineupSheetsConnector


class FreeAgentAnalyzer:
    """Analyzes free agents and finds top 5 players at each position."""
    
    def __init__(self, sheet_id: str, verbose: bool = True):
        """Initialize the free agent analyzer."""
        self.sheet_id = sheet_id
        self.verbose = verbose
        self.connector = LineupSheetsConnector(verbose=verbose)
        
        # Positions to analyze (excluding K and P)
        self.positions = ['QB', 'RB', 'FB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 
                         'LDE', 'DT', 'RDE', 'SLB', 'MLB', 'WLB', 'CB', 'FS', 'SS']
        
        # Position column mappings from MaxFormulas sheet
        self.position_columns = {
            'QB': 'QB',
            'RB': 'RB', 
            'FB': 'FB',
            'TE': 'TE',
            'WR': 'WR',
            'LT': 'OT/G',
            'RT': 'OT/G', 
            'LG': 'OT/G',
            'RG': 'OT/G',
            'C': 'C',
            'CB': 'CB',
            'FS': 'FS',
            'SS': 'SS', 
            'MLB': 'MLB',
            'WLB': 'WLB',
            'SLB': 'SLB',
            'DE': 'DE',
            'RDE': 'DE',
            'LDE': 'DE', 
            'DT': 'DT'
        }
        
        # Position-specific key skills mapping
        self.position_key_skills = {
            'QB': 'PassAccuracyMax',
            'RB': 'MaxSpeedMax',
            'FB': 'MaxSpeedMax', 
            'WR': 'MaxSpeedMax',
            'TE': 'MaxSpeedMax',
            'LT': 'PassBlockingMax',
            'LG': 'PassBlockingMax',
            'C': 'PassBlockingMax',
            'RG': 'PassBlockingMax',
            'RT': 'PassBlockingMax',
            'LDE': 'MaxSpeedMax',
            'DT': 'StrengthMax',
            'RDE': 'MaxSpeedMax',
            'SLB': 'MaxSpeedMax',
            'MLB': 'MaxSpeedMax',
            'WLB': 'MaxSpeedMax',
            'CB': 'MaxSpeedMax',
            'FS': 'MaxSpeedMax',
            'SS': 'MaxSpeedMax'
        }
        
        # Skill display names
        self.skill_names = {
            'PassAccuracyMax': 'Pass Acc',
            'MaxSpeedMax': 'Speed',
            'StrengthMax': 'Strength', 
            'PassBlockingMax': 'Pass Block'
        }
        
        # Data containers
        self.players_data = None
        self.position_ratings = None
        self.top_players = {}
        
    def load_data(self):
        """Load player data and position ratings from Google Sheets."""
        if self.verbose:
            print("🔄 LOADING FREE AGENT DATA")
            print("=" * 50)
            
        # Load player base information
        self.players_data = self.connector.get_worksheet_data(self.sheet_id, "Player Import")
        
        # Load position ratings 
        self.position_ratings = self.connector.get_worksheet_data(self.sheet_id, "MaxFormulas")
        
        # Clean and prepare data
        self._prepare_data()
        
        if self.verbose:
            print(f"✅ Loaded {len(self.players_data)} players")
            print(f"✅ Loaded position ratings for {len(self.position_ratings)} player evaluations")
            
    def _prepare_data(self):
        """Clean and prepare the loaded data."""
        # Convert rating columns to numeric
        rating_cols = ['QB', 'RB', 'FB', 'TE', 'WR', 'OT/G', 'C', 'DE', 'DT', 
                      'SLB', 'MLB', 'WLB', 'CB', 'SS', 'FS']
        
        for col in rating_cols:
            if col in self.position_ratings.columns:
                self.position_ratings[col] = pd.to_numeric(self.position_ratings[col], errors='coerce')
        
        if self.verbose:
            print(f"📊 Prepared data for {len(self.position_ratings)} players")
            
    def get_top_players_for_position(self, position: str, top_n: int = 5) -> list:
        """Find the top N players for a specific position."""
        # Get the column name for this position
        rating_column = self.position_columns.get(position)
        if not rating_column or rating_column not in self.position_ratings.columns:
            if self.verbose:
                print(f"⚠️ No rating column found for position {position}")
            return []
            
        # Get all players and their ratings for this position
        position_data = self.position_ratings.copy()
        
        # Remove players with NaN ratings
        position_data = position_data.dropna(subset=[rating_column])
        
        if position_data.empty:
            return []
            
        # Sort by rating (highest first) and get top N
        top_players_data = position_data.nlargest(top_n, rating_column)
        
        top_players = []
        for _, player in top_players_data.iterrows():
            # Get the key skill for this position from player data
            key_skill_column = self.position_key_skills.get(position, 'MaxSpeedMax')
            key_skill_value = 'N/A'
            
            # Look up the key skill value and overall rating in the original player data
            if self.players_data is not None:
                player_row = self.players_data[self.players_data['PlayerID'] == player['PlayerID']]
                if not player_row.empty:
                    if key_skill_column in player_row.columns:
                        key_skill_value = player_row.iloc[0][key_skill_column]
            
            player_info = {
                'player_id': player['PlayerID'],
                'first_name': player['FirstName'],
                'last_name': player['LastName'],
                'original_position': player['Pos'],
                'position_rating': player[rating_column],
                'key_skill': key_skill_value,
                'key_skill_name': self.skill_names.get(key_skill_column, 'Skill')
            }
            top_players.append(player_info)
            
        return top_players
        
    def analyze_all_positions(self):
        """Analyze all positions and find top 5 players for each."""
        if self.verbose:
            print("\n🏈 ANALYZING FREE AGENT MARKET")
            print("=" * 50)
            
        self.top_players = {}
        
        for position in self.positions:
            top_5 = self.get_top_players_for_position(position, 5)
            self.top_players[position] = top_5
            
            if self.verbose:
                print(f"\n📊 Top 5 {position}:")
                for i, player in enumerate(top_5, 1):
                    name = f"{player['first_name']} {player['last_name']}"
                    rating = player['position_rating']
                    orig_pos = player['original_position']
                    key_skill = player.get('key_skill', 'N/A')
                    skill_name = player.get('key_skill_name', 'Skill')
                    print(f"  {i}. {name:<25} ({orig_pos}) - {rating:.1f} - {key_skill} {skill_name}")
                    
        if self.verbose:
            total_players = sum(len(players) for players in self.top_players.values())
            print(f"\n✅ Analysis complete! Found top 5 players for {len(self.positions)} positions ({total_players} total players)")
            
    def generate_position_report(self) -> dict:
        """Generate organized report by position group."""
        report = {
            'Offense': {
                'Quarterbacks': self.top_players.get('QB', []),
                'Running Backs': self.top_players.get('RB', []) + self.top_players.get('FB', []),
                'Wide Receivers': self.top_players.get('WR', []),
                'Tight Ends': self.top_players.get('TE', []),
                'Offensive Line': (self.top_players.get('LT', []) + self.top_players.get('LG', []) + 
                                 self.top_players.get('C', []) + self.top_players.get('RG', []) + 
                                 self.top_players.get('RT', []))
            },
            'Defense': {
                'Defensive Backs': (self.top_players.get('CB', []) + self.top_players.get('FS', []) + 
                                  self.top_players.get('SS', [])),
                'Linebackers': (self.top_players.get('MLB', []) + self.top_players.get('WLB', []) + 
                              self.top_players.get('SLB', [])),
                'Defensive Line': (self.top_players.get('LDE', []) + self.top_players.get('DT', []) + 
                                 self.top_players.get('RDE', []))
            }
        }
        
        return report
        
    def print_position_report(self):
        """Print formatted position report."""
        report = self.generate_position_report()
        
        print("\n🏈 FREE AGENT ANALYSIS REPORT")
        print("=" * 60)
        
        for section_name, section in report.items():
            print(f"\n📋 {section_name.upper()}")
            print("-" * 30)
            
            for group_name, players in section.items():
                if players:
                    print(f"\n{group_name}:")
                    # Sort by position rating
                    sorted_players = sorted(players, key=lambda x: x['position_rating'], reverse=True)
                    for i, player in enumerate(sorted_players[:15], 1):  # Show top 15 for combined groups
                        name = f"{player['first_name']} {player['last_name']}"
                        pos = player['original_position']
                        rating = player['position_rating']
                        key_skill = player.get('key_skill', 'N/A')
                        skill_name = player.get('key_skill_name', 'Skill')
                        print(f"  {i:2d}. {name:<20} ({pos}) - {rating:.1f} - {key_skill} {skill_name}")
                        
    def export_to_sheets(self, tab_name: str = "Free Agent Analysis"):
        """Export results to a new tab in Google Sheets."""
        if self.verbose:
            print(f"\n📤 EXPORTING TO GOOGLE SHEETS")
            print("=" * 50)
            
        try:
            # Prepare export data
            export_data = []
            
            # Define position order for export
            position_order = ['QB', 'RB', 'FB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 
                            'LDE', 'DT', 'RDE', 'SLB', 'MLB', 'WLB', 'CB', 'FS', 'SS']
            
            # Export each position as its own section
            first_section = True
            for position in position_order:
                if position in self.top_players and self.top_players[position]:
                    players = self.top_players[position]
                    
                    # Add spacing between sections (except first)
                    if not first_section:
                        export_data.append(["", "", "", "", "", ""])
                    first_section = False
                    
                    # Position header
                    pos_display_name = {
                        'QB': 'QUARTERBACKS',
                        'RB': 'RUNNING BACKS', 
                        'FB': 'FULLBACKS',
                        'WR': 'WIDE RECEIVERS',
                        'TE': 'TIGHT ENDS',
                        'LT': 'LEFT TACKLES',
                        'LG': 'LEFT GUARDS',
                        'C': 'CENTERS',
                        'RG': 'RIGHT GUARDS', 
                        'RT': 'RIGHT TACKLES',
                        'LDE': 'LEFT DEFENSIVE ENDS',
                        'DT': 'DEFENSIVE TACKLES',
                        'RDE': 'RIGHT DEFENSIVE ENDS',
                        'SLB': 'STRONG LINEBACKERS',
                        'MLB': 'MIDDLE LINEBACKERS',
                        'WLB': 'WEAK LINEBACKERS',
                        'CB': 'CORNERBACKS',
                        'FS': 'FREE SAFETIES',
                        'SS': 'STRONG SAFETIES'
                    }.get(position, position)
                    
                    export_data.append([pos_display_name, "", "", "", "", ""])
                    export_data.append([
                        "Rank", "Player Name", "Original Pos", "Position Rating", "Key Skill", ""
                    ])
                    
                    # Add top 5 players for this position
                    for i, player in enumerate(players, 1):
                        export_data.append([
                            i,
                            f"{player['first_name']} {player['last_name']}",
                            player['original_position'],
                            float(player['position_rating']) if player['position_rating'] != 'N/A' else 0,
                            f"{player.get('key_skill', 'N/A')} ({player.get('key_skill_name', 'Skill')})",
                            ""
                        ])
            
            # Get spreadsheet and delete/recreate worksheet
            spreadsheet = self.connector.get_sheet(self.sheet_id)
            
            try:
                # Delete existing worksheet if it exists
                existing_worksheet = spreadsheet.worksheet(tab_name)
                spreadsheet.del_worksheet(existing_worksheet)
                if self.verbose:
                    print(f"🗑️ Deleted existing '{tab_name}' tab")
            except:
                # Worksheet doesn't exist, that's fine
                pass
                
            # Create new worksheet
            worksheet = spreadsheet.add_worksheet(title=tab_name, rows=len(export_data)+10, cols=6)
            if self.verbose:
                print(f"📝 Created new '{tab_name}' tab")
            
            # Upload data
            worksheet.update('A1', export_data)
            
            # Format section headers and column headers
            position_headers = [
                'QUARTERBACKS', 'RUNNING BACKS', 'FULLBACKS', 'WIDE RECEIVERS', 'TIGHT ENDS',
                'LEFT TACKLES', 'LEFT GUARDS', 'CENTERS', 'RIGHT GUARDS', 'RIGHT TACKLES',
                'LEFT DEFENSIVE ENDS', 'DEFENSIVE TACKLES', 'RIGHT DEFENSIVE ENDS', 
                'STRONG LINEBACKERS', 'MIDDLE LINEBACKERS', 'WEAK LINEBACKERS',
                'CORNERBACKS', 'FREE SAFETIES', 'STRONG SAFETIES'
            ]
            
            # Find section header rows and format them
            for i, row in enumerate(export_data):
                if row and row[0] in position_headers:
                    # Format section headers
                    cell_range = f'A{i+1}:F{i+1}'
                    worksheet.format(cell_range, {
                        'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                        'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True}
                    })
                elif row and row[0] == 'Rank':
                    # Format column headers
                    cell_range = f'A{i+1}:F{i+1}'
                    worksheet.format(cell_range, {
                        'backgroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8},
                        'textFormat': {'bold': True}
                    })
            
            total_players = sum(len(players) for players in self.top_players.values())
            if self.verbose:
                print(f"✅ Successfully exported {total_players} players to '{tab_name}'")
                
        except Exception as e:
            print(f"❌ Failed to export to Google Sheets: {e}")
            
    def run_analysis(self, export_to_sheets: bool = True):
        """Run complete free agent analysis."""
        if self.verbose:
            print("🚀 STARTING FREE AGENT ANALYSIS")
            print("=" * 60)
            
        # Load data
        self.load_data()
        
        # Analyze all positions
        self.analyze_all_positions()
        
        # Display results
        self.print_position_report()
        
        # Export to Google Sheets
        if export_to_sheets:
            self.export_to_sheets()
        
        total_players = sum(len(players) for players in self.top_players.values())
        if self.verbose:
            print(f"\n✅ Free agent analysis complete! Analyzed {len(self.positions)} positions, found {total_players} top players.")
            

if __name__ == "__main__":
    # Run the free agent analyzer
    sheet_id = "12D_Kxx1hqPgsJ9qQtkY_zAYigGtUnz7F9uznpKK131s"
    
    analyzer = FreeAgentAnalyzer(sheet_id, verbose=True)
    analyzer.run_analysis()