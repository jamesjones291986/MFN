#!/usr/bin/env python3
"""
Automated MFN Game Planning Script

One-command solution for complete game planning workflow:
1. Download latest season data
2. Scout opponent's play tendencies by personnel sets
3. Find best counter plays against their tendencies
4. Generate targeting analysis for selected plays
5. Output formatted game plan

Usage: python3 automated_gameplan_fixed.py --team BOS --league USFL [--season 2011]
"""

import argparse
import sys
import os
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Import MFN modules directly without path manipulation
from util import Config
from GameLogDownloader import GameLogDownloader
from SeasonCompiler import SeasonCompiler
from main import format_df, adj_ev
from auto_downloader import auto_download_season
from quick_update import update_season_only


class AutomatedGamePlan:
    def __init__(self, league: str, season: int, opponent: str):
        self.league = league
        self.season = season
        self.opponent = opponent
        self.season_data = None
        self.opponent_tendencies = {}
        self.counter_plays = {}
        self.targeting_analysis = {}
        
    def run_full_workflow(self) -> Dict:
        """Execute the complete automated game planning workflow"""
        print(f"🏈 Starting automated game plan for {self.opponent} in {self.league} {self.season}")
        print("=" * 60)
        
        # Step 1: Ensure latest data is available
        print("📥 Step 1: Updating season data...")
        self._update_season_data()
        
        # Step 2: Load and prepare data
        print("📊 Step 2: Loading season data...")
        self._load_season_data()
        
        # Step 3: Scout opponent tendencies by personnel sets
        print("🔍 Step 3: Scouting opponent tendencies...")
        self._scout_opponent_by_personnel()
        
        # Step 4: Find counter plays against their tendencies
        print("⚔️  Step 4: Finding counter plays...")
        self._find_counter_plays()
        
        # Step 5: Generate targeting analysis
        print("🎯 Step 5: Analyzing targeting patterns...")
        self._analyze_targeting_patterns()
        
        # Step 6: Generate formatted output
        print("📋 Step 6: Generating game plan...")
        game_plan = self._generate_game_plan()
        
        # Step 7: Save and display results
        self._save_and_display_results(game_plan)
        
        return game_plan
    
    def _update_season_data(self):
        """Download latest data and compile season if needed"""
        try:
            # Try auto-download first (for current/ongoing seasons)
            print(f"   Checking for new games in {self.league} {self.season}...")
            games_found = auto_download_season(self.league, self.season, force=False)
            
            if games_found:
                print(f"   ✅ Found {len(games_found)} games, compiling season...")
                # Compile the season data
                schedule_path = f"{Config.root}/{self.league}/{self.league}_{self.season}.csv"
                if os.path.exists(schedule_path):
                    SeasonCompiler.compile(self.league, self.season, override_path=schedule_path)
                    print("   ✅ Season data updated successfully")
                else:
                    print(f"   ⚠️  Schedule file not found: {schedule_path}")
            else:
                print("   ℹ️  No new games found, using existing data")
                
        except Exception as e:
            print(f"   ⚠️  Auto-download failed: {e}")
            print("   ℹ️  Using existing season data")
    
    def _load_season_data(self):
        """Load the season data for analysis"""
        try:
            feather_path = f"{Config.seasons}/{self.league}_{self.season}.feather"
            if os.path.exists(feather_path):
                raw_data = pd.read_feather(feather_path)
                print(f"   ✅ Loaded {len(raw_data)} plays from {feather_path}")
                # Process through format_df to get derived columns
                print(f"   🔄 Processing data through format_df...")
                self.season_data = format_df(raw_data)
                print(f"   ✅ Processed data: {len(self.season_data)} plays with derived columns")
            else:
                # Try to load and format from CSV if feather doesn't exist
                print(f"   ⚠️  Feather file not found, attempting to load from CSV...")
                csv_path = f"{Config.root}/{self.league}/{self.league}_{self.season}.csv"
                if os.path.exists(csv_path):
                    raw_data = pd.read_csv(csv_path)
                    self.season_data = format_df(raw_data)
                    print(f"   ✅ Loaded and formatted {len(self.season_data)} plays from CSV")
                else:
                    raise FileNotFoundError(f"No data file found for {self.league} {self.season}")
                    
        except Exception as e:
            print(f"   ❌ Error loading season data: {e}")
            sys.exit(1)
    
    def _scout_opponent_by_personnel(self):
        """Analyze opponent's play tendencies organized by personnel sets"""
        if self.season_data is None:
            print("   ❌ No season data available for scouting")
            return
        
        # Filter data for the opponent team
        opponent_data = self.season_data[
            (self.season_data['HasBall'] == self.opponent) |
            (self.season_data['DefTeam'] == self.opponent)
        ].copy()
        
        if opponent_data.empty:
            print(f"   ❌ No data found for team {self.opponent}")
            return
        
        print(f"   📊 Analyzing {len(opponent_data)} plays by {self.opponent}")
        
        # Scout offensive tendencies by personnel
        offense_data = opponent_data[opponent_data['HasBall'] == self.opponent]
        offensive_tendencies = self._analyze_play_tendencies(
            offense_data, 'OffPersonnel', 'OffensivePlay', 'offense'
        )
        
        # Scout defensive tendencies (by offensive personnel they face)
        defense_data = opponent_data[opponent_data['DefTeam'] == self.opponent]
        defensive_tendencies = self._analyze_play_tendencies(
            defense_data, 'OffPersonnel', 'DefensivePlay', 'defense'
        )
        
        self.opponent_tendencies = {
            'offense': offensive_tendencies,
            'defense': defensive_tendencies
        }
        
        print(f"   ✅ Found tendencies for {len(offensive_tendencies)} offensive personnel sets")
        print(f"   ✅ Found tendencies for {len(defensive_tendencies)} defensive personnel sets")
    
    def _analyze_play_tendencies(self, data: pd.DataFrame, personnel_col: str, 
                                play_col: str, side: str) -> Dict:
        """Analyze play frequency by personnel set"""
        tendencies = {}
        
        # Group by personnel set and analyze play frequency
        personnel_groups = data.groupby(personnel_col)
        
        for personnel, group in personnel_groups:
            if len(group) < 5:  # Skip personnel sets with too few plays
                continue
                
            play_counts = group[play_col].value_counts()
            total_plays = len(group)
            
            # Calculate play frequency percentages
            play_frequencies = {}
            for play, count in play_counts.items():
                if pd.notna(play) and count >= 2:  # Skip null plays and very rare ones
                    frequency = (count / total_plays) * 100
                    play_frequencies[play] = {
                        'count': count,
                        'frequency': round(frequency, 1),
                        'total_plays': total_plays
                    }
            
            if play_frequencies:
                tendencies[personnel] = {
                    'total_plays': total_plays,
                    'plays': play_frequencies
                }
        
        return tendencies
    
    def _find_counter_plays(self):
        """Find best counter plays against opponent tendencies using historical data"""
        print("   🔍 Analyzing historical matchup data...")
        
        # Load all available historical data for counter-play analysis
        historical_data = self._load_historical_data()
        
        if historical_data.empty:
            print("   ⚠️  No historical data available for counter-play analysis")
            return
        
        self.counter_plays = {
            'vs_offense': self._find_defensive_counters(historical_data),
            'vs_defense': self._find_offensive_counters(historical_data)
        }
        
        print("   ✅ Counter-play analysis complete")
    
    def _load_historical_data(self) -> pd.DataFrame:
        """Load all available historical data for analysis"""
        all_data = []
        
        # Load data from recent seasons only (for performance)
        print("   📦 Loading historical data from recent seasons...")
        recent_seasons = ['USFL_2010', 'USFL_2009', 'qad_2049', 'qad_2048']  # Limit for testing
        
        for season_file in recent_seasons:
            # Skip current season to avoid circular reference
            if season_file == f"{self.league}_{self.season}":
                continue
                
            feather_path = f"{Config.seasons}/{season_file}.feather"
            if os.path.exists(feather_path):
                try:
                    raw_df = pd.read_feather(feather_path)
                    # Process through format_df to get personnel columns
                    processed_df = format_df(raw_df)
                    league_name, season_year = season_file.split('_')
                    processed_df['source_league'] = league_name
                    processed_df['source_season'] = int(season_year)
                    all_data.append(processed_df)
                    print(f"   ✅ Processed {season_file}: {len(processed_df)} plays")
                except Exception as e:
                    print(f"   ⚠️  Could not load {feather_path}: {e}")
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            print(f"   📊 Combined historical data: {len(combined_data)} plays for analysis")
            return combined_data
        else:
            return pd.DataFrame()
    
    def _find_defensive_counters(self, historical_data: pd.DataFrame) -> Dict:
        """Find best defensive plays against opponent's offensive tendencies"""
        defensive_counters = {}
        
        for personnel, tendency_data in self.opponent_tendencies['offense'].items():
            print(f"   📊 Finding counters for {personnel} personnel...")
            personnel_counters = {}
            
            for off_play, play_data in tendency_data['plays'].items():
                # Find historical matchups where this offensive play was used
                matchup_data = historical_data[
                    (historical_data['OffensivePlay'] == off_play) &
                    (historical_data['OffPersonnel'] == personnel)
                ].copy()
                
                if len(matchup_data) >= 10:  # Need sufficient sample size
                    # Analyze defensive success against this play
                    def_success = self._analyze_defensive_success(matchup_data)
                    personnel_counters[off_play] = {
                        'opponent_frequency': play_data['frequency'],
                        'sample_size': len(matchup_data),
                        'best_counters': def_success
                    }
            
            if personnel_counters:
                defensive_counters[personnel] = personnel_counters
        
        return defensive_counters
    
    def _find_offensive_counters(self, historical_data: pd.DataFrame) -> Dict:
        """Find best offensive plays against opponent's defensive tendencies"""
        offensive_counters = {}
        
        for personnel, tendency_data in self.opponent_tendencies['defense'].items():
            print(f"   🎯 Finding counters for {personnel} defense...")
            personnel_counters = {}
            
            for def_play, play_data in tendency_data['plays'].items():
                # Find historical matchups against this defensive play
                matchup_data = historical_data[
                    (historical_data['DefensivePlay'] == def_play) &
                    (historical_data['OffPersonnel'] == personnel)
                ].copy()
                
                if len(matchup_data) >= 10:  # Need sufficient sample size
                    # Analyze offensive success against this defense
                    off_success = self._analyze_offensive_success(matchup_data)
                    personnel_counters[def_play] = {
                        'opponent_frequency': play_data['frequency'],
                        'sample_size': len(matchup_data),
                        'best_counters': off_success
                    }
            
            if personnel_counters:
                offensive_counters[personnel] = personnel_counters
        
        return offensive_counters
    
    def _analyze_defensive_success(self, matchup_data: pd.DataFrame) -> List[Dict]:
        """Analyze which defensive plays were most successful"""
        # Group by defensive play and calculate success metrics
        def_analysis = matchup_data.groupby('DefensivePlay').agg({
            'YardsGained': ['mean', 'count'],
            'ev': 'mean'  # Expected value
        }).round(2)
        
        def_analysis.columns = ['avg_yards_allowed', 'play_count', 'avg_ev']
        def_analysis = def_analysis[def_analysis['play_count'] >= 3]  # Minimum sample
        
        # Sort by lowest yards allowed (best defense)
        def_analysis = def_analysis.sort_values('avg_yards_allowed')
        
        # Return top 5 defensive counters
        best_counters = []
        for def_play, stats in def_analysis.head(5).iterrows():
            best_counters.append({
                'defensive_play': def_play,
                'avg_yards_allowed': stats['avg_yards_allowed'],
                'sample_size': int(stats['play_count']),
                'expected_value': stats['avg_ev']
            })
        
        return best_counters
    
    def _analyze_offensive_success(self, matchup_data: pd.DataFrame) -> List[Dict]:
        """Analyze which offensive plays were most successful"""
        # Group by offensive play and calculate success metrics  
        off_analysis = matchup_data.groupby('OffensivePlay').agg({
            'YardsGained': ['mean', 'count'],
            'ev': 'mean'  # Expected value
        }).round(2)
        
        off_analysis.columns = ['avg_yards_gained', 'play_count', 'avg_ev']
        off_analysis = off_analysis[off_analysis['play_count'] >= 3]  # Minimum sample
        
        # Sort by highest yards gained (best offense)
        off_analysis = off_analysis.sort_values('avg_yards_gained', ascending=False)
        
        # Return top 5 offensive counters
        best_counters = []
        for off_play, stats in off_analysis.head(5).iterrows():
            best_counters.append({
                'offensive_play': off_play,
                'avg_yards_gained': stats['avg_yards_gained'],
                'sample_size': int(stats['play_count']),
                'expected_value': stats['avg_ev']
            })
        
        return best_counters
    
    def _analyze_targeting_patterns(self):
        """Analyze which positions are targeted most by our selected plays"""
        print("   🎯 Analyzing targeting patterns for recommended plays...")
        
        # Get all recommended offensive plays
        recommended_plays = []
        for personnel_data in self.counter_plays['vs_defense'].values():
            for def_play_data in personnel_data.values():
                for counter in def_play_data['best_counters']:
                    recommended_plays.append(counter['offensive_play'])
        
        # Get top 18 unique plays (remove duplicates, keep most frequent)
        play_frequency = pd.Series(recommended_plays).value_counts()
        top_18_plays = play_frequency.head(18).index.tolist()
        
        print(f"   📊 Analyzing targeting for top {len(top_18_plays)} recommended plays")
        
        # Load historical data to analyze targeting patterns
        historical_data = self._load_historical_data()
        
        if historical_data.empty:
            print("   ⚠️  No historical data for targeting analysis")
            return
        
        # Analyze targeting by personnel set for our recommended plays
        targeting_by_personnel = {}
        
        for personnel in ['5WR', '1RB/4WR', '1TE/4WR', '1RB/1TE/3WR', '1RB/2TE/2WR']:
            personnel_data = historical_data[
                (historical_data['OffensivePlay'].isin(top_18_plays)) &
                (historical_data['OffPersonnel'] == personnel)
            ]
            
            if len(personnel_data) > 0:
                targeting_analysis = self._calculate_position_targeting(personnel_data)
                targeting_by_personnel[personnel] = targeting_analysis
        
        self.targeting_analysis = {
            'recommended_plays': top_18_plays,
            'targeting_by_personnel': targeting_by_personnel
        }
        
        print("   ✅ Targeting analysis complete")
    
    def _calculate_position_targeting(self, play_data: pd.DataFrame) -> Dict:
        """Calculate which positions are targeted most frequently"""
        # This is a simplified version - you'll need to enhance based on your data structure
        # Look for patterns in receiver targeting, rushing attempts, etc.
        
        targeting_stats = {}
        
        # Analyze pass targeting if data is available
        pass_plays = play_data[play_data['OffPlayType'].isin(['Short Pass', 'Medium Pass', 'Long Pass'])]
        if len(pass_plays) > 0:
            # You'll need to implement position parsing based on your data structure
            # This is a placeholder that you can customize
            targeting_stats['pass_targets'] = {
                'total_passes': len(pass_plays),
                'avg_yards_per_attempt': pass_plays['YardsGained'].mean(),
                'completion_rate': len(pass_plays[pass_plays['YardsGained'] > 0]) / len(pass_plays) * 100
            }
        
        # Analyze rushing if data is available
        rush_plays = play_data[play_data['OffPlayType'].isin(['Inside Run', 'Outside Run'])]
        if len(rush_plays) > 0:
            targeting_stats['rush_attempts'] = {
                'total_rushes': len(rush_plays),
                'avg_yards_per_carry': rush_plays['YardsGained'].mean()
            }
        
        return targeting_stats
    
    def _generate_game_plan(self) -> Dict:
        """Generate the final formatted game plan"""
        game_plan = {
            'opponent': self.opponent,
            'league': self.league,
            'season': self.season,
            'generated_at': pd.Timestamp.now().isoformat(),
            'opponent_scouting': self.opponent_tendencies,
            'recommended_counters': self.counter_plays,
            'targeting_analysis': self.targeting_analysis,
            'summary': self._generate_summary()
        }
        
        return game_plan
    
    def _generate_summary(self) -> Dict:
        """Generate a summary of key recommendations"""
        summary = {
            'key_defensive_recommendations': [],
            'key_offensive_recommendations': [],
            'top_personnel_matchups': [],
            'targeting_priorities': []
        }
        
        # Extract key defensive recommendations
        for personnel, counters in self.counter_plays.get('vs_offense', {}).items():
            for off_play, counter_data in counters.items():
                if counter_data['best_counters']:
                    best_counter = counter_data['best_counters'][0]
                    summary['key_defensive_recommendations'].append({
                        'vs_personnel': personnel,
                        'vs_play': off_play,
                        'opponent_frequency': counter_data['opponent_frequency'],
                        'recommended_defense': best_counter['defensive_play'],
                        'expected_yards_allowed': best_counter['avg_yards_allowed']
                    })
        
        # Extract key offensive recommendations  
        for personnel, counters in self.counter_plays.get('vs_defense', {}).items():
            for def_play, counter_data in counters.items():
                if counter_data['best_counters']:
                    best_counter = counter_data['best_counters'][0]
                    summary['key_offensive_recommendations'].append({
                        'vs_personnel': personnel,
                        'vs_play': def_play,
                        'opponent_frequency': counter_data['opponent_frequency'],
                        'recommended_offense': best_counter['offensive_play'],
                        'expected_yards_gained': best_counter['avg_yards_gained']
                    })
        
        return summary
    
    def _save_and_display_results(self, game_plan: Dict):
        """Save results to file and display formatted output"""
        # Save detailed JSON
        output_file = f"automated_gameplan_{self.opponent}_{self.league}_{self.season}.json"
        with open(output_file, 'w') as f:
            json.dump(game_plan, f, indent=2)
        
        print(f"\n💾 Detailed game plan saved to: {output_file}")
        
        # Display formatted summary
        self._display_formatted_summary(game_plan)
    
    def _display_formatted_summary(self, game_plan: Dict):
        """Display a clean, formatted summary for game planning"""
        print("\n" + "="*80)
        print(f"🏈 AUTOMATED GAME PLAN: {self.opponent} ({self.league} {self.season})")
        print("="*80)
        
        # Opponent Scouting Summary
        print("\n📊 OPPONENT SCOUTING SUMMARY")
        print("-" * 40)
        
        offense_tendencies = game_plan['opponent_scouting'].get('offense', {})
        if offense_tendencies:
            print("🏃 OFFENSIVE TENDENCIES:")
            for personnel, data in list(offense_tendencies.items())[:3]:  # Top 3 personnel
                print(f"   {personnel} ({data['total_plays']} plays):")
                for play, play_data in list(data['plays'].items())[:3]:  # Top 3 plays
                    print(f"     • {play}: {play_data['frequency']}% ({play_data['count']} times)")
        
        defense_tendencies = game_plan['opponent_scouting'].get('defense', {})
        if defense_tendencies:
            print("\n🛡️  DEFENSIVE TENDENCIES:")
            for personnel, data in list(defense_tendencies.items())[:3]:  # Top 3 personnel
                print(f"   {personnel} ({data['total_plays']} plays):")
                for play, play_data in list(data['plays'].items())[:3]:  # Top 3 plays
                    print(f"     • {play}: {play_data['frequency']}% ({play_data['count']} times)")
        
        # Counter Recommendations
        print("\n⚔️  RECOMMENDED COUNTERS")
        print("-" * 40)
        
        summary = game_plan.get('summary', {})
        
        if summary.get('key_defensive_recommendations'):
            print("🛡️  DEFENSIVE GAME PLAN:")
            for rec in summary['key_defensive_recommendations'][:5]:  # Top 5
                print(f"   vs {rec['vs_personnel']} running {rec['vs_play']} ({rec['opponent_frequency']}%)")
                print(f"     → Use: {rec['recommended_defense']}")
                print(f"     → Expected: {rec['expected_yards_allowed']} yards allowed")
                print()
        
        if summary.get('key_offensive_recommendations'):
            print("🏃 OFFENSIVE GAME PLAN:")
            for rec in summary['key_offensive_recommendations'][:5]:  # Top 5
                print(f"   vs {rec['vs_personnel']} running {rec['vs_play']} ({rec['opponent_frequency']}%)")
                print(f"     → Use: {rec['recommended_offense']}")
                print(f"     → Expected: {rec['expected_yards_gained']} yards gained")
                print()
        
        # Targeting Analysis
        targeting = game_plan.get('targeting_analysis', {})
        if targeting.get('recommended_plays'):
            print("🎯 TOP 18 RECOMMENDED OFFENSIVE PLAYS")
            print("-" * 40)
            for i, play in enumerate(targeting['recommended_plays'], 1):
                print(f"{i:2}. {play}")
        
        if targeting.get('targeting_by_personnel'):
            print("\n📍 TARGETING ANALYSIS BY PERSONNEL")
            print("-" * 40)
            for personnel, data in targeting['targeting_by_personnel'].items():
                print(f"{personnel}:")
                if 'pass_targets' in data:
                    pass_data = data['pass_targets']
                    print(f"   Passes: {pass_data['total_passes']} attempts, "
                          f"{pass_data['avg_yards_per_attempt']:.1f} Y/A, "
                          f"{pass_data['completion_rate']:.1f}% completion")
                if 'rush_attempts' in data:
                    rush_data = data['rush_attempts']
                    print(f"   Rushes: {rush_data['total_rushes']} attempts, "
                          f"{rush_data['avg_yards_per_carry']:.1f} Y/C")
                print()
        
        print("="*80)
        print("✅ Game plan generation complete! Ready to dominate! 🏆")


def main():
    parser = argparse.ArgumentParser(description='Automated MFN Game Planning')
    parser.add_argument('--team', required=True, help='Opponent team abbreviation (e.g., BOS)')
    parser.add_argument('--league', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--season', type=int, help='Season year (defaults to latest available)')
    parser.add_argument('--output-format', choices=['json', 'csv', 'both'], 
                       default='json', help='Output format for results')
    
    args = parser.parse_args()
    
    # Determine season if not provided
    if not args.season:
        available_seasons = Config.ls_dictionary.get(args.league)
        if available_seasons:
            args.season = max(available_seasons)
            print(f"Using latest available season: {args.season}")
        else:
            print(f"Error: League '{args.league}' not found in configuration")
            print(f"Available leagues: {list(Config.ls_dictionary.keys())}")
            sys.exit(1)
    
    # Create and run the automated game plan
    try:
        game_planner = AutomatedGamePlan(args.league, args.season, args.team)
        game_plan = game_planner.run_full_workflow()
        
        print(f"\n🎉 Automated game planning complete for {args.team}!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Game planning interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during game planning: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()