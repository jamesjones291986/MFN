#!/usr/bin/env python3
"""
MFN Lineup Analyzer - Automated Position Assignment System
Takes roster data and assigns optimal positions based on priority system.
"""

import pandas as pd
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from sheets_connector import LineupSheetsConnector


class LineupAnalyzer:
    """Analyzes roster and assigns optimal positions using priority system."""
    
    def __init__(self, sheet_id: str, verbose: bool = True):
        """Initialize the lineup analyzer."""
        self.sheet_id = sheet_id
        self.verbose = verbose
        self.connector = LineupSheetsConnector(verbose=verbose)
        
        # Position priority order (most important first) - 53 total roster spots
        self.position_priorities = [
            # Offense - QB and Skill Positions (16 spots)
            'QB', 'WR', 'RB', 'WR', 'TE', 'WR', 'RB', 'FB', 'WR', 'WR', 'RB', 'TE', 'WR', 'RB', 'QB', 'QB',
            # Offense - Starting Line (5 spots)
            'LT', 'RT', 'LG', 'C', 'RG',
            # Offense - Backup Line (5 spots)  
            'LT', 'RT', 'LG', 'C', 'RG',
            # Defense - Secondary & Core (22 spots)
            'CB', 'FS', 'SS', 'MLB', 'CB', 'CB', 'WLB', 'SLB', 'RDE', 'LDE', 'DT', 'DT',
            # Defense - Depth (11 spots)
            'CB', 'FS', 'SS', 'MLB', 'WLB', 'SLB', 'RDE', 'LDE', 'DT', 'CB', 'CB',
            # Special Teams (2 spots)
            'K', 'P'
        ]
        
        # Position column mappings from MaxFormulas sheet
        self.position_columns = {
            'QB': 'QB',
            'RB': 'RB', 
            'FB': 'FB',
            'TE': 'TE',
            'WR': 'WR',
            'LT': 'OT/G',    # Assuming OT/G covers tackle positions
            'RT': 'OT/G', 
            'LG': 'OT/G',    # Assuming OT/G covers guard positions  
            'RG': 'OT/G',
            'C': 'C',
            'CB': 'CB',
            'FS': 'FS',
            'SS': 'SS', 
            'MLB': 'MLB',
            'WLB': 'WLB',
            'SLB': 'SLB',
            'DE': 'DE',      # Will need to map RDE/LDE
            'RDE': 'DE',
            'LDE': 'DE', 
            'DT': 'DT',
            'K': 'K',
            'P': 'P'
        }
        
        # Position movement restrictions
        self.position_restrictions = {
            'CB': ['RDE', 'LDE', 'DT'],     # These positions cannot move to CB
            'FS': ['RDE', 'LDE', 'DT'],     # These positions cannot move to FS  
            'SS': ['RDE', 'LDE', 'DT'],     # These positions cannot move to SS
            'WR': ['TE'],                   # TE cannot move to WR
            # OL positions can only move within OL
            'LT': ['non-OL'], 'RT': ['non-OL'], 'LG': ['non-OL'], 'RG': ['non-OL'], 'C': ['non-OL']
        }
        
        # OL positions for restriction checking
        self.ol_positions = ['LT', 'RT', 'LG', 'RG', 'C']
        
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
            'SS': 'MaxSpeedMax',
            'K': 'KickAccuracyMax',
            'P': 'PuntStrengthMax'
        }
        
        # Skill display names
        self.skill_names = {
            'PassAccuracyMax': 'Pass Acc',
            'MaxSpeedMax': 'Speed',
            'StrengthMax': 'Strength', 
            'PassBlockingMax': 'Pass Block',
            'KickAccuracyMax': 'Kick Acc',
            'PuntStrengthMax': 'Punt Str'
        }
        
        # Data containers
        self.players_data = None
        self.position_ratings = None
        self.assigned_positions = {}
        self.available_players = []
        self.special_teams_analysis = {}
        
    def load_data(self):
        """Load player data and position ratings from Google Sheets."""
        if self.verbose:
            print("🔄 LOADING ROSTER DATA")
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
                      'SLB', 'MLB', 'WLB', 'CB', 'SS', 'FS', 'K', 'P']
        
        for col in rating_cols:
            if col in self.position_ratings.columns:
                self.position_ratings[col] = pd.to_numeric(self.position_ratings[col], errors='coerce')
        
        # Create available players list (all players initially)
        self.available_players = list(self.position_ratings['PlayerID'].unique())
        
        if self.verbose:
            print(f"📊 Prepared data for {len(self.available_players)} unique players")
            
    def _can_player_move_to_position(self, original_pos: str, target_pos: str) -> bool:
        """Check if a player can move from original position to target position."""
        # Handle OL restrictions - OL can only move within OL
        if target_pos in self.ol_positions:
            if original_pos not in self.ol_positions:
                return False
        elif original_pos in self.ol_positions:
            return False
            
        # Check specific position restrictions
        if target_pos in self.position_restrictions:
            restricted_from = self.position_restrictions[target_pos]
            if original_pos in restricted_from:
                return False
                
        return True
        
    def get_best_player_for_position(self, position: str) -> dict:
        """Find the best available player for a specific position."""
        if not self.available_players:
            return None
            
        # Get the column name for this position
        rating_column = self.position_columns.get(position)
        if not rating_column or rating_column not in self.position_ratings.columns:
            if self.verbose:
                print(f"⚠️ No rating column found for position {position}")
            return None
            
        # Filter to available players
        available_data = self.position_ratings[
            self.position_ratings['PlayerID'].isin(self.available_players)
        ].copy()
        
        if available_data.empty:
            return None
            
        # Apply position movement restrictions
        if position in self.position_restrictions or position in self.ol_positions:
            eligible_players = []
            for _, player in available_data.iterrows():
                if self._can_player_move_to_position(player['Pos'], position):
                    eligible_players.append(player.name)
            
            if not eligible_players:
                return None
                
            available_data = available_data.loc[eligible_players]
            
        # Find player with highest rating at this position
        best_idx = available_data[rating_column].idxmax()
        best_player = available_data.loc[best_idx]
        
        # Get the key skill for this position from player data
        key_skill_column = self.position_key_skills.get(position, 'MaxSpeedMax')
        key_skill_value = 'N/A'
        
        # Look up the key skill value in the original player data
        if self.players_data is not None:
            player_row = self.players_data[self.players_data['PlayerID'] == best_player['PlayerID']]
            if not player_row.empty and key_skill_column in player_row.columns:
                key_skill_value = player_row.iloc[0][key_skill_column]
        
        return {
            'player_id': best_player['PlayerID'],
            'first_name': best_player['FirstName'],
            'last_name': best_player['LastName'],
            'original_position': best_player['Pos'],
            'assigned_position': position,
            'rating': best_player[rating_column],
            'key_skill': key_skill_value,
            'key_skill_name': self.skill_names.get(key_skill_column, 'Skill')
        }
        
    def assign_positions(self):
        """Assign positions to all players based on priority system."""
        if self.verbose:
            print("\n🏈 ASSIGNING OPTIMAL POSITIONS")
            print("=" * 50)
            
        self.assigned_positions = {}
        assignment_number = 1
        
        for position in self.position_priorities:
            # Get position with number (e.g., WR1, WR2, etc.)
            position_counts = {}
            for assigned_pos in self.assigned_positions.values():
                base_pos = assigned_pos['assigned_position']
                position_counts[base_pos] = position_counts.get(base_pos, 0) + 1
                
            position_number = position_counts.get(position, 0) + 1
            
            # Special handling for K and P - no numbers
            if position in ['K', 'P']:
                position_name = position
            else:
                position_name = f"{position}{position_number}"
            
            # Find best available player
            best_player = self.get_best_player_for_position(position)
            
            if best_player:
                # Assign this player
                best_player['position_name'] = position_name
                best_player['priority_rank'] = assignment_number
                self.assigned_positions[position_name] = best_player
                
                # Remove from available players
                self.available_players.remove(best_player['player_id'])
                
                if self.verbose:
                    name = f"{best_player['first_name']} {best_player['last_name']}"
                    rating = best_player['rating']
                    orig_pos = best_player['original_position']
                    key_skill = best_player.get('key_skill', 'N/A')
                    skill_name = best_player.get('key_skill_name', 'Skill')
                    print(f"  {assignment_number:2d}. {position_name:<4} - {name:<25} ({orig_pos}) - {rating:.1f} overall - {key_skill} {skill_name}")
                    
                assignment_number += 1
            else:
                if self.verbose:
                    print(f"  ⚠️  No available players for {position_name}")
                    
        if self.verbose:
            print(f"\n✅ Assigned {len(self.assigned_positions)} positions")
            remaining = len(self.available_players)
            if remaining > 0:
                print(f"📋 {remaining} players remain unassigned (depth/practice squad)")
                
    def analyze_special_teams(self):
        """Analyze special teams positions: Long Snapper, Kick/Punt Returns, Kick Holder."""
        if self.verbose:
            print("\n🏈 SPECIAL TEAMS ANALYSIS")
            print("=" * 50)
            
        # Special teams columns from MaxFormulas
        st_columns = {
            'long_snapper': 'L Snp',
            'kick_returner': 'KR', 
            'punt_returner': 'PR',
            'kick_holder': 'K Hld'
        }
        
        self.special_teams_analysis = {}
        
        # Get all available data (including assigned players for ST roles)
        all_data = self.position_ratings.copy()
        
        for st_role, column in st_columns.items():
            if column in all_data.columns:
                # Convert to numeric
                all_data[column] = pd.to_numeric(all_data[column], errors='coerce')
                
                # Sort by rating and get top performers
                top_players = all_data.nlargest(3, column)
                
                role_results = []
                for _, player in top_players.iterrows():
                    role_results.append({
                        'name': f"{player['FirstName']} {player['LastName']}",
                        'original_position': player['Pos'],
                        'rating': player[column],
                        'player_id': player['PlayerID']
                    })
                
                self.special_teams_analysis[st_role] = role_results
                
                if self.verbose:
                    print(f"\n{st_role.replace('_', ' ').title()}:")
                    for i, player in enumerate(role_results, 1):
                        name = player['name']
                        pos = player['original_position']
                        rating = player['rating']
                        print(f"  {i}. {name:<25} ({pos}) - {rating:.1f}")
            else:
                if self.verbose:
                    print(f"⚠️ Column '{column}' not found for {st_role}")
                
    def generate_depth_chart(self) -> dict:
        """Generate organized depth chart by position group."""
        depth_chart = {
            'Offense': {
                'Quarterbacks': [],
                'Running Backs': [],
                'Wide Receivers': [],
                'Tight Ends': [],
                'Offensive Line': []
            },
            'Defense': {
                'Defensive Backs': [],
                'Linebackers': [],
                'Defensive Line': []
            },
            'Special Teams': {
                'Kickers': [],
                'Punters': []
            }
        }
        
        # Group positions
        position_groups = {
            'QB': ('Offense', 'Quarterbacks'),
            'RB': ('Offense', 'Running Backs'),
            'FB': ('Offense', 'Running Backs'),
            'WR': ('Offense', 'Wide Receivers'),
            'TE': ('Offense', 'Tight Ends'),
            'LT': ('Offense', 'Offensive Line'),
            'LG': ('Offense', 'Offensive Line'),
            'C': ('Offense', 'Offensive Line'),
            'RG': ('Offense', 'Offensive Line'),
            'RT': ('Offense', 'Offensive Line'),
            'CB': ('Defense', 'Defensive Backs'),
            'FS': ('Defense', 'Defensive Backs'),
            'SS': ('Defense', 'Defensive Backs'),
            'MLB': ('Defense', 'Linebackers'),
            'WLB': ('Defense', 'Linebackers'),
            'SLB': ('Defense', 'Linebackers'),
            'DE': ('Defense', 'Defensive Line'),
            'RDE': ('Defense', 'Defensive Line'),
            'LDE': ('Defense', 'Defensive Line'),
            'DT': ('Defense', 'Defensive Line'),
            'K': ('Special Teams', 'Kickers'),
            'P': ('Special Teams', 'Punters')
        }
        
        # Sort assignments by priority rank
        sorted_assignments = sorted(
            self.assigned_positions.items(),
            key=lambda x: x[1]['priority_rank']
        )
        
        # Add to appropriate groups
        for position_name, player in sorted_assignments:
            base_position = player['assigned_position']
            if base_position in position_groups:
                section, group = position_groups[base_position]
                depth_chart[section][group].append({
                    'position': position_name,
                    'name': f"{player['first_name']} {player['last_name']}",
                    'original_pos': player['original_position'],
                    'rating': player['rating'],
                    'priority': player['priority_rank']
                })
                
        return depth_chart
        
    def print_depth_chart(self):
        """Print formatted depth chart."""
        depth_chart = self.generate_depth_chart()
        
        print("\n🏈 OPTIMIZED DEPTH CHART")
        print("=" * 60)
        
        for section_name, section in depth_chart.items():
            print(f"\n📋 {section_name.upper()}")
            print("-" * 30)
            
            for group_name, players in section.items():
                if players:  # Only show groups with assigned players
                    print(f"\n{group_name}:")
                    for player in players:
                        name = player['name']
                        pos = player['position']
                        orig = player['original_pos']
                        rating = player['rating']
                        priority = player['priority']
                        # Find the corresponding assigned player to get key skill info
                        assigned_player = self.assigned_positions.get(pos, {})
                        key_skill = assigned_player.get('key_skill', 'N/A')
                        skill_name = assigned_player.get('key_skill_name', 'Skill')
                        print(f"  {priority:2d}. {pos:<4} - {name:<20} ({orig}) - {rating:.1f} - {key_skill} {skill_name}")
                        
    def export_to_sheets(self, tab_name: str = "Optimal Lineup"):
        """Export results to a new tab in Google Sheets."""
        if self.verbose:
            print(f"\n📤 EXPORTING TO GOOGLE SHEETS")
            print("=" * 50)
            
        try:
            # Prepare export data
            export_data = []
            
            # Sort assignments by priority rank
            sorted_assignments = sorted(
                self.assigned_positions.items(),
                key=lambda x: x[1]['priority_rank']
            )
            
            # Define complete position order
            position_order = ['QB', 'RB', 'FB', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 
                            'LDE', 'DT', 'RDE', 'SLB', 'MLB', 'WLB', 'CB', 'FS', 'SS', 'K', 'P']
            
            # Group players by position
            positions_dict = {}
            for position_name, player in sorted_assignments:
                pos_base = player['assigned_position']
                if pos_base not in positions_dict:
                    positions_dict[pos_base] = []
                positions_dict[pos_base].append((position_name, player))
            
            # Sort players within each position by number
            for pos_base in positions_dict:
                positions_dict[pos_base].sort(key=lambda x: int(x[0].replace(pos_base, '')) if x[0].replace(pos_base, '').isdigit() else 1)
            
            # Export each position as its own section
            first_section = True
            for pos_base in position_order:
                if pos_base in positions_dict:
                    players = positions_dict[pos_base]
                    
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
                        'SS': 'STRONG SAFETIES',
                        'K': 'KICKERS',
                        'P': 'PUNTERS'
                    }.get(pos_base, pos_base)
                    
                    export_data.append([pos_display_name, "", "", "", "", ""])
                    export_data.append([
                        "Priority", "Position", "Player Name", "Original Pos", 
                        "Overall Rating", "Key Skill"
                    ])
                    
                    # Add players for this position
                    for position_name, player in players:
                        export_data.append([
                            player['priority_rank'],
                            position_name,
                            f"{player['first_name']} {player['last_name']}",
                            player['original_position'],
                            float(player['rating']) if player['rating'] != 'N/A' else 0,
                            f"{player.get('key_skill', 'N/A')} ({player.get('key_skill_name', 'Skill')})"
                        ])
            
            # SPECIAL TEAMS SPECIALISTS
            export_data.append(["", "", "", "", "", ""])
            export_data.append(["ST SPECIALISTS", "", "", "", "", ""])
            export_data.append(["", "", "", "", "", ""])
            
            for st_role, players in self.special_teams_analysis.items():
                export_data.append([st_role.replace('_', ' ').title(), "", "", "", "", ""])
                for i, player in enumerate(players, 1):
                    export_data.append([
                        f"#{i}",
                        "",
                        player['name'],
                        player['original_position'],
                        float(player['rating']) if player['rating'] != 'N/A' else 0,
                        ""
                    ])
                export_data.append(["", "", "", "", "", ""])
            
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
            # Define all position section headers
            position_headers = [
                'QUARTERBACKS', 'RUNNING BACKS', 'FULLBACKS', 'WIDE RECEIVERS', 'TIGHT ENDS',
                'LEFT TACKLES', 'LEFT GUARDS', 'CENTERS', 'RIGHT GUARDS', 'RIGHT TACKLES',
                'LEFT DEFENSIVE ENDS', 'DEFENSIVE TACKLES', 'RIGHT DEFENSIVE ENDS', 
                'STRONG LINEBACKERS', 'MIDDLE LINEBACKERS', 'WEAK LINEBACKERS',
                'CORNERBACKS', 'FREE SAFETIES', 'STRONG SAFETIES', 'KICKERS', 'PUNTERS',
                'ST SPECIALISTS'
            ]
            
            # Find section header rows
            for i, row in enumerate(export_data):
                if row and row[0] in position_headers:
                    # Format section headers
                    cell_range = f'A{i+1}:F{i+1}'
                    worksheet.format(cell_range, {
                        'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                        'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True}
                    })
                elif row and row[0] == 'Priority':
                    # Format column headers
                    cell_range = f'A{i+1}:F{i+1}'
                    worksheet.format(cell_range, {
                        'backgroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8},
                        'textFormat': {'bold': True}
                    })
            
            if self.verbose:
                print(f"✅ Successfully exported {len(sorted_assignments)} positions to '{tab_name}'")
                
        except Exception as e:
            print(f"❌ Failed to export to Google Sheets: {e}")
            
    def run_analysis(self, export_to_sheets: bool = True):
        """Run complete lineup analysis."""
        if self.verbose:
            print("🚀 STARTING MFN LINEUP ANALYSIS")
            print("=" * 60)
            
        # Load data
        self.load_data()
        
        # Assign positions
        self.assign_positions()
        
        # Analyze special teams
        self.analyze_special_teams()
        
        # Display results
        self.print_depth_chart()
        
        # Export to Google Sheets
        if export_to_sheets:
            self.export_to_sheets()
        
        if self.verbose:
            print(f"\n✅ Analysis complete! {len(self.assigned_positions)} positions assigned.")
            

if __name__ == "__main__":
    # Run the lineup analyzer
    sheet_id = "12D_Kxx1hqPgsJ9qQtkY_zAYigGtUnz7F9uznpKK131s"
    
    analyzer = LineupAnalyzer(sheet_id, verbose=True)
    analyzer.run_analysis()