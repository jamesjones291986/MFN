#!/usr/bin/env python3
"""
Quick Opponent Analysis Tool
===========================

Simple wrapper for team-specific success analysis.

Usage:
    python analyze_opponent.py MIC
    python analyze_opponent.py SJS --season 2017
    python analyze_opponent.py PHI --league USFL --season 2018 --detailed
"""

import sys
import argparse
from pathlib import Path

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from team_specific_analysis.team_specific_success_analyzer import TeamSuccessAnalyzer

def quick_analysis(opponent, league='USFL', season=2018, detailed=False):
    """Run quick analysis with common defaults."""
    
    print(f"🎯 Quick Analysis: What works against {opponent}")
    print(f"League: {league}, Season: {season}")
    print("=" * 50)
    
    try:
        min_attempts = 1 if detailed else 2
        analyzer = TeamSuccessAnalyzer(league, season, opponent, min_attempts)
        
        # Run the analysis
        results = analyzer.generate_full_report()
        
        # Add quick summary
        print(f"\n📋 QUICK SUMMARY")
        print("=" * 20)
        print(f"✅ Analysis complete for {opponent}")
        print(f"💡 Review recommendations above for your gameplan")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Quick opponent analysis')
    parser.add_argument('opponent', help='Opponent team abbreviation (e.g., MIC, SJS, PHI)')
    parser.add_argument('--league', default='USFL', help='League (default: USFL)')
    parser.add_argument('--season', type=int, default=2018, help='Season (default: 2018)')
    parser.add_argument('--detailed', action='store_true', help='More detailed analysis (lower min attempts)')
    
    args = parser.parse_args()
    
    results = quick_analysis(args.opponent.upper(), args.league, args.season, args.detailed)
    
    return 0 if results else 1

if __name__ == "__main__":
    sys.exit(main())