#!/usr/bin/env python3
"""
Draft-Prioritized Multi-Position Analyzer
Creates the exact same format as the existing tab but with enhanced boom predictions
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent / "boom_analysis"))
sys.path.append(str(Path(__file__).parent.parent / "archive"))

from fixed_projection_analyzer import FixedProjectionAnalyzer

class DraftPrioritizedAnalyzer(FixedProjectionAnalyzer):
    """Analyzer that matches the exact format of Draft-Prioritized Multi-Position Analysis."""
    
    def analyze_player_max_potential(self, prospect: Dict) -> Dict:
        """Calculate player's ENHANCED MAX POTENTIAL rating (like original tab)."""
        analysis = {
            'player_name': f"{prospect['first_name']} {prospect['last_name']}",
            'original_position': prospect['position'],
            'volatility': prospect['volatility'],
            'current_weight': prospect.get('weight', 200),
            'base_speed': prospect.get('MaxSpeed_current', 50),
            'position_ratings': {},
            'best_position': None,
            'best_current_rating': 0,
            'best_projected_rating': 0,  # This will be ENHANCED max potential
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
            
            # Current rating at this position
            current_rating, current_debug = self._calculate_position_rating_fixed(prospect, position, use_current=True)
            # MAX potential rating 
            max_rating, max_debug = self._calculate_position_rating_fixed(prospect, position, use_current=False)
            
            # Apply enhancement like original tab (volatility and speed bonuses)
            enhanced_rating = self._apply_original_enhancement(
                max_rating, prospect['volatility'], adjusted_speed, position
            )
            
            analysis['position_ratings'][position] = {
                'current': current_rating,
                'max_potential': max_rating,
                'projected': enhanced_rating,  # Use enhanced rating
                'improvement': enhanced_rating - current_rating,
                'adjusted_speed': adjusted_speed,
                'speed_qualified': adjusted_speed >= 88,
                'debug_info': current_debug[:5]  # Store top 5 skills for debugging
            }
            
            # Track best position using ENHANCED rating (like original tab)
            if enhanced_rating > analysis['best_projected_rating']:
                analysis['best_position'] = position
                analysis['best_current_rating'] = current_rating
                analysis['best_projected_rating'] = enhanced_rating  # Use enhanced rating
                analysis['best_adjusted_speed'] = adjusted_speed
        
        return analysis
    
    def _apply_original_enhancement(self, max_rating: float, volatility: float, 
                                  adjusted_speed: float, position: str) -> float:
        """Apply enhancement bonuses like the original tab."""
        enhanced = max_rating
        
        # Volatility bonus - high volatility players get potential boost
        if volatility >= 80:
            enhanced += 8.0  # High volatility bonus
        elif volatility >= 60:
            enhanced += 6.0  # Medium-high volatility bonus
        elif volatility >= 40:
            enhanced += 4.0  # Medium volatility bonus
        elif volatility >= 20:
            enhanced += 2.0  # Low volatility bonus
        
        # Speed bonus for skill positions
        skill_positions = ['WR', 'RB', 'TE', 'FS', 'SS', 'QB']
        if position in skill_positions and adjusted_speed >= 85:
            speed_bonus = min(6.0, (adjusted_speed - 85) * 0.5)  # Up to 6 point bonus
            enhanced += speed_bonus
        
        # Position-specific bonuses
        if position == 'QB' and volatility <= 30:  # Stable QBs get bonus
            enhanced += 3.0
        
        return min(100.0, enhanced)  # Cap at 100
    
    def calculate_boom_percentage(self, prospect: Dict, position: str, max_rating: float, boom_rating: float) -> str:
        """Calculate boom percentage based on volatility and improvement potential."""
        volatility = prospect['volatility']
        improvement = boom_rating - max_rating
        
        # Base boom chance on volatility
        if volatility >= 80:
            base_boom = 75
        elif volatility >= 60:
            base_boom = 60
        elif volatility >= 40:
            base_boom = 45
        elif volatility >= 20:
            base_boom = 30
        else:
            base_boom = 15
        
        # Adjust based on improvement potential
        if improvement >= 5:
            base_boom += 15
        elif improvement >= 2:
            base_boom += 10
        elif improvement >= 1:
            base_boom += 5
        
        # Cap at 95%
        boom_chance = min(95, base_boom)
        
        return f"{boom_chance}%"
    
    def get_player_profile(self, prospect: Dict, best_position: str) -> str:
        """Generate player profile based on position and characteristics."""
        volatility = prospect['volatility']
        speed = prospect.get('MaxSpeed_current', 50)
        
        profiles = []
        
        # Position-based profiles
        if best_position in ['QB']:
            profiles.append("Field General")
        elif best_position in ['RB', 'FB']:
            if speed >= 85:
                profiles.append("Speed Back")
            else:
                profiles.append("Power Runner")
        elif best_position in ['WR']:
            if speed >= 90:
                profiles.append("Burner")
            else:
                profiles.append("Possession WR")
        elif best_position in ['TE']:
            profiles.append("Hybrid TE")
        elif best_position in ['LT', 'LG', 'C', 'RG', 'RT']:
            profiles.append("Anchor")
        elif best_position in ['LDE', 'RDE']:
            if speed >= 85:
                profiles.append("Speed Rusher")
            else:
                profiles.append("Power Rusher")
        elif best_position in ['DT']:
            profiles.append("Run Stopper")
        elif best_position in ['LLB', 'MLB', 'RLB']:
            if speed >= 85:
                profiles.append("Coverage LB")
            else:
                profiles.append("Run Stopper")
        elif best_position in ['LCB', 'RCB']:
            if speed >= 90:
                profiles.append("Lockdown CB")
            else:
                profiles.append("Zone CB")
        elif best_position in ['FS', 'SS']:
            if speed >= 88:
                profiles.append("Ball Hawk")
            else:
                profiles.append("In-Box Safety")
        
        # Volatility-based additions
        if volatility >= 80:
            profiles.append("High Risk/Reward")
        elif volatility >= 60:
            profiles.append("Developmental")
        
        return ", ".join(profiles) if profiles else "Solid Prospect"

def run_draft_prioritized_analysis():
    """Run analysis in the exact format of Draft-Prioritized Multi-Position Analysis."""
    sheet_id = "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"
    
    print("🚀 DRAFT-PRIORITIZED MULTI-POSITION ANALYSIS (Enhanced)")
    print("=" * 70)
    print("Matching existing format with enhanced boom predictions")
    print("=" * 70)
    
    analyzer = DraftPrioritizedAnalyzer(sheet_id, verbose=True)
    analyzer.load_data()
    
    # Analyze all non-specialist prospects
    analyses = []
    used_players = set()
    
    print(f"\n🔬 Analyzing prospects...")
    
    for prospect in analyzer.draft_prospects:
        if prospect['position'] not in ['P', 'K']:  # Skip specialists
            player_name = f"{prospect['first_name']} {prospect['last_name']}"
            if player_name not in used_players:
                # Use MAX POTENTIAL method to match original tab's high ratings
                analysis = analyzer.analyze_player_max_potential(prospect)
                analyses.append((prospect, analysis))  # Store both prospect and analysis
                used_players.add(player_name)
    
    print(f"✅ Analyzed {len(analyses)} prospects")
    
    # Sort prioritizing speed-qualified skill positions (same as original Draft-Prioritized tab)
    def draft_priority_sort_key(analysis_tuple):
        prospect, analysis = analysis_tuple
        
        # Position groups for prioritization
        skill_positions = ['WR', 'RB', 'TE', 'FS', 'SS', 'QB']
        premium_positions = ['QB', 'LT', 'RT', 'LG', 'RG', 'C'] 
        
        best_pos = analysis['best_position']
        rating = analysis['best_projected_rating']
        speed_qualified = analysis['best_adjusted_speed'] >= 88
        
        # Priority tiers:
        # 1. Speed-qualified skill positions (highest priority)
        # 2. Speed-qualified premium positions  
        # 3. Non-speed-qualified skill positions
        # 4. Everything else by rating
        
        if speed_qualified and best_pos in skill_positions:
            priority = 4  # Highest priority
        elif speed_qualified and best_pos in premium_positions:
            priority = 3
        elif best_pos in skill_positions:
            priority = 2
        else:
            priority = 1  # Lowest priority
            
        return (priority, rating)
    
    analyses.sort(key=draft_priority_sort_key, reverse=True)
    
    # Export to Google Sheets in exact format
    print(f"\n📤 Exporting to Google Sheets in Draft-Prioritized format...")
    export_draft_prioritized(analyses, analyzer, sheet_id)
    
    # Display draft board in target format
    print(f"\n🎯 DRAFT-PRIORITIZED MULTI-POSITION ANALYSIS")
    print("=" * 120)
    print(f"{'Rank':<4} {'Name':<16} {'Orig':<4} {'Vol':<3} {'Cur':<3} {'Best Pos':<8} {'Best OVR':<8} {'Max Spd':<7} {'2nd Pos':<8} {'2nd OVR':<7} {'Profile':<20}")
    print("-" * 120)
    
    for i, (prospect, analysis) in enumerate(analyses[:30], 1):  # Top 30        
        name = analysis['player_name'][:15]
        orig_pos = analysis['original_position'][:3]
        vol = int(analysis['volatility'])
        cur_rating = int(prospect.get('current_overall', 50))  # Current overall
        
        best_pos = analysis['best_position'][:7]
        best_ovr = analysis['best_projected_rating']
        max_spd = analysis['best_adjusted_speed']
        
        # Get second best position
        positions_sorted = sorted(analysis['position_ratings'].items(), 
                                key=lambda x: x[1]['projected'], reverse=True)
        second_pos = positions_sorted[1][0][:7] if len(positions_sorted) > 1 else ""
        second_ovr = positions_sorted[1][1]['projected'] if len(positions_sorted) > 1 else 0
        
        profile = analyzer.get_player_profile(prospect, best_pos)[:19]
        
        print(f"{i:<4} {name:<16} {orig_pos:<4} {vol:<3} {cur_rating:<3} {best_pos:<8} {best_ovr:<8.1f} {max_spd:<7.1f} {second_pos:<8} {second_ovr:<7.1f} {profile:<20}")
    
    return analyses

def export_draft_prioritized(analyses: List, analyzer, sheet_id: str):
    """Export in exact Draft-Prioritized Multi-Position Analysis format."""
    
    from sheets_connector import SheetsConnector
    
    # Prepare data for export
    export_data = []
    
    # Header row - exact match
    headers = [
        'Rank', 'Name', 'Orig', 'Vol', 'Cur', 'Best Pos', 'Best OVR', 'Max Spd',
        '2nd Pos', '2nd OVR', '3rd Pos', '3rd OVR', 'Profile', 'Boom%'
    ]
    export_data.append(headers)
    
    # Data rows
    for i, (prospect, analysis) in enumerate(analyses, 1):  # All prospects
        # Use original analysis results directly
        name = analysis['player_name']
        orig_pos = analysis['original_position']
        vol = int(analysis['volatility'])
        cur_rating = int(prospect.get('current_overall', 50))  # Current overall rating
        
        # Use original projected ratings
        best_pos = analysis['best_position']
        best_ovr = round(analysis['best_projected_rating'], 1)
        max_spd = round(analysis['best_adjusted_speed'], 1)
        
        # Get top 3 positions from original analysis
        positions_sorted = sorted(analysis['position_ratings'].items(), 
                                key=lambda x: x[1]['projected'], reverse=True)
        
        second_pos = positions_sorted[1][0] if len(positions_sorted) > 1 else ""
        second_ovr = round(positions_sorted[1][1]['projected'], 1) if len(positions_sorted) > 1 else 0
        
        third_pos = positions_sorted[2][0] if len(positions_sorted) > 2 else ""
        third_ovr = round(positions_sorted[2][1]['projected'], 1) if len(positions_sorted) > 2 else 0
        
        # Profile and boom percentage
        profile = analyzer.get_player_profile(prospect, best_pos)
        boom_pct = analyzer.calculate_boom_percentage(
            prospect, best_pos, 
            analysis['best_current_rating'],
            best_ovr
        )
        
        row = [
            i,  # Rank
            name,  # Name
            orig_pos,  # Orig
            vol,  # Vol
            cur_rating,  # Cur
            best_pos,  # Best Pos
            best_ovr,  # Best OVR
            max_spd,  # Max Spd
            second_pos,  # 2nd Pos
            second_ovr,  # 2nd OVR
            third_pos,  # 3rd Pos
            third_ovr,  # 3rd OVR
            profile,  # Profile
            boom_pct  # Boom%
        ]
        export_data.append(row)
    
    # Export using sheets connector
    connector = SheetsConnector(verbose=True)
    
    try:
        # Export directly using raw data
        spreadsheet = connector.client.open_by_key(sheet_id)
        
        # Update the ORIGINAL tab instead of creating a new one
        try:
            worksheet = spreadsheet.worksheet("Draft-Prioritized Multi-Position Analysis")
            # Clear existing content
            worksheet.clear()
            print(f"✅ Updating original 'Draft-Prioritized Multi-Position Analysis' tab")
        except:
            # Fallback to creating new worksheet
            worksheet = spreadsheet.add_worksheet(title="Draft-Prioritized Multi-Position Analysis", rows=1000, cols=15)
            print(f"✅ Created new 'Draft-Prioritized Multi-Position Analysis' tab")
        
        # Export the data directly
        if export_data:
            # Update with all data at once
            worksheet.update(values=export_data, range_name=f'A1:N{len(export_data)}')
            
            print(f"✅ Exported {len(export_data)-1} players to Google Sheets")
            print(f"✅ Updated 'Draft-Prioritized Multi-Position Analysis' tab with current data")
        else:
            print("❌ No data to export")
            
    except Exception as e:
        print(f"❌ Error exporting to sheets: {e}")
        print("Draft board analysis completed locally")

if __name__ == "__main__":
    analyses = run_draft_prioritized_analysis()