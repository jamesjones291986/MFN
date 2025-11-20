"""
Data Processor - Handles loading and cleaning draft player data
"""

import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional


class DataProcessor:
    """Processes and cleans draft-eligible player data."""
    
    def __init__(self, file_path: str, verbose: bool = False):
        """Initialize the data processor."""
        self.file_path = Path(file_path)
        self.verbose = verbose
        self.players = []
        
    def load_players(self) -> List[Dict]:
        """Load players from the input file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.file_path}")
            
        if self.verbose:
            print(f"Loading players from: {self.file_path}")
            
        # Determine file format and load accordingly
        if self.file_path.suffix.lower() == '.csv':
            return self._load_csv()
        elif self.file_path.suffix.lower() in ['.xlsx', '.xls']:
            return self._load_excel()
        else:
            raise ValueError(f"Unsupported file format: {self.file_path.suffix}")
            
    def _load_csv(self) -> List[Dict]:
        """Load players from CSV file."""
        players = []
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean and normalize the data
                player = self._clean_player_data(row)
                if player:
                    players.append(player)
                    
        if self.verbose:
            print(f"Loaded {len(players)} players from CSV")
            
        return players
        
    def _load_excel(self) -> List[Dict]:
        """Load players from Excel file."""
        try:
            df = pd.read_excel(self.file_path)
            players = []
            
            for _, row in df.iterrows():
                player = self._clean_player_data(row.to_dict())
                if player:
                    players.append(player)
                    
            if self.verbose:
                print(f"Loaded {len(players)} players from Excel")
                
            return players
            
        except ImportError:
            raise ImportError("pandas and openpyxl are required for Excel support. Install with: pip install pandas openpyxl")
            
    def _clean_player_data(self, raw_data: Dict) -> Optional[Dict]:
        """Clean and normalize player data."""
        try:
            # Extract and clean key fields
            player = {
                'name': self._clean_string(raw_data.get('Name') or raw_data.get('Player Name', '')),
                'position': self._clean_string(raw_data.get('Position') or raw_data.get('Pos', '')),
                'age': self._safe_int(raw_data.get('Age', 0)),
                'college': self._clean_string(raw_data.get('College') or raw_data.get('School', '')),
                'height': self._clean_string(raw_data.get('Height') or raw_data.get('Ht', '')),
                'weight': self._safe_int(raw_data.get('Weight') or raw_data.get('Wt', 0)),
                
                # Physical attributes (if available)
                'speed': self._safe_float(raw_data.get('Speed', 0)),
                'acceleration': self._safe_float(raw_data.get('Acceleration', 0)),
                'agility': self._safe_float(raw_data.get('Agility', 0)),
                'strength': self._safe_float(raw_data.get('Strength', 0)),
                'awareness': self._safe_float(raw_data.get('Awareness', 0)),
                'intelligence': self._safe_float(raw_data.get('Intelligence', 0)),
                'durability': self._safe_float(raw_data.get('Durability', 0)),
                
                # Keep original data for reference
                '_raw': raw_data
            }
            
            # Skip players with missing essential data
            if not player['name'] or not player['position']:
                if self.verbose:
                    print(f"Skipping player with missing name or position: {raw_data}")
                return None
                
            return player
            
        except Exception as e:
            if self.verbose:
                print(f"Error processing player data: {e}")
            return None
            
    def _clean_string(self, value) -> str:
        """Clean string values."""
        if value is None:
            return ''
        return str(value).strip()
        
    def _safe_int(self, value) -> int:
        """Safely convert to integer."""
        try:
            if value is None or value == '':
                return 0
            return int(float(value))
        except (ValueError, TypeError):
            return 0
            
    def _safe_float(self, value) -> float:
        """Safely convert to float."""
        try:
            if value is None or value == '':
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0
            
    def filter_by_position(self, players: List[Dict], position: str) -> List[Dict]:
        """Filter players by position."""
        position = position.upper()
        filtered = [p for p in players if p['position'].upper() == position]
        
        if self.verbose:
            print(f"Filtered to {len(filtered)} {position} players")
            
        return filtered
        
    def get_position_counts(self, players: List[Dict]) -> Dict[str, int]:
        """Get count of players by position."""
        counts = {}
        for player in players:
            pos = player['position']
            counts[pos] = counts.get(pos, 0) + 1
        return dict(sorted(counts.items()))