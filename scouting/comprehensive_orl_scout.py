#!/usr/bin/env python3
"""
Comprehensive ORL Defensive Scouting Script
===========================================

This script does proper defensive scouting:
1. Analyzes ORL's 2018 defensive play calling patterns by personnel set
2. Searches ALL feather files to find effectiveness of plays against those defenses
3. Generates comprehensive recommendations

Usage:
    python comprehensive_orl_scout.py
"""

import sys
import pandas as pd
from pathlib import Path
from collections import defaultdict

# Add path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from util import Config
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class ComprehensiveORLScout:
    """Comprehensive scouting of ORL defensive tendencies."""
    
    def __init__(self):
        self.target_team = 'ORL'
        self.scout_year = 2018
        self.scout_league = 'USFL'
        
        # Data storage
        self.orl_defensive_tendencies = {}
        self.all_plays_database = None
        self.effectiveness_results = {}
        
        print(f"🎯 Comprehensive ORL Defensive Scouting")
        print(f"   Target: {self.target_team}")
        print(f"   Scout Year: {self.scout_year}")
        print(f"   Database: ALL seasons/leagues")
        print("=" * 60)
    
    def analyze_orl_2018_defensive_patterns(self):
        """Step 1: Analyze what defensive plays ORL called in 2018 by offensive personnel."""
        
        print(f"\n🔍 STEP 1: Analyzing {self.target_team} {self.scout_year} Defensive Patterns")
        print("-" * 50)
        
        # Load ORL's 2018 season
        df_2018 = Config.load_feather(self.scout_league, self.scout_year)
        if df_2018 is None or df_2018.empty:
            raise ValueError(f"No data found for {self.scout_league} {self.scout_year}")
        
        print(f"✅ Loaded {len(df_2018):,} plays from {self.scout_league} {self.scout_year}")
        
        # Find games where ORL was on defense (opponent was on offense)
        orl_games = df_2018.groupby('Game ID')['HasBall'].unique()
        games_with_orl = [game_id for game_id, teams in orl_games.items() if self.target_team in teams]
        
        # Get plays where ORL was on defense
        orl_defense_plays = df_2018[
            (df_2018['Game ID'].isin(games_with_orl)) &
            (df_2018['HasBall'] != self.target_team) &  # ORL not on offense = ORL on defense
            (df_2018['HasBall'].notna()) &
            (df_2018['DefensivePlay'].notna()) &
            (df_2018['OffPersonnel'].notna()) &
            (~df_2018['DefensivePlay'].isin(['Punt Return', 'Kick Return', 'FG Block']))
        ].copy()
        
        print(f"📊 Found {len(orl_defense_plays):,} defensive plays by {self.target_team}")
        
        if orl_defense_plays.empty:
            raise ValueError(f"No defensive plays found for {self.target_team}")
        
        # Analyze defensive play calling by offensive personnel
        print(f"\n📋 {self.target_team} Defensive Play Calling by Offensive Personnel:")
        
        personnel_defense_patterns = {}
        
        for personnel in orl_defense_plays['OffPersonnel'].unique():
            if pd.isna(personnel):
                continue
                
            personnel_plays = orl_defense_plays[orl_defense_plays['OffPersonnel'] == personnel]
            
            # Count defensive play calls for this personnel
            def_play_counts = personnel_plays['DefensivePlay'].value_counts()
            total_plays = len(personnel_plays)
            
            if total_plays >= 5:  # Only include personnel with meaningful sample size
                personnel_defense_patterns[personnel] = {
                    'total_plays': total_plays,
                    'defensive_calls': {}
                }
                
                print(f"\n   {personnel} ({total_plays} plays):")
                
                for def_play, count in def_play_counts.head(10).items():
                    percentage = (count / total_plays) * 100
                    personnel_defense_patterns[personnel]['defensive_calls'][def_play] = {
                        'count': count,
                        'percentage': percentage
                    }
                    print(f"     {def_play}: {count} times ({percentage:.1f}%)")
        
        self.orl_defensive_tendencies = personnel_defense_patterns
        
        print(f"\n✅ Analyzed {len(personnel_defense_patterns)} personnel groupings")
        return personnel_defense_patterns
    
    def load_comprehensive_database(self):
        """Step 2: Load ALL feather files for comprehensive effectiveness analysis."""
        
        print(f"\n📚 STEP 2: Loading Comprehensive Database")
        print("-" * 40)
        
        all_dfs = []
        total_plays = 0
        leagues_processed = 0
        
        print(f"🔄 Loading from all leagues and seasons...")
        
        for league, seasons in Config.ls_dictionary.items():
            for season in seasons:
                try:
                    df = Config.load_feather(league, season)
                    if df is not None and not df.empty:
                        # Add league/season identifiers
                        df['Source_League'] = league
                        df['Source_Season'] = season
                        
                        # Filter for relevant plays
                        relevant_plays = df[
                            (df['OffensivePlay'].notna()) &
                            (df['DefensivePlay'].notna()) &
                            (df['OffPersonnel'].notna()) &
                            (~df['OffensivePlay'].isin(['Field Goal', 'Punt', 'Victory', 'Kickoff'])) &
                            (~df['DefensivePlay'].isin(['Punt Return', 'Kick Return', 'FG Block']))
                        ].copy()
                        
                        if not relevant_plays.empty:
                            all_dfs.append(relevant_plays)
                            play_count = len(relevant_plays)
                            total_plays += play_count
                            leagues_processed += 1
                            print(f"   ✅ {league} {season}: {play_count:,} plays")
                        
                except Exception as e:
                    print(f"   ⚠️ {league} {season}: Error loading - {e}")
                    continue
        
        if not all_dfs:
            raise ValueError("No valid data found across any league/season")
        
        print(f"\n🔄 Combining data from {leagues_processed} league-seasons...")
        self.all_plays_database = pd.concat(all_dfs, ignore_index=True)
        
        print(f"✅ Comprehensive Database Loaded:")
        print(f"   📊 Total Plays: {len(self.all_plays_database):,}")
        print(f"   🏈 League-Seasons: {leagues_processed}")
        print(f"   🎯 Unique Offensive Plays: {self.all_plays_database['OffensivePlay'].nunique():,}")
        print(f"   🛡️ Unique Defensive Plays: {self.all_plays_database['DefensivePlay'].nunique():,}")
        
        return self.all_plays_database
    
    def analyze_effectiveness_against_orl_defenses(self):
        """Step 3: For each ORL defensive tendency, find what offensive plays work best."""
        
        print(f"\n⚔️ STEP 3: Analyzing Offensive Effectiveness vs {self.target_team} Defenses")
        print("-" * 70)
        
        if self.all_plays_database is None:
            raise ValueError("Must load comprehensive database first")
        
        all_recommendations = {}
        
        for personnel, defense_data in self.orl_defensive_tendencies.items():
            print(f"\n📋 ANALYZING vs {personnel} Personnel:")
            print("=" * 50)
            
            personnel_recommendations = {}
            
            # Analyze top defensive calls for this personnel
            top_defenses = sorted(
                defense_data['defensive_calls'].items(), 
                key=lambda x: x[1]['percentage'], 
                reverse=True
            )[:5]  # Top 5 most frequent defenses
            
            for def_play, def_stats in top_defenses:
                print(f"\n🛡️ When {self.target_team} calls '{def_play}' vs {personnel}")
                print(f"   (Called {def_stats['percentage']:.1f}% of the time - {def_stats['count']} times)")
                
                # Find all instances of this defense across entire database
                defense_instances = self.all_plays_database[
                    (self.all_plays_database['DefensivePlay'] == def_play) &
                    (self.all_plays_database['OffPersonnel'] == personnel)
                ].copy()
                
                if defense_instances.empty:
                    print(f"   ❌ No instances found in database")
                    continue
                
                print(f"   📊 Found {len(defense_instances):,} instances across all data")
                
                # Calculate offensive play effectiveness
                off_effectiveness = {}
                
                for off_play in defense_instances['OffensivePlay'].unique():
                    play_data = defense_instances[defense_instances['OffensivePlay'] == off_play]
                    
                    if len(play_data) < 3:  # Minimum sample size
                        continue
                    
                    attempts = len(play_data)
                    avg_yards = play_data['YardsGained'].mean()
                    total_yards = play_data['YardsGained'].sum()
                    
                    # Calculate success metrics
                    touchdowns = 0
                    interceptions = 0
                    sacks = 0
                    sack_yards = 0
                    
                    if 'Text' in play_data.columns:
                        touchdowns = len(play_data[play_data['Text'].str.contains('TOUCHDOWN', na=False)])
                        interceptions = len(play_data[play_data['Text'].str.contains('INTERCEPTED', na=False)])
                        sacks = len(play_data[play_data['Text'].str.contains('sacked', na=False)])
                        sack_yards = abs(play_data[play_data['Text'].str.contains('sacked', na=False)]['YardsGained'].sum())
                    
                    # ANY/A calculation
                    any_a = (total_yards + 20*touchdowns - 60*interceptions - sack_yards) / attempts
                    
                    # Success rate (different thresholds for run vs pass)
                    play_type = play_data['OffPlayType'].iloc[0] if 'OffPlayType' in play_data.columns else 'Unknown'
                    success_threshold = 4.0 if play_type in ['Inside Run', 'Outside Run'] else 6.0
                    successful = len(play_data[play_data['YardsGained'] >= success_threshold])
                    success_rate = (successful / attempts) * 100
                    
                    off_effectiveness[off_play] = {
                        'attempts': attempts,
                        'avg_yards': round(avg_yards, 2),
                        'any_a': round(any_a, 2),
                        'success_rate': round(success_rate, 1),
                        'td_rate': round((touchdowns / attempts) * 100, 1),
                        'int_rate': round((interceptions / attempts) * 100, 1),
                        'play_type': play_type
                    }
                
                # Sort by ANY/A effectiveness
                if off_effectiveness:
                    sorted_plays = sorted(
                        off_effectiveness.items(),
                        key=lambda x: x[1]['any_a'],
                        reverse=True
                    )
                    
                    print(f"   🎯 TOP OFFENSIVE PLAYS (by ANY/A):")
                    print(f"   {'Rank':<4} {'Play':<40} {'Att':<4} {'YPP':<5} {'ANY/A':<6} {'SR%':<5}")
                    print("   " + "-" * 70)
                    
                    for rank, (play, stats) in enumerate(sorted_plays[:10], 1):
                        play_short = play[:37] + "..." if len(play) > 40 else play
                        print(f"   {rank:<4} {play_short:<40} {stats['attempts']:<4} {stats['avg_yards']:<5} {stats['any_a']:<6} {stats['success_rate']:<5}")
                    
                    personnel_recommendations[def_play] = {
                        'defense_frequency': def_stats['percentage'],
                        'defense_count': def_stats['count'],
                        'database_instances': len(defense_instances),
                        'top_plays': dict(sorted_plays[:10])
                    }
                else:
                    print(f"   ❌ No offensive plays with sufficient sample size")
            
            all_recommendations[personnel] = personnel_recommendations
        
        self.effectiveness_results = all_recommendations
        return all_recommendations
    
    def generate_comprehensive_report(self):
        """Step 4: Generate the final comprehensive scouting report."""
        
        print(f"\n📋 STEP 4: COMPREHENSIVE SCOUTING REPORT")
        print("=" * 60)
        print(f"🎯 TARGET: {self.target_team} ({self.scout_league} {self.scout_year})")
        print(f"📊 ANALYSIS: Based on {len(self.all_plays_database):,} plays from all leagues/seasons")
        print("=" * 60)
        
        for personnel, defenses in self.effectiveness_results.items():
            print(f"\n🏈 WHEN YOU USE {personnel} PERSONNEL:")
            print("=" * 50)
            
            for defense, data in defenses.items():
                print(f"\n🛡️ If {self.target_team} calls '{defense}'")
                print(f"   📊 They call this {data['defense_frequency']:.1f}% of the time ({data['defense_count']} times)")
                print(f"   📈 Analysis based on {data['database_instances']:,} database instances")
                print(f"   🎯 RECOMMENDED OFFENSIVE PLAYS:")
                
                for rank, (play, stats) in enumerate(data['top_plays'].items(), 1):
                    print(f"     {rank}. {play}")
                    print(f"        {stats['avg_yards']} YPP, {stats['any_a']} ANY/A, {stats['success_rate']}% success ({stats['attempts']} attempts)")
        
        print(f"\n✅ SCOUTING REPORT COMPLETE")
        return self.effectiveness_results
    
    def run_comprehensive_scout(self):
        """Run the complete comprehensive scouting analysis."""
        
        try:
            # Step 1: Analyze ORL's 2018 defensive patterns
            self.analyze_orl_2018_defensive_patterns()
            
            # Step 2: Load comprehensive database
            self.load_comprehensive_database()
            
            # Step 3: Analyze effectiveness
            self.analyze_effectiveness_against_orl_defenses()
            
            # Step 4: Generate report
            self.generate_comprehensive_report()
            
            print(f"\n🎉 COMPREHENSIVE ORL SCOUTING COMPLETE!")
            return True
            
        except Exception as e:
            print(f"❌ Error during comprehensive scouting: {e}")
            return False

def main():
    """Main function."""
    scout = ComprehensiveORLScout()
    success = scout.run_comprehensive_scout()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())