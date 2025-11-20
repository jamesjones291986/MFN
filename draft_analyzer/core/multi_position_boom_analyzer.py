#!/usr/bin/env python3
"""
Multi-Position Boom Analyzer
Calculates each player's boom potential at every position to find optimal placement
"""

import sys
from pathlib import Path
import csv

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from proper_boom_projection_model import ProperBoomProjectionModel
from sheets_connector import SheetsConnector

class MultiPositionBoomAnalyzer:
    """Analyzer that finds each player's best position and overall potential."""
    
    def __init__(self):
        self.boom_model = ProperBoomProjectionModel()
        self.all_positions = ['QB', 'RB', 'FB', 'TE', 'WR', 'LT', 'LG', 'C', 'RG', 'RT', 
                             'LDE', 'DT', 'RDE', 'SLB', 'MLB', 'WLB', 'CB', 'SS', 'FS', 'P', 'K']
        
        # Key skills for each position based on weights analysis
        self.position_key_skills = {
            'QB': 'PassAccuracyMax',
            'RB': 'MaxSpeedMax', 
            'FB': 'MaxSpeedMax',
            'TE': 'MaxSpeedMax',
            'WR': 'MaxSpeedMax',
            'LT': 'PassBlockingMax',
            'LG': 'PassBlockingMax',
            'C': 'PassBlockingMax',
            'RG': 'PassBlockingMax',
            'RT': 'PassBlockingMax',
            'LDE': 'MaxSpeedMax',
            'DT': 'StrengthMax',
            'RDE': 'MaxSpeedMax',
            'SLB': 'MaxSpeedMax',
            'MLB': 'MaxSpeedMax',
            'WLB': 'MaxSpeedMax',
            'CB': 'MaxSpeedMax',
            'SS': 'MaxSpeedMax',
            'FS': 'MaxSpeedMax',
            'P': 'PuntStrengthMax',
            'K': 'KickAccuracyMax'
        }
        
        # Minimum skill requirements for position eligibility
        self.position_min_requirements = {
            'QB': 50,   # Pass Accuracy minimum
            'RB': 75,   # Max Speed minimum for skill positions
            'FB': 75,   # Max Speed minimum 
            'TE': 75,   # Max Speed minimum for TE
            'WR': 80,   # Max Speed minimum for WR
            'LT': 40,   # Pass Blocking minimum (can boom +32)
            'LG': 40,   # Pass Blocking minimum
            'C': 40,    # Pass Blocking minimum
            'RG': 40,   # Pass Blocking minimum
            'RT': 40,   # Pass Blocking minimum
            'LDE': 70,  # Max Speed minimum for edge rush
            'DT': 50,   # Strength minimum for DT
            'RDE': 70,  # Max Speed minimum for edge rush
            'SLB': 70,  # Max Speed minimum for coverage
            'MLB': 60,  # Max Speed minimum (lower for run-stuffing)
            'WLB': 70,  # Max Speed minimum for coverage
            'CB': 80,   # Max Speed minimum for coverage
            'SS': 75,   # Max Speed minimum
            'FS': 80,   # Max Speed minimum for deep coverage
            'P': 60,    # Punt Strength minimum
            'K': 60     # Kick Accuracy minimum
        }
    
    def get_valid_positions_for_player(self, original_position):
        """Get valid positions a player can move to based on restrictions."""
        # Define restricted moves
        big_men = ['DT', 'RDE', 'LDE']
        defensive_backs = ['CB', 'SS', 'FS'] 
        offensive_line = ['LT', 'RT', 'LG', 'RG', 'C']
        
        valid_positions = []
        
        for position in self.all_positions:
            # Big men cannot go to defensive backs
            if original_position in big_men and position in defensive_backs:
                continue
            
            # Offensive line players can only go to other OL positions
            if original_position in offensive_line and position not in offensive_line:
                continue
            
            # Non-OL players cannot go to OL positions
            if original_position not in offensive_line and position in offensive_line:
                continue
                
            # TE cannot go to WR
            if original_position == 'TE' and position == 'WR':
                continue
            
            # Position is valid
            valid_positions.append(position)
        
        return valid_positions

    def is_position_eligible(self, player_data, position):
        """Check if player meets minimum skill requirements for a position."""
        key_skill = self.position_key_skills.get(position)
        min_requirement = self.position_min_requirements.get(position, 0)
        
        if not key_skill or min_requirement == 0:
            return True  # No requirements defined
        
        try:
            skill_value = float(player_data.get(key_skill, 0))
            
            # For speed-based positions, check weight-adjusted speed
            if key_skill == 'MaxSpeedMax':
                current_weight = float(player_data.get('Weight', 200))
                target_weight = self.boom_model.position_target_weights.get(position, current_weight)
                weight_change = target_weight - current_weight
                speed_change = -(weight_change / 9.5)
                adjusted_speed = max(0, min(100, skill_value + speed_change))
                return adjusted_speed >= min_requirement
            else:
                return skill_value >= min_requirement
        except (ValueError, TypeError):
            return False

    def analyze_player_all_positions(self, player_data):
        """Calculate a player's overall at every valid position after boom."""
        try:
            name = f"{player_data.get('FirstName', '')} {player_data.get('LastName', '')}"
            original_position = player_data.get('Pos', 'QB')
            volatility = float(player_data.get('Volatility', 0))
            current_overall = float(player_data.get('Cur', 0))
            
            # Get valid positions for this player based on restrictions
            valid_positions = self.get_valid_positions_for_player(original_position)
            
            # Get the player's projected boom skills (same regardless of position)
            projected_skills, profile_name, boom_prob, weight_adjustment = self.boom_model.project_boom_skills(player_data, volatility)
            
            # Calculate overall at each valid position
            position_overalls = {}
            
            for position in valid_positions:
                # Check if player is eligible for this position based on key skill
                if not self.is_position_eligible(player_data, position):
                    continue
                    
                try:
                    # Calculate weight adjustment for this position
                    current_weight = float(player_data.get('Weight', 200))
                    target_weight = self.boom_model.position_target_weights.get(position, current_weight)
                    weight_change = target_weight - current_weight
                    speed_change = -(weight_change / 9.5)
                    
                    # Adjust speed skills for this position's weight
                    adjusted_skills = projected_skills.copy()
                    if 'MaxSpeed' in adjusted_skills:
                        original_max = adjusted_skills['MaxSpeed']['max']
                        original_speed = adjusted_skills['MaxSpeed']['projected_max']
                        adjusted_speed = max(0, min(100, original_speed + speed_change))
                        # Use proper boom model calculation: 80% of the way from max to new projected max
                        projected_current = original_max + (adjusted_speed - original_max) * 0.8
                        adjusted_skills['MaxSpeed'] = {
                            **adjusted_skills['MaxSpeed'],
                            'projected_current': min(projected_current, adjusted_speed),
                            'projected_max': adjusted_speed
                        }
                    
                    if 'Acceleration' in adjusted_skills:
                        original_max = adjusted_skills['Acceleration']['max']
                        original_accel = adjusted_skills['Acceleration']['projected_max']
                        adjusted_accel = max(0, min(100, original_accel + speed_change))
                        # Use proper boom model calculation: 80% of the way from max to new projected max
                        projected_current = original_max + (adjusted_accel - original_max) * 0.8
                        adjusted_skills['Acceleration'] = {
                            **adjusted_skills['Acceleration'],
                            'projected_current': min(projected_current, adjusted_accel),
                            'projected_max': adjusted_accel
                        }
                    
                    # Calculate overall for this position
                    overall = self.boom_model.calculate_overall_rating(position, adjusted_skills)
                    
                    position_overalls[position] = {
                        'overall': round(overall, 1),
                        'weight_change': round(weight_change, 1),
                        'speed_change': round(speed_change, 1)
                    }
                    
                except Exception as e:
                    position_overalls[position] = {
                        'overall': 0.0,
                        'weight_change': 0.0,
                        'speed_change': 0.0
                    }
            
            # Find best positions
            sorted_positions = sorted(position_overalls.items(), key=lambda x: x[1]['overall'], reverse=True)
            
            # Apply position preference logic: prefer LB over DE unless DE is clearly the only good option
            best_position = sorted_positions[0][0]
            best_overall = sorted_positions[0][1]['overall']
            
            # Check if best position is DE and if we should prefer LB instead
            if best_position in ['LDE', 'RDE'] and len(sorted_positions) > 1:
                second_best_overall = sorted_positions[1][1]['overall']
                
                # Only keep DE as best position if 2nd best is 65 or less
                if second_best_overall > 65:
                    # Look for the best non-DE, non-DT position
                    for pos, data in sorted_positions:
                        if pos not in ['LDE', 'RDE', 'DT']:
                            best_position = pos
                            best_overall = data['overall']
                            break
            
            # Calculate projected max speed at best position
            best_position_data = sorted_positions[0][1]
            current_weight = float(player_data.get('Weight', 200))
            target_weight = self.boom_model.position_target_weights.get(best_position, current_weight)
            weight_change = target_weight - current_weight
            speed_change = -(weight_change / 9.5)
            
            original_max_speed = float(player_data.get('MaxSpeedMax', 0))
            projected_max_speed_at_best_pos = max(0, min(100, original_max_speed + speed_change))
            
            top_positions = []
            for pos, data in sorted_positions[:5]:
                top_positions.append({
                    'position': pos,
                    'overall': data['overall'],
                    'weight_change': data['weight_change'],
                    'speed_change': data['speed_change']
                })
            
            return {
                'name': name,
                'original_position': original_position,
                'volatility': volatility,
                'current_overall': current_overall,
                'best_position': best_position,
                'best_overall': best_overall,
                'projected_max_speed_at_best_pos': round(projected_max_speed_at_best_pos, 1),
                'volatility_profile': profile_name,
                'boom_probability': boom_prob * 100,
                'current_weight': current_weight,
                'top_positions': top_positions,
                'all_position_overalls': position_overalls
            }
            
        except Exception as e:
            print(f"Error analyzing {player_data.get('FirstName', '')} {player_data.get('LastName', '')}: {e}")
            return None
    
    def get_position_tier(self, position):
        """Return tier for positions (lower tier = higher priority)."""
        if position in ['QB', 'WR', 'RB', 'TE', 'CB', 'FS', 'SS']:
            return 1  # Premium positions - sort by overall within this tier
        elif position in ['MLB', 'WLB', 'SLB', 'LT', 'RT', 'C', 'LG', 'RG', 'FB']:
            return 2  # Mid-round positions - sort by overall within this tier  
        else:  # LDE, RDE, DT, K, P
            return 3  # Late round positions - sort by overall within this tier
    
    def should_filter_player(self, player_data, projection):
        """Check if player should be filtered out based on position-specific requirements."""
        try:
            # Get player data
            max_speed = float(player_data.get('MaxSpeedMax', 0))
            current_speed = float(player_data.get('MaxSpeedCur', 0))
            original_position = player_data.get('Pos', '')
            pass_blocking_max = float(player_data.get('PassBlockingMax', 0))
            
            # Get all position overalls
            all_overalls = [pos['overall'] for pos in projection['top_positions']]
            max_overall = max(all_overalls) if all_overalls else 0
            
            # Speed positions that absolutely need speed
            speed_critical_positions = ['WR', 'RB', 'CB', 'FS', 'SS']
            
            # Check if player's best position is speed-critical
            best_position = projection['best_position']
            
            # Filter 1: K/P specialists - must be 90+ projected overall
            if best_position in ['K', 'P']:
                if max_overall < 90:
                    return True, f"K/P specialist ({best_position}) but only {max_overall:.1f} overall (need 90+)"
            
            # Filter 2: DE players - must have 70+ overall OR 80+ speed
            if best_position in ['LDE', 'RDE']:
                if max_overall < 70 and max_speed < 80:
                    return True, f"DE ({best_position}) with {max_overall:.1f} overall and {max_speed} speed (need 70+ overall OR 80+ speed)"
            
            # Filter 2b: Players projected as DE but too slow - check if DT is viable
            if best_position in ['LDE', 'RDE'] and max_speed < 75:
                # For slow players projected as DE, check their DT projection instead
                dt_overalls = [pos['overall'] for pos in projection['top_positions'] 
                             if pos['position'] == 'DT']
                max_dt_overall = max(dt_overalls) if dt_overalls else 0
                
                if max_dt_overall < 75:
                    return True, f"Slow DE ({best_position}) with {max_speed} speed, but DT projection only {max_dt_overall:.1f} (need 75+ for DT)"
            
            # Filter 3: DT players - must have 75+ overall
            if best_position == 'DT':
                if max_overall < 75:
                    return True, f"DT with only {max_overall:.1f} overall (need 75+)"
            
            # Filter 4: Speed-critical positions with insufficient speed
            if best_position in speed_critical_positions:
                if max_speed < 70:
                    return True, f"Speed position ({best_position}) but only {max_speed} max speed"
            
            # Filter 5: TE special case - needs speed OR OL viability
            if original_position == 'TE':
                # If TE has low speed, check if viable at OL
                if max_speed < 70:
                    # Check if has good pass blocking AND can get 70+ overall at OL
                    ol_positions = ['LT', 'LG', 'C', 'RG', 'RT']
                    ol_overalls = [pos['overall'] for pos in projection['top_positions'] 
                                 if pos['position'] in ol_positions]
                    max_ol_overall = max(ol_overalls) if ol_overalls else 0
                    
                    if pass_blocking_max < 50 or max_ol_overall < 70:  # Lower PB threshold since it can boom +32
                        return True, f"TE with low speed ({max_speed}) and insufficient OL ability (PB:{pass_blocking_max}, OL:{max_ol_overall})"
            
            # Filter 6: OL positions need pass blocking (but it can boom +32!)
            ol_positions = ['LT', 'LG', 'C', 'RG', 'RT']
            if best_position in ol_positions:
                if pass_blocking_max < 40:  # Very low threshold - PB can boom +32 points
                    return True, f"OL position ({best_position}) but only {pass_blocking_max} pass blocking (too low even with boom)"
            
            # Filter 7: High speed potential but low current speed (original filter)
            if max_speed >= 95:
                if current_speed < 75:
                    return True, f"High speed potential ({max_speed}) but low current speed ({current_speed})"
            
            # Filter 8: Medium speed range with low overall everywhere
            if 75 <= max_speed <= 84:
                if max_overall < 70:
                    return True, f"Medium speed ({max_speed}) but low overall ({max_overall})"
            
            # Filter 9: Very low overall everywhere (catch-all)
            if max_overall < 50:
                return True, f"Very low overall ({max_overall}) at all positions"
            
            # Filter 10: Players with 65 or less max overall (with exception for 65-69 with high key skill)
            if max_overall <= 65:
                return True, f"Max overall only {max_overall:.1f} (too low for draft consideration)"
            
            # Filter 11: Players with 65-69 overall but lacking high key skill
            if 65 < max_overall < 70:
                key_skill = self.position_key_skills.get(best_position)
                if key_skill:
                    key_skill_value = float(player_data.get(key_skill, 0))
                    if key_skill_value < 80:
                        return True, f"Low-mid overall ({max_overall:.1f}) without elite key skill ({key_skill}: {key_skill_value})"
            
            return False, ""
            
        except (ValueError, TypeError) as e:
            return False, f"Error parsing player data: {e}"

    def analyze_rookie_class_multi_position(self, rookies_data):
        """Analyze entire rookie class across all positions with filtering and prioritization."""
        print(f"🔄 Analyzing {len(rookies_data)} rookies across all {len(self.all_positions)} positions...")
        
        multi_position_projections = []
        filtered_count = 0
        filter_reasons = {}
        
        for i, rookie in enumerate(rookies_data, 1):
            if i % 50 == 0:
                print(f"   Processed {i}/{len(rookies_data)} players...")
            
            projection = self.analyze_player_all_positions(rookie)
            if projection:
                # Check if player should be filtered
                should_filter, reason = self.should_filter_player(rookie, projection)
                
                if should_filter:
                    filtered_count += 1
                    filter_reasons[reason] = filter_reasons.get(reason, 0) + 1
                    continue
                
                multi_position_projections.append(projection)
        
        print(f"   Filtered out {filtered_count} players:")
        for reason, count in filter_reasons.items():
            print(f"     - {count} players: {reason}")
        
        # Custom sort: First by position tier, then by overall (highest first) within each tier
        def sort_key(projection):
            position_tier = self.get_position_tier(projection['best_position'])
            return (position_tier, -projection['best_overall'])  # negative for descending overall
        
        multi_position_projections.sort(key=sort_key)
        
        return multi_position_projections
    
    def create_sheets_output(self, projections, sheet_id):
        """Create a new sheet tab with the multi-position analysis."""
        try:
            connector = SheetsConnector(verbose=True)
            sheet = connector.client.open_by_key(sheet_id)
            
            # Create new worksheet
            new_ws_name = "Draft-Prioritized Multi-Position Analysis"
            
            # Delete if exists
            try:
                existing_ws = sheet.worksheet(new_ws_name)
                sheet.del_worksheet(existing_ws)
            except:
                pass
            
            # Create new worksheet
            new_ws = sheet.add_worksheet(title=new_ws_name, rows=len(projections)+10, cols=15)
            
            # Create headers (shortened for cleaner display)
            headers = [
                'Rank', 'Name', 'Orig', 'Vol', 'Cur', 'Best Pos', 'Best OVR', 'Max Spd',
                '2nd Pos', '2nd OVR', '3rd Pos', '3rd OVR', 'Profile', 'Boom%'
            ]
            
            # Add headers
            new_ws.update('A1', [headers])
            
            # Prepare data rows
            data_rows = []
            for i, projection in enumerate(projections, 1):
                top_pos = projection['top_positions']
                
                row = [
                    i,  # Rank
                    projection['name'],
                    projection['original_position'],
                    projection['volatility'],
                    projection['current_overall'],
                    projection['best_position'],
                    projection['best_overall'],
                    projection['projected_max_speed_at_best_pos'],
                    top_pos[1]['position'] if len(top_pos) > 1 else '',
                    top_pos[1]['overall'] if len(top_pos) > 1 else 0,
                    top_pos[2]['position'] if len(top_pos) > 2 else '',
                    top_pos[2]['overall'] if len(top_pos) > 2 else 0,
                    projection['volatility_profile'],
                    f"{projection['boom_probability']:.0f}%"
                ]
                data_rows.append(row)
            
            # Add data in batches (Google Sheets has limits)
            batch_size = 200
            for i in range(0, len(data_rows), batch_size):
                batch = data_rows[i:i+batch_size]
                start_row = i + 2  # +2 because row 1 is headers, and we're 0-indexed
                end_row = start_row + len(batch) - 1
                
                range_name = f'A{start_row}:N{end_row}'  # 14 columns now
                new_ws.update(range_name, batch)
            
            print(f"✅ Created new sheet tab: '{new_ws_name}'")
            return new_ws.url
            
        except Exception as e:
            print(f"❌ Failed to create Google Sheet: {e}")
            return None

def refresh_rookies_data(sheet_id=None):
    """Refresh rookies data from Google Sheets and save to CSV."""
    print("🔄 Refreshing rookies data from Google Sheets...")
    
    try:
        connector = SheetsConnector(verbose=True)
        if not connector.client:
            print("❌ Failed to connect to Google Sheets")
            return False
        
        # Use default sheet ID if not provided
        if not sheet_id:
            sheet_id = "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"
        
        # Load from Player Import tab
        sheet = connector.client.open_by_key(sheet_id)
        worksheet = sheet.worksheet("Player Import")  # Adjust tab name if needed
        rookies_data = worksheet.get_all_records()
        
        # Filter to rookies only
        rookies = [row for row in rookies_data if row.get('Exp') == 'R']
        
        print(f"📥 Downloaded {len(rookies)} rookies from Google Sheets")
        
        # Save to CSV
        csv_file = "live_rookies.csv"
        if rookies:
            with open(csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=rookies[0].keys())
                writer.writeheader()
                writer.writerows(rookies)
            
            print(f"💾 Saved {len(rookies)} rookies to {csv_file}")
            return True
        else:
            print("⚠️ No rookie data found")
            return False
            
    except Exception as e:
        print(f"❌ Error refreshing data: {e}")
        return False

def analyze_rookies_multi_position(csv_file_path="live_rookies.csv", sheet_id=None, refresh=False):
    """Main function to analyze rookies across all positions."""
    
    # Refresh data if requested
    if refresh:
        if not refresh_rookies_data(sheet_id):
            print("❌ Failed to refresh data, using existing CSV file")
    
    analyzer = MultiPositionBoomAnalyzer()
    
    print(f"🚀 MULTI-POSITION BOOM ANALYZER (Draft-Prioritized)")
    print("=" * 100)
    print("🎯 Finding each player's BEST position prioritized by draft value")
    print("📊 Speed filtering: Remove 100spd/75cur and 75-84spd/<70ovr players")
    print("🚫 Position restrictions: No big men→DBs, OL stays OL, no TE→WR")
    print("📋 Tier 1: QB/WR/RB/TE/CB/FS/SS → Tier 2: LBs/OL/FB → Tier 3: DE/DT/K/P")
    
    try:
        # Load rookie data
        rookies_data = []
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rookies_data.append(row)
        
        print(f"\n✅ Loaded {len(rookies_data)} rookies from {csv_file_path}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file_path}")
        print("💡 Try running with --refresh to download fresh data from Google Sheets")
        return
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return
    
    # Analyze all players across all positions
    projections = analyzer.analyze_rookie_class_multi_position(rookies_data)
    
    if not projections:
        print("❌ No valid projections generated")
        return
    
    print(f"\n📊 Analyzed {len(projections)} players across all positions")
    
    # Display top prospects by tier and overall
    print(f"\n🏆 TOP DRAFT PROSPECTS (Tier 1: Premium Positions by Overall)")
    print("=" * 140)
    print(f"{'#':<3} {'Name':<25} {'Orig':<4} {'Vol':<3} {'Best Pos':<8} {'Best Overall':<11} {'2nd Pos':<7} {'2nd Overall':<11} {'3rd Pos':<7} {'3rd Overall':<11}")
    print("-" * 140)
    
    for i, projection in enumerate(projections[:50], 1):  # Show more since we're filtering
        top_pos = projection['top_positions']
        
        pos2 = top_pos[1]['position'] if len(top_pos) > 1 else '-'
        overall2 = top_pos[1]['overall'] if len(top_pos) > 1 else 0
        pos3 = top_pos[2]['position'] if len(top_pos) > 2 else '-'
        overall3 = top_pos[2]['overall'] if len(top_pos) > 2 else 0
        
        print(f"{i:<3} {projection['name'][:24]:<25} {projection['original_position']:<4} "
              f"{projection['volatility']:<3.0f} {projection['best_position']:<8} {projection['best_overall']:<11.1f} "
              f"{pos2:<7} {overall2:<11.1f} {pos3:<7} {overall3:<11.1f}")
    
    # Position flexibility analysis
    print(f"\n🔄 POSITION FLEXIBILITY ANALYSIS")
    print("-" * 80)
    
    flexible_players = [p for p in projections if len([pos for pos in p['top_positions'] if pos['overall'] >= 85]) >= 2]
    
    print(f"Players with 85+ overall at multiple positions: {len(flexible_players)}")
    print()
    
    for player in flexible_players[:10]:
        good_positions = [pos for pos in player['top_positions'] if pos['overall'] >= 85]
        pos_str = ", ".join([f"{pos['position']}({pos['overall']:.1f})" for pos in good_positions])
        print(f"  {player['name'][:20]:<20} Vol: {player['volatility']:2.0f} - {pos_str}")
    
    # Position group analysis
    print(f"\n🎯 DRAFT-PRIORITIZED POSITION BREAKDOWN")
    print("-" * 80)
    
    position_groups = {
        "Skill Positions (Early Draft)": ['QB', 'WR', 'RB', 'TE'],
        "Key Defensive (Premium)": ['CB', 'FS', 'SS'],
        "Linebackers (Value)": ['MLB', 'WLB', 'SLB'],
        "Offensive Line": ['LT', 'RT', 'C', 'LG', 'RG'],
        "Late Round/Specialists": ['LDE', 'RDE', 'DT', 'K', 'P', 'FB']
    }
    
    for group_name, positions in position_groups.items():
        group_players = [p for p in projections if p['best_position'] in positions]
        if group_players:
            print(f"\n{group_name} ({len(group_players)} players):")
            for i, player in enumerate(group_players[:3], 1):  # Top 3 per group
                print(f"  {i}. {player['name'][:18]:<18} {player['best_position']:<3} {player['best_overall']:5.1f} overall")
    
    # Save to CSV
    output_file = Path(csv_file_path).parent / "draft_prioritized_analysis.csv"
    with open(output_file, 'w', newline='') as file:
        fieldnames = ['rank', 'name', 'original_position', 'volatility', 'best_position', 'best_overall', 'max_speed_at_best_pos',
                     'pos2', 'pos2_overall', 'pos3', 'pos3_overall', 'pos4', 'pos4_overall', 'pos5', 'pos5_overall']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, projection in enumerate(projections, 1):
            top_pos = projection['top_positions']
            row = {
                'rank': i,
                'name': projection['name'],
                'original_position': projection['original_position'],
                'volatility': projection['volatility'],
                'best_position': projection['best_position'],
                'best_overall': projection['best_overall'],
                'max_speed_at_best_pos': projection['projected_max_speed_at_best_pos'],
                'pos2': top_pos[1]['position'] if len(top_pos) > 1 else '',
                'pos2_overall': top_pos[1]['overall'] if len(top_pos) > 1 else 0,
                'pos3': top_pos[2]['position'] if len(top_pos) > 2 else '',
                'pos3_overall': top_pos[2]['overall'] if len(top_pos) > 2 else 0,
                'pos4': top_pos[3]['position'] if len(top_pos) > 3 else '',
                'pos4_overall': top_pos[3]['overall'] if len(top_pos) > 3 else 0,
                'pos5': top_pos[4]['position'] if len(top_pos) > 4 else '',
                'pos5_overall': top_pos[4]['overall'] if len(top_pos) > 4 else 0,
            }
            writer.writerow(row)
    
    print(f"\n💾 Draft-prioritized analysis saved to: {output_file}")
    
    # Create Google Sheet if ID provided
    if sheet_id:
        print(f"\n📊 Creating Google Sheet tab...")
        sheet_url = analyzer.create_sheets_output(projections, sheet_id)
        if sheet_url:
            print(f"✅ Google Sheet created successfully!")
    
    return projections

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='MFN Multi-Position Boom Analyzer')
    parser.add_argument('--refresh', action='store_true', help='Refresh data from Google Sheets before analysis')
    parser.add_argument('--csv', default='live_rookies.csv', help='CSV file path (default: live_rookies.csv)')
    parser.add_argument('--sheet-id', default='1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A', help='Google Sheets ID')
    
    # Support legacy command line args for backwards compatibility
    if len(sys.argv) >= 2 and not sys.argv[1].startswith('--'):
        csv_file = sys.argv[1]
        sheet_id = sys.argv[2] if len(sys.argv) > 2 else "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"
        analyze_rookies_multi_position(csv_file, sheet_id)
    else:
        args = parser.parse_args()
        analyze_rookies_multi_position(args.csv, args.sheet_id, args.refresh)