#!/usr/bin/env python3
"""
Build volatility prediction model based on position + volatility + skill patterns
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from sheets_connector import SheetsConnector
from fixed_position_analyzer import FixedMultiPositionAnalyzer
from typing import Dict, List, Tuple
import json

def build_volatility_prediction_model():
    """Build comprehensive volatility prediction model by position and skill."""
    predraft_sheet_id = "1zMWPtzgVYyZJUsLoEbA_FCWPYGg1NiYqSjvv8Z0ABRs"
    postdraft_sheet_id = "19MKSdFfwFnOhDwGacrQPHmJJaQTbIAXn_UPM5p5wmW4"
    
    print("🔮 BUILDING VOLATILITY PREDICTION MODEL")
    print("=" * 70)
    print("Analyzing position + volatility + skill patterns for boom prediction")
    print("=" * 70)
    
    # Load draft data
    connector = SheetsConnector(verbose=False)
    
    # Pre-draft
    spreadsheet = connector.client.open_by_key(predraft_sheet_id)
    ws = spreadsheet.worksheets()[0]
    predraft_data = ws.get_all_records()
    
    # Post-draft
    spreadsheet = connector.client.open_by_key(postdraft_sheet_id)
    ws = spreadsheet.worksheets()[0]
    postdraft_data = ws.get_all_records()
    
    # Create lookups
    predraft_by_id = {str(p.get('PlayerID', '')): p for p in predraft_data if p.get('PlayerID')}
    postdraft_by_id = {str(p.get('PlayerID', '')): p for p in postdraft_data if p.get('PlayerID')}
    
    print(f"✅ Loaded {len(predraft_by_id)} pre-draft and {len(postdraft_by_id)} post-draft players")
    
    # Position-specific skills mapping (based on weights)
    position_key_skills = {
        'QB': ['PassAccuracy', 'ArmStrength', 'LookOffDef', 'Scrambling'],
        'RB': ['RouteRunning', 'Catching', 'BallSecurity', 'BreakTackle'],
        'WR': ['RouteRunning', 'Catching'],
        'TE': ['RouteRunning', 'Catching', 'Blocking'],
        'LT': ['Blocking'], 'LG': ['Blocking'], 'C': ['Blocking'], 'RG': ['Blocking'], 'RT': ['Blocking'],
        'LDE': ['PassRush', 'RunDefense'], 'RDE': ['PassRush', 'RunDefense'],
        'DT': ['PassRush', 'RunDefense'],
        'LLB': ['PassRush', 'RunDefense', 'ManCoverage', 'ZoneCoverage'],
        'MLB': ['PassRush', 'RunDefense', 'ManCoverage', 'ZoneCoverage'],
        'RLB': ['PassRush', 'RunDefense', 'ManCoverage', 'ZoneCoverage'],
        'LCB': ['ManCoverage', 'ZoneCoverage'], 'RCB': ['ManCoverage', 'ZoneCoverage'],
        'SS': ['ManCoverage', 'ZoneCoverage', 'Tackling'],
        'FS': ['ManCoverage', 'ZoneCoverage', 'Tackling']
    }
    
    # Collect volatility patterns
    volatility_patterns = {}  # {position: {skill: {vol_range: [changes]}}}
    
    print(f"\n🔍 Analyzing volatility patterns by position and skill...")
    
    for player_id in predraft_by_id:
        if player_id in postdraft_by_id:
            pre = predraft_by_id[player_id]
            post = postdraft_by_id[player_id]
            
            position = pre.get('Pos', '')
            volatility = float(pre.get('Volatility', 0)) if pre.get('Volatility') else 0
            
            # Only analyze positions we care about
            if position not in position_key_skills:
                continue
            
            # Categorize volatility
            if volatility <= 20:
                vol_range = 'Very Low (0-20)'
            elif volatility <= 40:
                vol_range = 'Low (21-40)'
            elif volatility <= 60:
                vol_range = 'Medium (41-60)'
            elif volatility <= 80:
                vol_range = 'High (61-80)'
            else:
                vol_range = 'Very High (81-100)'
            
            # Initialize position data
            if position not in volatility_patterns:
                volatility_patterns[position] = {}
            
            # Analyze each relevant skill for this position
            for skill in position_key_skills[position]:
                try:
                    pre_cur = float(pre.get(f'{skill}Cur', 0))
                    pre_max = float(pre.get(f'{skill}Max', 0))
                    post_max = float(post.get(f'{skill}Max', 0))
                    
                    if pre_cur > 0 and pre_max >= pre_cur:  # Valid data
                        gap = pre_max - pre_cur
                        max_change = post_max - pre_max
                        
                        # Initialize skill data
                        if skill not in volatility_patterns[position]:
                            volatility_patterns[position][skill] = {}
                        if vol_range not in volatility_patterns[position][skill]:
                            volatility_patterns[position][skill][vol_range] = []
                        
                        # Store the change data
                        volatility_patterns[position][skill][vol_range].append({
                            'pre_cur': pre_cur,
                            'pre_max': pre_max,
                            'post_max': post_max,
                            'gap': gap,
                            'max_change': max_change,
                            'volatility': volatility,
                            'name': f"{pre.get('FirstName', '')} {pre.get('LastName', '')}"
                        })
                except:
                    continue
    
    # Build prediction model
    prediction_model = {}
    
    print(f"\n📊 VOLATILITY PREDICTION MODEL BY POSITION:")
    print("=" * 90)
    
    for position in sorted(volatility_patterns.keys()):
        print(f"\n🎯 {position}:")
        print("-" * 50)
        
        prediction_model[position] = {}
        
        for skill in position_key_skills[position]:
            if skill in volatility_patterns[position]:
                print(f"\n  {skill}:")
                
                prediction_model[position][skill] = {}
                skill_data = volatility_patterns[position][skill]
                
                for vol_range in ['Very Low (0-20)', 'Low (21-40)', 'Medium (41-60)', 'High (61-80)', 'Very High (81-100)']:
                    if vol_range in skill_data and len(skill_data[vol_range]) >= 2:
                        changes = [d['max_change'] for d in skill_data[vol_range]]
                        gaps = [d['gap'] for d in skill_data[vol_range]]
                        
                        max_boom = max(changes)
                        max_bust = min(changes)
                        avg_change = sum(changes) / len(changes)
                        avg_gap = sum(gaps) / len(gaps)
                        
                        # Store prediction data
                        prediction_model[position][skill][vol_range] = {
                            'max_boom': max_boom,
                            'max_bust': max_bust,
                            'avg_change': avg_change,
                            'avg_gap': avg_gap,
                            'sample_size': len(changes),
                            'examples': skill_data[vol_range][:3]  # Top 3 examples
                        }
                        
                        print(f"    {vol_range:<18}: {len(changes):>2} samples, "
                              f"Max boom: {max_boom:+4.1f}, Max bust: {max_bust:+4.1f}, "
                              f"Avg: {avg_change:+4.1f}, Avg gap: {avg_gap:4.1f}")
                        
                        # Show best example
                        if changes:
                            best_example = max(skill_data[vol_range], key=lambda x: x['max_change'])
                            print(f"      Best: {best_example['name'][:20]:<20} "
                                  f"Gap:{best_example['gap']:3.0f} → {best_example['max_change']:+3.0f}")
    
    # Create prediction function
    def predict_skill_growth(position: str, skill: str, current: float, max_val: float, volatility: float) -> Dict:
        """Predict skill growth based on position, skill, and volatility patterns."""
        
        gap = max_val - current
        
        # Determine volatility range
        if volatility <= 20:
            vol_range = 'Very Low (0-20)'
        elif volatility <= 40:
            vol_range = 'Low (21-40)'
        elif volatility <= 60:
            vol_range = 'Medium (41-60)'
        elif volatility <= 80:
            vol_range = 'High (61-80)'
        else:
            vol_range = 'Very High (81-100)'
        
        # Get prediction from model
        if (position in prediction_model and 
            skill in prediction_model[position] and 
            vol_range in prediction_model[position][skill]):
            
            pattern = prediction_model[position][skill][vol_range]
            
            # Conservative prediction (average change)
            conservative_growth = pattern['avg_change']
            
            # Boom prediction (75th percentile of max_boom and avg_change)
            boom_growth = pattern['max_boom'] * 0.75
            
            # Bust prediction (75th percentile of max_bust and avg_change)  
            bust_growth = pattern['max_bust'] * 0.75
            
            return {
                'conservative': max_val + conservative_growth,
                'boom': min(100, max_val + boom_growth),  # Cap at 100
                'bust': max(current, max_val + bust_growth),  # Floor at current
                'confidence': 'High' if pattern['sample_size'] >= 5 else 'Medium',
                'sample_size': pattern['sample_size'],
                'pattern_data': pattern
            }
        else:
            # Fallback prediction if no specific pattern found
            if volatility <= 30:
                growth_factor = 0.3
            elif volatility <= 60:
                growth_factor = 0.5
            else:
                growth_factor = 0.7
            
            fallback_growth = gap * growth_factor * 0.4  # Conservative fallback
            
            return {
                'conservative': max_val + fallback_growth * 0.5,
                'boom': min(100, max_val + fallback_growth),
                'bust': max(current, max_val - fallback_growth * 0.5),
                'confidence': 'Low',
                'sample_size': 0,
                'pattern_data': None
            }
    
    # Save model and return prediction function
    return prediction_model, predict_skill_growth

def test_prediction_model():
    """Test the prediction model with some examples."""
    print(f"\n🧪 TESTING PREDICTION MODEL:")
    print("=" * 60)
    
    model, predict_growth = build_volatility_prediction_model()
    
    # Test cases
    test_cases = [
        {'pos': 'QB', 'skill': 'PassAccuracy', 'cur': 30, 'max': 55, 'vol': 85, 'desc': 'High vol QB with low accuracy'},
        {'pos': 'QB', 'skill': 'PassAccuracy', 'cur': 50, 'max': 75, 'vol': 25, 'desc': 'Low vol QB with med accuracy'},
        {'pos': 'WR', 'skill': 'RouteRunning', 'cur': 40, 'max': 70, 'vol': 70, 'desc': 'High vol WR'},
        {'pos': 'LDE', 'skill': 'PassRush', 'cur': 35, 'max': 60, 'vol': 90, 'desc': 'Very high vol pass rusher'},
    ]
    
    print(f"{'Test Case':<30} {'Conservative':<12} {'Boom':<8} {'Bust':<8} {'Confidence':<10}")
    print("-" * 70)
    
    for test in test_cases:
        prediction = predict_growth(test['pos'], test['skill'], test['cur'], test['max'], test['vol'])
        print(f"{test['desc'][:29]:<30} {prediction['conservative']:<12.1f} {prediction['boom']:<8.1f} "
              f"{prediction['bust']:<8.1f} {prediction['confidence']:<10}")
    
    return model, predict_growth

if __name__ == "__main__":
    model, predictor = test_prediction_model()