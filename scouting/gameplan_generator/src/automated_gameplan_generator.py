"""
Automated Gameplan Generator for MFN
====================================

This script automates the process of:
1. Analyzing team offensive tendencies by formation
2. Finding the best defensive plays to call against those tendencies
3. Generating comprehensive gameplans with top defensive recommendations

Usage:
    # Scout a specific team
    python automated_gameplan_generator.py --league USFL --season 2011 --team SJS
    
    # Scout all teams in a league/season
    python automated_gameplan_generator.py --league USFL --season 2011 --all-teams
"""

import pandas as pd
import numpy as np
import argparse
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Import existing utilities
sys.path.append('/Users/jamesjones/projects/mfn/scouting')
sys.path.append('/Users/jamesjones/projects/mfn/lineup_analyzer')
from main import format_df, adj_ev, all_plays, run_plays, pass_plays, def_excludes, off_excludes
from util import Config

# Import Google Sheets connector
try:
    from sheets_connector import LineupSheetsConnector
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False
    print("Warning: Google Sheets connector not available. Install requirements to enable sheets export.")


class GameplanGenerator:
    """Automated gameplan generator for MFN teams."""
    
    def __init__(self, min_play_threshold: float = 2.0, top_plays_limit: int = 30, sheets_id: str = None):
        """
        Initialize the gameplan generator.
        
        Args:
            min_play_threshold: Minimum percentage for a play to be considered significant
            top_plays_limit: Number of top defensive plays to recommend per category
            sheets_id: Google Sheets ID for export (optional, defaults to Config.GAMEPLAN_SHEET_ID)
        """
        self.min_play_threshold = min_play_threshold
        self.top_plays_limit = top_plays_limit
        
        # Store available plays for filtering recommendations
        self.available_defensive_plays = None
        self.available_offensive_plays = None
        
        # Use provided sheets_id or default from config
        if sheets_id:
            self.sheets_id = sheets_id
        else:
            # Import here to avoid circular imports
            from util import Config
            self.sheets_id = getattr(Config, 'GAMEPLAN_SHEET_ID', None)
        
        # Initialize Google Sheets connector if available and requested
        self.sheets_connector = None
        if SHEETS_AVAILABLE and self.sheets_id:
            try:
                self.sheets_connector = LineupSheetsConnector(verbose=True)
                print(f"✅ Google Sheets integration enabled for sheet: {self.sheets_id}")
            except Exception as e:
                print(f"❌ Failed to initialize Google Sheets connector: {e}")
                self.sheets_connector = None
        
        # Personnel group mappings (matching your existing format)
        self.personnel_map = {
            '1RB/1TE/3WR': '113',
            '1RB/2TE/2WR': '122', 
            '2RB/3WR': '203',
            '2RB/1TE/2WR': '212',
            '2RB/2TE/1WR': '221',
            '3RB/1TE/1WR': '311',
            '1RB/4WR': '104',
            '5WR': '105'
        }
        
        # Load only historical data that has required columns for proper analysis
        print("Loading historical data with proper format for analysis...")
        try:
            # Load only seasons that have the required columns for meaningful analysis
            required_columns = ['OffPersonnel', 'OffPlayType']
            historical_dfs = []
            loaded_combinations = []
            
            for league, years in Config.ls_dictionary.items():
                for year in years:
                    try:
                        df = Config.load_feather(league, year)
                        if df is not None and all(col in df.columns for col in required_columns):
                            historical_dfs.append(df)
                            loaded_combinations.append((league, year, len(df)))
                    except Exception as e:
                        continue
            
            if historical_dfs:
                all_historical = pd.concat(historical_dfs, ignore_index=True)
                print(f"📊 Loaded {len(all_historical):,} raw plays from {len(loaded_combinations)} league/season combinations")
                
                # Show which combinations we loaded
                for league, year, count in loaded_combinations[:5]:
                    print(f"  - {league} {year}: {count:,} plays")
                if len(loaded_combinations) > 5:
                    print(f"  ... and {len(loaded_combinations) - 5} more combinations")
                
                # Process through format_df to get all required columns
                try:
                    print(f"🔄 Processing through format_df...")
                    formatted_historical = format_df(all_historical)
                    print(f"✅ Successfully processed {len(formatted_historical):,} plays")
                except Exception as format_error:
                    print(f"⚠️  format_df failed ({format_error}), creating essential columns manually...")
                    formatted_historical = all_historical.copy()
                    
                    # Add essential columns that adj_ev needs
                    if 'YTGL' not in formatted_historical.columns:
                        # Calculate YTGL from Ball @ if available
                        if 'Ball @' in formatted_historical.columns:
                            # Calculate YTGL correctly based on format_df logic
                            # Ball @ format is "TEAM YardLine", extract yard line
                            ball_at_parts = formatted_historical['Ball @'].str.partition(' ')
                            yard_lines = pd.to_numeric(ball_at_parts[2], errors='coerce').fillna(50)
                            
                            # If HasBall team equals the team in Ball @, it's their side so use 100 - yard_line
                            # Otherwise use yard_line as-is (they're going toward the other team's goal)
                            formatted_historical['YTGL'] = yard_lines.copy()
                            if 'HasBall' in formatted_historical.columns:
                                same_team_mask = formatted_historical['HasBall'] == ball_at_parts[0]
                                formatted_historical.loc[same_team_mask, 'YTGL'] = 100 - formatted_historical.loc[same_team_mask, 'YTGL']
                        else:
                            formatted_historical['YTGL'] = 50
                    
                    # Add ytgl_bucket for expected value calculations (matches format_df logic)
                    if 'ytgl_bucket' not in formatted_historical.columns:
                        bucket_size = 10  # Same as in format_df
                        formatted_historical['ytgl_bucket'] = (
                            formatted_historical['YTGL'].floordiv(bucket_size) * bucket_size
                        ).astype(str)
                    
                    # Add expected value (simplified)
                    if 'ev' not in formatted_historical.columns:
                        # Simple expected value based on yards gained and field position
                        formatted_historical['ev'] = (
                            formatted_historical['YardsGained'] / 
                            (formatted_historical['YTGL'] / 50.0)
                        ).fillna(0)
                    
                    # Ensure other required columns exist
                    if 'YTG' not in formatted_historical.columns:
                        formatted_historical['YTG'] = 10  # Default yards to go
                    if 'Down' not in formatted_historical.columns:
                        formatted_historical['Down'] = 1  # Default to 1st down
                
                # Check for personnel data completeness and enhance if needed
                unknown_personnel = (formatted_historical['OffPersonnel'] == 'Unknown').sum()
                if unknown_personnel > 0:
                    print(f"⚠️  Historical data has {unknown_personnel:,} unknown personnel groupings")
                    print("🔄 Enhancing historical data with personnel mappings...")
                    formatted_historical = self._enhance_historical_with_personnel(formatted_historical)
                
                # Filter to reasonable data for analysis
                self.historical_data = formatted_historical[
                    (formatted_historical['OffensivePlay'].notna()) &
                    (formatted_historical['DefensivePlay'].notna()) &
                    (formatted_historical['HasBall'].notna())
                ].reset_index(drop=True)
                
                # Show summary of loaded data
                if 'League' in self.historical_data.columns and 'Season' in self.historical_data.columns:
                    leagues_seasons = self.historical_data.groupby(['League', 'Season']).size()
                    print(f"📊 Final dataset: {len(self.historical_data):,} plays from {len(leagues_seasons)} league/season combinations")
                    print("Top 5 league/season combinations:")
                    for (league, season), count in leagues_seasons.sort_values(ascending=False).head(5).items():
                        print(f"  - {league} {season}: {count:,} plays")
                else:
                    print(f"📊 Final dataset: {len(self.historical_data):,} plays")
                    
            else:
                print("Warning: No historical data found")
                self.historical_data = pd.DataFrame()
        except Exception as e:
            print(f"Warning: Could not load historical data: {e}")
            self.historical_data = pd.DataFrame()
    
    def _basic_format_df(self, df):
        """Basic formatting for data without the complex processing that causes issues."""
        # Make a copy to avoid pandas warnings
        df = df.copy()
        
        # For now, just ensure we have the basic columns we need and handle missing data
        required_columns = ['League', 'HasBall', 'OffensivePlay', 'DefensivePlay', 'YardsGained']
        
        # Check if all required columns exist
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"Warning: Missing columns in data: {missing_cols}")
            return pd.DataFrame()
        
        # Basic cleanup - remove null plays
        df = df.dropna(subset=['OffensivePlay', 'DefensivePlay', 'HasBall'])
        
        # Add any missing columns with defaults
        if 'Season' not in df.columns:
            # Extract season from League if it's in format like "USFL_2018"
            # or default to a reasonable value
            df['Season'] = 2018  # Default season
        if 'OffPlayType' not in df.columns:
            df['OffPlayType'] = 'Unknown'
        if 'OffPersonnel' not in df.columns:
            df['OffPersonnel'] = 'Unknown'
        if 'YTGL' not in df.columns:
            df['YTGL'] = 50  # Default field position
        if 'YTG' not in df.columns and 'YTG' in df.columns:
            pass  # Already exists
        elif 'YTG' not in df.columns:
            df['YTG'] = 10   # Default yards to go
        if 'Down' not in df.columns and 'Down' in df.columns:
            pass  # Already exists
        elif 'Down' not in df.columns:
            df['Down'] = 1   # Default down
        if 'ev' not in df.columns:
            df['ev'] = 0     # Default expected value
        if 'ytgl_bucket' not in df.columns:
            df['ytgl_bucket'] = '20-80'  # Default bucket
        if 'DefTeam' not in df.columns:
            # Create DefTeam column - it's the team that doesn't have the ball
            # This is a simplified approach
            df['DefTeam'] = 'Unknown'
        
        return df.reset_index(drop=True)
    
    def _enhance_historical_with_personnel(self, df):
        """Enhance historical data with personnel groupings from global reference files."""
        try:
            # Load global reference files for personnel mapping
            global_off_path = '/Users/jamesjones/personal/game_logs/MFN Global Reference - OffPlays.csv'
            global_off_ref = pd.read_csv(global_off_path)
            
            # Create a mapping of offensive plays to personnel
            play_to_personnel = dict(zip(global_off_ref['OffPlay'], global_off_ref['OffPersonnel']))
            
            # Update personnel for plays that have mappings
            enhanced_df = df.copy()
            for i, row in enhanced_df.iterrows():
                offensive_play = row.get('OffensivePlay')
                if offensive_play in play_to_personnel:
                    enhanced_df.at[i, 'OffPersonnel'] = play_to_personnel[offensive_play]
            
            # Report results
            before_count = (df['OffPersonnel'] == 'Unknown').sum()
            after_count = (enhanced_df['OffPersonnel'] == 'Unknown').sum()
            mapped_count = before_count - after_count
            print(f"✅ Enhanced {mapped_count} plays with personnel mappings")
            
            # Show personnel distribution
            personnel_counts = enhanced_df['OffPersonnel'].value_counts().head(5)
            print(f"📊 Top personnel groups: {dict(personnel_counts)}")
            
            return enhanced_df
            
        except Exception as e:
            print(f"⚠️  Warning: Could not enhance historical data with personnel: {e}")
            return df
    
    def load_available_plays(self):
        """
        Load available defensive and offensive plays based on playbook references.
        Reads playbook info from Info tab and filters using global reference files.
        """
        try:
            # First, try to get playbook info from the Info tab
            playbooks = self._get_playbook_info()
            if not playbooks:
                print("⚠️  No playbook info found - recommendations will not be filtered")
                return
                
            # Load the global reference files
            defensive_plays = self._load_plays_from_reference('defensive', playbooks.get('defense'))
            offensive_plays = self._load_plays_from_reference('offensive', playbooks.get('offense'))
            
            self.available_defensive_plays = defensive_plays
            self.available_offensive_plays = offensive_plays
            
            def_count = len(defensive_plays) if defensive_plays else 0
            off_count = len(offensive_plays) if offensive_plays else 0
            print(f"📋 Loaded {def_count} defensive plays and {off_count} offensive plays from playbook references")
            
        except Exception as e:
            print(f"⚠️  Error loading available plays: {e}")
    
    def _get_playbook_info(self):
        """Get playbook information from the Info tab."""
        if not SHEETS_AVAILABLE or not self.sheets_connector:
            return None
            
        try:
            sheet = self.sheets_connector.client.open_by_key(self.sheets_id)
            
            # Check if Info tab exists
            worksheets = [ws.title for ws in sheet.worksheets()]
            if 'Info' not in worksheets:
                print("⚠️  Info tab not found in spreadsheet")
                return None
                
            info_ws = sheet.worksheet('Info')
            
            # Get all data and look for playbook references
            data = info_ws.get_all_records()
            if not data:
                print("⚠️  Info tab is empty")
                return None
            
            playbooks = {}
            
            # Load the reference files to get valid playbook names
            import pandas as pd
            try:
                def_ref = pd.read_csv('/Users/jamesjones/projects/mfn/scouting/MFN Global Reference - DefPlays.csv')
                off_ref = pd.read_csv('/Users/jamesjones/projects/mfn/scouting/MFN Global Reference - OffPlays.csv')
                
                valid_def_playbooks = [col for col in def_ref.columns if col not in ['DefPlay', 'DefSecondary', 'DefLinebackers', 'DefFormation', 'DefPersonnel']]
                valid_off_playbooks = [col for col in off_ref.columns if col not in ['OffPlay', 'OffPlayType', 'OffFormation', 'OffPersonnel']]
            except:
                valid_def_playbooks = []
                valid_off_playbooks = []
            
            for row in data:
                # Look for defense and offense playbook columns (many variations)
                for key, value in row.items():
                    key_clean = str(key).strip()
                    value_clean = str(value).strip() if value else ''
                    key_lower = key_clean.lower()
                    
                    # Method 1: Check if VALUE matches a known playbook name
                    if value_clean:
                        if value_clean in valid_def_playbooks:
                            playbooks['defense'] = value_clean
                        elif value_clean in valid_off_playbooks:
                            playbooks['offense'] = value_clean
                        
                        # Also check traditional column name patterns with values
                        elif 'defense' in key_lower and 'playbook' in key_lower:
                            playbooks['defense'] = value_clean
                        elif 'offense' in key_lower and 'playbook' in key_lower:
                            playbooks['offense'] = value_clean
                    
                    # Method 2: Check if COLUMN NAME matches a known playbook (with non-empty value)
                    if value_clean and key_clean in valid_def_playbooks:
                        playbooks['defense'] = key_clean
                    elif value_clean and key_clean in valid_off_playbooks:
                        playbooks['offense'] = key_clean
            return playbooks if playbooks else None
            
        except Exception as e:
            print(f"⚠️  Could not read playbook info from Info tab: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _load_plays_from_reference(self, play_type, playbook_name):
        """Load available plays from global reference files."""
        if not playbook_name:
            return None
            
        try:
            # Determine which reference file to use
            if play_type == 'defensive':
                ref_file = '/Users/jamesjones/projects/mfn/scouting/MFN Global Reference - DefPlays.csv'
                play_column = 'DefPlay'
            else:
                ref_file = '/Users/jamesjones/projects/mfn/scouting/MFN Global Reference - OffPlays.csv'
                play_column = 'OffPlay'
            
            # Load the reference file
            import pandas as pd
            df = pd.read_csv(ref_file)
            
            # Check if the playbook column exists
            if playbook_name not in df.columns:
                print(f"⚠️  Playbook '{playbook_name}' not found in {play_type} reference file")
                print(f"Available playbooks: {[col for col in df.columns if col not in [play_column, 'OffPlayType', 'OffFormation', 'OffPersonnel', 'DefSecondary', 'DefLinebackers', 'DefFormation', 'DefPersonnel']]}")
                return None
            
            # Filter plays where the playbook has a 1
            available_plays = df[df[playbook_name] == 1][play_column].tolist()
            return available_plays
            
        except Exception as e:
            print(f"⚠️  Error loading {play_type} plays from reference: {e}")
            return None
    
    def filter_recommendations_by_available_plays(self, recommendations: Dict) -> Dict:
        """
        Filter defensive and offensive recommendations to only include available plays.
        
        Args:
            recommendations: Dictionary containing 'overall_defense', 'overall_offense', etc.
            
        Returns:
            Filtered recommendations dictionary
        """
        if not self.available_defensive_plays and not self.available_offensive_plays:
            return recommendations  # No filtering if no available plays loaded
            
        filtered = recommendations.copy()
        
        # Filter defensive recommendations
        if self.available_defensive_plays:
            for key in ['overall_defense', 'pass_defense', 'run_defense']:
                if key in filtered and filtered[key]:
                    original_count = len(filtered[key])
                    filtered[key] = [
                        play for play in filtered[key] 
                        if play.get('DefensivePlay') in self.available_defensive_plays
                    ]
                    filtered_count = len(filtered[key])
                    if filtered_count < original_count:
                        print(f"🎯 Filtered {key}: {original_count} → {filtered_count} (available plays only)")
        
        # Filter offensive recommendations  
        if self.available_offensive_plays:
            for key in ['overall_offense', 'pass_offense', 'run_offense']:
                if key in filtered and filtered[key]:
                    original_count = len(filtered[key])
                    filtered[key] = [
                        play for play in filtered[key] 
                        if play.get('OffensivePlay') in self.available_offensive_plays
                    ]
                    filtered_count = len(filtered[key])
                    if filtered_count < original_count:
                        print(f"🎯 Filtered {key}: {original_count} → {filtered_count} (available plays only)")
        
        return filtered
    
    def analyze_team_tendencies(self, league: str, season: int, team: str) -> Dict:
        """
        Analyze a team's offensive and defensive tendencies by formation/personnel.
        
        Args:
            league: League name (e.g., 'USFL')
            season: Season year
            team: Team acronym
            
        Returns:
            Dictionary with team tendencies by personnel group
        """
        # Load specific season data
        try:
            season_data = Config.load_feather(league, season)
            if season_data is None:
                raise ValueError(f"Could not find data for {league} {season}")
            
            # Use basic formatting instead of the complex format_df
            season_data = self._basic_format_df(season_data)
            if season_data.empty:
                raise ValueError(f"No valid data for {league} {season}")
                
        except Exception as e:
            raise ValueError(f"Could not load data for {league} {season}: {e}")
        
        # Filter for this team's offensive plays
        team_offense = season_data.loc[
            (season_data.HasBall == team) & 
            (season_data.League == league) &
            (~season_data.OffensivePlay.isin(off_excludes))
        ].copy()
        
        # For defensive plays, we need to identify games where this team was actually playing
        # First, get all Game IDs where this team had offensive plays
        team_games = team_offense['Game ID'].unique()
        
        # Filter for defensive plays: games where this team was playing, but they DON'T have the ball
        team_defense = season_data.loc[
            (season_data['Game ID'].isin(team_games)) &  # Only games this team played in
            (season_data.HasBall != team) &              # When they don't have the ball
            (season_data.HasBall.notna()) & 
            (season_data.League == league) &
            (~season_data.DefensivePlay.isin(def_excludes))
        ].copy()
        
        if len(team_offense) == 0:
            raise ValueError(f"No offensive plays found for {team} in {league} {season}")
        
        team_tendencies = {}
        
        # Analyze offensive tendencies by formation
        for personnel_group in team_offense.OffPersonnel.unique():
            if pd.isna(personnel_group):
                continue
                
            personnel_plays = team_offense[team_offense.OffPersonnel == personnel_group]
            
            # Calculate play percentages
            play_counts = personnel_plays.groupby('OffensivePlay').size()
            play_percentages = (play_counts / len(personnel_plays) * 100).sort_values(ascending=False)
            
            # Filter to only include top 75% of plays (most common plays only)
            cumulative_percentage = 0
            top_75_plays = []
            for play_name, percentage in play_percentages.items():
                # Always include the first play
                if len(top_75_plays) == 0:
                    top_75_plays.append(play_name)
                    cumulative_percentage += percentage
                # Include additional plays only if we haven't reached 75% yet
                elif cumulative_percentage < 75.0:
                    top_75_plays.append(play_name)
                    cumulative_percentage += percentage
                else:
                    break
            
            # Create filtered series with only top 75% plays
            top_75_percent = play_percentages[play_percentages.index.isin(top_75_plays)]
            
            # Also apply minimum threshold filter
            significant_plays = top_75_percent[top_75_percent >= self.min_play_threshold]
            
            if len(significant_plays) > 0:
                # Get play types for each play
                play_details = []
                for play_name in significant_plays.index:
                    play_data = personnel_plays[personnel_plays.OffensivePlay == play_name].iloc[0]
                    play_details.append({
                        'play': play_name,
                        'percentage': significant_plays[play_name],
                        'play_type': play_data.get('OffPlayType', 'Unknown'),
                        'count': play_counts[play_name]
                    })
                
                team_tendencies[personnel_group] = {
                    'total_plays': len(personnel_plays),
                    'offensive_plays': play_details
                }
        
        # Analyze defensive tendencies by formation (what defense they call vs each offensive formation)
        for personnel_group in team_defense.OffPersonnel.unique():
            if pd.isna(personnel_group):
                continue
                
            # Get defensive plays called against this offensive formation
            def_vs_formation = team_defense[team_defense.OffPersonnel == personnel_group]
            
            if len(def_vs_formation) == 0:
                continue
            
            # Calculate defensive play percentages
            def_play_counts = def_vs_formation.groupby('DefensivePlay').size()
            def_play_percentages = (def_play_counts / len(def_vs_formation) * 100).sort_values(ascending=False)
            
            # Filter to only include top 75% of defensive plays (most common defensive plays only)
            cumulative_def_percentage = 0
            top_75_def_plays = []
            for play_name, percentage in def_play_percentages.items():
                # Always include the first play
                if len(top_75_def_plays) == 0:
                    top_75_def_plays.append(play_name)
                    cumulative_def_percentage += percentage
                # Include additional plays only if we haven't reached 75% yet
                elif cumulative_def_percentage < 75.0:
                    top_75_def_plays.append(play_name)
                    cumulative_def_percentage += percentage
                else:
                    break
            
            # Create filtered series with only top 75% defensive plays
            top_75_percent_def = def_play_percentages[def_play_percentages.index.isin(top_75_def_plays)]
            
            # Also apply minimum threshold filter
            significant_def_plays = top_75_percent_def[top_75_percent_def >= self.min_play_threshold]
            
            if len(significant_def_plays) > 0:
                # Get defensive play details
                def_play_details = []
                for play_name in significant_def_plays.index:
                    def_play_details.append({
                        'play': play_name,
                        'percentage': significant_def_plays[play_name],
                        'count': def_play_counts[play_name]
                    })
                
                # Add defensive tendencies to existing formation data
                if personnel_group in team_tendencies:
                    team_tendencies[personnel_group]['defensive_plays'] = def_play_details
                    team_tendencies[personnel_group]['total_defensive_plays'] = len(def_vs_formation)
                else:
                    team_tendencies[personnel_group] = {
                        'total_plays': 0,
                        'offensive_plays': [],
                        'defensive_plays': def_play_details,
                        'total_defensive_plays': len(def_vs_formation)
                    }
        
        return team_tendencies
    
    def find_offensive_counter_plays(self, defensive_plays: List[str], personnel_group: str) -> Dict:
        """
        Find the best offensive plays to counter specific defensive plays.
        
        Args:
            defensive_plays: List of defensive play names
            personnel_group: Personnel group (e.g., '1RB/1TE/3WR')
            
        Returns:
            Dictionary with recommended offensive plays
        """
        # Filter historical data for these specific defensive plays
        counter_data = self.historical_data.loc[
            (self.historical_data.DefensivePlay.isin(defensive_plays)) &
            (~self.historical_data.OffensivePlay.isin(off_excludes)) &
            (self.historical_data.OffPersonnel == personnel_group)
        ].copy()
        
        if len(counter_data) == 0:
            return {'error': f'No historical data found for {personnel_group} vs defenses: {defensive_plays}'}
        
        # Analyze best offensive plays against these defenses
        # We want HIGH yards per play, ANY/A, etc. (opposite of defense analysis)
        results = {}
        
        # Separate pass and run plays for different analysis
        pass_data = counter_data[counter_data.OffPlayType.isin(pass_plays)]
        run_data = counter_data[counter_data.OffPlayType.isin(run_plays)]
        
        # Analyze best passing offense
        if len(pass_data) > 0:
            pass_offense = adj_ev(pass_data, 'OffensivePlay', pass_plays, 'desc')
            if not pass_offense.empty:
                # Filter to only effective offensive plays (YPP > 4)
                effective_pass_offense = pass_offense[pass_offense['ypp'] > 4.0]
                if not effective_pass_offense.empty:
                    # Sort by ANY/A (higher is better for offense)
                    pass_offense_sorted = effective_pass_offense.sort_values('any/a', ascending=False).head(self.top_plays_limit)
                    results['pass_offense'] = pass_offense_sorted.to_dict('records')
        
        # Analyze best running offense  
        if len(run_data) > 0:
            run_offense = adj_ev(run_data, 'OffensivePlay', run_plays, 'desc')
            if not run_offense.empty:
                # Filter to only effective offensive plays (YPP > 4)
                effective_run_offense = run_offense[run_offense['ypp'] > 4.0]
                if not effective_run_offense.empty:
                    # Sort by yards per play (higher is better for offense)
                    run_offense_sorted = effective_run_offense.sort_values('ypp', ascending=False).head(self.top_plays_limit)
                    results['run_offense'] = run_offense_sorted.to_dict('records')
        
        # Overall best offense against these defenses
        if len(counter_data) > 0:
            overall_offense = adj_ev(counter_data, 'OffensivePlay', all_plays, 'desc')
            if not overall_offense.empty:
                # Filter to only effective offensive plays (YPP > 4)
                effective_overall_offense = overall_offense[overall_offense['ypp'] > 4.0]
                if not effective_overall_offense.empty:
                    overall_offense_sorted = effective_overall_offense.sort_values('ypp', ascending=False).head(self.top_plays_limit)
                    results['overall_offense'] = overall_offense_sorted.to_dict('records')
        
        return results
    
    def find_counter_plays(self, offensive_plays: List[str], personnel_group: str) -> Dict:
        """
        Find the best defensive plays to counter specific offensive plays.
        
        Args:
            offensive_plays: List of offensive play names
            personnel_group: Personnel group (e.g., '1RB/1TE/3WR')
            
        Returns:
            Dictionary with recommended defensive plays
        """
        # Filter historical data for these specific offensive plays
        counter_data = self.historical_data.loc[
            (self.historical_data.OffensivePlay.isin(offensive_plays)) &
            (~self.historical_data.DefensivePlay.isin(def_excludes)) &
            (self.historical_data.OffPersonnel == personnel_group)
        ].copy()
        
        if len(counter_data) == 0:
            return {'error': f'No historical data found for {personnel_group} plays: {offensive_plays}'}
        
        # Separate pass and run plays for different analysis
        pass_data = counter_data[counter_data.OffPlayType.isin(pass_plays)]
        run_data = counter_data[counter_data.OffPlayType.isin(run_plays)]
        
        results = {}
        
        # Analyze pass defense
        if len(pass_data) > 0:
            pass_defense = adj_ev(pass_data, 'DefensivePlay', pass_plays, 'asc')
            if not pass_defense.empty:
                # Filter to only effective defensive plays (YPP < 6)
                effective_pass_defense = pass_defense[pass_defense['ypp'] < 6.0]
                if not effective_pass_defense.empty:
                    # Sort by ANY/A (lower is better for defense)
                    pass_defense_sorted = effective_pass_defense.sort_values('any/a').head(self.top_plays_limit)
                    results['pass_defense'] = pass_defense_sorted.to_dict('records')
        
        # Analyze run defense  
        if len(run_data) > 0:
            run_defense = adj_ev(run_data, 'DefensivePlay', run_plays, 'asc')
            if not run_defense.empty:
                # Filter to only effective defensive plays (YPP < 6)
                effective_run_defense = run_defense[run_defense['ypp'] < 6.0]
                if not effective_run_defense.empty:
                    # Sort by yards per play (lower is better for defense)
                    run_defense_sorted = effective_run_defense.sort_values('ypp').head(self.top_plays_limit)
                    results['run_defense'] = run_defense_sorted.to_dict('records')
        
        # Overall defense against all plays
        if len(counter_data) > 0:
            overall_defense = adj_ev(counter_data, 'DefensivePlay', all_plays, 'asc')
            if not overall_defense.empty:
                # Filter to only effective defensive plays (YPP < 6)
                effective_overall_defense = overall_defense[overall_defense['ypp'] < 6.0]
                if not effective_overall_defense.empty:
                    overall_defense_sorted = effective_overall_defense.sort_values('ypp').head(self.top_plays_limit)
                    results['overall_defense'] = overall_defense_sorted.to_dict('records')
        
        return results
    
    def generate_team_gameplan(self, league: str, season: int, team: str) -> Dict:
        """
        Generate a complete gameplan for defending against a specific team.
        
        Args:
            league: League name
            season: Season year  
            team: Team acronym
            
        Returns:
            Complete gameplan with defensive recommendations by formation
        """
        print(f"\nGenerating gameplan for {team} ({league} {season})")
        
        # Analyze team tendencies
        tendencies = self.analyze_team_tendencies(league, season, team)
        
        if not tendencies:
            return {'error': f'No significant offensive tendencies found for {team}'}
        
        # Load available plays for filtering recommendations
        self.load_available_plays()
        
        gameplan = {
            'team': team,
            'league': league, 
            'season': season,
            'formations': {}
        }
        
        # Generate defensive recommendations for each formation
        for personnel_group, tendency_data in tendencies.items():
            print(f"Analyzing {personnel_group}...")
            
            # Get list of plays this team runs from this formation
            offensive_plays = [play['play'] for play in tendency_data.get('offensive_plays', [])]
            defensive_plays = [play['play'] for play in tendency_data.get('defensive_plays', [])]
            
            # Find defensive counter plays (what defense to call vs their offense)
            try:
                defensive_counters = self.find_counter_plays(offensive_plays, personnel_group)
                # Filter by available plays
                defensive_counters = self.filter_recommendations_by_available_plays(defensive_counters)
            except Exception as e:
                print(f"Warning: Failed to find defensive counters for {personnel_group}: {e}")
                defensive_counters = {}
            
            # Find offensive counter plays (what offense to call vs their defense)
            offensive_counters = {}
            if defensive_plays:
                try:
                    offensive_counters = self.find_offensive_counter_plays(defensive_plays, personnel_group)
                    # Filter by available plays
                    offensive_counters = self.filter_recommendations_by_available_plays(offensive_counters)
                except Exception as e:
                    print(f"Warning: Failed to find offensive counters for {personnel_group}: {e}")
                    offensive_counters = {}
            
            # Map to short formation code
            formation_code = self.personnel_map.get(personnel_group, personnel_group)
            
            gameplan['formations'][formation_code] = {
                'personnel_group': personnel_group,
                'team_tendencies': tendency_data,
                'defensive_counters': defensive_counters,
                'offensive_counters': offensive_counters
            }
        
        return gameplan
    
    def generate_all_teams_gameplan(self, league: str, season: int) -> Dict:
        """
        Generate gameplans for all teams in a league/season.
        
        Args:
            league: League name
            season: Season year
            
        Returns:
            Dictionary with gameplans for all teams
        """
        print(f"\nGenerating gameplans for all teams in {league} {season}")
        
        # Load season data to find all teams
        file_name = f"{league}_{season}.feather"
        try:
            season_data = format_df(Config.load_specific_feather(file_name)).reset_index(drop=True)
        except:
            raise ValueError(f"Could not load data for {league} {season}")
        
        # Find all teams
        all_teams = season_data['HasBall'].dropna().unique()
        all_teams = [team for team in all_teams if team != '']  # Remove empty strings
        
        print(f"Found {len(all_teams)} teams: {', '.join(all_teams)}")
        
        all_gameplans = {}
        
        for team in all_teams:
            try:
                gameplan = self.generate_team_gameplan(league, season, team)
                if 'error' not in gameplan:
                    all_gameplans[team] = gameplan
                else:
                    print(f"Warning: {gameplan['error']}")
            except Exception as e:
                print(f"Error generating gameplan for {team}: {e}")
        
        return all_gameplans
    
    def export_gameplan(self, gameplan: Dict, output_file: str = None):
        """
        Export gameplan to a readable format.
        
        Args:
            gameplan: Gameplan dictionary
            output_file: Optional file path to save results
        """
        if isinstance(gameplan, dict) and 'team' in gameplan:
            # Single team gameplan
            self._export_single_gameplan(gameplan, output_file)
        else:
            # Multiple team gameplans
            self._export_all_gameplans(gameplan, output_file)
    
    def _export_single_gameplan(self, gameplan: Dict, output_file: str = None):
        """Export a single team's gameplan."""
        team = gameplan['team']
        league = gameplan['league']
        season = gameplan['season']
        
        output = []
        output.append(f"COMPLETE GAMEPLAN: {team} ({league} {season})")
        output.append("=" * 60)
        
        for formation_code, formation_data in gameplan['formations'].items():
            personnel = formation_data['personnel_group']
            tendencies = formation_data['team_tendencies']
            defensive_counters = formation_data['defensive_counters']
            offensive_counters = formation_data['offensive_counters']
            
            output.append(f"\n{formation_code} FORMATION ({personnel})")
            output.append("-" * 40)
            
            # Show team offensive tendencies
            if 'offensive_plays' in tendencies and tendencies['offensive_plays']:
                output.append(f"\n{team}'s Offensive Tendencies:")
                for play_info in tendencies['offensive_plays'][:10]:  # Top 10
                    output.append(f"  • {play_info['play']:40} {play_info['percentage']:5.1f}% ({play_info['count']} plays)")
            
            # Show team defensive tendencies
            if 'defensive_plays' in tendencies and tendencies['defensive_plays']:
                output.append(f"\n{team}'s Defensive Tendencies vs {personnel}:")
                for play_info in tendencies['defensive_plays'][:10]:  # Top 10
                    output.append(f"  • {play_info['play']:40} {play_info['percentage']:5.1f}% ({play_info['count']} plays)")
            
            # Show defensive recommendations (what defense to call vs their offense)
            if 'pass_defense' in defensive_counters:
                limit = min(self.top_plays_limit, len(defensive_counters['pass_defense']))
                output.append(f"\nBest Pass Defense vs Their Offense (Top {limit}):")
                for i, play in enumerate(defensive_counters['pass_defense'][:limit], 1):
                    metrics = f"ANY/A: {play.get('any/a', 0):5.2f} | YPP: {play.get('ypp', 0):5.2f} | EV: {play.get('ev_adj', 0):5.3f} | Cnt: {play.get('cnt', 0)}"
                    output.append(f"  {i:2}. {play['DefensivePlay']:35} {metrics}")
            
            if 'run_defense' in defensive_counters:
                limit = min(self.top_plays_limit, len(defensive_counters['run_defense']))
                output.append(f"\nBest Run Defense vs Their Offense (Top {limit}):")
                for i, play in enumerate(defensive_counters['run_defense'][:limit], 1):
                    metrics = f"YPP: {play.get('ypp', 0):5.2f} | EV: {play.get('ev_adj', 0):5.3f} | Cnt: {play.get('cnt', 0)}"
                    output.append(f"  {i:2}. {play['DefensivePlay']:35} {metrics}")
            
            if 'overall_defense' in defensive_counters:
                limit = min(self.top_plays_limit, len(defensive_counters['overall_defense']))
                output.append(f"\nBest Overall Defense vs Their Offense (Top {limit}):")
                for i, play in enumerate(defensive_counters['overall_defense'][:limit], 1):
                    metrics = f"YPP: {play.get('ypp', 0):5.2f} | EV: {play.get('ev_adj', 0):5.3f} | Cnt: {play.get('cnt', 0)}"
                    output.append(f"  {i:2}. {play['DefensivePlay']:35} {metrics}")
            
            # Show offensive recommendations (what offense to call vs their defense)
            if offensive_counters and 'pass_offense' in offensive_counters:
                limit = min(self.top_plays_limit, len(offensive_counters['pass_offense']))
                output.append(f"\nBest Pass Offense vs Their Defense (Top {limit}):")
                for i, play in enumerate(offensive_counters['pass_offense'][:limit], 1):
                    metrics = f"ANY/A: {play.get('any/a', 0):5.2f} | YPP: {play.get('ypp', 0):5.2f} | EV: {play.get('ev_adj', 0):5.3f} | Cnt: {play.get('cnt', 0)}"
                    output.append(f"  {i:2}. {play['OffensivePlay']:35} {metrics}")
            
            if offensive_counters and 'run_offense' in offensive_counters:
                limit = min(self.top_plays_limit, len(offensive_counters['run_offense']))
                output.append(f"\nBest Run Offense vs Their Defense (Top {limit}):")
                for i, play in enumerate(offensive_counters['run_offense'][:limit], 1):
                    metrics = f"YPP: {play.get('ypp', 0):5.2f} | EV: {play.get('ev_adj', 0):5.3f} | Cnt: {play.get('cnt', 0)}"
                    output.append(f"  {i:2}. {play['OffensivePlay']:35} {metrics}")
            
            if offensive_counters and 'overall_offense' in offensive_counters:
                limit = min(self.top_plays_limit, len(offensive_counters['overall_offense']))
                output.append(f"\nBest Overall Offense vs Their Defense (Top {limit}):")
                for i, play in enumerate(offensive_counters['overall_offense'][:limit], 1):
                    metrics = f"YPP: {play.get('ypp', 0):5.2f} | EV: {play.get('ev_adj', 0):5.3f} | Cnt: {play.get('cnt', 0)}"
                    output.append(f"  {i:2}. {play['OffensivePlay']:35} {metrics}")
            
            output.append("")
        
        # Add summary table combining all offensive plays from all formations, sorted by YPP
        all_offensive_plays = []
        for formation_code, formation_data in gameplan['formations'].items():
            offensive_counters = formation_data.get('offensive_counters', {})
            if 'overall_offense' in offensive_counters:
                for play in offensive_counters['overall_offense']:
                    play_with_personnel = play.copy()
                    play_with_personnel['Personnel'] = formation_data.get('personnel_group', formation_code)
                    all_offensive_plays.append(play_with_personnel)
        
        if all_offensive_plays:
            # Sort all plays by YPP (descending)
            all_offensive_plays_sorted = sorted(all_offensive_plays, 
                                              key=lambda x: x.get('ypp', 0), 
                                              reverse=True)
            
            output.append("\nALL OFFENSIVE PLAYS SUMMARY (Sorted by YPP)")
            output.append("=" * 80)
            
            for i, play in enumerate(all_offensive_plays_sorted[:30], 1):  # Top 30
                personnel = play.get('Personnel', 'N/A')
                metrics = f"YPP: {play.get('ypp', 0):5.2f} | ANY/A: {play.get('any/a', 0):5.2f} | EV: {play.get('ev_adj', 0):5.3f} | Cnt: {play.get('cnt', 0)}"
                output.append(f"  {i:2}. {play['OffensivePlay']:35} [{personnel}] {metrics}")
        
        result = "\n".join(output)
        print(result)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(result)
            print(f"\nGameplan saved to: {output_file}")
        
        # Export to Google Sheets if configured
        if self.sheets_connector and self.sheets_id:
            self.export_to_google_sheets(gameplan)
    
    def _export_all_gameplans(self, all_gameplans: Dict, output_file: str = None):
        """Export all teams' gameplans."""
        output = []
        output.append("ALL TEAMS DEFENSIVE GAMEPLANS")
        output.append("=" * 60)
        
        for team, gameplan in all_gameplans.items():
            output.append(f"\n\n{team} GAMEPLAN:")
            output.append("-" * 30)
            
            for formation_code, formation_data in gameplan['formations'].items():
                output.append(f"\n{formation_code} ({formation_data['personnel_group']}):")
                
                # Top 5 offensive plays they run
                team_tendencies = formation_data['team_tendencies']
                if 'offensive_plays' in team_tendencies and team_tendencies['offensive_plays']:
                    offensive_tendencies = team_tendencies['offensive_plays'][:5]
                    output.append(f"  Offense:")
                    for play_info in offensive_tendencies:
                        output.append(f"    • {play_info['play']} ({play_info['percentage']:.1f}%)")
                
                # Top 5 defensive plays they call
                if 'defensive_plays' in team_tendencies and team_tendencies['defensive_plays']:
                    defensive_tendencies = team_tendencies['defensive_plays'][:5]
                    output.append(f"  Defense:")
                    for play_info in defensive_tendencies:
                        output.append(f"    • {play_info['play']} ({play_info['percentage']:.1f}%)")
                
                # Top 5 defensive counters
                if 'overall_defense' in formation_data.get('defensive_counters', {}):
                    def_counters = formation_data['defensive_counters']['overall_defense'][:5]
                    output.append(f"  Best Defense vs Their Offense:")
                    for play in def_counters:
                        output.append(f"    • {play['DefensivePlay']}")
                
                # Top 5 offensive counters
                if 'overall_offense' in formation_data.get('offensive_counters', {}):
                    off_counters = formation_data['offensive_counters']['overall_offense'][:5]
                    output.append(f"  Best Offense vs Their Defense:")
                    for play in off_counters:
                        output.append(f"    • {play['OffensivePlay']}")
        
        result = "\n".join(output)
        print(result)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(result)
            print(f"\nAll gameplans saved to: {output_file}")
    
    def export_to_google_sheets(self, gameplan: Dict):
        """
        Export gameplan data to Google Sheets in structured format.
        """
        try:
            team = gameplan['team']
            league = gameplan['league'] 
            season = gameplan['season']
            
            print(f"\n📊 Exporting {team} gameplan to Google Sheets...")
            
            # Get the spreadsheet
            spreadsheet = self.sheets_connector.get_sheet(self.sheets_id)
            
            # Create or clear the team's worksheet
            tab_name = f"{team}_{league}_{season}"
            try:
                existing_worksheet = spreadsheet.worksheet(tab_name)
                spreadsheet.del_worksheet(existing_worksheet)
                print(f"🗑️ Deleted existing '{tab_name}' tab")
            except:
                pass  # Worksheet doesn't exist
            
            # Create new worksheet with sufficient size
            worksheet = spreadsheet.add_worksheet(title=tab_name, rows=1000, cols=20)
            
            # Prepare data for export
            export_data = []
            
            # Header
            export_data.append([f"COMPLETE GAMEPLAN: {team} ({league} {season})", "", "", "", "", "", "", "", ""])
            export_data.append(["", "", "", "", "", "", "", "", ""])
            
            # Process each formation
            for formation_code, formation_data in gameplan['formations'].items():
                personnel = formation_data['personnel_group']
                tendencies = formation_data['team_tendencies']
                defensive_counters = formation_data['defensive_counters']
                offensive_counters = formation_data['offensive_counters']
                
                # Formation header
                export_data.append([f"{formation_code} FORMATION ({personnel})", "", "", "", "", "", "", "", ""])
                export_data.append(["", "", "", "", "", "", "", "", ""])
                
                # Team offensive tendencies
                if 'offensive_plays' in tendencies and tendencies['offensive_plays']:
                    export_data.append([f"{team}'s Offensive Tendencies:", "", "", "", "", "", "", "", ""])
                    export_data.append(["Play", "Percentage", "Count", "Play Type", "", "", "", "", ""])
                    for play_info in tendencies['offensive_plays'][:15]:
                        export_data.append([
                            play_info['play'],
                            f"{play_info['percentage']:.1f}%",
                            int(play_info['count']),
                            play_info.get('play_type', ''),
                            "", "", "", "", ""
                        ])
                    export_data.append(["", "", "", "", "", "", "", "", ""])
                
                # Team defensive tendencies
                if 'defensive_plays' in tendencies and tendencies['defensive_plays']:
                    export_data.append([f"{team}'s Defensive Tendencies vs {personnel}:", "", "", "", "", "", "", "", ""])
                    export_data.append(["Play", "Percentage", "Count", "", "", "", "", "", ""])
                    for play_info in tendencies['defensive_plays'][:15]:
                        export_data.append([
                            play_info['play'],
                            f"{play_info['percentage']:.1f}%",
                            int(play_info['count']),
                            "", "", "", "", "", ""
                        ])
                    export_data.append(["", "", "", "", "", "", "", "", ""])
                
                # Defensive recommendations
                if 'overall_defense' in defensive_counters:
                    export_data.append(["Best Defense vs Their Offense:", "", "", "", "", "", "", "", ""])
                    export_data.append(["Rank", "Defensive Play", "YPP", "EV_Adj", "Count", "ANY/A", "INT Rate", "Sack Rate", "TD Rate"])
                    for i, play in enumerate(defensive_counters['overall_defense'][:self.top_plays_limit], 1):
                        # Debug: print what columns we have
                        if i == 1:
                            print(f"Debug: Defensive play columns: {play.keys()}")
                        # Handle potential inf/NaN values
                        def safe_float(val, default=0):
                            try:
                                if val is None or val == '' or str(val).lower() in ['nan', 'inf', '-inf']:
                                    return default
                                val = float(val)
                                if val != val or val == float('inf') or val == float('-inf'):  # Check for NaN or inf
                                    return default
                                return round(val, 3)
                            except:
                                return default
                        
                        export_data.append([
                            int(i),
                            str(play['DefensivePlay']),
                            safe_float(play.get('ypp', 0)),
                            safe_float(play.get('ev_adj', 0)),
                            int(play.get('cnt', 0)),
                            safe_float(play.get('any/a', 0)),
                            safe_float(play.get('int_rate', 0)),
                            safe_float(play.get('sack_rate', 0)),
                            safe_float(play.get('td_rate', 0))
                        ])
                    export_data.append(["", "", "", "", "", "", "", "", ""])
                
                # Offensive recommendations
                if offensive_counters and 'overall_offense' in offensive_counters:
                    export_data.append(["Best Offense vs Their Defense:", "", "", "", "", "", "", "", ""])
                    export_data.append(["Rank", "Offensive Play", "YPP", "EV_Adj", "Count", "ANY/A", "INT Rate", "Sack Rate", "TD Rate"])
                    for i, play in enumerate(offensive_counters['overall_offense'][:self.top_plays_limit], 1):
                        # Handle potential inf/NaN values
                        def safe_float(val, default=0):
                            try:
                                if val is None or val == '' or str(val).lower() in ['nan', 'inf', '-inf']:
                                    return default
                                val = float(val)
                                if val != val or val == float('inf') or val == float('-inf'):  # Check for NaN or inf
                                    return default
                                return round(val, 3)
                            except:
                                return default
                        
                        export_data.append([
                            int(i),
                            str(play['OffensivePlay']),
                            safe_float(play.get('ypp', 0)),
                            safe_float(play.get('ev_adj', 0)),
                            int(play.get('cnt', 0)),
                            safe_float(play.get('any/a', 0)),
                            safe_float(play.get('int_rate', 0)),
                            safe_float(play.get('sack_rate', 0)),
                            safe_float(play.get('td_rate', 0))
                        ])
                    export_data.append(["", "", "", "", "", "", "", "", ""])
                
                export_data.append(["", "", "", "", "", "", "", "", ""])
            
            # Add summary section with all offensive plays sorted by YPP
            all_offensive_plays = []
            for formation_code, formation_data in gameplan['formations'].items():
                offensive_counters = formation_data.get('offensive_counters', {})
                if 'overall_offense' in offensive_counters:
                    for play in offensive_counters['overall_offense']:
                        play_with_personnel = play.copy()
                        play_with_personnel['Personnel'] = formation_data.get('personnel_group', formation_code)
                        all_offensive_plays.append(play_with_personnel)
            
            if all_offensive_plays:
                # Sort all plays by YPP (descending)
                all_offensive_plays_sorted = sorted(all_offensive_plays, 
                                                  key=lambda x: x.get('ypp', 0), 
                                                  reverse=True)
                
                export_data.append(["ALL OFFENSIVE PLAYS SUMMARY (Sorted by YPP)", "", "", "", "", "", "", "", ""])
                export_data.append(["", "", "", "", "", "", "", "", ""])
                export_data.append(["Rank", "Offensive Play", "Personnel", "YPP", "ANY/A", "EV_Adj", "Count", "INT Rate", "Sack Rate"])
                
                for i, play in enumerate(all_offensive_plays_sorted[:30], 1):  # Top 30
                    def safe_float(val, default=0):
                        try:
                            if val is None or val == '' or str(val).lower() in ['nan', 'inf', '-inf']:
                                return default
                            val = float(val)
                            if val != val or val == float('inf') or val == float('-inf'):
                                return default
                            return round(val, 3)
                        except:
                            return default
                    
                    export_data.append([
                        int(i),
                        str(play['OffensivePlay']),
                        str(play.get('Personnel', 'N/A')),
                        safe_float(play.get('ypp', 0)),
                        safe_float(play.get('any/a', 0)),
                        safe_float(play.get('ev_adj', 0)),
                        int(play.get('cnt', 0)),
                        safe_float(play.get('int_rate', 0)),
                        safe_float(play.get('sack_rate', 0))
                    ])
                export_data.append(["", "", "", "", "", "", "", "", ""])
            
            # Upload to Google Sheets
            if export_data:
                print(f"📝 Writing {len(export_data)} rows to Google Sheets...")
                try:
                    worksheet.update('A1', export_data)
                    print(f"✅ Data written successfully")
                except Exception as e:
                    print(f"❌ Error writing data: {e}")
                    raise
                
                # Format headers
                header_format = {
                    "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 1.0},
                    "textFormat": {"bold": True}
                }
                
                # Find and format formation headers
                for i, row in enumerate(export_data, 1):
                    if row[0] and 'FORMATION' in str(row[0]):
                        worksheet.format(f'A{i}:I{i}', header_format)
                    elif row[0] and ('Tendencies' in str(row[0]) or 'Best' in str(row[0])):
                        worksheet.format(f'A{i}:I{i}', header_format)
                
                # Auto-resize columns to fit content using gspread batch update
                print("📏 Auto-resizing columns to fit content...")
                try:
                    # Use gspread's batch_update method for auto-resize
                    auto_resize_request = {
                        'requests': [
                            {
                                'autoResizeDimensions': {
                                    'dimensions': {
                                        'sheetId': worksheet.id,
                                        'dimension': 'COLUMNS',
                                        'startIndex': 0,  # Column A (0-indexed)
                                        'endIndex': 9     # Column I (0-indexed, exclusive end)
                                    }
                                }
                            }
                        ]
                    }
                    
                    # Execute using gspread's batch_update method
                    spreadsheet.batch_update(auto_resize_request)
                    print("✅ Columns auto-resized successfully")
                    
                except Exception as resize_error:
                    print(f"⚠️  Warning: Could not auto-resize columns: {resize_error}")
                    print(f"   You can manually resize columns in Google Sheets by selecting all and double-clicking column borders")
                
                print(f"✅ Successfully exported {team} gameplan to Google Sheets tab: '{tab_name}'")
            
        except Exception as e:
            print(f"❌ Failed to export to Google Sheets: {e}")
            import traceback
            print("Full error details:")
            traceback.print_exc()


def main():
    """Main function to run the gameplan generator."""
    parser = argparse.ArgumentParser(description='Generate automated MFN defensive gameplans')
    parser.add_argument('--league', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--season', required=True, type=int, help='Season year')
    parser.add_argument('--team', help='Specific team to scout (e.g., SJS)')
    parser.add_argument('--all-teams', action='store_true', help='Generate gameplans for all teams')
    parser.add_argument('--save-txt', action='store_true', help='Save gameplan as txt file in gameplans/ directory')
    parser.add_argument('--output', help='Custom output file path (only used with --save-txt)')
    parser.add_argument('--threshold', type=float, default=2.0, help='Minimum play percentage threshold')
    parser.add_argument('--top-plays', type=int, default=30, help='Number of top plays to recommend')
    parser.add_argument('--sheets-id', help='Google Sheets ID for export (optional, defaults to Config.GAMEPLAN_SHEET_ID)')
    
    args = parser.parse_args()
    
    if not args.team and not args.all_teams:
        print("Error: Must specify either --team or --all-teams")
        return
    
    # Initialize generator
    generator = GameplanGenerator(
        min_play_threshold=args.threshold,
        top_plays_limit=args.top_plays,
        sheets_id=args.sheets_id
    )
    
    try:
        if args.all_teams:
            # Generate for all teams
            gameplans = generator.generate_all_teams_gameplan(args.league, args.season)
            
            # Only create txt file if --save-txt flag is used
            if args.save_txt:
                # Create gameplans directory if it doesn't exist
                gameplans_dir = Path("gameplans")
                gameplans_dir.mkdir(exist_ok=True)
                
                # Set output file path
                if args.output:
                    output_file = args.output
                else:
                    output_file = gameplans_dir / f"gameplans_{args.league}_{args.season}_all_teams.txt"
                
                generator.export_gameplan(gameplans, output_file)
            else:
                # Just export to Google Sheets without creating txt file
                generator.export_gameplan(gameplans, None)
        else:
            # Generate for specific team
            gameplan = generator.generate_team_gameplan(args.league, args.season, args.team)
            
            # Only create txt file if --save-txt flag is used
            if args.save_txt:
                # Create gameplans directory if it doesn't exist
                gameplans_dir = Path("gameplans")
                gameplans_dir.mkdir(exist_ok=True)
                
                # Set output file path
                if args.output:
                    output_file = args.output
                else:
                    output_file = gameplans_dir / f"gameplan_{args.league}_{args.season}_{args.team}.txt"
                
                generator.export_gameplan(gameplan, output_file)
            else:
                # Just export to Google Sheets without creating txt file
                generator.export_gameplan(gameplan, None)
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()