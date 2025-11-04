"""
Personnel-Based Play Calling Analysis
Analyzes optimal plays for each personnel grouping vs opponent defensive tendencies
"""

import pandas as pd
from main import format_df, adj_ev
from util import Config
import json


class PersonnelAnalyzer:
    """Analyzes play effectiveness by personnel groupings"""
    
    def __init__(self):
        self.personnel_groups = {
            # Standard groupings
            '11': '1RB/1TE/3WR',
            '12': '1RB/2TE/2WR', 
            '21': '2RB/1TE/2WR',
            '22': '2RB/2TE/1WR',
            '10': '1RB/4WR',
            '01': '5WR',
            '13': '1RB/3TE/1WR',
            '23': '2RB/3TE',
            '31': '3RB/1TE/1WR',
            '20': '2RB/3WR'
        }
        
        self.defensive_packages = {
            'Base': ['3-4 Under', '3-4 Over', '4-3 Under', '4-3 Over'],
            'Nickel': ['Nickel Normal', 'Nickel Strong', 'Nickel Weak'],
            'Dime': ['Dime Normal', 'Dime Flat', 'Dime Strong'],
            'Quarter': ['Quarter Normal'],
            'Goal Line': ['Goal Line', '6-1', '5-2']
        }

    def analyze_opponent_by_personnel(self, league, season, opponent_team):
        """Analyze what defenses opponent uses vs each offensive personnel group"""
        print(f"Analyzing {opponent_team}'s defensive tendencies by offensive personnel...")
        
        # Load season data
        tdf = format_df(Config.load_feather(league, season))
        
        # Get games where opponent was on defense
        opponent_games = tdf.loc[tdf.away_ac.eq(opponent_team) | tdf.home_ac.eq(opponent_team)]
        opponent_defense = opponent_games.loc[opponent_games.DefTeam.eq(opponent_team)]
        
        # Exclude special teams
        def_excludes = (None, 'FG Block', 'Punt Return', 'Kick Return', 'Onsides Kick Return Onside Kick Return')
        opponent_defense = opponent_defense.loc[~opponent_defense.DefensivePlay.isin(def_excludes)]
        
        # Group by offensive personnel (what they faced) and defensive response
        personnel_defense = {}
        
        for personnel_code, personnel_name in self.personnel_groups.items():
            # Filter for plays vs this personnel group
            vs_personnel = opponent_defense.loc[opponent_defense.OffPersonnel.eq(personnel_name)]
            
            if len(vs_personnel) < 10:  # Need minimum sample size
                continue
            
            # Count defensive plays vs this personnel
            def_counts = vs_personnel.groupby('DefensivePlay').size()
            total_vs_personnel = len(vs_personnel)
            def_percentages = (def_counts / total_vs_personnel * 100).round(1)
            
            # Only keep defenses used >5% of time vs this personnel
            common_defenses = def_percentages[def_percentages >= 5.0].sort_values(ascending=False)
            
            if not common_defenses.empty:
                personnel_defense[personnel_name] = {
                    'total_plays': total_vs_personnel,
                    'defenses': common_defenses.to_dict()
                }
        
        return personnel_defense

    def find_best_plays_by_personnel(self, personnel_defense_data, analysis_data):
        """Find best offensive plays for each personnel group vs opponent's defenses"""
        print("Finding optimal plays for each personnel grouping...")
        
        personnel_recommendations = {}
        
        for personnel, def_data in personnel_defense_data.items():
            print(f"\n  Analyzing {personnel}...")
            recommendations = []
            
            # For each defense they commonly use vs this personnel
            for def_play, frequency in def_data['defenses'].items():
                if frequency < 10:  # Skip rare defenses
                    continue
                
                # Find best offensive plays vs this defense with this personnel
                vs_defense = analysis_data.loc[
                    (analysis_data.DefensivePlay.eq(def_play)) &
                    (analysis_data.OffPersonnel.eq(personnel))
                ]
                
                if len(vs_defense) < 20:  # Need minimum sample
                    continue
                
                try:
                    # Run adj_ev analysis for this specific matchup
                    best_plays = adj_ev(vs_defense, 'OffensivePlay', 
                                      vs_defense['OffensivePlay'].unique(), 'desc')
                    
                    # Filter for plays with good sample size and performance
                    good_plays = best_plays.loc[
                        (best_plays.cnt >= 15) & 
                        (best_plays.ypp >= 4.0)
                    ].head(3)
                    
                    for _, play in good_plays.iterrows():
                        recommendations.append({
                            'vs_defense': def_play,
                            'def_frequency': frequency,
                            'play': play['OffensivePlay'],
                            'ypp': play['ypp'],
                            'any_a': play['any/a'],
                            'sample_size': play['cnt'],
                            'play_type': play['OffPlayType']
                        })
                        
                except Exception as e:
                    print(f"    Error analyzing vs {def_play}: {e}")
                    continue
            
            if recommendations:
                # Sort by defense frequency * play effectiveness
                for rec in recommendations:
                    rec['weighted_score'] = rec['def_frequency'] * rec['ypp'] / 100
                
                recommendations.sort(key=lambda x: x['weighted_score'], reverse=True)
                personnel_recommendations[personnel] = recommendations
        
        return personnel_recommendations

    def generate_personnel_gameplan(self, league, season, opponent_team):
        """Generate complete personnel-based gameplan"""
        print(f"\n🏈 PERSONNEL-BASED GAMEPLAN vs {opponent_team}")
        print("=" * 60)
        
        # Step 1: Analyze opponent's defensive tendencies by personnel
        personnel_defense = self.analyze_opponent_by_personnel(league, season, opponent_team)
        
        if not personnel_defense:
            print("❌ Insufficient data for personnel analysis")
            return None
        
        # Step 2: Load analysis data (use all available data for better sample sizes)
        analysis_data = format_df(Config.load_all_seasons())
        
        # Step 3: Find best plays for each personnel group
        recommendations = self.find_best_plays_by_personnel(personnel_defense, analysis_data)
        
        # Step 4: Generate formatted report
        self.format_personnel_report(recommendations, personnel_defense, opponent_team)
        
        # Step 5: Save detailed data
        output_file = f"{Config.root}/personnel_gameplan_vs_{opponent_team}_{league}_{season}.json"
        gameplan_data = {
            'opponent': opponent_team,
            'league': league,
            'season': season,
            'personnel_defense': personnel_defense,
            'recommendations': recommendations
        }
        
        with open(output_file, 'w') as f:
            json.dump(gameplan_data, f, indent=2, default=str)
        
        print(f"\n💾 Detailed personnel gameplan saved to: {output_file}")
        
        return gameplan_data

    def format_personnel_report(self, recommendations, personnel_defense, opponent_team):
        """Format the personnel-based gameplan for display"""
        
        for personnel, plays in recommendations.items():
            if not plays:
                continue
                
            print(f"\n👥 {personnel} PERSONNEL")
            print("=" * 50)
            
            # Show what defenses they use vs this personnel
            def_data = personnel_defense.get(personnel, {})
            total_plays = def_data.get('total_plays', 0)
            
            print(f"📊 {opponent_team} vs {personnel} ({total_plays} plays analyzed):")
            for def_play, freq in list(def_data.get('defenses', {}).items())[:3]:
                print(f"   {def_play}: {freq}%")
            
            print(f"\n🎯 RECOMMENDED PLAYS:")
            print("-" * 30)
            
            # Group plays by defense they're good against
            current_defense = None
            play_count = 0
            
            for play in plays[:8]:  # Top 8 plays for this personnel
                if play['vs_defense'] != current_defense:
                    if current_defense is not None:
                        print()
                    current_defense = play['vs_defense']
                    print(f"   vs {current_defense} ({play['def_frequency']}%):")
                    play_count = 0
                
                play_count += 1
                if play_count <= 2:  # Max 2 plays per defense
                    print(f"     {play_count}. {play['play']}")
                    print(f"        {play['ypp']:.1f} ypp | {play['any_a']:.1f} any/a | {play['sample_size']} plays")

    def get_quick_personnel_summary(self, gameplan_data):
        """Generate a quick reference summary for game day"""
        if not gameplan_data or 'recommendations' not in gameplan_data:
            return "No gameplan data available"
        
        summary = []
        summary.append(f"🏈 QUICK REFERENCE vs {gameplan_data['opponent']}")
        summary.append("=" * 40)
        
        for personnel, plays in gameplan_data['recommendations'].items():
            if not plays:
                continue
                
            summary.append(f"\n{personnel}:")
            # Get the top play for this personnel
            top_play = plays[0]
            summary.append(f"  ⭐ {top_play['play']} ({top_play['ypp']:.1f} ypp)")
            if len(plays) > 1:
                summary.append(f"  💡 {plays[1]['play']} ({plays[1]['ypp']:.1f} ypp)")
        
        return "\n".join(summary)


# Integration function for CLI
def create_personnel_gameplan(league, season, opponent_team):
    """Create personnel-based gameplan for CLI"""
    analyzer = PersonnelAnalyzer()
    return analyzer.generate_personnel_gameplan(league, season, opponent_team)


if __name__ == "__main__":
    # Example usage
    analyzer = PersonnelAnalyzer()
    analyzer.generate_personnel_gameplan('USFL', 2002, 'BOS')