#!/usr/bin/env python3
"""
Fixed Multi-Position MFN Draft Analyzer with corrected skill mappings
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from mfn_draft_analyzer import MFNDraftAnalyzer

class FixedMultiPositionAnalyzer(MFNDraftAnalyzer):
    """Fixed analyzer with corrected skill mapping between weights and player data."""
    
    def __init__(self, sheet_id: str, verbose: bool = False):
        """Initialize with corrected skill mappings."""
        super().__init__(sheet_id, verbose)
        
        # Position groups for draft strategy
        self.offensive_skill_positions = ['WR', 'RB', 'TE']
        self.defensive_positions = ['LCB', 'RCB', 'FS', 'SS', 'MLB', 'LLB', 'RLB']
        self.premium_positions = ['QB', 'LT', 'RT', 'LG', 'RG', 'C']
        self.defensive_line = ['LDE', 'RDE', 'DT']
        
        # All positions to analyze
        self.all_positions = ['QB', 'RB', 'FB', 'TE', 'WR', 'LT', 'LG', 'C', 'RG', 'RT', 
                             'LDE', 'DT', 'RDE', 'LLB', 'MLB', 'RLB', 'LCB', 'SS', 'FS', 'RCB']
        
        # Position weight requirements (approximate)
        self.position_weights = {
            'QB': 225, 'RB': 215, 'FB': 240, 'TE': 250, 'WR': 200,
            'LT': 315, 'LG': 310, 'C': 305, 'RG': 310, 'RT': 315,
            'LDE': 275, 'DT': 310, 'RDE': 275, 
            'LLB': 245, 'MLB': 250, 'RLB': 245,
            'LCB': 190, 'RCB': 190, 'SS': 200, 'FS': 195
        }
        
        # CORRECTED skill mapping between weights sheet and player data
        self.skill_mapping = {
            'Max Speed': 'MaxSpeed',              # FIXED
            'Acceleration': 'Acceleration', 
            'Strength': 'Strength',
            'Intelligence': 'Intelligence',
            'Discipline': 'Discipline',
            'Pass Accuracy': 'PassAccuracy',
            'Hard Count': 'HardCount',
            'Arm Strength': 'ArmStrength',
            'Passing Release': 'PassingRelease',
            'Look Off Def': 'LookOffDef',
            'Scrambling skill': 'Scrambling',    # FIXED
            'Ball Carrying': 'BallSecurity',     # FIXED: Critical RB skill
            'Avoid Fumble': 'Avoid Fumble',      
            'Break Tackle': 'BreakTackle',       # FIXED: Critical RB skill
            'Pass Catching': 'Catching',         # FIXED: Critical RB skill
            'Route-Running': 'RouteRunning',     # FIXED: Critical RB skill
            'Pass Blocking': 'Blocking',         # FIXED
            'Run Blocking': 'Blocking',          # FIXED: Maps to same skill
            'M2M Coverage': 'ManCoverage',       # FIXED: Critical defensive skill
            'Zone coverage': 'ZoneCoverage',     # FIXED: Critical defensive skill
            'Tackle Ability': 'Tackling',       # FIXED: Critical defensive skill
            'Punish Receiver': 'Punishing',     # FIXED
            'Pass Rush': 'PassRush',
            'Run Defense': 'RunDefense',
            'Hand Fighting': 'HandFighting',
            'Kick Strength': 'KickStrength',
            'Kick Accuracy': 'KickAccuracy',
            'Kick Timing': 'KickTiming',
            'Punt Strength': 'PuntStrength',
            'Punt Timing': 'PuntTiming',
            'Punt Accuracy': 'PuntAccuracy',
            'B&R Coverage': 'Coverage',          # FIXED
            'Pass Rec Courage': 'Catching',     # FIXED: Maps to catching ability
            'Strip Ball': 'HandFighting',       # FIXED: Similar skill
            'B&R Avoidance': 'Avoid Fumble',    # FIXED: Similar skill
        }
    
    def _calculate_position_rating_fixed(self, prospect: Dict, position: str, use_current: bool = True) -> float:
        """Calculate position-specific rating using CORRECTED skill mappings."""
        if position not in self.all_positions:
            return 0.0
            
        total_weighted_score = 0
        total_weight = 0
        debug_info = []
        
        for weights_skill_name, position_weights in self.weights.items():
            if position in position_weights:
                weight = position_weights[position]
                
                if weight > 0:  # Only include skills with positive weights
                    # Map weights skill name to player data skill name
                    player_skill_name = self.skill_mapping.get(weights_skill_name)
                    
                    if player_skill_name:  # Skip unmapped skills
                        # Get skill value from player data
                        skill_key = f"{player_skill_name}_current" if use_current else f"{player_skill_name}_max"
                        skill_value = prospect.get(skill_key, 0)
                        
                        # Include skill even if value is 0 (important for penalties)
                        weighted_score = skill_value * weight
                        total_weighted_score += weighted_score
                        total_weight += weight
                        
                        debug_info.append({
                            'weights_skill': weights_skill_name,
                            'player_skill': player_skill_name,
                            'weight': weight,
                            'value': skill_value,
                            'weighted_score': weighted_score
                        })
        
        rating = total_weighted_score / total_weight if total_weight > 0 else 0
        return rating, debug_info
    
    def analyze_player_all_positions_fixed(self, prospect: Dict) -> Dict:
        """Calculate player's rating at all positions with corrected skill mappings."""
        analysis = {
            'player_name': f"{prospect['first_name']} {prospect['last_name']}",
            'original_position': prospect['position'],
            'volatility': prospect['volatility'],
            'current_weight': prospect.get('weight', 200),
            'base_speed': prospect.get('MaxSpeed_current', 50),
            'position_ratings': {},
            'best_position': None,
            'best_current_rating': 0,
            'best_projected_rating': 0,
            'best_adjusted_speed': 0,
            'tier_classification': None
        }
        
        # Calculate ratings for all positions
        for position in self.all_positions:
            # Calculate adjusted speed for this position
            adjusted_speed = self._calculate_adjusted_speed(
                analysis['base_speed'], 
                analysis['current_weight'], 
                position
            )
            
            # Current rating at this position (using fixed calculation)
            current_rating, current_debug = self._calculate_position_rating_fixed(prospect, position, use_current=True)
            max_rating, max_debug = self._calculate_position_rating_fixed(prospect, position, use_current=False)
            
            # Project with volatility
            projected_rating = self._calculate_conservative_projection(
                current_rating, max_rating, prospect['volatility'], position
            )
            
            analysis['position_ratings'][position] = {
                'current': current_rating,
                'max_potential': max_rating,
                'projected': projected_rating,
                'improvement': projected_rating - current_rating,
                'adjusted_speed': adjusted_speed,
                'speed_qualified': adjusted_speed >= 88,
                'debug_info': current_debug[:5]  # Store top 5 skills for debugging
            }
            
            # Track best position
            if projected_rating > analysis['best_projected_rating']:
                analysis['best_position'] = position
                analysis['best_current_rating'] = current_rating
                analysis['best_projected_rating'] = projected_rating
                analysis['best_adjusted_speed'] = adjusted_speed
        
        return analysis
    
    def _calculate_adjusted_speed(self, base_speed: float, current_weight: float, position: str) -> float:
        """Calculate speed adjusted for position weight requirements."""
        if position not in self.position_weights:
            return base_speed
        
        target_weight = self.position_weights[position]
        weight_difference = current_weight - target_weight
        
        # Every 9.5 pounds = 1 speed point change
        speed_adjustment = -weight_difference / 9.5
        
        adjusted_speed = base_speed + speed_adjustment
        return max(0, min(100, adjusted_speed))
    
    def _calculate_conservative_projection(self, current: float, max_potential: float, 
                                        volatility: float, position: str) -> float:
        """Conservative projection focusing on positive volatility impact."""
        
        if max_potential <= current:
            return current
        
        potential_growth = max_potential - current
        
        if volatility <= 20:
            growth_factor = 0.85
        elif volatility <= 40:
            growth_factor = 0.75
        elif volatility <= 60:
            growth_factor = 0.60
        elif volatility <= 80:
            growth_factor = 0.50
        else:
            growth_factor = 0.40
        
        if position in ['QB', 'LT', 'LG', 'C', 'RG', 'RT']:
            growth_factor *= 1.2
        
        projected_growth = potential_growth * growth_factor
        return current + projected_growth


def test_fixed_analyzer():
    """Test the fixed analyzer on Jeremy Standish."""
    sheet_id = "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"
    
    print("🔧 TESTING FIXED SKILL MAPPINGS")
    print("=" * 60)
    
    analyzer = FixedMultiPositionAnalyzer(sheet_id, verbose=True)
    analyzer.load_data()
    
    # Find Jeremy Standish
    standish = None
    for prospect in analyzer.draft_prospects:
        if f"{prospect['first_name']} {prospect['last_name']}" == "Jeremy Standish":
            standish = prospect
            break
    
    if not standish:
        print("Jeremy Standish not found")
        return
    
    # Analyze with fixed mappings
    analysis = analyzer.analyze_player_all_positions_fixed(standish)
    
    print(f"\n🏈 JEREMY STANDISH - FIXED ANALYSIS")
    print("-" * 50)
    print(f"Original Position: {analysis['original_position']}")
    print(f"Base Speed: {analysis['base_speed']}")
    print(f"Volatility: {analysis['volatility']}")
    
    # Show RB and FS ratings with debug info
    for pos in ['RB', 'FS']:
        rating_data = analysis['position_ratings'][pos]
        print(f"\n{pos} Position:")
        print(f"  Rating: {rating_data['current']:.1f}")
        print(f"  Adjusted Speed: {rating_data['adjusted_speed']:.1f}")
        print(f"  Top Skills Used:")
        for skill_info in rating_data['debug_info']:
            print(f"    {skill_info['weights_skill']:<15} → {skill_info['player_skill']:<15}: {skill_info['value']:>5.1f} × {skill_info['weight']:>3.0f} = {skill_info['weighted_score']:>6.0f}")
    
    print(f"\nBest Position: {analysis['best_position']} ({analysis['best_projected_rating']:.1f})")
    
    # Show top 5 positions
    print(f"\nTop 5 Position Fits:")
    positions_sorted = sorted(analysis['position_ratings'].items(), 
                            key=lambda x: x[1]['projected'], reverse=True)
    
    for i, (pos, data) in enumerate(positions_sorted[:5], 1):
        speed_icon = "⚡" if data['speed_qualified'] else " "
        print(f"  {i}. {pos}: {data['projected']:.1f} (speed: {data['adjusted_speed']:.0f}{speed_icon})")


if __name__ == "__main__":
    test_fixed_analyzer()