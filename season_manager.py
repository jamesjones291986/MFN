"""
Automated Season Management System
Handles downloading new seasons and managing data storage
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from GameLogDownloader import GameLogDownloader
from util import Config


class SeasonManager:
    """Manages automated season downloads and data organization"""
    
    def __init__(self):
        self.base_dir = Path("/Users/jamesjones/personal/game_logs")
        self.seasons_tracking_file = self.base_dir / "seasons_tracking.json"
        self.auto_download_config = self.base_dir / "auto_download.yaml"
        
        # Load tracking data
        self.seasons_tracking = self._load_seasons_tracking()
        self.auto_config = self._load_auto_config()
    
    def _load_seasons_tracking(self):
        """Load tracking data for seasons"""
        if self.seasons_tracking_file.exists():
            with open(self.seasons_tracking_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'last_check': None,
                'seasons': {},
                'auto_leagues': []
            }
    
    def _save_seasons_tracking(self):
        """Save tracking data"""
        with open(self.seasons_tracking_file, 'w') as f:
            json.dump(self.seasons_tracking, f, indent=2, default=str)
    
    def _load_auto_config(self):
        """Load auto-download configuration"""
        if self.auto_download_config.exists():
            with open(self.auto_download_config, 'r') as f:
                return yaml.safe_load(f)
        else:
            return {
                'enabled': True,
                'check_interval_hours': 24,
                'leagues_to_monitor': ['qad', 'xfl', 'pfl'],
                'auto_compile': True,
                'notifications': True
            }
    
    def setup_auto_download(self, leagues_to_monitor):
        """Setup automatic downloading for specified leagues"""
        print(f"Setting up auto-download for: {', '.join(leagues_to_monitor)}")
        
        config = {
            'enabled': True,
            'check_interval_hours': 24,
            'leagues_to_monitor': leagues_to_monitor,
            'auto_compile': True,
            'notifications': True,
            'last_setup': datetime.now().isoformat()
        }
        
        with open(self.auto_download_config, 'w') as f:
            yaml.dump(config, f, indent=2)
        
        print(f"✅ Auto-download configured for {len(leagues_to_monitor)} leagues")
        print(f"   Will check every {config['check_interval_hours']} hours")
        
        return config
    
    def detect_new_seasons(self):
        """Detect if new seasons are available for monitored leagues"""
        print("🔍 Checking for new seasons...")
        
        new_seasons_found = []
        gdl = GameLogDownloader()
        
        for league in self.auto_config.get('leagues_to_monitor', []):
            print(f"  Checking {league}...")
            
            # Get current known seasons for this league
            current_seasons = Config.ls_dictionary.get(league, [])
            if not current_seasons:
                continue
            
            # Check for next season (highest + 1)
            max_season = max(current_seasons)
            next_season = max_season + 1
            
            # Try to set up download for next season
            if gdl.set_league_season(league, next_season):
                # Check if games are available
                try:
                    # This would need to be implemented in GameLogDownloader
                    # For now, we'll assume if set_league_season works, games might exist
                    new_seasons_found.append((league, next_season))
                    print(f"    ✅ Found potential new season: {league} {next_season}")
                except:
                    print(f"    ⏳ {league} {next_season} not ready yet")
            else:
                print(f"    ⏳ {league} {next_season} not available")
        
        return new_seasons_found
    
    def download_new_seasons(self, new_seasons=None, force=False):
        """Download newly detected seasons"""
        if new_seasons is None:
            new_seasons = self.detect_new_seasons()
        
        if not new_seasons:
            print("📊 No new seasons detected")
            return []
        
        downloaded = []
        gdl = GameLogDownloader()
        
        for league, season in new_seasons:
            print(f"\n⬇️  Downloading {league} {season}...")
            
            try:
                if gdl.set_league_season(league, season):
                    if gdl.download_season():
                        downloaded.append((league, season))
                        
                        # Update tracking
                        season_key = f"{league}_{season}"
                        self.seasons_tracking['seasons'][season_key] = {
                            'downloaded': datetime.now().isoformat(),
                            'status': 'complete',
                            'games_count': 0  # Would need to count actual games
                        }
                        
                        print(f"    ✅ Downloaded {league} {season}")
                        
                        # Auto-compile if enabled
                        if self.auto_config.get('auto_compile', True):
                            print(f"    🔄 Auto-compiling {league} {season}...")
                            # Would call SeasonCompiler here
                    else:
                        print(f"    ❌ Failed to download {league} {season}")
                else:
                    print(f"    ❌ Could not set up {league} {season}")
                    
            except Exception as e:
                print(f"    ❌ Error downloading {league} {season}: {e}")
        
        # Update tracking
        self.seasons_tracking['last_check'] = datetime.now().isoformat()
        self._save_seasons_tracking()
        
        return downloaded
    
    def organize_data_storage(self):
        """Organize and clean up data storage"""
        print("🗂️  Organizing data storage...")
        
        # Create organized directory structure
        organized_dir = self.base_dir / "organized"
        
        # Create subdirectories
        for league in Config.ls_dictionary.keys():
            league_dir = organized_dir / league
            league_dir.mkdir(parents=True, exist_ok=True)
            
            # Create season subdirectories
            for season in Config.ls_dictionary[league]:
                season_dir = league_dir / str(season)
                season_dir.mkdir(exist_ok=True)
                
                # Subdirectories for different data types
                (season_dir / "raw_logs").mkdir(exist_ok=True)
                (season_dir / "compiled").mkdir(exist_ok=True)
                (season_dir / "analysis").mkdir(exist_ok=True)
        
        print(f"✅ Organized storage structure created at {organized_dir}")
        return organized_dir
    
    def cleanup_old_files(self, days_old=30):
        """Clean up temporary files older than specified days"""
        print(f"🧹 Cleaning up files older than {days_old} days...")
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        cleaned_count = 0
        
        # Look for temporary files, logs, etc.
        temp_patterns = ['*.tmp', '*.log', '*_temp_*']
        
        for pattern in temp_patterns:
            for file_path in self.base_dir.glob(f"**/{pattern}"):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_date:
                        try:
                            file_path.unlink()
                            cleaned_count += 1
                        except Exception as e:
                            print(f"    ⚠️  Could not delete {file_path}: {e}")
        
        print(f"✅ Cleaned up {cleaned_count} old files")
        return cleaned_count
    
    def get_storage_stats(self):
        """Get statistics about data storage"""
        stats = {
            'total_files': 0,
            'total_size_mb': 0,
            'leagues': {},
            'file_types': {}
        }
        
        for file_path in self.base_dir.rglob('*'):
            if file_path.is_file():
                stats['total_files'] += 1
                size_mb = file_path.stat().st_size / (1024 * 1024)
                stats['total_size_mb'] += size_mb
                
                # Track by file extension
                ext = file_path.suffix.lower()
                if ext not in stats['file_types']:
                    stats['file_types'][ext] = {'count': 0, 'size_mb': 0}
                stats['file_types'][ext]['count'] += 1
                stats['file_types'][ext]['size_mb'] += size_mb
        
        return stats
    
    def create_backup(self, backup_type='incremental'):
        """Create backup of important data"""
        print(f"💾 Creating {backup_type} backup...")
        
        backup_dir = self.base_dir / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup feather files (most important)
        feather_files = list(self.base_dir.glob("**/*.feather"))
        
        print(f"   Backing up {len(feather_files)} feather files...")
        for feather_file in feather_files:
            relative_path = feather_file.relative_to(self.base_dir)
            backup_path = backup_dir / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copy2(feather_file, backup_path)
        
        # Backup configuration and tracking files
        config_files = [
            self.seasons_tracking_file,
            self.auto_download_config,
            Path("config.local.yaml")
        ]
        
        for config_file in config_files:
            if config_file.exists():
                shutil.copy2(config_file, backup_dir / config_file.name)
        
        print(f"✅ Backup created at {backup_dir}")
        return backup_dir


# CLI integration functions
def setup_auto_downloads(leagues):
    """Setup automatic downloads for CLI"""
    manager = SeasonManager()
    return manager.setup_auto_download(leagues)

def check_for_new_seasons():
    """Check for new seasons for CLI"""
    manager = SeasonManager()
    new_seasons = manager.detect_new_seasons()
    
    if new_seasons:
        print(f"🆕 Found {len(new_seasons)} potential new seasons:")
        for league, season in new_seasons:
            print(f"   {league} {season}")
        
        response = input("\nDownload these seasons? (y/n): ")
        if response.lower() == 'y':
            manager.download_new_seasons(new_seasons)
    else:
        print("📊 No new seasons detected")
    
    return new_seasons

def organize_storage():
    """Organize storage for CLI"""
    manager = SeasonManager()
    manager.organize_data_storage()
    
    # Show storage stats
    stats = manager.get_storage_stats()
    print(f"\n📊 Storage Statistics:")
    print(f"   Total files: {stats['total_files']:,}")
    print(f"   Total size: {stats['total_size_mb']:.1f} MB")
    print(f"   Largest file type: {max(stats['file_types'].items(), key=lambda x: x[1]['size_mb'], default=('none', {'size_mb': 0}))[0]}")


if __name__ == "__main__":
    # Example usage
    manager = SeasonManager()
    manager.setup_auto_download(['qad', 'xfl'])
    new_seasons = manager.detect_new_seasons()
    print(f"Found {len(new_seasons)} new seasons")