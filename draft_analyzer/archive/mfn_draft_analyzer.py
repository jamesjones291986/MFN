#!/usr/bin/env python3
"""
MFN Draft Analyzer - Uses existing weights system to project draft prospects
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from sheets_connector import SheetsConnector

class MFNDraftAnalyzer:
    """Analyzes MFN draft prospects using existing weights and volatility system."""
    
    def __init__(self, sheet_id: str, verbose: bool = False):
        """Initialize the analyzer with the sheet ID."""
        self.sheet_id = sheet_id
        self.verbose = verbose
        self.connector = SheetsConnector(verbose=verbose)
        
        # Data storage
        self.weights = {}
        self.draft_prospects = []
        self.analyzed_prospects = []
        
    def load_data(self):
        """Load weights and draft prospects from the sheet."""
        if not self.connector.client:
            raise ConnectionError("Failed to connect to Google Sheets")
            
        spreadsheet = self.connector.client.open_by_key(self.sheet_id)
        
        # Load weights
        if self.verbose:
            print("📊 Loading position weights...")
        self._load_weights(spreadsheet)
        
        # Load draft prospects
        if self.verbose:
            print("👥 Loading draft prospects...")
        self._load_prospects(spreadsheet)
        
        if self.verbose:
            print(f"✅ Loaded {len(self.draft_prospects)} draft prospects")
            
    def _load_weights(self, spreadsheet):
        """Load position weights from the Weights worksheet."""
        weights_ws = spreadsheet.worksheet('Weights')
        weights_data = weights_ws.get_all_records()
        
        # Convert to dictionary structure
        positions = ['QB', 'RB', 'FB', 'TE', 'WR', 'LT', 'LG', 'C', 'RG', 'RT', 
                    'P', 'K', 'LDE', 'DT', 'RDE', 'LLB', 'MLB', 'RLB', 'LCB', 'SS', 'FS', 'RCB']
        
        for row in weights_data:
            skill = row.get('Skill', '').strip()
            if skill:
                self.weights[skill] = {}
                for pos in positions:
                    weight_val = row.get(pos, '')
                    if weight_val and str(weight_val).replace('.', '').isdigit():
                        self.weights[skill][pos] = float(weight_val)
                        
        if self.verbose:
            print(f"   Loaded weights for {len(self.weights)} skills")
            
    def _load_prospects(self, spreadsheet):
        """Load draft prospects from Player Import worksheet."""
        prospects_ws = spreadsheet.worksheet('Player Import')
        self.draft_prospects = prospects_ws.get_all_records()
        
        # Filter to only rookies (Exp = 'R') and clean data
        rookie_prospects = []
        for prospect in self.draft_prospects:
            if prospect.get('Exp') == 'R':
                # Clean and validate the prospect data
                cleaned_prospect = self._clean_prospect_data(prospect)
                if cleaned_prospect:
                    rookie_prospects.append(cleaned_prospect)
                    
        self.draft_prospects = rookie_prospects
        
    def _clean_prospect_data(self, prospect: Dict) -> Dict:
        """Clean and validate prospect data."""
        try:
            # Basic required fields
            if not all([prospect.get('FirstName'), prospect.get('LastName'), prospect.get('Pos')]):
                return None
                
            # Convert numeric fields
            cleaned = {
                'player_id': str(prospect.get('PlayerID', '')),
                'first_name': str(prospect.get('FirstName', '')).strip(),
                'last_name': str(prospect.get('LastName', '')).strip(),
                'position': str(prospect.get('Pos', '')).strip(),
                'height': str(prospect.get('Height', '')),
                'weight': self._safe_float(prospect.get('Weight', 0)),
                'current_overall': self._safe_float(prospect.get('Cur', 0)),
                'max_overall': self._safe_float(prospect.get('Max', 0)),
                'volatility': self._safe_float(prospect.get('Volatility', 0)),
                'college': str(prospect.get('College', '')).strip(),
                'team': str(prospect.get('Team', '')).strip(),
                'health': self._safe_float(prospect.get('Health', 100))
            }
            
            # Add skill data (current and max for each skill)
            self._add_skill_data(cleaned, prospect)
            
            return cleaned
            
        except Exception as e:
            if self.verbose:
                print(f"Warning: Error cleaning prospect data: {e}")
            return None
            
    def _safe_float(self, value) -> float:
        """Safely convert value to float."""
        try:
            if value is None or value == '':
                return 0.0
            return float(value)
        except:
            return 0.0
            
    def _add_skill_data(self, cleaned_prospect: Dict, raw_prospect: Dict):
        """Add current and max skill values to the prospect."""
        skills = ['MaxSpeed', 'Acceleration', 'Strength', 'Intelligence', 'Discipline',
                 'PassAccuracy', 'HardCount', 'ArmStrength', 'PassingRelease', 'LookOffDef',
                 'Scrambling', 'BallHandling', 'BallSecurity', 'Catching', 'RouteRunning',
                 'Blocking', 'HandFighting', 'KickStrength', 'KickAccuracy', 'KickTiming',
                 'PuntStrength', 'PuntTiming', 'PuntAccuracy', 'Coverage', 'Tackling',
                 'PassRush', 'RunDefense', 'ManCoverage', 'ZoneCoverage', 'Punishing',
                 'PuntBlocking', 'BreakTackle', 'Avoid Fumble']
        
        for skill in skills:
            current_val = self._safe_float(raw_prospect.get(f'{skill}Cur', 0))
            max_val = self._safe_float(raw_prospect.get(f'{skill}Max', 0))
            
            cleaned_prospect[f'{skill}_current'] = current_val
            cleaned_prospect[f'{skill}_max'] = max_val
            cleaned_prospect[f'{skill}_gap'] = max_val - current_val if max_val > 0 else 0
            
    def analyze_prospects(self):
        """Analyze all prospects and calculate projections."""
        if not self.draft_prospects:
            raise ValueError("No draft prospects loaded")
            
        if self.verbose:
            print("🔄 Analyzing prospect projections...")
            
        for prospect in self.draft_prospects:
            analyzed = self._analyze_single_prospect(prospect)
            self.analyzed_prospects.append(analyzed)
            
        # Sort by projected value (descending)
        self.analyzed_prospects.sort(key=lambda x: x['projected_value'], reverse=True)
        
        # Add draft rankings
        for i, prospect in enumerate(self.analyzed_prospects, 1):
            prospect['draft_rank'] = i
            
        if self.verbose:
            print(f"✅ Analyzed {len(self.analyzed_prospects)} prospects")
            
    def _analyze_single_prospect(self, prospect: Dict) -> Dict:
        """Analyze a single prospect and calculate projections."""
        analyzed = prospect.copy()
        
        position = prospect['position']
        volatility = prospect['volatility']
        
        # Calculate current and projected position ratings
        analyzed['current_position_rating'] = self._calculate_position_rating(prospect, position, use_current=True)
        analyzed['max_position_rating'] = self._calculate_position_rating(prospect, position, use_current=False)
        
        # Calculate volatility-adjusted projection
        analyzed['projected_growth'] = self._calculate_projected_growth(prospect, position)
        analyzed['projected_rating'] = analyzed['current_position_rating'] + analyzed['projected_growth']
        
        # Calculate overall value score
        analyzed['projected_value'] = self._calculate_projected_value(analyzed)
        
        # Add development potential category
        analyzed['development_tier'] = self._categorize_development_potential(analyzed)
        
        return analyzed
        
    def _calculate_position_rating(self, prospect: Dict, position: str, use_current: bool = True) -> float:
        """Calculate position-specific rating using loaded weights."""
        if position not in ['QB', 'RB', 'FB', 'TE', 'WR', 'LT', 'LG', 'C', 'RG', 'RT', 
                           'P', 'K', 'LDE', 'DT', 'RDE', 'LLB', 'MLB', 'RLB', 'LCB', 'SS', 'FS', 'RCB']:
            return 0.0
            
        total_weighted_score = 0
        total_weight = 0
        
        for skill, position_weights in self.weights.items():
            if position in position_weights:
                weight = position_weights[position]
                
                if weight > 0:  # Only include skills with positive weights
                    # Get skill value
                    skill_key = f"{skill}_current" if use_current else f"{skill}_max"
                    skill_value = prospect.get(skill_key, 0)
                    
                    if skill_value > 0:
                        total_weighted_score += skill_value * weight
                        total_weight += weight
                        
        return total_weighted_score / total_weight if total_weight > 0 else 0
        
    def _calculate_projected_growth(self, prospect: Dict, position: str) -> float:
        """Calculate volatility-adjusted projected growth."""
        volatility = prospect['volatility']
        max_rating = self._calculate_position_rating(prospect, position, use_current=False)
        current_rating = self._calculate_position_rating(prospect, position, use_current=True)
        
        potential_growth = max_rating - current_rating
        
        # Apply volatility factor
        # Your rule: 10 volatility points = 1 overall change for most positions
        # QB and OL: 10 volatility points = 2 overall change
        
        if position in ['QB', 'LT', 'LG', 'C', 'RG', 'RT']:
            volatility_factor = volatility * 0.2  # 2 points per 10 volatility
        else:
            volatility_factor = volatility * 0.1  # 1 point per 10 volatility
            
        # Growth is limited by potential and volatility
        projected_growth = min(potential_growth, volatility_factor)
        
        return max(0, projected_growth)  # Can't have negative growth
        
    def _calculate_projected_value(self, analyzed_prospect: Dict) -> float:
        """Calculate overall draft value considering multiple factors."""
        projected_rating = analyzed_prospect['projected_rating']
        current_rating = analyzed_prospect['current_position_rating']
        growth_potential = analyzed_prospect['projected_growth']
        volatility = analyzed_prospect['volatility']
        
        # Base score is the projected rating
        value_score = projected_rating
        
        # Bonus for immediate impact (high current rating)
        immediate_impact_bonus = current_rating * 0.3
        
        # Bonus for growth potential
        growth_bonus = growth_potential * 0.5
        
        # Slight bonus for optimal volatility (not too low, not too high)
        if 40 <= volatility <= 80:
            volatility_bonus = 5
        elif 20 <= volatility <= 40 or 80 <= volatility <= 90:
            volatility_bonus = 2
        else:
            volatility_bonus = 0
            
        total_value = value_score + immediate_impact_bonus + growth_bonus + volatility_bonus
        
        return total_value
        
    def _categorize_development_potential(self, analyzed_prospect: Dict) -> str:
        """Categorize the development potential of a prospect."""
        growth = analyzed_prospect['projected_growth']
        current = analyzed_prospect['current_position_rating']
        
        if current >= 75:
            if growth >= 10:
                return "Elite Ready"
            else:
                return "Pro Ready"
        elif current >= 60:
            if growth >= 15:
                return "High Upside"
            elif growth >= 8:
                return "Solid Development"
            else:
                return "Role Player"
        else:
            if growth >= 20:
                return "Project - High Upside"
            elif growth >= 10:
                return "Project - Medium Upside"
            else:
                return "Deep Sleeper"
                
    def get_top_prospects(self, n: int = 50, position: str = None) -> List[Dict]:
        """Get top N prospects, optionally filtered by position."""
        prospects = self.analyzed_prospects
        
        if position:
            prospects = [p for p in prospects if p['position'] == position.upper()]
            
        return prospects[:n]
        
    def get_position_rankings(self, position: str) -> List[Dict]:
        """Get all prospects at a specific position, ranked."""
        return [p for p in self.analyzed_prospects if p['position'] == position.upper()]
        
    def print_draft_board(self, top_n: int = 30):
        """Print a formatted draft board."""
        if not self.analyzed_prospects:
            print("No analyzed prospects available")
            return
            
        print(f"\n🏈 MFN DRAFT BOARD - TOP {top_n} PROSPECTS")
        print("=" * 100)
        print(f"{'Rank':<4} {'Player':<25} {'Pos':<3} {'Current':<7} {'Projected':<9} {'Growth':<6} {'Value':<6} {'Tier':<20}")
        print("-" * 100)
        
        for i, prospect in enumerate(self.analyzed_prospects[:top_n], 1):
            name = f"{prospect['first_name']} {prospect['last_name']}"
            current = f"{prospect['current_position_rating']:.1f}"
            projected = f"{prospect['projected_rating']:.1f}"
            growth = f"{prospect['projected_growth']:.1f}"
            value = f"{prospect['projected_value']:.1f}"
            tier = prospect['development_tier']
            
            print(f"{i:<4} {name:<25} {prospect['position']:<3} {current:<7} {projected:<9} {growth:<6} {value:<6} {tier:<20}")


def main():
    """Main function to run the draft analyzer."""
    sheet_id = "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"
    
    print("🏈 MFN Draft Analyzer")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = MFNDraftAnalyzer(sheet_id, verbose=True)
        
        # Load data
        analyzer.load_data()
        
        # Analyze prospects
        analyzer.analyze_prospects()
        
        # Print results
        analyzer.print_draft_board(top_n=40)
        
        # Show position breakdowns
        positions = ['QB', 'RB', 'WR', 'TE']
        for pos in positions:
            pos_prospects = analyzer.get_position_rankings(pos)
            if pos_prospects:
                print(f"\n🎯 TOP {pos} PROSPECTS:")
                print("-" * 50)
                for i, prospect in enumerate(pos_prospects[:8], 1):
                    name = f"{prospect['first_name']} {prospect['last_name']}"
                    value = f"{prospect['projected_value']:.1f}"
                    tier = prospect['development_tier']
                    print(f"  {i}. {name:<25} Value: {value:<6} ({tier})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()