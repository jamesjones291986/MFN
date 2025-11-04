"""
Auto-Discovery Game Log Downloader
Downloads game logs without requiring Google Sheets schedule data
Automatically discovers available games for new seasons
"""

import os
import requests
import time
from util import Config


class AutoGameLogDownloader:
    """Downloads game logs by auto-discovering available games"""
    
    def __init__(self):
        self.root = Config.root
        self.domain_map = Config.domain_map
        
        # Known USFL season patterns (Game 1 IDs)
        self.usfl_base_games = {
            2016: 13443,
            2017: 13760,
            2018: 14077
        }
        self.usfl_games_per_season = 317  # Calculated from pattern
        
    def build_game_log_url(self, league, season, game_id):
        """Build URL for a specific game log"""
        domain = self.domain_map.get(league, league.lower())
        return f"https://{domain}.myfootballnow.com/log/download/{game_id}"
    
    def test_game_exists(self, league, season, game_id):
        """Test if a game ID exists by trying to access it"""
        url = self.build_game_log_url(league, season, game_id)
        
        try:
            response = requests.head(url, timeout=10)  # Use HEAD for faster check
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def download_game_log(self, league, season, game_id, force=False):
        """Download a specific game log"""
        # Create league/season directory
        season_dir = os.path.join(self.root, league, str(season))
        os.makedirs(season_dir, exist_ok=True)
        
        # File path for this game
        file_path = os.path.join(season_dir, f"{game_id}.csv")
        
        # Skip if already exists (unless force)
        if os.path.exists(file_path) and not force:
            return True
        
        # Download the game log
        url = self.build_game_log_url(league, season, game_id)
        
        try:
            print(f"    Downloading game {game_id}...")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"      ❌ Game {game_id} not found (HTTP {response.status_code})")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"      ❌ Error downloading game {game_id}: {e}")
            return False
    
    def auto_discover_season(self, league, season, force=False, max_games=500):
        """Auto-discover and download all available games for a season"""
        print(f"\n🔍 Auto-discovering {league} {season} games...")
        
        # Start from game ID 1 and work up
        games_found = []
        consecutive_misses = 0
        max_consecutive_misses = 20  # Stop after 20 consecutive missing games
        
        for game_id in range(1, max_games + 1):
            # Test if this game exists
            if self.test_game_exists(league, season, game_id):
                # Game exists, try to download it
                if self.download_game_log(league, season, game_id, force):
                    games_found.append(game_id)
                    consecutive_misses = 0  # Reset counter
                else:
                    consecutive_misses += 1
            else:
                consecutive_misses += 1
            
            # Stop if we've missed too many consecutive games
            if consecutive_misses >= max_consecutive_misses:
                print(f"    Stopped after {consecutive_misses} consecutive missing games")
                break
            
            # Small delay to be respectful to the server
            time.sleep(0.1)
        
        print(f"✅ Found and downloaded {len(games_found)} games for {league} {season}")
        
        if games_found:
            print(f"   Game IDs: {min(games_found)} to {max(games_found)}")
        
        return games_found
    
    def predict_usfl_range(self, season):
        """Predict the game ID range for a USFL season based on known patterns"""
        # If we have a known base game for this season, use it
        if season in self.usfl_base_games:
            start_game = self.usfl_base_games[season]
            return (start_game, start_game + self.usfl_games_per_season - 1)
        
        # Try to predict based on pattern
        # Find the closest known season
        known_seasons = sorted(self.usfl_base_games.keys())
        
        if season < min(known_seasons):
            # Extrapolate backwards
            base_season = min(known_seasons)
            years_diff = base_season - season
            predicted_start = self.usfl_base_games[base_season] - (years_diff * self.usfl_games_per_season)
        elif season > max(known_seasons):
            # Extrapolate forwards
            base_season = max(known_seasons)
            years_diff = season - base_season
            predicted_start = self.usfl_base_games[base_season] + (years_diff * self.usfl_games_per_season)
        else:
            # Interpolate between known seasons
            return None  # Use fallback for now
        
        if predicted_start > 0:
            return (predicted_start, predicted_start + self.usfl_games_per_season - 1)
        
        return None
    
    def smart_range_discovery(self, league, season, force=False):
        """Smart discovery that tries to find the game ID range first"""
        print(f"\n🧠 Smart discovery for {league} {season}...")
        
        # Use known patterns for specific leagues
        if league == 'USFL':
            predicted_range = self.predict_usfl_range(season)
            if predicted_range:
                print(f"  🎯 Using predicted USFL range: {predicted_range[0]}-{predicted_range[1]}")
                test_ranges = [predicted_range]
            else:
                test_ranges = [(13000, 16000)]  # Fallback for USFL
        else:
            # Try some common game ID ranges to find where games exist
            test_ranges = [
                (1, 100),       # Very early seasons
                (1000, 2000),   # Early seasons  
                (5000, 6000),   # Mid seasons
                (10000, 15000), # Recent seasons
                (15000, 20000), # Very recent seasons
                (17000, 19000), # Calculated range for 2018
                (20000, 25000), # Latest seasons
                (25000, 30000), # Future seasons
                (30000, 35000), # Even newer seasons
            ]
        
        found_range = None
        
        # Find which range has games
        for start, end in test_ranges:
            print(f"  Testing range {start}-{end}...")
            
            # Test a few games in this range
            test_games = [start, start + 50, start + 100, end - 100, end - 50, end]
            games_in_range = []
            
            for game_id in test_games:
                if self.test_game_exists(league, season, game_id):
                    games_in_range.append(game_id)
            
            if games_in_range:
                found_range = (start, end)
                print(f"    ✅ Found games in range {start}-{end}")
                break
        
        if found_range:
            # Now do detailed discovery in the found range
            return self.auto_discover_season_in_range(league, season, found_range[0], found_range[1], force)
        else:
            print("    ❌ No games found in any tested range")
            return []
    
    def auto_discover_season_in_range(self, league, season, start_id, end_id, force=False):
        """Discover games within a specific ID range"""
        print(f"🔍 Detailed scan of {league} {season} games {start_id}-{end_id}...")
        
        games_found = []
        
        for game_id in range(start_id, end_id + 1):
            if self.test_game_exists(league, season, game_id):
                if self.download_game_log(league, season, game_id, force):
                    games_found.append(game_id)
            
            # Progress indicator
            if game_id % 100 == 0:
                print(f"    Scanned up to game {game_id}... ({len(games_found)} found)")
            
            time.sleep(0.05)  # Small delay
        
        print(f"✅ Downloaded {len(games_found)} games from range {start_id}-{end_id}")
        return games_found


# CLI integration function
def auto_download_season(league, season, force=False, smart=True):
    """Auto-download a season without needing Google Sheets"""
    downloader = AutoGameLogDownloader()
    
    if smart:
        return downloader.smart_range_discovery(league, season, force)
    else:
        return downloader.auto_discover_season(league, season, force)


if __name__ == "__main__":
    # Example usage
    downloader = AutoGameLogDownloader()
    downloader.smart_range_discovery('USFL', 2018)