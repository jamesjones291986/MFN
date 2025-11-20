"""
Configuration file for MFN Draft Analyzer
"""

import os
from pathlib import Path

# Google Sheets Configuration
GOOGLE_SHEETS_CONFIG = {
    # Path to your Google Service Account credentials JSON file
    'credentials_path': os.path.join(Path(__file__).parent, 'credentials.json'),
    
    # Google Sheets IDs for different draft data sources
    'sheet_ids': {
        'draft_prospects': '',  # Add your draft prospects sheet ID here
        'team_needs': '',       # Add team needs sheet ID here  
        'historical_data': '',  # Add historical draft data sheet ID here
    },
    
    # Worksheet names within the spreadsheets
    'worksheet_names': {
        'prospects': 'Draft Prospects',
        'team_needs': 'Team Needs',
        'scouting_reports': 'Scouting Reports',
        'player_stats': 'Player Stats'
    }
}

# Draft Analysis Settings
ANALYSIS_CONFIG = {
    'default_top_players': 100,
    'min_age': 18,
    'max_age': 28,
    
    # Position groupings for analysis
    'position_groups': {
        'offense': ['QB', 'RB', 'FB', 'WR', 'TE', 'OL', 'C', 'G', 'T'],
        'defense': ['DL', 'DE', 'DT', 'LB', 'MLB', 'OLB', 'DB', 'CB', 'S', 'FS', 'SS'],
        'special_teams': ['K', 'P', 'LS']
    },
    
    # Scoring thresholds for different grades
    'grade_thresholds': {
        'A+': 90,
        'A': 85, 
        'A-': 80,
        'B+': 75,
        'B': 70,
        'B-': 65,
        'C+': 60,
        'C': 55,
        'C-': 50,
        'D+': 45,
        'D': 40
    }
}

# Export Settings
EXPORT_CONFIG = {
    'default_format': 'csv',
    'output_directory': 'output',
    'include_raw_data': False,
    
    # CSV export columns
    'csv_columns': [
        'draft_rank', 'name', 'position', 'age', 'college', 'height', 'weight',
        'overall_score', 'draft_grade', 'projected_round',
        'physical_score', 'mental_score', 'position_score', 'size_score',
        'speed', 'acceleration', 'agility', 'strength', 'awareness', 'intelligence', 'durability'
    ]
}

# Validate configuration
def validate_config():
    """Validate that required configuration is present."""
    credentials_path = GOOGLE_SHEETS_CONFIG['credentials_path']
    
    if not os.path.exists(credentials_path):
        print(f"⚠️  Warning: Google credentials file not found at {credentials_path}")
        print("   Please ensure you have a valid service account JSON file.")
        return False
        
    return True