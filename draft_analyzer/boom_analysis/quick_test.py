#!/usr/bin/env python3
"""
Quick test of boom analysis
"""

from boom_adjusted_draft_analyzer import BoomAdjustedDraftAnalyzer

def quick_boom_test():
    # Test with your draft sheet ID
    sheet_id = "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"  # Update this
    
    print("🚀 Testing Boom Analysis")
    print("=" * 50)
    
    analyzer = BoomAdjustedDraftAnalyzer(sheet_id, verbose=False)
    analyzer.load_data()
    
    # Test one prospect
    prospect = analyzer.draft_prospects[0]
    analysis = analyzer.analyze_prospect_boom_scenarios(prospect)
    
    name = analysis['player_name']
    vol = analysis['volatility']
    best_pos = analysis['best_boom_position']
    boom_rating = analysis['best_boom_rating']
    conservative_rating = analysis['best_conservative_rating']
    
    print(f"\n🎯 Test Prospect: {name}")
    print(f"Volatility: {vol}")
    print(f"Best Position: {best_pos}")
    print(f"Boom Rating: {boom_rating:.1f}")
    print(f"Conservative Rating: {conservative_rating:.1f}")
    print(f"Upside: {boom_rating - conservative_rating:+.1f}")
    
    # Show speed calculation example
    scenario = analysis['scenarios'][best_pos]
    print(f"Speed at {best_pos}: {scenario['adjusted_speed']:.1f}")

if __name__ == "__main__":
    quick_boom_test()