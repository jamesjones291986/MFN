#!/usr/bin/env python3
"""
Proper Boom-Only Projection Model for MFN Rookies
- Only projects booms (max ratings can only go UP)
- Uses actual MFN skill weights to calculate overall ratings
- Accounts for weight changes affecting speed
"""

import sys
from pathlib import Path
import statistics
import csv

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from sheets_connector import SheetsConnector

class ProperBoomProjectionModel:
    """Model that properly calculates overall ratings using skill weights and boom-only logic."""
    
    def __init__(self):
        # Load skill weights from Google Sheets
        self.skill_weights = self.load_skill_weights()
        
        # Volatility profiles for boom probability
        self.volatility_profiles = {
            'ultra_safe': {'min_vol': 0, 'max_vol': 20, 'boom_prob': 0.037},
            'safe_floor': {'min_vol': 21, 'max_vol': 40, 'boom_prob': 0.025},
            'balanced_low': {'min_vol': 41, 'max_vol': 60, 'boom_prob': 0.081},
            'balanced_high': {'min_vol': 61, 'max_vol': 80, 'boom_prob': 0.071},
            'high_risk': {'min_vol': 81, 'max_vol': 100, 'boom_prob': 0.130}
        }
        
        # Target weights for positions
        self.position_target_weights = {
            'QB': 220, 'RB': 217, 'FB': 243, 'TE': 257, 'WR': 198,
            'LT': 312, 'LG': 308, 'C': 283, 'RG': 316, 'RT': 319,
            'LDE': 276, 'DT': 300, 'RDE': 276, 'SLB': 241, 'MLB': 245,
            'WLB': 237, 'CB': 191, 'SS': 207, 'FS': 206, 'P': 210, 'K': 200
        }
        
        # Map skill names from sheet to our data
        self.skill_name_mapping = {
            'Max Speed': 'MaxSpeed',
            'Acceleration': 'Acceleration',
            'Strength': 'Strength',
            'Intelligence': 'Intelligence',
            'Discipline': 'Discipline',
            'Pass Accuracy': 'PassAccuracy',
            'Hard Count': 'HardCount',
            'Arm Strength': 'ArmStrength',
            'Passing Release': 'PassingRelease',
            'Look Off Def': 'LookOffDef',
            'Scrambling skill': 'ScramblingSkill',
            'Field of Vision': 'FieldOfVision',
            'Pass Catching': 'PassCatching',
            'B&R Avoidance': 'B&RAvoidance',
            'Route-Running': 'RouteRunning',
            'Pass Rec Courage': 'PassRecCourage',
            'Tackle Ability': 'TackleAbility',
            'Strip Ball': 'StripBall',
            'Break Tackle': 'BreakTackle',
            'Ball Carrying': 'BallCarrying',
            'Avoid Fumble': 'AvoidFumble',
            'Run Blocking': 'RunBlocking',
            'Pass Blocking': 'PassBlocking',
            'Short Snapping': 'ShortSnapping',
            'Long Snapping': 'LongSnapping',
            'Pass Rush': 'PassRush',
            'Run Defense': 'RunDefense',
            'Punt Strength': 'PuntStrength',
            'Punt Accuracy': 'PuntAccuracy',
            'Kick Strength': 'KickStrength',
            'Kick Accuracy': 'KickAccuracy',
            'Kick Holding': 'KickHolding',
            'Punt Timing': 'PuntTiming',
            'Kick Catching': 'KickCatching',
            'Punish Receiver': 'PunishReceiver',
            'Zone coverage': 'ZoneCoverage',
            'M2M Coverage': 'M2MCoverage',
            'B&R Coverage': 'B&RCoverage'
        }
    
    def load_skill_weights(self):
        """Load skill weights from Google Sheets."""
        try:
            connector = SheetsConnector(verbose=False)
            sheet = connector.client.open_by_key('1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A')
            weights_ws = sheet.worksheet('Weights')
            weights_data = weights_ws.get_all_records()
            
            # Convert to proper format
            skill_weights = {}
            for row in weights_data:
                skill_name = row['Skill']
                skill_weights[skill_name] = {}
                for pos in ['QB', 'RB', 'FB', 'TE', 'WR', 'LT', 'LG', 'C', 'RG', 'RT', 
                           'LDE', 'DT', 'RDE', 'SLB', 'MLB', 'WLB', 'CB', 'SS', 'FS', 'P', 'K']:
                    weight_val = row.get(pos, 0)
                    if weight_val == '' or weight_val is None:
                        weight_val = 0
                    skill_weights[skill_name][pos] = int(weight_val) if str(weight_val).isdigit() else 0
            
            return skill_weights
        except Exception as e:
            print(f"Failed to load skill weights: {e}")
            return {}
    
    def calculate_weight_adjustment(self, current_weight, position, max_speed):
        """Calculate speed changes due to weight gain/loss."""
        target_weight = self.position_target_weights.get(position, current_weight)
        weight_change = target_weight - current_weight
        
        # Every 9.5 pounds = 1 speed point
        speed_change = -(weight_change / 9.5)
        
        # Apply speed change
        adjusted_max_speed = max(0, min(100, max_speed + speed_change))
        
        return {
            'weight_change': weight_change,
            'speed_change': speed_change,
            'adjusted_max_speed': adjusted_max_speed,
            'target_weight': target_weight
        }
    
    def project_boom_skills(self, player_data, volatility):
        """Project how much each skill will boom based on volatility."""
        # Classify volatility
        profile_name = 'unknown'
        boom_prob = 0.05
        
        for name, profile in self.volatility_profiles.items():
            if profile['min_vol'] <= volatility <= profile['max_vol']:
                profile_name = name
                boom_prob = profile['boom_prob']
                break
        
        # Project skill improvements - BOOM ONLY!
        projected_skills = {}
        weight_adjustment = None
        
        # Get current weight and position for speed adjustment
        position = player_data.get('Pos', 'QB')
        current_weight = float(player_data.get('Weight', 200))
        
        for skill_sheet_name, skill_data_name in self.skill_name_mapping.items():
            try:
                current_val = float(player_data.get(f'{skill_data_name}Cur', 0))
                max_val = float(player_data.get(f'{skill_data_name}Max', 0))
                
                if skill_data_name == 'MaxSpeed' and weight_adjustment is None:
                    # Calculate weight adjustment for speed
                    weight_adjustment = self.calculate_weight_adjustment(current_weight, position, max_val)
                    projected_max = weight_adjustment['adjusted_max_speed']
                else:
                    # For non-speed skills, assume boom based on volatility
                    potential_gain = max_val - current_val
                    
                    # BOOM ASSUMPTION: Players with higher volatility get bigger booms
                    if volatility <= 20:
                        boom_factor = 0.8  # Even low vol players boom significantly
                    elif volatility <= 40:
                        boom_factor = 0.85
                    elif volatility <= 60:
                        boom_factor = 0.9
                    elif volatility <= 80:
                        boom_factor = 0.95
                    else:  # 81-100 volatility
                        boom_factor = 1.0  # High vol = max boom
                    
                    # Project the skill to boom significantly above current max
                    skill_boom = potential_gain * boom_factor
                    projected_max = max_val + skill_boom
                    projected_max = min(projected_max, 100)  # Cap at 100
                
                # Assume they reach close to their projected max after boom
                projected_current = max_val + (projected_max - max_val) * 0.8  # 80% of the way to new max
                
                projected_skills[skill_data_name] = {
                    'current': current_val,
                    'max': max_val,
                    'projected_max': projected_max,
                    'projected_current': min(projected_current, projected_max)
                }
                
            except (ValueError, TypeError):
                continue
        
        return projected_skills, profile_name, boom_prob, weight_adjustment
    
    def calculate_overall_rating(self, position, projected_skills):
        """Calculate overall rating using MFN skill weights."""
        if not self.skill_weights or position not in ['QB', 'RB', 'FB', 'TE', 'WR', 'LT', 'LG', 'C', 'RG', 'RT', 
                                                      'LDE', 'DT', 'RDE', 'SLB', 'MLB', 'WLB', 'CB', 'SS', 'FS', 'P', 'K']:
            # Fallback calculation
            return 50.0
        
        total_weighted_score = 0
        total_possible_score = 0
        
        for skill_sheet_name, skill_data_name in self.skill_name_mapping.items():
            weight = self.skill_weights.get(skill_sheet_name, {}).get(position, 0)
            
            if weight > 0 and skill_data_name in projected_skills:
                skill_value = projected_skills[skill_data_name]['projected_current']
                total_weighted_score += skill_value * weight
                total_possible_score += 100 * weight
        
        if total_possible_score == 0:
            return 50.0
        
        overall_rating = (total_weighted_score / total_possible_score) * 100
        return overall_rating
    
    def project_player_boom(self, player_data):
        """Project a single player's boom potential."""
        try:
            name = f"{player_data.get('FirstName', '')} {player_data.get('LastName', '')}"
            position = player_data.get('Pos', 'QB')
            volatility = float(player_data.get('Volatility', 0))
            current_overall = float(player_data.get('Cur', 0))
            max_overall = float(player_data.get('Max', 0))
            current_weight = float(player_data.get('Weight', 200))
            
            # Project skill improvements
            projected_skills, profile_name, boom_prob, weight_adjustment = self.project_boom_skills(player_data, volatility)
            
            # Calculate new overall rating from projected skills
            projected_overall = self.calculate_overall_rating(position, projected_skills)
            
            # Also calculate what the max could be if all skills hit their projected max
            max_projected_skills = {k: {'projected_current': v['projected_max']} for k, v in projected_skills.items()}
            potential_max_overall = self.calculate_overall_rating(position, max_projected_skills)
            
            result = {
                'name': name,
                'position': position,
                'current_rating': current_overall,
                'original_max': max_overall,
                'volatility': volatility,
                'projected_overall': round(projected_overall, 1),
                'potential_max_overall': round(potential_max_overall, 1),
                'volatility_profile': profile_name,
                'boom_probability': boom_prob * 100,
                'current_weight': current_weight,
                'projected_skills': projected_skills
            }
            
            # Add weight adjustment details if available
            if weight_adjustment:
                result.update({
                    'target_weight': weight_adjustment['target_weight'],
                    'weight_change': round(weight_adjustment['weight_change'], 1),
                    'speed_change': round(weight_adjustment['speed_change'], 1)
                })
            
            return result
            
        except Exception as e:
            print(f"Error projecting {player_data.get('FirstName', '')} {player_data.get('LastName', '')}: {e}")
            return None
    
    def analyze_rookie_class(self, rookies_data):
        """Analyze entire rookie class with proper boom projections."""
        projections = []
        
        for rookie in rookies_data:
            projection = self.project_player_boom(rookie)
            if projection:
                projections.append(projection)
        
        # Sort by projected overall
        projections.sort(key=lambda x: x['projected_overall'], reverse=True)
        
        return projections

def test_proper_model():
    """Test with Floyd White to validate the model."""
    print("🔬 TESTING PROPER BOOM-ONLY MODEL")
    print("=" * 60)
    
    # Find Floyd White in the data
    with open('live_rookies.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['FirstName'] == 'Floyd' and row['LastName'] == 'White':
                floyd_data = row
                break
    
    model = ProperBoomProjectionModel()
    projection = model.project_player_boom(floyd_data)
    
    print(f"Floyd White Analysis:")
    print(f"  Current Overall: {projection['current_rating']}")
    print(f"  Original Max: {projection['original_max']}")
    print(f"  Projected Overall: {projection['projected_overall']}")
    print(f"  Potential Max: {projection['potential_max_overall']}")
    print(f"  Volatility: {projection['volatility']} ({projection['volatility_profile']})")
    print(f"  Boom Probability: {projection['boom_probability']:.1f}%")
    print(f"  Actual (your league): 84")
    print(f"  Difference: {abs(84 - projection['projected_overall']):.1f} points")

if __name__ == "__main__":
    test_proper_model()