"""
Quick Update and Gameplan Generator
One-command workflow to update data and generate gameplans
"""

import os
from auto_downloader import AutoGameLogDownloader
from SeasonCompiler import SeasonCompiler
from advanced_gameplan import create_comprehensive_gameplan


def update_season_and_gameplan(league, season, opponent=None, force_download=False):
    """
    Complete workflow: Download latest → Compile → Generate gameplan
    """
    print(f"🔄 UPDATING {league} {season} AND GENERATING GAMEPLAN")
    print("=" * 60)
    
    # Step 1: Download latest game logs
    print(f"\n📥 Step 1: Downloading latest {league} {season} game logs...")
    downloader = AutoGameLogDownloader()
    
    try:
        games_found = downloader.smart_range_discovery(league, season, force_download)
        
        if not games_found:
            print(f"❌ No games found for {league} {season}")
            return False
            
        print(f"✅ Downloaded {len(games_found)} games")
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("💡 Try manual download or check if season exists")
        return False
    
    # Step 2: Compile into feather file
    print(f"\n🔄 Step 2: Compiling {league} {season} into feather file...")
    
    try:
        # Check if we have a schedule file, if not create a basic one
        schedule_path = f"./data/{league}/{league}_{season}.csv"
        
        if not os.path.exists(schedule_path):
            print(f"   Creating basic schedule file for compilation...")
            create_basic_schedule(league, season, games_found)
        
        # Compile season
        SeasonCompiler.compile(league, season, override_path=schedule_path)
        print(f"✅ Compiled {league}_{season}.feather")
        
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        print("💡 You may need to create a schedule file manually")
        return False
    
    # Step 3: Generate gameplan if opponent specified
    if opponent:
        print(f"\n🎯 Step 3: Generating gameplan vs {opponent}...")
        
        try:
            create_comprehensive_gameplan(league, season, opponent)
            print(f"✅ Gameplan vs {opponent} generated!")
            
        except Exception as e:
            print(f"❌ Gameplan generation failed: {e}")
            print("💡 Try running scout command first to verify team exists")
            return False
    
    print(f"\n🎉 SUCCESS! {league} {season} is updated and ready for analysis")
    
    if opponent:
        print(f"🏈 Your gameplan vs {opponent} is ready!")
        print(f"\n💡 Quick commands:")
        print(f"   Scout: python3 mfn_cli.py scout {league} {season} {opponent}")
        print(f"   Gameplan: python3 mfn_cli.py comprehensive {league} {season} {opponent}")
    
    return True


def create_basic_schedule(league, season, game_ids):
    """Create a basic schedule file from downloaded game IDs"""
    schedule_data = []
    
    # Create basic schedule structure
    for i, game_id in enumerate(game_ids, 1):
        schedule_data.append({
            'Season': season,
            'Type': 'Regular',
            'Week': ((i - 1) // 16) + 1,  # Assume 16 games per week
            'Game ID': game_id
        })
    
    import pandas as pd
    df = pd.DataFrame(schedule_data)
    
    # Create directory if needed
    os.makedirs(f"./data/{league}", exist_ok=True)
    
    # Save schedule
    schedule_path = f"./data/{league}/{league}_{season}.csv"
    df.to_csv(schedule_path, index=False)
    
    print(f"   Created basic schedule: {schedule_path}")
    return schedule_path


def quick_update_workflow(league, season, opponent=None):
    """Quick workflow for getting latest data and gameplan"""
    return update_season_and_gameplan(league, season, opponent, force_download=True)


# For situations where you just want to update without gameplan
def update_season_only(league, season):
    """Update season data without generating gameplan"""
    return update_season_and_gameplan(league, season, opponent=None, force_download=True)


if __name__ == "__main__":
    # Example usage
    quick_update_workflow('USFL', 2018, 'SCS')