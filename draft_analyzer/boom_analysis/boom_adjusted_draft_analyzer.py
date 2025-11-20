#!/usr/bin/env python3
"""
Boom-adjusted draft analyzer using volatility prediction model
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from fixed_position_analyzer import FixedMultiPositionAnalyzer
from volatility_prediction_model import build_volatility_prediction_model
from typing import Dict, List, Tuple

class BoomAdjustedDraftAnalyzer(FixedMultiPositionAnalyzer):
    """Draft analyzer with boom potential predictions."""
    
    def __init__(self, sheet_id: str, verbose: bool = False):
        """Initialize with volatility prediction model."""
        super().__init__(sheet_id, verbose)
        
        print("🔮 Loading volatility prediction model...")
        self.volatility_model, self.predict_skill_growth = build_volatility_prediction_model()
        print("✅ Volatility prediction model loaded")
        
        # Position-specific key skills (for boom calculations)
        self.position_key_skills = {
            'QB': ['PassAccuracy', 'ArmStrength', 'LookOffDef', 'Scrambling'],
            'RB': ['RouteRunning', 'Catching', 'BallSecurity', 'BreakTackle'],
            'WR': ['RouteRunning', 'Catching'],
            'TE': ['RouteRunning', 'Catching', 'Blocking'],
            'LT': ['Blocking'], 'LG': ['Blocking'], 'C': ['Blocking'], 'RG': ['Blocking'], 'RT': ['Blocking'],
            'LDE': ['PassRush', 'RunDefense'], 'RDE': ['PassRush', 'RunDefense'], 'DT': ['PassRush', 'RunDefense'],
            'LLB': ['PassRush', 'RunDefense', 'ManCoverage', 'ZoneCoverage'],
            'MLB': ['PassRush', 'RunDefense', 'ManCoverage', 'ZoneCoverage'],
            'RLB': ['PassRush', 'RunDefense', 'ManCoverage', 'ZoneCoverage'],
            'LCB': ['ManCoverage', 'ZoneCoverage'], 'RCB': ['ManCoverage', 'ZoneCoverage'],
            'SS': ['ManCoverage', 'ZoneCoverage', 'Tackling'],
            'FS': ['ManCoverage', 'ZoneCoverage', 'Tackling']
        }
    
    def calculate_boom_adjusted_rating(self, prospect: Dict, position: str, scenario: str = 'boom') -> tuple:
        """Calculate position rating using boom-adjusted skill values."""
        
        total_weighted_score = 0
        total_weight = 0
        boom_info = []
        
        volatility = prospect['volatility']
        
        for weights_skill_name, position_weights in self.weights.items():
            if position in position_weights:
                weight = position_weights[position]
                
                if weight > 0:
                    # Map to player skill name
                    player_skill_name = self.skill_mapping.get(weights_skill_name)
                    
                    if player_skill_name:
                        # Get current and max values
                        current_key = f"{player_skill_name}_current"
                        max_key = f"{player_skill_name}_max"
                        
                        current_val = prospect.get(current_key, 0)
                        max_val = prospect.get(max_key, 0)
                        
                        if current_val > 0 and max_val > 0:
                            # Skip speed skills (don't change with volatility)
                            if player_skill_name in ['MaxSpeed', 'Acceleration']:
                                skill_value = max_val  # Use original max
                                growth_prediction = None
                            else:
                                # Get boom prediction for this skill
                                growth_prediction = self.predict_skill_growth(
                                    position, player_skill_name, current_val, max_val, volatility
                                )
                                
                                # Choose scenario value
                                if scenario == 'boom':
                                    skill_value = growth_prediction['boom']
                                elif scenario == 'conservative':
                                    skill_value = growth_prediction['conservative']
                                elif scenario == 'bust':
                                    skill_value = growth_prediction['bust']
                                else:
                                    skill_value = max_val  # Original max
                            
                            # Add to overall calculation
                            weighted_score = skill_value * weight
                            total_weighted_score += weighted_score
                            total_weight += weight
                            
                            boom_info.append({
                                'skill': weights_skill_name,
                                'player_skill': player_skill_name,
                                'current': current_val,
                                'original_max': max_val,
                                'boom_max': skill_value,
                                'growth': skill_value - max_val if player_skill_name not in ['MaxSpeed', 'Acceleration'] else 0,
                                'weight': weight,
                                'weighted_score': weighted_score,
                                'prediction': growth_prediction
                            })
        
        overall_rating = total_weighted_score / total_weight if total_weight > 0 else 0
        return overall_rating, boom_info
    
    def analyze_prospect_boom_scenarios(self, prospect: Dict) -> Dict:
        """Analyze a prospect's boom, conservative, and bust scenarios."""
        
        analysis = {
            'player_name': f"{prospect['first_name']} {prospect['last_name']}",
            'original_position': prospect['position'],
            'volatility': prospect['volatility'],
            'current_weight': prospect.get('weight', 200),
            'base_speed': prospect.get('MaxSpeed_current', 50),
            'scenarios': {},
            'best_boom_position': None,
            'best_boom_rating': 0,
            'best_conservative_position': None,
            'best_conservative_rating': 0
        }
        
        # Calculate scenarios for each position
        for position in self.all_positions:
            boom_rating, boom_info = self.calculate_boom_adjusted_rating(prospect, position, 'boom')
            conservative_rating, conservative_info = self.calculate_boom_adjusted_rating(prospect, position, 'conservative')
            bust_rating, bust_info = self.calculate_boom_adjusted_rating(prospect, position, 'bust')
            original_rating, original_info = self.calculate_boom_adjusted_rating(prospect, position, 'original')
            
            # Calculate adjusted speed for this position
            adjusted_speed = self._calculate_corrected_adjusted_speed(
                analysis['base_speed'], 
                analysis['current_weight'], 
                position
            )
            
            analysis['scenarios'][position] = {
                'boom_rating': boom_rating,
                'conservative_rating': conservative_rating,
                'bust_rating': bust_rating,
                'original_rating': original_rating,
                'adjusted_speed': adjusted_speed,
                'speed_qualified': adjusted_speed >= 88,
                'boom_info': boom_info[:5],  # Top 5 skills
                'upside': boom_rating - original_rating,
                'downside': original_rating - bust_rating
            }
            
            # Track best positions
            if boom_rating > analysis['best_boom_rating']:
                analysis['best_boom_position'] = position
                analysis['best_boom_rating'] = boom_rating
            
            if conservative_rating > analysis['best_conservative_rating']:
                analysis['best_conservative_position'] = position
                analysis['best_conservative_rating'] = conservative_rating
        
        return analysis
    
    def _calculate_corrected_adjusted_speed(self, base_speed: float, current_weight: float, position: str) -> float:
        """Calculate speed adjusted for position weight requirements (CORRECTED)."""
        
        if position not in self.position_weights:
            return base_speed
        
        target_weight = self.position_weights[position]
        weight_change_needed = target_weight - current_weight
        
        # Every 9.5 pounds = 1 speed point change
        # If player needs to GAIN weight, they lose speed
        # If player needs to LOSE weight, they gain speed
        speed_adjustment = -weight_change_needed / 9.5
        
        adjusted_speed = base_speed + speed_adjustment
        return max(0, min(100, adjusted_speed))

def run_boom_adjusted_draft_analysis():
    """Run boom-adjusted draft analysis."""
    sheet_id = "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"
    
    print("🚀 BOOM-ADJUSTED MFN DRAFT ANALYSIS")
    print("=" * 70)
    print("Using volatility prediction model for boom potential ratings")
    print("=" * 70)
    
    analyzer = BoomAdjustedDraftAnalyzer(sheet_id, verbose=True)
    analyzer.load_data()
    
    # Analyze all non-specialist prospects
    boom_analyses = []
    used_players = set()
    
    print(f"\n🔬 Analyzing boom scenarios for all prospects...")
    
    for prospect in analyzer.draft_prospects:
        if prospect['position'] not in ['P', 'K']:
            player_name = f"{prospect['first_name']} {prospect['last_name']}"
            if player_name not in used_players:
                analysis = analyzer.analyze_prospect_boom_scenarios(prospect)
                boom_analyses.append(analysis)
                used_players.add(player_name)
    
    print(f"✅ Analyzed {len(boom_analyses)} prospects")
    
    # Create multiple draft boards
    create_boom_draft_board(boom_analyses, 'boom')
    create_boom_draft_board(boom_analyses, 'conservative') 
    create_boom_draft_board(boom_analyses, 'upside')
    
    return boom_analyses

def create_boom_draft_board(analyses: List[Dict], scenario: str):
    """Create draft board for specific scenario."""
    
    if scenario == 'boom':
        title = "BOOM POTENTIAL DRAFT BOARD"
        subtitle = "Maximum upside if everything goes right"
        sort_key = lambda x: (1 if x['scenarios'][x['best_boom_position']]['speed_qualified'] else 0, 
                             x['best_boom_rating'])
        rating_key = 'best_boom_rating'
        position_key = 'best_boom_position'
    elif scenario == 'conservative':
        title = "CONSERVATIVE PROJECTION DRAFT BOARD"
        subtitle = "Expected realistic development"
        sort_key = lambda x: (1 if x['scenarios'][x['best_conservative_position']]['speed_qualified'] else 0,
                             x['best_conservative_rating'])
        rating_key = 'best_conservative_rating'
        position_key = 'best_conservative_position'
    else:  # upside
        title = "HIGHEST UPSIDE DRAFT BOARD"
        subtitle = "Biggest gap between boom and current projection"
        sort_key = lambda x: (1 if x['scenarios'][x['best_boom_position']]['speed_qualified'] else 0,
                             x['scenarios'][x['best_boom_position']]['upside'])
        rating_key = 'best_boom_rating'
        position_key = 'best_boom_position'
    
    # Sort prospects
    sorted_analyses = sorted(analyses, key=sort_key, reverse=True)
    
    print(f"\n🎯 {title}")
    print("=" * 80)
    print(subtitle)
    print("=" * 80)
    
    if scenario == 'upside':
        print(f"{'Rank':<4} {'Player':<18} {'Pos':<8} {'Orig':<6} {'Boom Rating':<11} {'Upside':<7} {'Speed':<5} {'Vol':<3}")
    else:
        print(f"{'Rank':<4} {'Player':<18} {'Pos':<8} {'Orig':<6} {'Rating':<11} {'Speed':<5} {'Vol':<3}")
    print("-" * 80)
    
    elite_count = 0
    quality_count = 0
    
    for i, analysis in enumerate(sorted_analyses[:30], 1):  # Top 30
        name = analysis['player_name'][:17]
        best_pos = analysis[position_key]
        orig_pos = analysis['original_position'][:5]
        rating = analysis[rating_key]
        vol = analysis['volatility']
        
        scenario_data = analysis['scenarios'][best_pos]
        speed = scenario_data['adjusted_speed']
        speed_indicator = "⚡" if speed >= 88 else " "
        
        if scenario == 'upside':
            upside = scenario_data['upside']
            print(f"{i:<4} {name:<18} {best_pos:<8} {orig_pos:<6} {rating:<11.1f} {upside:<+7.1f} {speed:<4.0f}{speed_indicator} {vol:<3.0f}")
        else:
            print(f"{i:<4} {name:<18} {best_pos:<8} {orig_pos:<6} {rating:<11.1f} {speed:<4.0f}{speed_indicator} {vol:<3.0f}")
        
        # Count tiers
        if rating >= 85 and speed >= 88:
            elite_count += 1
        elif rating >= 80 and speed >= 88:
            quality_count += 1
    
    # Summary
    print(f"\n📊 {scenario.upper()} SUMMARY:")
    print(f"🔥 Elite prospects (85+ rating + speed): {elite_count}")
    print(f"🎯 Quality prospects (80+ rating + speed): {quality_count}")
    
    # Show detailed analysis for top 5
    print(f"\n🔬 DETAILED {scenario.upper()} ANALYSIS (Top 5):")
    print("=" * 80)
    
    for analysis in sorted_analyses[:5]:
        name = analysis['player_name']
        pos = analysis[position_key]
        vol = analysis['volatility']
        rating = analysis[rating_key]
        
        scenario_data = analysis['scenarios'][pos]
        speed = scenario_data['adjusted_speed']
        
        print(f"\n🎯 {name} ({pos})")
        print(f"   {scenario.title()} Rating: {rating:.1f}")
        print(f"   Speed: {speed:.1f} {'⚡' if speed >= 88 else ''}")
        print(f"   Volatility: {vol}")
        
        if scenario_data['boom_info']:
            print(f"   Key Skill Projections:")
            for skill_info in scenario_data['boom_info'][:4]:
                if skill_info['growth'] != 0:
                    conf = skill_info['prediction']['confidence'] if skill_info['prediction'] else 'N/A'
                    print(f"     {skill_info['skill']:<15}: {skill_info['original_max']:>3.0f} → {skill_info['boom_max']:>3.0f} (+{skill_info['growth']:>2.0f}) [{conf}]")

if __name__ == "__main__":
    analyses = run_boom_adjusted_draft_analysis()