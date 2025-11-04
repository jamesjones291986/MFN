"""
Game Planning Module for MFN
Generates optimal offensive plays to counter opponent's defensive tendencies
"""

import pandas as pd
from main import format_df, adj_ev, all_plays
from util import Config


def get_opponent_defensive_tendencies(league, season, team, min_percentage=2.0):
    """Get opponent's most common defensive plays"""
    print(f"Analyzing {team}'s defensive tendencies in {league} {season}...")
    
    # Load and format data
    tdf = format_df(Config.load_feather(league, season))
    
    # Filter for games where this team was on defense
    team_games = tdf.loc[tdf.away_ac.eq(team) | tdf.home_ac.eq(team)]
    defensive_plays = team_games.loc[team_games.DefTeam.eq(team)]
    
    # Exclude special teams plays
    def_excludes = (None, 'FG Block', 'Punt Return', 'Kick Return', 'Onsides Kick Return Onside Kick Return')
    defensive_plays = defensive_plays.loc[~defensive_plays.DefensivePlay.isin(def_excludes)]
    
    # Calculate defensive play percentages
    play_counts = defensive_plays.groupby('DefensivePlay').DefensivePlay.count()
    total_plays = defensive_plays.shape[0]
    
    if total_plays == 0:
        print(f"No defensive data found for {team}")
        return pd.DataFrame()
    
    play_percentages = (100 * play_counts / total_plays).round(2)
    
    # Filter for plays used at least min_percentage of the time
    common_plays = play_percentages.loc[play_percentages >= min_percentage].sort_values(ascending=False)
    
    return common_plays


def find_best_plays_vs_defense(defensive_plays, data_df, min_play_count=20):
    """Find the best offensive plays against specific defensive plays"""
    print(f"Finding best offensive plays against {len(defensive_plays)} defensive schemes...")
    
    results = []
    
    for def_play in defensive_plays.index:
        # Filter data for when this defensive play was called
        vs_def_data = data_df.loc[data_df.DefensivePlay.eq(def_play)]
        
        if vs_def_data.empty:
            continue
            
        # Run analysis to find best offensive plays against this defense
        try:
            best_plays = adj_ev(vs_def_data, 'OffensivePlay', all_plays, 'desc')
            
            # Filter for statistically significant play counts
            best_plays = best_plays.loc[best_plays.cnt >= min_play_count]
            
            if not best_plays.empty:
                # Add defensive context
                best_plays['vs_defense'] = def_play
                best_plays['def_frequency'] = defensive_plays[def_play]
                results.append(best_plays.head(5))  # Top 5 plays vs this defense
                
        except Exception as e:
            print(f"Error analyzing plays vs {def_play}: {e}")
            continue
    
    if results:
        return pd.concat(results, ignore_index=True)
    else:
        return pd.DataFrame()


def generate_gameplan(league, season, opponent_team, your_league=None, your_season=None):
    """Generate a complete gameplan against an opponent"""
    print(f"\n🏈 GENERATING GAMEPLAN vs {opponent_team} ({league} {season})")
    print("=" * 60)
    
    # Step 1: Get opponent's defensive tendencies
    opponent_defense = get_opponent_defensive_tendencies(league, season, opponent_team)
    
    if opponent_defense.empty:
        print(f"❌ No defensive data found for {opponent_team}")
        return None
    
    print(f"\n📊 {opponent_team}'s Defensive Tendencies:")
    print("-" * 40)
    for play, percentage in opponent_defense.head(10).items():
        print(f"  {play}: {percentage}%")
    
    # Step 2: Load broader dataset for play analysis
    if your_league and your_season:
        analysis_data = format_df(Config.load_feather(your_league, your_season))
        print(f"\n🔍 Using {your_league} {your_season} data for play analysis")
    else:
        analysis_data = format_df(Config.load_all_seasons())
        print(f"\n🔍 Using all available data for play analysis")
    
    # Step 3: Find best plays against their defense
    recommended_plays = find_best_plays_vs_defense(opponent_defense, analysis_data)
    
    if recommended_plays.empty:
        print("\n❌ No play recommendations found")
        return None
    
    # Step 4: Generate gameplan report
    print(f"\n🎯 RECOMMENDED OFFENSIVE PLAYS vs {opponent_team}")
    print("=" * 60)
    
    # Group by defensive play for organized output
    for def_play in opponent_defense.head(5).index:  # Top 5 most common defenses
        def_freq = opponent_defense[def_play]
        vs_this_def = recommended_plays.loc[recommended_plays.vs_defense.eq(def_play)]
        
        if not vs_this_def.empty:
            print(f"\n🛡️  vs {def_play} (they use {def_freq}% of time):")
            print("-" * 50)
            
            for _, play in vs_this_def.head(3).iterrows():  # Top 3 plays vs this defense
                print(f"  ✅ {play['OffensivePlay']}")
                print(f"     {play['ypp']:.1f} ypp | {play['any/a']:.1f} any/a | {play['cnt']} plays analyzed")
                print(f"     Personnel: {play['OffPersonnel']} | Type: {play['OffPlayType']}")
                print()
    
    # Step 5: Overall best plays regardless of defense
    print(f"\n⭐ TOP OVERALL PLAYS FOR YOUR GAMEPLAN:")
    print("-" * 40)
    
    # Aggregate recommendations weighted by opponent's defensive frequency
    gameplan_plays = (recommended_plays
                     .groupby('OffensivePlay')
                     .agg({
                         'ypp': 'mean',
                         'any/a': 'mean', 
                         'cnt': 'sum',
                         'def_frequency': 'sum',  # Total coverage against their defense
                         'OffPlayType': 'first',
                         'OffPersonnel': 'first'
                     })
                     .sort_values('ypp', ascending=False))
    
    for i, (play, data) in enumerate(gameplan_plays.head(10).iterrows(), 1):
        print(f"{i:2d}. {play}")
        print(f"    {data['ypp']:.1f} ypp | {data['any/a']:.1f} any/a | Covers {data['def_frequency']:.1f}% of their defense")
        print(f"    {data['OffPersonnel']} | {data['OffPlayType']}")
        print()
    
    # Step 6: Save detailed gameplan
    output_file = f"{Config.root}/gameplan_vs_{opponent_team}_{league}_{season}.csv"
    recommended_plays.to_csv(output_file, index=False)
    print(f"💾 Detailed gameplan saved to: {output_file}")
    
    return {
        'opponent_defense': opponent_defense,
        'recommended_plays': recommended_plays,
        'gameplan_summary': gameplan_plays,
        'output_file': output_file
    }


def quick_gameplan(league, season, opponent_team):
    """Quick gameplan generation with simplified output"""
    return generate_gameplan(league, season, opponent_team)


# Example usage functions
def example_gameplan():
    """Example: Generate gameplan vs BOS in USFL 2002"""
    return generate_gameplan('USFL', 2002, 'BOS')


if __name__ == "__main__":
    # Example usage
    example_gameplan()