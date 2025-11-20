"""
Player Analyzer - Analyzes draft prospects and calculates projections
"""

import math
from typing import List, Dict, Tuple
from collections import defaultdict


class PlayerAnalyzer:
    """Analyzes players and generates performance projections."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the player analyzer."""
        self.verbose = verbose
        
        # Position-specific weights for different attributes
        self.position_weights = {
            'QB': {
                'intelligence': 0.25,
                'awareness': 0.20,
                'speed': 0.10,
                'acceleration': 0.10,
                'agility': 0.05,
                'strength': 0.15,
                'durability': 0.15
            },
            'RB': {
                'speed': 0.25,
                'acceleration': 0.20,
                'agility': 0.20,
                'strength': 0.15,
                'awareness': 0.10,
                'durability': 0.10
            },
            'WR': {
                'speed': 0.30,
                'acceleration': 0.20,
                'agility': 0.20,
                'awareness': 0.15,
                'intelligence': 0.10,
                'durability': 0.05
            },
            'TE': {
                'strength': 0.25,
                'speed': 0.15,
                'awareness': 0.20,
                'agility': 0.15,
                'intelligence': 0.15,
                'durability': 0.10
            },
            'OL': {  # Offensive Line
                'strength': 0.35,
                'intelligence': 0.25,
                'awareness': 0.20,
                'agility': 0.10,
                'durability': 0.10
            },
            'DL': {  # Defensive Line
                'strength': 0.30,
                'speed': 0.20,
                'acceleration': 0.20,
                'awareness': 0.15,
                'agility': 0.10,
                'durability': 0.05
            },
            'LB': {  # Linebacker
                'speed': 0.20,
                'acceleration': 0.15,
                'strength': 0.20,
                'awareness': 0.25,
                'agility': 0.15,
                'durability': 0.05
            },
            'DB': {  # Defensive Back
                'speed': 0.30,
                'acceleration': 0.25,
                'agility': 0.20,
                'awareness': 0.20,
                'intelligence': 0.05
            }
        }
        
        # Default weights for unknown positions
        self.default_weights = {
            'speed': 0.20,
            'acceleration': 0.15,
            'agility': 0.15,
            'strength': 0.15,
            'awareness': 0.15,
            'intelligence': 0.10,
            'durability': 0.10
        }
        
    def analyze_players(self, players: List[Dict]) -> List[Dict]:
        """Analyze all players and add projections."""
        analyzed_players = []
        
        for player in players:
            analyzed_player = self._analyze_single_player(player)
            analyzed_players.append(analyzed_player)
            
        if self.verbose:
            print(f"Analyzed {len(analyzed_players)} players")
            
        return analyzed_players
        
    def _analyze_single_player(self, player: Dict) -> Dict:
        """Analyze a single player and calculate scores."""
        # Copy the original player data
        analyzed = player.copy()
        
        # Calculate various scores
        analyzed['physical_score'] = self._calculate_physical_score(player)
        analyzed['mental_score'] = self._calculate_mental_score(player)
        analyzed['position_score'] = self._calculate_position_specific_score(player)
        analyzed['age_factor'] = self._calculate_age_factor(player['age'])
        analyzed['size_score'] = self._calculate_size_score(player)
        
        # Calculate overall draft score
        analyzed['overall_score'] = self._calculate_overall_score(analyzed)
        
        # Add draft grade and round projection
        analyzed['draft_grade'] = self._assign_draft_grade(analyzed['overall_score'])
        analyzed['projected_round'] = self._project_draft_round(analyzed['overall_score'])
        
        return analyzed
        
    def _calculate_physical_score(self, player: Dict) -> float:
        """Calculate physical attributes score."""
        physical_attrs = ['speed', 'acceleration', 'agility', 'strength', 'durability']
        
        total_score = 0
        count = 0
        
        for attr in physical_attrs:
            value = player.get(attr, 0)
            if value > 0:
                # Normalize to 0-100 scale (assuming MFN uses 0-100 scale)
                normalized = min(100, max(0, value))
                total_score += normalized
                count += 1
                
        return total_score / count if count > 0 else 0
        
    def _calculate_mental_score(self, player: Dict) -> float:
        """Calculate mental attributes score."""
        mental_attrs = ['awareness', 'intelligence']
        
        total_score = 0
        count = 0
        
        for attr in mental_attrs:
            value = player.get(attr, 0)
            if value > 0:
                normalized = min(100, max(0, value))
                total_score += normalized
                count += 1
                
        return total_score / count if count > 0 else 0
        
    def _calculate_position_specific_score(self, player: Dict) -> float:
        """Calculate position-specific weighted score."""
        position = player['position'].upper()
        
        # Get weights for this position (or use default)
        weights = self.position_weights.get(position, self.default_weights)
        
        weighted_score = 0
        total_weight = 0
        
        for attr, weight in weights.items():
            value = player.get(attr, 0)
            if value > 0:
                normalized = min(100, max(0, value))
                weighted_score += normalized * weight
                total_weight += weight
                
        return weighted_score / total_weight if total_weight > 0 else 0
        
    def _calculate_age_factor(self, age: int) -> float:
        """Calculate age factor (younger players get bonus)."""
        if age <= 0:
            return 1.0
            
        # Optimal age range is 20-22
        if 20 <= age <= 22:
            return 1.0
        elif age < 20:
            # Very young players get slight penalty for inexperience
            return 0.95
        elif age <= 24:
            # Slightly older is still good
            return 0.98
        elif age <= 26:
            # Getting older, some penalty
            return 0.90
        else:
            # Too old for typical draft prospect
            return 0.80
            
    def _calculate_size_score(self, player: Dict) -> float:
        """Calculate size appropriateness for position."""
        position = player['position'].upper()
        height = player.get('height', '')
        weight = player.get('weight', 0)
        
        # If no size data, return neutral
        if not height or weight <= 0:
            return 50.0
            
        # Parse height (assuming format like "6'2" or "6-2")
        height_inches = self._parse_height(height)
        
        # Position-specific size expectations
        size_expectations = {
            'QB': {'height_range': (71, 77), 'weight_range': (200, 240)},  # 5'11" - 6'5"
            'RB': {'height_range': (67, 73), 'weight_range': (190, 230)},  # 5'7" - 6'1"
            'WR': {'height_range': (69, 76), 'weight_range': (170, 220)},  # 5'9" - 6'4"
            'TE': {'height_range': (73, 79), 'weight_range': (240, 280)},  # 6'1" - 6'7"
            'OL': {'height_range': (74, 81), 'weight_range': (290, 350)},  # 6'2" - 6'9"
            'DL': {'height_range': (72, 78), 'weight_range': (250, 320)},  # 6'0" - 6'6"
            'LB': {'height_range': (70, 76), 'weight_range': (220, 260)},  # 5'10" - 6'4"
            'DB': {'height_range': (68, 74), 'weight_range': (180, 210)},  # 5'8" - 6'2"
        }
        
        expectations = size_expectations.get(position)
        if not expectations:
            return 50.0
            
        # Score height
        height_score = self._score_within_range(height_inches, expectations['height_range'])
        
        # Score weight  
        weight_score = self._score_within_range(weight, expectations['weight_range'])
        
        # Average the two scores
        return (height_score + weight_score) / 2
        
    def _parse_height(self, height_str: str) -> int:
        """Parse height string to inches."""
        try:
            # Handle formats like "6'2", "6-2", "6 2"
            height_str = height_str.replace("'", " ").replace("-", " ").replace("\"", "")
            parts = height_str.split()
            
            if len(parts) >= 2:
                feet = int(parts[0])
                inches = int(parts[1])
                return feet * 12 + inches
            elif len(parts) == 1 and len(parts[0]) >= 2:
                # Handle format like "72" (total inches)
                return int(parts[0])
                
        except:
            pass
            
        return 0
        
    def _score_within_range(self, value: float, ideal_range: Tuple[float, float]) -> float:
        """Score how well a value fits within an ideal range."""
        min_val, max_val = ideal_range
        
        if min_val <= value <= max_val:
            # Perfect score for being in range
            return 100.0
        elif value < min_val:
            # Penalty for being under ideal
            diff = min_val - value
            penalty = min(50, diff * 2)  # Max 50% penalty
            return 100 - penalty
        else:
            # Penalty for being over ideal
            diff = value - max_val
            penalty = min(50, diff * 2)  # Max 50% penalty
            return 100 - penalty
            
    def _calculate_overall_score(self, player: Dict) -> float:
        """Calculate overall draft score."""
        # Weight the different components
        weights = {
            'position_score': 0.40,  # Most important - position-specific skills
            'physical_score': 0.25,  # Physical attributes
            'mental_score': 0.20,    # Mental attributes
            'size_score': 0.10,      # Size appropriateness
            'age_factor': 0.05       # Age bonus/penalty
        }
        
        total_score = 0
        
        for component, weight in weights.items():
            if component == 'age_factor':
                # Age factor is a multiplier, not additive
                continue
                
            score = player.get(component, 0)
            total_score += score * weight
            
        # Apply age factor as multiplier
        age_factor = player.get('age_factor', 1.0)
        final_score = total_score * age_factor
        
        return min(100, max(0, final_score))
        
    def _assign_draft_grade(self, overall_score: float) -> str:
        """Assign letter grade based on overall score."""
        if overall_score >= 90:
            return "A+"
        elif overall_score >= 85:
            return "A"
        elif overall_score >= 80:
            return "A-"
        elif overall_score >= 75:
            return "B+"
        elif overall_score >= 70:
            return "B"
        elif overall_score >= 65:
            return "B-"
        elif overall_score >= 60:
            return "C+"
        elif overall_score >= 55:
            return "C"
        elif overall_score >= 50:
            return "C-"
        elif overall_score >= 45:
            return "D+"
        elif overall_score >= 40:
            return "D"
        else:
            return "F"
            
    def _project_draft_round(self, overall_score: float) -> str:
        """Project which round a player might be drafted."""
        if overall_score >= 88:
            return "1st Round"
        elif overall_score >= 80:
            return "2nd Round"
        elif overall_score >= 72:
            return "3rd Round"
        elif overall_score >= 65:
            return "4th Round"
        elif overall_score >= 58:
            return "5th Round"
        elif overall_score >= 52:
            return "6th Round"
        elif overall_score >= 45:
            return "7th Round"
        else:
            return "Undrafted FA"