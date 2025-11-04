"""
Targeting Analysis Module
Analyzes where opponents target their passes by position
"""

import pandas as pd
import os
from main import format_df
from util import Config


def analyze_team_targeting_patterns(league, season, team, min_percentage=2.0):
    """
    Analyze which positions a team targets with their passes
    This tells you where to put your best defensive players
    """
    print(f"Analyzing {team}'s pass targeting patterns...")
    
    # Load season data
    tdf = format_df(Config.load_feather(league, season))
    
    # Filter for this team's offensive plays
    team_games = tdf.loc[tdf.away_ac.eq(team) | tdf.home_ac.eq(team)]
    team_offense = team_games.loc[team_games.HasBall.eq(team)]
    
    # Try to load MFN-Targets.csv from files directory
    targets_file = os.path.join(Config.root, 'MFN-Targets.csv')
    if not os.path.exists(targets_file):
        print(f"  Warning: {targets_file} not found.")
        return None
    
    targets_df = pd.read_csv(targets_file)
    
    # Get team's most common offensive plays
    team_plays = (team_offense.groupby('OffensivePlay')
                  .size()
                  .sort_values(ascending=False))
    
    total_plays = team_plays.sum()
    play_percentages = (team_plays / total_plays * 100).round(1)
    
    # Filter for plays used at least min_percentage of time
    common_plays = play_percentages[play_percentages >= min_percentage]
    
    if common_plays.empty:
        print(f"  No common plays found for {team}")
        return None
    
    # Get targeting data for their common plays
    team_targeting = targets_df[targets_df['OffensivePlay'].isin(common_plays.index)]
    
    if team_targeting.empty:
        print(f"  No targeting data found for {team}'s plays")
        return None
    
    # Calculate weighted targeting percentages
    targeting_summary = {}
    total_weighted_targets = 0
    
    for _, row in team_targeting.iterrows():
        play = row['OffensivePlay']
        target = row['target']
        target_pct = float(str(row['tgt %']).replace('%', ''))
        play_frequency = play_percentages.get(play, 0)
        
        # Weight by how often they run this play
        weighted_targets = target_pct * play_frequency / 100
        
        if target in targeting_summary:
            targeting_summary[target] += weighted_targets
        else:
            targeting_summary[target] = weighted_targets
        
        total_weighted_targets += weighted_targets
    
    # Convert to percentages and sort
    if total_weighted_targets > 0:
        targeting_percentages = {
            target: (weighted / total_weighted_targets * 100)
            for target, weighted in targeting_summary.items()
        }
        
        # Sort by percentage
        sorted_targets = sorted(targeting_percentages.items(), 
                              key=lambda x: x[1], reverse=True)
        
        return {
            'team': team,
            'targeting_percentages': sorted_targets,
            'common_plays': common_plays,
            'total_plays_analyzed': total_plays
        }
    
    return None


def format_targeting_report(targeting_data):
    """Format targeting analysis for display"""
    if not targeting_data:
        return "No targeting data available"
    
    team = targeting_data['team']
    targets = targeting_data['targeting_percentages']
    
    report = []
    report.append(f"\n🎯 PASS TARGETING ANALYSIS for {team}")
    report.append("=" * 50)
    report.append("Where to put your BEST defensive players:")
    report.append("-" * 40)
    
    for i, (position, percentage) in enumerate(targets[:8], 1):  # Top 8 targets
        if percentage >= 1.0:  # Only show significant targets
            report.append(f"{i:2d}. {position}: {percentage:.1f}%")
    
    report.append(f"\n📊 Based on {targeting_data['total_plays_analyzed']} offensive plays")
    
    return "\n".join(report)


def get_targeting_recommendations(targeting_data):
    """Get specific defensive recommendations based on targeting"""
    if not targeting_data:
        return []
    
    targets = targeting_data['targeting_percentages']
    recommendations = []
    
    # Top target gets your best coverage
    if targets and targets[0][1] >= 10:
        top_target = targets[0][0]
        recommendations.append(f"🔒 Put your BEST coverage defender on {top_target} (targeted {targets[0][1]:.1f}% of time)")
    
    # Secondary targets
    for position, percentage in targets[1:4]:  # Next 3 most targeted
        if percentage >= 5:
            recommendations.append(f"👀 Watch for passes to {position} ({percentage:.1f}%)")
    
    return recommendations


# Integration function for the main scouting report
def add_targeting_to_scouting(league, season, team):
    """Add targeting analysis to existing scouting reports"""
    targeting_data = analyze_team_targeting_patterns(league, season, team)
    
    if targeting_data:
        print(format_targeting_report(targeting_data))
        
        recommendations = get_targeting_recommendations(targeting_data)
        if recommendations:
            print(f"\n💡 DEFENSIVE RECOMMENDATIONS:")
            print("-" * 30)
            for rec in recommendations:
                print(f"  {rec}")
    
    return targeting_data


if __name__ == "__main__":
    # Example usage
    add_targeting_to_scouting('USFL', 2002, 'BOS')