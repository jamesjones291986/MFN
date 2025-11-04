"""
Advanced Personnel-Specific Gameplan Generator
Creates comprehensive offensive and defensive gameplans based on personnel-specific tendencies
"""

import pandas as pd
from main import format_df, adj_ev
from util import Config
import json


class AdvancedGameplanGenerator:
    """Generates detailed personnel-specific gameplans"""
    
    def __init__(self):
        self.personnel_groups = {
            '11': '1RB/1TE/3WR',      # Most common
            '12': '1RB/2TE/2WR',      # Heavy TE
            '21': '2RB/1TE/2WR',      # I-Formation
            '22': '2RB/2TE/1WR',      # Power running
            '10': '1RB/4WR',          # 4-wide
            '01': '5WR',              # Empty backfield
            '13': '1RB/3TE/1WR',      # Heavy TE
            '23': '2RB/3TE',          # Goal line
            '31': '3RB/1TE/1WR',      # Power running
            '20': '2RB/3WR'           # Spread run
        }
    
    def analyze_opponent_defense_by_personnel(self, league, season, opponent):
        """Analyze what defenses opponent uses vs each offensive personnel group"""
        print(f"🔍 Analyzing {opponent}'s defensive responses by personnel...")
        
        # Load season data
        tdf = format_df(Config.load_feather(league, season))
        
        # Get opponent's defensive plays
        opponent_games = tdf.loc[tdf.away_ac.eq(opponent) | tdf.home_ac.eq(opponent)]
        opponent_defense = opponent_games.loc[opponent_games.DefTeam.eq(opponent)]
        
        # Exclude special teams
        def_excludes = [None, 'FG Block', 'Punt Return', 'Kick Return', 'Onsides Kick Return Onside Kick Return']
        opponent_defense = opponent_defense.loc[~opponent_defense.DefensivePlay.isin(def_excludes)]
        
        personnel_defense_map = {}
        
        for personnel_code, personnel_name in self.personnel_groups.items():
            # Filter for this personnel group
            vs_personnel = opponent_defense.loc[opponent_defense.OffPersonnel.eq(personnel_name)]
            
            if len(vs_personnel) < 5:  # Need minimum plays
                continue
            
            # Get their most common defenses vs this personnel
            def_counts = vs_personnel.groupby('DefensivePlay').size()
            total_plays = len(vs_personnel)
            def_percentages = (def_counts / total_plays * 100).round(1)
            
            # Keep defenses used at least 10% of time
            common_defenses = def_percentages[def_percentages >= 10.0].sort_values(ascending=False)
            
            if not common_defenses.empty:
                personnel_defense_map[personnel_name] = {
                    'total_plays': total_plays,
                    'top_defense': common_defenses.index[0],
                    'top_defense_pct': common_defenses.iloc[0],
                    'all_defenses': common_defenses.to_dict()
                }
                
                print(f"  {personnel_name}: vs {common_defenses.index[0]} ({common_defenses.iloc[0]:.1f}%)")
        
        return personnel_defense_map
    
    def analyze_opponent_offense_by_personnel(self, league, season, opponent):
        """Analyze what offensive plays opponent uses from each personnel group"""
        print(f"🔍 Analyzing {opponent}'s offensive plays by personnel...")
        
        # Load season data
        tdf = format_df(Config.load_feather(league, season))
        
        # Get opponent's offensive plays
        opponent_games = tdf.loc[tdf.away_ac.eq(opponent) | tdf.home_ac.eq(opponent)]
        opponent_offense = opponent_games.loc[opponent_games.HasBall.eq(opponent)]
        
        # Exclude special teams
        off_excludes = [None, 'Field Goal', 'Punt', 'Victory', 'Kickoff', 'Onsides Kick Onside Kick']
        opponent_offense = opponent_offense.loc[~opponent_offense.OffensivePlay.isin(off_excludes)]
        
        personnel_offense_map = {}
        
        for personnel_code, personnel_name in self.personnel_groups.items():
            # Filter for this personnel group
            from_personnel = opponent_offense.loc[opponent_offense.OffPersonnel.eq(personnel_name)]
            
            if len(from_personnel) < 5:  # Need minimum plays
                continue
            
            # Get their most common plays from this personnel
            play_counts = from_personnel.groupby('OffensivePlay').size()
            total_plays = len(from_personnel)
            play_percentages = (play_counts / total_plays * 100).round(1)
            
            # Keep plays used at least 10% of time
            common_plays = play_percentages[play_percentages >= 10.0].sort_values(ascending=False)
            
            if not common_plays.empty:
                personnel_offense_map[personnel_name] = {
                    'total_plays': total_plays,
                    'top_play': common_plays.index[0],
                    'top_play_pct': common_plays.iloc[0],
                    'all_plays': common_plays.to_dict()
                }
                
                print(f"  {personnel_name}: {common_plays.index[0]} ({common_plays.iloc[0]:.1f}%)")
        
        return personnel_offense_map
    
    def find_best_offensive_plays_vs_defense(self, defense_name, personnel_name, analysis_data):
        """Find best offensive plays from specific personnel vs specific defense"""
        # Filter for this matchup
        matchup_data = analysis_data.loc[
            (analysis_data.DefensivePlay.eq(defense_name)) &
            (analysis_data.OffPersonnel.eq(personnel_name))
        ]
        
        if len(matchup_data) < 15:  # Need minimum sample
            return []
        
        try:
            # Run expected value analysis
            unique_plays = matchup_data['OffensivePlay'].unique()
            best_plays = adj_ev(matchup_data, 'OffensivePlay', unique_plays, 'desc')
            
            # Filter for good sample size and performance
            good_plays = best_plays.loc[
                (best_plays.cnt >= 10) & 
                (best_plays.ypp >= 3.0)
            ].head(3)  # Top 3 plays for this matchup
            
            recommendations = []
            for _, play in good_plays.iterrows():
                recommendations.append({
                    'play': play['OffensivePlay'],
                    'ypp': play['ypp'],
                    'any_a': play['any/a'],
                    'sample_size': play['cnt'],
                    'play_type': play['OffPlayType'],
                    'personnel': personnel_name,
                    'vs_defense': defense_name
                })
            
            return recommendations
            
        except Exception as e:
            print(f"    Error analyzing {personnel_name} vs {defense_name}: {e}")
            return []
    
    def find_best_defensive_plays_vs_offense(self, offensive_play, personnel_name, analysis_data):
        """Find best defensive plays vs specific offensive play from personnel"""
        # Filter for this matchup
        matchup_data = analysis_data.loc[
            (analysis_data.OffensivePlay.eq(offensive_play)) &
            (analysis_data.OffPersonnel.eq(personnel_name))
        ]
        
        if len(matchup_data) < 15:  # Need minimum sample
            return []
        
        try:
            # For defense, we want to minimize opponent's yards per play
            def_counts = matchup_data.groupby('DefensivePlay').agg({
                'play_yards': ['mean', 'count'],
                'OffensivePlay': 'count'
            }).round(2)
            
            def_counts.columns = ['avg_yards_allowed', 'play_count', 'total_plays']
            def_counts = def_counts.loc[def_counts.play_count >= 10]  # Minimum sample
            
            # Sort by least yards allowed (best defense)
            best_defenses = def_counts.sort_values('avg_yards_allowed').head(3)
            
            recommendations = []
            for defense, data in best_defenses.iterrows():
                recommendations.append({
                    'defense': defense,
                    'avg_yards_allowed': data['avg_yards_allowed'],
                    'sample_size': data['play_count'],
                    'vs_play': offensive_play,
                    'vs_personnel': personnel_name
                })
            
            return recommendations
            
        except Exception as e:
            print(f"    Error analyzing defense vs {offensive_play} from {personnel_name}: {e}")
            return []
    
    def generate_comprehensive_gameplan(self, league, season, opponent):
        """Generate complete 18+ play offensive and defensive gameplan"""
        print(f"\n🏈 COMPREHENSIVE GAMEPLAN vs {opponent}")
        print("=" * 70)
        
        # Load analysis data
        analysis_data = format_df(Config.load_all_seasons())
        
        # Step 1: Analyze opponent's personnel-specific tendencies
        opponent_defense_by_personnel = self.analyze_opponent_defense_by_personnel(league, season, opponent)
        opponent_offense_by_personnel = self.analyze_opponent_offense_by_personnel(league, season, opponent)
        
        # Step 2: Generate offensive gameplan
        print(f"\n⚡ OFFENSIVE GAMEPLAN - 18+ PLAYS:")
        print("=" * 50)
        
        offensive_gameplan = []
        play_count = 0
        
        for personnel_name, defense_info in opponent_defense_by_personnel.items():
            top_defense = defense_info['top_defense']
            defense_pct = defense_info['top_defense_pct']
            
            print(f"\n👥 {personnel_name} vs {top_defense} ({defense_pct}%):")
            
            # Find best plays for this personnel vs their top defense
            best_plays = self.find_best_offensive_plays_vs_defense(
                top_defense, personnel_name, analysis_data
            )
            
            for i, play_rec in enumerate(best_plays, 1):
                play_count += 1
                print(f"  {play_count:2d}. {play_rec['play']}")
                print(f"      {play_rec['ypp']:.1f} ypp | {play_rec['any_a']:.1f} any/a | {play_rec['sample_size']} plays")
                
                offensive_gameplan.append(play_rec)
                
                if play_count >= 18:  # Stop at 18 plays
                    break
            
            if play_count >= 18:
                break
        
        # Step 3: Generate defensive gameplan
        print(f"\n🛡️  DEFENSIVE GAMEPLAN:")
        print("=" * 50)
        
        defensive_gameplan = []
        
        for personnel_name, offense_info in opponent_offense_by_personnel.items():
            top_play = offense_info['top_play']
            play_pct = offense_info['top_play_pct']
            
            print(f"\n👥 vs {personnel_name} running {top_play} ({play_pct}%):")
            
            # Find best defenses vs their top play from this personnel
            best_defenses = self.find_best_defensive_plays_vs_offense(
                top_play, personnel_name, analysis_data
            )
            
            for i, def_rec in enumerate(best_defenses, 1):
                print(f"  {i}. {def_rec['defense']}")
                print(f"     Allows {def_rec['avg_yards_allowed']:.1f} ypp | {def_rec['sample_size']} plays")
                
                defensive_gameplan.append(def_rec)
        
        # Step 4: Save comprehensive gameplan
        gameplan_data = {
            'opponent': opponent,
            'league': league,
            'season': season,
            'opponent_defense_by_personnel': opponent_defense_by_personnel,
            'opponent_offense_by_personnel': opponent_offense_by_personnel,
            'offensive_gameplan': offensive_gameplan,
            'defensive_gameplan': defensive_gameplan,
            'total_offensive_plays': len(offensive_gameplan),
            'total_defensive_schemes': len(defensive_gameplan)
        }
        
        output_file = f"{Config.root}/comprehensive_gameplan_vs_{opponent}_{league}_{season}.json"
        with open(output_file, 'w') as f:
            json.dump(gameplan_data, f, indent=2, default=str)
        
        print(f"\n💾 Comprehensive gameplan saved to: {output_file}")
        print(f"📊 Generated {len(offensive_gameplan)} offensive plays and {len(defensive_gameplan)} defensive schemes")
        
        return gameplan_data


# CLI integration
def create_comprehensive_gameplan(league, season, opponent):
    """Create comprehensive gameplan for CLI"""
    generator = AdvancedGameplanGenerator()
    return generator.generate_comprehensive_gameplan(league, season, opponent)


if __name__ == "__main__":
    # Test
    generator = AdvancedGameplanGenerator()
    generator.generate_comprehensive_gameplan('USFL', 2011, 'SCS')