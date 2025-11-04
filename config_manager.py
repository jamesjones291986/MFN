"""
Configuration management for MFN Data Analysis
Handles loading configuration from YAML files with local overrides
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional


class ConfigManager:
    """Manages configuration loading with local overrides"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or Path(__file__).parent)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with local overrides"""
        # Load base config
        base_config_path = self.config_dir / "config.yaml"
        if not base_config_path.exists():
            raise FileNotFoundError(f"Base config file not found: {base_config_path}")
        
        with open(base_config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Load local overrides if they exist
        local_config_path = self.config_dir / "config.local.yaml"
        if local_config_path.exists():
            with open(local_config_path, 'r') as f:
                local_config = yaml.safe_load(f)
            config = self._merge_configs(config, local_config)
        
        return config
    
    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge override config into base config"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    @property
    def root_dir(self) -> str:
        """Get the root data directory"""
        return self.config['data']['root_dir']
    
    @property
    def feathers_dir(self) -> str:
        """Get the feathers data directory"""
        return self.config['data']['feathers_dir']
    
    @property
    def global_files_dir(self) -> str:
        """Get the global files directory"""
        return self.config['data']['global_files_dir']
    
    @property
    def global_off_file(self) -> str:
        """Get path to global offensive plays reference file"""
        filename = self.config['reference_files']['global_off']
        return os.path.join(self.global_files_dir, filename)
    
    @property
    def global_def_file(self) -> str:
        """Get path to global defensive plays reference file"""
        filename = self.config['reference_files']['global_def']
        return os.path.join(self.global_files_dir, filename)
    
    @property
    def credentials_file(self) -> str:
        """Get path to Google Sheets credentials file"""
        filename = self.config['google_sheets']['credentials_file']
        return os.path.join(self.config_dir, filename)
    
    def get_leagues(self) -> Dict[str, Dict[str, Any]]:
        """Get all league configurations"""
        return self.config['leagues']
    
    def get_league_seasons(self, league: str) -> List[int]:
        """Get seasons for a specific league"""
        if league not in self.config['leagues']:
            raise ValueError(f"Unknown league: {league}")
        return self.config['leagues'][league]['seasons']
    
    def get_league_domain(self, league: str) -> str:
        """Get domain for a specific league"""
        if league not in self.config['leagues']:
            raise ValueError(f"Unknown league: {league}")
        return self.config['leagues'][league]['domain']
    
    def get_league_sheet_id(self, league: str) -> Optional[str]:
        """Get Google Sheet ID for a specific league"""
        if league not in self.config['leagues']:
            raise ValueError(f"Unknown league: {league}")
        return self.config['leagues'][league].get('sheet_id')
    
    def get_ls_dictionary(self) -> Dict[str, List[int]]:
        """Get league-seasons dictionary in the format expected by existing code"""
        return {
            league: config['seasons']
            for league, config in self.config['leagues'].items()
        }
    
    def get_domain_map(self) -> Dict[str, str]:
        """Get domain mapping in the format expected by existing code"""
        return {
            league: config['domain']
            for league, config in self.config['leagues'].items()
        }
    
    def get_sheet_lookup(self) -> Dict[str, str]:
        """Get sheet lookup in the format expected by existing code"""
        return {
            league: config['sheet_id']
            for league, config in self.config['leagues'].items()
            if 'sheet_id' in config
        }
    
    def get_version_map(self) -> Dict[str, Dict[int, str]]:
        """Get version mapping for all leagues"""
        version_map = {}
        target_version = self.config['analysis']['target_version']
        
        for league, config in self.config['leagues'].items():
            version_map[league] = {
                season: target_version
                for season in config['seasons']
            }
        
        return version_map
    
    @property
    def target_version(self) -> str:
        """Get the target game version for analysis"""
        return self.config['analysis']['target_version']
    
    @property
    def ytgl_bucket_size(self) -> int:
        """Get the yards-to-goal-line bucket size"""
        return self.config['analysis']['ytgl_bucket_size']
    
    @property
    def min_play_count(self) -> int:
        """Get minimum play count for statistical significance"""
        return self.config['analysis']['min_play_count']
    
    @property
    def pass_threshold(self) -> int:
        """Get pass threshold for defensive analysis"""
        return self.config['analysis']['pass_threshold']
    
    @property
    def run_threshold(self) -> int:
        """Get run threshold for defensive analysis"""
        return self.config['analysis']['run_threshold']
    
    @property
    def run_plays(self) -> List[str]:
        """Get list of run play types"""
        return self.config['analysis']['run_plays']
    
    @property
    def pass_plays(self) -> List[str]:
        """Get list of pass play types"""
        return self.config['analysis']['pass_plays']
    
    @property
    def all_plays(self) -> List[str]:
        """Get list of all play types"""
        return self.run_plays + self.pass_plays
    
    @property
    def def_excludes(self) -> List[str]:
        """Get list of defensive plays to exclude from analysis"""
        return self.config['analysis']['def_excludes']
    
    @property
    def off_excludes(self) -> List[str]:
        """Get list of offensive plays to exclude from analysis"""
        return self.config['analysis']['off_excludes']
    
    @property
    def auto_save(self) -> bool:
        """Get auto-save setting for analysis results"""
        return self.config['output']['auto_save']
    
    @property
    def default_format(self) -> str:
        """Get default output format for data exports"""
        return self.config['output']['default_format']
    
    @property
    def debug_mode(self) -> bool:
        """Get debug mode setting"""
        return self.config['output']['debug_mode']


# Global instance for backward compatibility
config_manager = ConfigManager()


def get_config() -> ConfigManager:
    """Get the global configuration manager instance"""
    return config_manager