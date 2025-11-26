#!/usr/bin/env python3
"""
Gameplan Generator Demo Script
==============================

Simple demonstration of how to use the automated gameplan generator.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append('/Users/jamesjones/projects/mfn/scouting')

from automated_gameplan_generator import GameplanGenerator

def main():
    print("🏈 MFN Automated Gameplan Generator Demo")
    print("=" * 50)
    
    # Initialize the generator
    print("\n1. Initializing gameplan generator...")
    generator = GameplanGenerator(
        min_play_threshold=3.0,  # Only consider plays called 3%+ of the time
        top_plays_limit=15       # Show top 15 defensive recommendations
    )
    
    # Example 1: Single team gameplan
    print("\n2. Generating gameplan for SJS (USFL 2011)...")
    try:
        gameplan = generator.generate_team_gameplan('USFL', 2011, 'SJS')
        generator.export_gameplan(gameplan, 'demo_sjs_gameplan.txt')
        print("✅ Single team gameplan generated successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Quick summary for multiple teams (optional - can be slow)
    print("\n3. Want to generate for all teams? (This will take a while)")
    response = input("Generate all teams? (y/n): ").lower().strip()
    
    if response == 'y':
        print("Generating gameplans for all teams in USFL 2011...")
        try:
            all_gameplans = generator.generate_all_teams_gameplan('USFL', 2011)
            generator.export_gameplan(all_gameplans, 'demo_all_teams_gameplans.txt')
            print("✅ All team gameplans generated successfully!")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("Skipping all teams generation.")
    
    print("\n🎉 Demo completed!")
    print("\nFiles generated:")
    print("- demo_sjs_gameplan.txt (detailed gameplan for SJS)")
    if response == 'y':
        print("- demo_all_teams_gameplans.txt (summary for all teams)")
    
    print("\nTo use the full script:")
    print("python3 automated_gameplan_generator.py --league USFL --season 2011 --team SJS")
    print("python3 automated_gameplan_generator.py --league USFL --season 2011 --all-teams")

if __name__ == "__main__":
    main()