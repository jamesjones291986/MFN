"""
Google Sheets Connector for MFN Draft Analyzer
Handles authentication and data loading from Google Sheets
"""

import gspread
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
from google.oauth2.service_account import Credentials

from config import GOOGLE_SHEETS_CONFIG


class SheetsConnector:
    """Handles Google Sheets authentication and data operations."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the sheets connector."""
        self.verbose = verbose
        self.client = None
        self._authenticate()
        
    def _authenticate(self):
        """Authenticate with Google Sheets API."""
        try:
            credentials_path = GOOGLE_SHEETS_CONFIG['credentials_path']
            
            if not Path(credentials_path).exists():
                raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
                
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Load credentials and create client
            credentials = Credentials.from_service_account_file(credentials_path, scopes=scope)
            self.client = gspread.authorize(credentials)
            
            if self.verbose:
                print("✅ Successfully authenticated with Google Sheets")
                
        except Exception as e:
            print(f"❌ Failed to authenticate with Google Sheets: {e}")
            self.client = None
            
    def load_draft_prospects(self, sheet_id: str = None, worksheet_name: str = None) -> List[Dict]:
        """Load draft prospects from Google Sheets."""
        if not self.client:
            raise ConnectionError("Not authenticated with Google Sheets")
            
        try:
            # Use provided sheet_id or default from config
            if not sheet_id:
                sheet_id = GOOGLE_SHEETS_CONFIG['sheet_ids']['draft_prospects']
                if not sheet_id:
                    raise ValueError("No draft prospects sheet ID configured")
                    
            # Use provided worksheet name or default
            if not worksheet_name:
                worksheet_name = GOOGLE_SHEETS_CONFIG['worksheet_names']['prospects']
                
            if self.verbose:
                print(f"Loading draft prospects from sheet: {sheet_id}")
                
            # Open the spreadsheet and worksheet
            spreadsheet = self.client.open_by_key(sheet_id)
            worksheet = spreadsheet.worksheet(worksheet_name)
            
            # Get all data as list of dictionaries
            data = worksheet.get_all_records()
            
            if self.verbose:
                print(f"Loaded {len(data)} prospects from Google Sheets")
                
            return data
            
        except Exception as e:
            print(f"❌ Error loading draft prospects: {e}")
            return []
            
    def load_team_needs(self, sheet_id: str = None, worksheet_name: str = None) -> Dict[str, List[str]]:
        """Load team needs from Google Sheets."""
        if not self.client:
            raise ConnectionError("Not authenticated with Google Sheets")
            
        try:
            if not sheet_id:
                sheet_id = GOOGLE_SHEETS_CONFIG['sheet_ids']['team_needs']
                if not sheet_id:
                    if self.verbose:
                        print("No team needs sheet configured, using defaults")
                    return {}
                    
            if not worksheet_name:
                worksheet_name = GOOGLE_SHEETS_CONFIG['worksheet_names']['team_needs']
                
            if self.verbose:
                print(f"Loading team needs from sheet: {sheet_id}")
                
            spreadsheet = self.client.open_by_key(sheet_id)
            worksheet = spreadsheet.worksheet(worksheet_name)
            
            # Get all data
            data = worksheet.get_all_records()
            
            # Convert to team -> positions mapping
            team_needs = {}
            for row in data:
                team = row.get('Team', '').strip()
                positions = []
                
                # Look for position columns (Position1, Position2, etc. or comma-separated)
                for key, value in row.items():
                    if 'position' in key.lower() and value:
                        if ',' in str(value):
                            # Handle comma-separated positions
                            positions.extend([pos.strip() for pos in str(value).split(',')])
                        else:
                            positions.append(str(value).strip())
                            
                if team and positions:
                    team_needs[team] = positions
                    
            if self.verbose:
                print(f"Loaded needs for {len(team_needs)} teams")
                
            return team_needs
            
        except Exception as e:
            print(f"❌ Error loading team needs: {e}")
            return {}
            
    def export_draft_board(self, players: List[Dict], sheet_id: str, worksheet_name: str = "Draft Board"):
        """Export draft board results to Google Sheets."""
        if not self.client:
            raise ConnectionError("Not authenticated with Google Sheets")
            
        try:
            if self.verbose:
                print(f"Exporting draft board to sheet: {sheet_id}")
                
            # Open spreadsheet
            spreadsheet = self.client.open_by_key(sheet_id)
            
            # Try to open existing worksheet or create new one
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
                # Clear existing content
                worksheet.clear()
            except gspread.WorksheetNotFound:
                # Create new worksheet
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=20)
                
            if not players:
                return
                
            # Prepare headers
            headers = [
                'Rank', 'Player Name', 'Position', 'Age', 'College', 'Height', 'Weight',
                'Overall Score', 'Draft Grade', 'Projected Round',
                'Physical Score', 'Mental Score', 'Position Score', 'Size Score',
                'Speed', 'Acceleration', 'Agility', 'Strength', 'Awareness', 'Intelligence', 'Durability'
            ]
            
            # Prepare data rows
            rows = [headers]
            
            for player in players:
                row = [
                    player.get('draft_rank', ''),
                    player.get('name', ''),
                    player.get('position', ''),
                    player.get('age', ''),
                    player.get('college', ''),
                    player.get('height', ''),
                    player.get('weight', ''),
                    round(player.get('overall_score', 0), 1),
                    player.get('draft_grade', ''),
                    player.get('projected_round', ''),
                    round(player.get('physical_score', 0), 1),
                    round(player.get('mental_score', 0), 1),
                    round(player.get('position_score', 0), 1),
                    round(player.get('size_score', 0), 1),
                    player.get('speed', ''),
                    player.get('acceleration', ''),
                    player.get('agility', ''),
                    player.get('strength', ''),
                    player.get('awareness', ''),
                    player.get('intelligence', ''),
                    player.get('durability', '')
                ]
                rows.append(row)
                
            # Update the worksheet with all data at once
            worksheet.update('A1', rows)
            
            # Format header row
            worksheet.format('A1:U1', {
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                'textFormat': {'bold': True}
            })
            
            if self.verbose:
                print(f"✅ Exported {len(players)} players to Google Sheets")
                
        except Exception as e:
            print(f"❌ Error exporting to Google Sheets: {e}")
            
    def load_scouting_reports(self, sheet_id: str = None, worksheet_name: str = None) -> Dict[str, Dict]:
        """Load detailed scouting reports for players."""
        if not self.client:
            raise ConnectionError("Not authenticated with Google Sheets")
            
        try:
            if not sheet_id:
                sheet_id = GOOGLE_SHEETS_CONFIG['sheet_ids']['draft_prospects']  # Same sheet, different tab
                
            if not worksheet_name:
                worksheet_name = GOOGLE_SHEETS_CONFIG['worksheet_names']['scouting_reports']
                
            if self.verbose:
                print(f"Loading scouting reports from sheet: {sheet_id}")
                
            spreadsheet = self.client.open_by_key(sheet_id)
            worksheet = spreadsheet.worksheet(worksheet_name)
            
            data = worksheet.get_all_records()
            
            # Convert to player_name -> report mapping
            reports = {}
            for row in data:
                player_name = row.get('Player Name', '').strip()
                if player_name:
                    reports[player_name] = row
                    
            if self.verbose:
                print(f"Loaded scouting reports for {len(reports)} players")
                
            return reports
            
        except Exception as e:
            if self.verbose:
                print(f"Note: Could not load scouting reports: {e}")
            return {}
            
    def test_connection(self) -> bool:
        """Test the Google Sheets connection."""
        if not self.client:
            return False
            
        try:
            # Try to access any configured sheet
            sheet_ids = GOOGLE_SHEETS_CONFIG['sheet_ids']
            for sheet_name, sheet_id in sheet_ids.items():
                if sheet_id:
                    spreadsheet = self.client.open_by_key(sheet_id)
                    if self.verbose:
                        print(f"✅ Successfully accessed {sheet_name} sheet")
                    return True
                    
            if self.verbose:
                print("⚠️  No sheet IDs configured to test")
            return False
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Connection test failed: {e}")
            return False