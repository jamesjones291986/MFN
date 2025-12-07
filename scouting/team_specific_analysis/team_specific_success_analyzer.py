#!/usr/bin/env python3
"""
Team-Specific Success Analyzer
=============================

Directly analyzes what offensive and defensive plays have been most successful 
against a specific opponent. Simple, actionable scouting.

Usage:
    python team_specific_success_analyzer.py --opponent MIC --league USFL --season 2018
    python team_specific_success_analyzer.py --opponent MIC --league USFL --season 2018 --min-attempts 3
"""

import pandas as pd
import numpy as np
import argparse
import sys
from util import Config

class TeamSuccessAnalyzer:
    """Analyzes what plays work best against a specific team."""
    
    def __init__(self, league: str, season: int, opponent: str, min_attempts: int = 3):
        self.league = league
        self.season = season
        self.opponent = opponent
        self.min_attempts = min_attempts
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load season data."""
        try:
            self.df = Config.load_feather(self.league, self.season)
            if self.df is None or self.df.empty:
                raise ValueError(f"No data found for {self.league} {self.season}")
            print(f"✅ Loaded {len(self.df)} plays from {self.league} {self.season}")
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")
    
    def analyze_offensive_success_vs_opponent(self):
        """Find the most successful offensive plays against the opponent."""
        
        print(f"\n🎯 OFFENSIVE PLAYS vs {self.opponent}")
        print("=" * 45)
        
        # Find games where opponent was on defense (opponent not HasBall)
        opponent_games = self.df.groupby('Game ID')['HasBall'].unique()
        games_with_opponent = [game_id for game_id, teams in opponent_games.items() 
                              if self.opponent in teams]
        
        # Filter for plays against opponent's defense
        vs_opponent_defense = self.df[
            (self.df['Game ID'].isin(games_with_opponent)) &
            (self.df['HasBall'] != self.opponent) &
            (self.df['HasBall'].notna()) &  # Exclude special teams
            (self.df['OffensivePlay'].notna()) &
            (~self.df['OffensivePlay'].isin(['Field Goal', 'Punt', 'Victory', 'Kickoff']))
        ].copy()
        
        if vs_opponent_defense.empty:
            print(f"❌ No offensive plays found against {self.opponent}")
            return {}
        
        print(f"📊 Analyzing {len(vs_opponent_defense)} plays against {self.opponent} defense")
        
        # Calculate success metrics by offensive play
        off_success = vs_opponent_defense.groupby('OffensivePlay').agg({
            'YardsGained': ['count', 'mean', 'sum', 'std'],
            'OffPlayType': lambda x: x.iloc[0],  # Get play type
            'OffPersonnel': lambda x: x.mode().iloc[0] if not x.empty else 'Unknown'  # Most common personnel
        }).round(2)
        
        # Flatten column names
        off_success.columns = ['Attempts', 'Avg_Yards', 'Total_Yards', 'Std_Dev', 'Play_Type', 'Personnel']
        
        # Filter by minimum attempts
        off_success = off_success[off_success['Attempts'] >= self.min_attempts]
        
        if off_success.empty:
            print(f"❌ No plays with {self.min_attempts}+ attempts found")
            return {}
        
        # Separate by play type
        run_plays = off_success[off_success['Play_Type'].isin(['Inside Run', 'Outside Run'])]
        pass_plays = off_success[off_success['Play_Type'].isin(['Short Pass', 'Medium Pass', 'Long Pass'])]
        
        # Show results
        print(f"\n🏃‍♂️ BEST RUNNING PLAYS vs {self.opponent}")
        print(f"   (Min {self.min_attempts} attempts, sorted by avg yards)")
        if not run_plays.empty:
            run_sorted = run_plays.sort_values('Avg_Yards', ascending=False)
            for play, stats in run_sorted.head(10).iterrows():
                success_rate = self._calculate_success_rate(vs_opponent_defense, play, 4.0)  # 4+ yards = success
                print(f"   {play}")
                print(f"     {stats['Avg_Yards']:.1f} yds/carry, {stats['Attempts']} attempts, {success_rate:.1f}% success rate")
                print(f"     Personnel: {stats['Personnel']}")
        else:
            print("   No running plays with sufficient attempts")
        
        print(f"\n🎯 BEST PASSING PLAYS vs {self.opponent}")
        print(f"   (Min {self.min_attempts} attempts, sorted by avg yards)")
        if not pass_plays.empty:
            pass_sorted = pass_plays.sort_values('Avg_Yards', ascending=False)
            for play, stats in pass_sorted.head(10).iterrows():
                success_rate = self._calculate_success_rate(vs_opponent_defense, play, 6.0)  # 6+ yards = success
                completion_rate = self._calculate_completion_rate(vs_opponent_defense, play)
                print(f"   {play}")
                print(f"     {stats['Avg_Yards']:.1f} yds/att, {stats['Attempts']} attempts, {success_rate:.1f}% success, {completion_rate:.1f}% comp")
                print(f"     Personnel: {stats['Personnel']}")
        else:
            print("   No passing plays with sufficient attempts")
        
        # Overall recommendations
        print(f"\n💡 KEY RECOMMENDATIONS vs {self.opponent}")
        print("=" * 40)
        
        best_run = run_sorted.iloc[0] if not run_sorted.empty else None
        best_pass = pass_sorted.iloc[0] if not pass_sorted.empty else None
        
        if best_run is not None:
            print(f"   🏃‍♂️ Best Run: {run_sorted.index[0]} ({best_run['Avg_Yards']:.1f} ypc)")
        
        if best_pass is not None:
            print(f"   🎯 Best Pass: {pass_sorted.index[0]} ({best_pass['Avg_Yards']:.1f} ypa)")
        
        # Compare run vs pass effectiveness
        if not run_sorted.empty and not pass_sorted.empty:
            avg_run_success = run_sorted['Avg_Yards'].mean()
            avg_pass_success = pass_sorted['Avg_Yards'].mean()
            
            if avg_pass_success > avg_run_success + 1.0:
                print(f"   📈 PASS-HEAVY APPROACH: Passing significantly more effective ({avg_pass_success:.1f} vs {avg_run_success:.1f})")
            elif avg_run_success > avg_pass_success + 1.0:
                print(f"   📈 RUN-HEAVY APPROACH: Running significantly more effective ({avg_run_success:.1f} vs {avg_pass_success:.1f})")
            else:
                print(f"   📈 BALANCED APPROACH: Run and pass similarly effective")
        
        return {
            'run_plays': run_sorted.to_dict('index'),
            'pass_plays': pass_sorted.to_dict('index')
        }
    
    def analyze_defensive_success_vs_opponent(self):
        """Find the most successful defensive plays against the opponent's offense."""
        
        print(f"\n🛡️ DEFENSIVE PLAYS vs {self.opponent} OFFENSE")
        print("=" * 50)
        
        # Find games where opponent was on offense (opponent HasBall)
        opponent_games = self.df.groupby('Game ID')['HasBall'].unique()
        games_with_opponent = [game_id for game_id, teams in opponent_games.items() 
                              if self.opponent in teams]
        
        # Filter for plays against opponent's offense
        vs_opponent_offense = self.df[
            (self.df['Game ID'].isin(games_with_opponent)) &
            (self.df['HasBall'] == self.opponent) &
            (self.df['DefensivePlay'].notna()) &
            (~self.df['DefensivePlay'].isin(['Punt Return', 'Kick Return', 'FG Block']))
        ].copy()
        
        if vs_opponent_offense.empty:
            print(f"❌ No defensive plays found against {self.opponent} offense")
            return {}
        
        print(f"📊 Analyzing {len(vs_opponent_offense)} plays against {self.opponent} offense")
        
        # Calculate defensive success metrics
        def_success = vs_opponent_offense.groupby('DefensivePlay').agg({
            'YardsGained': ['count', 'mean', 'sum', 'std'],
            'OffPlayType': lambda x: x.mode().iloc[0] if not x.empty else 'Mixed'  # Most common off play type faced
        }).round(2)
        
        # Flatten column names
        def_success.columns = ['Attempts', 'Avg_Yards_Allowed', 'Total_Yards_Allowed', 'Std_Dev', 'Primary_OffType']
        
        # Filter by minimum attempts
        def_success = def_success[def_success['Attempts'] >= self.min_attempts]
        
        if def_success.empty:
            print(f"❌ No defensive plays with {self.min_attempts}+ attempts found")
            return {}
        
        # Sort by yards allowed (ascending = better defense)
        def_sorted = def_success.sort_values('Avg_Yards_Allowed', ascending=True)
        
        print(f"\n🛡️ BEST DEFENSIVE PLAYS vs {self.opponent}")
        print(f"   (Min {self.min_attempts} attempts, sorted by fewest yards allowed)")
        
        for defense, stats in def_sorted.head(10).iterrows():
            stop_rate = self._calculate_defensive_stop_rate(vs_opponent_offense, defense)
            disruption_rate = self._calculate_disruption_rate(vs_opponent_offense, defense)
            print(f"   {defense}")
            print(f"     {stats['Avg_Yards_Allowed']:.1f} yds allowed/play, {stats['Attempts']} attempts, {stop_rate:.1f}% stop rate, {disruption_rate:.1f}% disruption rate")
            print(f"     Primary vs: {stats['Primary_OffType']}")
        
        # Recommendations
        print(f"\n💡 DEFENSIVE RECOMMENDATIONS vs {self.opponent}")
        print("=" * 45)
        
        best_overall_def = def_sorted.index[0]
        best_overall_stats = def_sorted.iloc[0]
        
        print(f"   🛡️ Best Overall Defense: {best_overall_def}")
        print(f"     ({best_overall_stats['Avg_Yards_Allowed']:.1f} yards allowed per play)")
        
        # Find best vs run and pass separately
        run_defenses = vs_opponent_offense[vs_opponent_offense['OffPlayType'].isin(['Inside Run', 'Outside Run'])]
        pass_defenses = vs_opponent_offense[vs_opponent_offense['OffPlayType'].isin(['Short Pass', 'Medium Pass', 'Long Pass'])]
        
        if not run_defenses.empty:
            best_vs_run = run_defenses.groupby('DefensivePlay')['YardsGained'].mean().sort_values().head(3)
            print(f"   🏃‍♂️ Best vs Run: {', '.join([f'{play} ({yards:.1f})' for play, yards in best_vs_run.items()])}")
        
        if not pass_defenses.empty:
            best_vs_pass = pass_defenses.groupby('DefensivePlay')['YardsGained'].mean().sort_values().head(3)
            print(f"   🎯 Best vs Pass: {', '.join([f'{play} ({yards:.1f})' for play, yards in best_vs_pass.items()])}")
        
        return def_sorted.to_dict('index')
    
    def _calculate_success_rate(self, data, play_name, success_threshold):
        """Calculate success rate for an offensive play."""
        play_data = data[data['OffensivePlay'] == play_name]
        if len(play_data) == 0:
            return 0.0
        successful_plays = len(play_data[play_data['YardsGained'] >= success_threshold])
        return (successful_plays / len(play_data)) * 100
    
    def _calculate_completion_rate(self, data, play_name):
        """
        Calculate completion rate for a passing play.
        This is an estimate, as we can't definitively determine incomplete passes from the data.
        We are assuming a pass is incomplete if YardsGained is 0, which is an educated guess.
        A completed pass for 0 yards will be incorrectly marked as incomplete.
        """
        play_data = data[data['OffensivePlay'] == play_name]
        if len(play_data) == 0:
            return 0.0
        # Assume incomplete passes result in 0 yards.
        completed_passes = len(play_data[play_data['YardsGained'] != 0])
        return (completed_passes / len(play_data)) * 100
    
    def _calculate_defensive_stop_rate(self, data, defense_name):
        """
        Calculate stop rate for a defensive play, using different criteria for run and pass plays.
        - Run play stop: < 4 yards gained
        - Pass play stop: < 6 yards gained
        """
        defense_data = data[data['DefensivePlay'] == defense_name]
        if len(defense_data) == 0:
            return 0.0

        run_plays = defense_data[defense_data['OffPlayType'].isin(['Inside Run', 'Outside Run'])]
        pass_plays = defense_data[defense_data['OffPlayType'].isin(['Short Pass', 'Medium Pass', 'Long Pass'])]

        run_stops = len(run_plays[run_plays['YardsGained'] < 4])
        pass_stops = len(pass_plays[pass_plays['YardsGained'] < 6])

        total_stops = run_stops + pass_stops
        total_plays = len(run_plays) + len(pass_plays)

        if total_plays == 0:
            return 0.0
        
        return (total_stops / total_plays) * 100
    
    def _calculate_disruption_rate(self, data, defense_name):
        """Calculate disruption rate for a defensive play (yards gained < 0)."""
        defense_data = data[data['DefensivePlay'] == defense_name]
        if len(defense_data) == 0:
            return 0.0
        disruptions = len(defense_data[defense_data['YardsGained'] < 0])
        return (disruptions / len(defense_data)) * 100
    
    def generate_full_report(self):
        """Generate complete offensive and defensive analysis."""
        print(f"🏈 TEAM-SPECIFIC SUCCESS ANALYSIS")
        print(f"Target: {self.opponent} ({self.league} {self.season})")
        print(f"Minimum attempts: {self.min_attempts}")
        print("=" * 60)
        
        off_results = self.analyze_offensive_success_vs_opponent()
        def_results = self.analyze_defensive_success_vs_opponent()
        
        return {
            'offensive': off_results,
            'defensive': def_results
        }

def main():
    """Main function to run team-specific analysis."""
    parser = argparse.ArgumentParser(description='Analyze successful plays against a specific opponent')
    parser.add_argument('--opponent', required=True, help='Opponent team abbreviation (e.g., MIC)')
    parser.add_argument('--league', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--season', type=int, required=True, help='Season year (e.g., 2018)')
    parser.add_argument('--min-attempts', type=int, default=3, help='Minimum attempts required for analysis (default: 3)')
    
    args = parser.parse_args()
    
    try:
        analyzer = TeamSuccessAnalyzer(args.league, args.season, args.opponent, args.min_attempts)
        results = analyzer.generate_full_report()
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())