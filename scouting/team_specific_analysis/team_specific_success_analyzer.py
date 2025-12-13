#!/usr/bin/env python3
"""
Team-Specific Success Analyzer
=============================

Directly analyzes what offensive and defensive plays have been most successful 
against a specific opponent. Simple, actionable scouting.

Usage:
    python team_specific_success_analyzer.py --opponent MIC --league USFL --season 2018
    python team_specific_success_analyzer.py --opponent MIC --league USFL --season 2018 --min-attempts 3
"""

import sys
import argparse
from pathlib import Path

# Check for required packages
def check_dependencies():
    """Check if required packages are installed and auto-install if missing."""
    missing_packages = []
    
    try:
        import pandas as pd
    except ImportError:
        missing_packages.append('pandas>=1.3.0')
    
    try:
        import numpy as np
    except ImportError:
        missing_packages.append('numpy>=1.20.0')
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   • {pkg}")
        
        # Auto-install missing packages
        import subprocess
        requirements_file = Path(__file__).parent.parent / "requirements.txt"
        
        if requirements_file.exists():
            print(f"\n🔧 Auto-installing dependencies from requirements.txt...")
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ], check=True, capture_output=True, text=True)
                print("✅ Dependencies installed successfully!")
                
                # Verify installation worked
                try:
                    import pandas as pd
                    import numpy as np
                    print("✅ Packages verified - ready to run!")
                    return True
                except ImportError as e:
                    print(f"❌ Installation verification failed: {e}")
                    if "numpy source directory" in str(e):
                        print("💡 This is likely a path conflict issue.")
                        print("   Try running the script from a different directory:")
                        print("   cd /Users/jamesjones/projects/mfn/scouting")
                        print("   python3 team_specific_analysis/team_specific_success_analyzer.py --opponent CHI --league USFL --season 2018")
                    return False
                    
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to auto-install dependencies: {e}")
                print(f"📝 Manual installation required:")
                print(f"   pip3 install -r {requirements_file}")
                return False
        else:
            print(f"\n💡 Manual installation required:")
            print(f"   pip3 install {' '.join(missing_packages)}")
            return False
    
    return True

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.append('/Users/jamesjones/projects/mfn/lineup_analyzer')

if not check_dependencies():
    sys.exit(1)

import pandas as pd
import numpy as np
from util import Config

# Try to import Google Sheets connector
try:
    from sheets_connector import LineupSheetsConnector
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False
    print("⚠️  Google Sheets connector not available.")

class TeamSuccessAnalyzer:
    """Analyzes what plays work best against a specific team."""
    
    def __init__(self, league: str, season: int, opponent: str, min_attempts: int = 1):
        self.league = league
        self.season = season
        self.opponent = opponent
        self.min_attempts = min_attempts
        self.df = None
        self.sheets_connector = None
        self.playbook_plays = []
        self.load_data()
        
        # Initialize Google Sheets if available
        if SHEETS_AVAILABLE:
            try:
                self.sheets_connector = LineupSheetsConnector(verbose=False)
                self.load_playbook()
            except Exception as e:
                print(f"⚠️  Could not initialize Google Sheets: {e}")
    
    def load_data(self):
        """Load season data."""
        try:
            self.df = Config.load_feather(self.league, self.season)
            if self.df is None or self.df.empty:
                raise ValueError(f"No data found for {self.league} {self.season}")
            print(f"✅ Loaded {len(self.df)} plays from {self.league} {self.season}")
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")
    
    def load_playbook(self):
        """Load playbook from Google Sheets."""
        if not SHEETS_AVAILABLE or self.sheets_connector is None:
            print("❌ Cannot load playbook - Google Sheets not available")
            return
        
        try:
            # Use the same sheet ID as gameplan generator
            sheet_id = Config.GAMEPLAN_SHEET_ID
            spreadsheet = self.sheets_connector.get_sheet(sheet_id)
            
            # Try to find standard playbook
            try:
                playbook_worksheet = spreadsheet.worksheet('standard_playbook')
                playbook_data = playbook_worksheet.get_all_values()
                
                if playbook_data:
                    # Find header row
                    header_row = None
                    for i, row in enumerate(playbook_data):
                        if 'Play Name' in row:
                            header_row = i
                            break
                    
                    if header_row is not None:
                        headers = playbook_data[header_row]
                        play_col_idx = headers.index('Play Name')
                        
                        for row in playbook_data[header_row + 1:]:
                            if len(row) > play_col_idx and row[play_col_idx].strip():
                                play_name = row[play_col_idx].strip()
                                # Remove numbering if present
                                if '. ' in play_name:
                                    play_name = play_name.split('. ', 1)[1]
                                self.playbook_plays.append(play_name)
                        
                        print(f"📋 Loaded {len(self.playbook_plays)} plays from standard_playbook")
                    else:
                        print("❌ Could not find 'Play Name' header in standard_playbook")
                else:
                    print("❌ No data found in standard_playbook tab")
            
            except Exception as e:
                print(f"❌ Could not load standard_playbook: {e}")
                worksheets = spreadsheet.worksheets()
                print("💡 Available tabs:", [ws.title for ws in worksheets])
                
        except Exception as e:
            print(f"❌ Error loading playbook: {e}")
    
    def load_csv_playbooks(self):
        """Load playbook assignments from MFN Global Reference CSV file."""
        
        csv_path = Path(__file__).parent.parent / "MFN Global Reference - OffPlays.csv"
        
        if not csv_path.exists():
            print(f"❌ MFN Global Reference CSV not found: {csv_path}")
            return {}
        
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            
            # Map CSV column names to readable playbook names
            playbook_columns = {
                'GenBal': 'Generally Balanced',
                'PassFoc': 'Pass Focused', 
                'RunFoc': 'Run Focused',
                'PossOff': 'Possession',
                'WestCoast': 'West Coast'
            }
            
            playbooks = {}
            
            for col, playbook_name in playbook_columns.items():
                if col in df.columns:
                    # Get plays where this playbook column = 1
                    playbook_plays = df[df[col] == 1]['OffPlay'].tolist()
                    playbooks[playbook_name] = playbook_plays
                    print(f"📋 {playbook_name}: {len(playbook_plays)} plays")
            
            print(f"✅ Loaded {len(playbooks)} playbooks from CSV")
            return playbooks
            
        except Exception as e:
            print(f"❌ Error loading CSV playbooks: {e}")
            return {}
    
    def analyze_offensive_success_vs_opponent(self):
        """Find the most successful offensive plays against the opponent (playbook-aware)."""
        
        print(f"\n🎯 PLAYBOOK ANALYSIS vs {self.opponent}")
        print("=" * 50)
        
        if not self.playbook_plays:
            print("❌ No playbook loaded - showing ALL plays instead")
            return self._analyze_all_offensive_plays()
        
        # Find games involving opponent
        opponent_games = self.df.groupby('Game ID')['HasBall'].unique()
        games_with_opponent = [game_id for game_id, teams in opponent_games.items() 
                              if self.opponent in teams]
        
        # Filter for plays against opponent's defense
        vs_opponent_defense = self.df[
            (self.df['Game ID'].isin(games_with_opponent)) &
            (self.df['HasBall'] != self.opponent) &
            (self.df['HasBall'].notna()) &
            (self.df['OffensivePlay'].notna()) &
            (~self.df['OffensivePlay'].isin(['Field Goal', 'Punt', 'Victory', 'Kickoff']))
        ].copy()
        
        # Filter by playbook plays only
        playbook_data = vs_opponent_defense[
            vs_opponent_defense['OffensivePlay'].isin(self.playbook_plays)
        ].copy()
        
        print(f"📊 Found {len(vs_opponent_defense)} total plays vs {self.opponent}")
        print(f"📋 Found {len(playbook_data)} playbook plays vs {self.opponent}")
        
        if playbook_data.empty:
            print("❌ No playbook plays found against opponent")
            return {}
        
        # Calculate effectiveness metrics for each play
        effectiveness = {}
        
        for play in playbook_data['OffensivePlay'].unique():
            play_data = playbook_data[playbook_data['OffensivePlay'] == play]
            
            if len(play_data) < self.min_attempts:
                continue
            
            attempts = len(play_data)
            avg_yards = play_data['YardsGained'].mean()
            total_yards = play_data['YardsGained'].sum()
            
            # Calculate ANY/A components
            touchdowns = len(play_data[play_data['Text'].str.contains('TOUCHDOWN', na=False)]) if 'Text' in play_data.columns else 0
            interceptions = len(play_data[play_data['Text'].str.contains('INTERCEPTED', na=False)]) if 'Text' in play_data.columns else 0
            sacks = len(play_data[play_data['Text'].str.contains('sacked', na=False)]) if 'Text' in play_data.columns else 0
            sack_yards = abs(play_data[play_data['Text'].str.contains('sacked', na=False)]['YardsGained'].sum()) if 'Text' in play_data.columns else 0
            
            # ANY/A calculation: (yards + 20*TD - 60*INT - sack_yards) / attempts
            any_a = (total_yards + 20*touchdowns - 60*interceptions - sack_yards) / attempts
            
            # Success rate (4+ yards for runs, 6+ for passes)
            play_type = play_data['OffPlayType'].iloc[0] if 'OffPlayType' in play_data.columns else 'Unknown'
            success_threshold = 4.0 if play_type in ['Inside Run', 'Outside Run'] else 6.0
            successful = len(play_data[play_data['YardsGained'] >= success_threshold])
            success_rate = (successful / attempts) * 100
            
            # Completion rate estimate (for passes)
            completion_rate = 0.0
            if play_type in ['Short Pass', 'Medium Pass', 'Long Pass']:
                # Estimate: assume 0 yards = incomplete pass (rough approximation)
                completed = len(play_data[play_data['YardsGained'] != 0])
                completion_rate = (completed / attempts) * 100
            
            effectiveness[play] = {
                'cnt': attempts,
                'ypp': round(avg_yards, 2),
                'any_a': round(any_a, 2),
                'success_rate': round(success_rate, 1),
                'completion_rate': round(completion_rate, 1),
                'td_rate': round((touchdowns / attempts) * 100, 1),
                'int_rate': round((interceptions / attempts) * 100, 1),
                'sack_rate': round((sacks / attempts) * 100, 1),
                'OffPlayType': play_type,
                'OffPersonnel': play_data['OffPersonnel'].mode().iloc[0] if 'OffPersonnel' in play_data.columns and not play_data['OffPersonnel'].empty else 'Unknown'
            }
        
        # Convert to DataFrame and sort by any/a
        effectiveness_df = pd.DataFrame.from_dict(effectiveness, orient='index')
        
        if effectiveness_df.empty:
            print("❌ No playbook plays with sufficient attempts found")
            return {}
        
        effectiveness_sorted = effectiveness_df.sort_values('any_a', ascending=False)
        
        # Output results
        print(f"\n📊 OFFENSIVE RECOMMENDATIONS vs {self.opponent} (ALL PLAYBOOK PLAYS)")
        print(f"{'Rank':<4} {'Play':<45} {'Cnt':<4} {'YPP':<5} {'ANY/A':<6} {'SR%':<5} {'Comp%':<5} {'TD%':<5}")
        print("-" * 100)
        
        for rank, (play, stats) in enumerate(effectiveness_sorted.iterrows(), 1):
            play_short = play[:42] + "..." if len(play) > 45 else play
            comp_str = f"{stats['completion_rate']:<5}" if stats['OffPlayType'] in ['Short Pass', 'Medium Pass', 'Long Pass'] else "N/A  "
            print(f"{rank:<4} {play_short:<45} {stats['cnt']:<4} {stats['ypp']:<5} {stats['any_a']:<6} {stats['success_rate']:<5} {comp_str} {stats['td_rate']:<5}")
        
        # Separate by play type for summary
        run_plays = effectiveness_sorted[effectiveness_sorted['OffPlayType'].isin(['Inside Run', 'Outside Run'])]
        pass_plays = effectiveness_sorted[effectiveness_sorted['OffPlayType'].isin(['Short Pass', 'Medium Pass', 'Long Pass'])]
        
        print(f"\n🏃‍♂️ TOP RUNNING PLAYS FROM PLAYBOOK (by ANY/A)")
        if not run_plays.empty:
            for rank, (play, stats) in enumerate(run_plays.head(10).iterrows(), 1):
                print(f"   {rank}. {play}")
                print(f"      {stats['ypp']} ypp, {stats['any_a']} any/a, {stats['success_rate']}% success, {stats['cnt']} attempts")
        else:
            print("   No running plays found in playbook vs opponent")
        
        print(f"\n🎯 TOP PASSING PLAYS FROM PLAYBOOK (by ANY/A)")
        if not pass_plays.empty:
            for rank, (play, stats) in enumerate(pass_plays.head(10).iterrows(), 1):
                print(f"   {rank}. {play}")
                print(f"      {stats['ypp']} ypp, {stats['any_a']} any/a, {stats['success_rate']}% success, {stats['completion_rate']}% comp, {stats['cnt']} attempts")
        else:
            print("   No passing plays found in playbook vs opponent")
        
        return {
            'run_plays': run_plays.to_dict('index'),
            'pass_plays': pass_plays.to_dict('index'),
            'all_plays': effectiveness_sorted.to_dict('index')
        }
    
    def analyze_all_plays_vs_opponent(self):
        """Analyze ALL plays vs opponent (not filtered by current playbook) to find top performers."""
        
        print(f"\n📊 ANALYZING ALL PLAYS vs {self.opponent}")
        print("=" * 50)
        
        # Find games involving opponent
        opponent_games = self.df.groupby('Game ID')['HasBall'].unique()
        games_with_opponent = [game_id for game_id, teams in opponent_games.items() 
                              if self.opponent in teams]
        
        # Filter for plays against opponent's defense
        vs_opponent_defense = self.df[
            (self.df['Game ID'].isin(games_with_opponent)) &
            (self.df['HasBall'] != self.opponent) &
            (self.df['HasBall'].notna()) &
            (self.df['OffensivePlay'].notna()) &
            (~self.df['OffensivePlay'].isin(['Field Goal', 'Punt', 'Victory', 'Kickoff']))
        ].copy()
        
        print(f"📊 Found {len(vs_opponent_defense)} total offensive plays vs {self.opponent}")
        
        if vs_opponent_defense.empty:
            print("❌ No offensive plays found against opponent")
            return {}
        
        # Calculate effectiveness metrics for ALL plays (minimum 3 attempts for reliability)
        min_attempts = 3
        effectiveness = {}
        
        for play in vs_opponent_defense['OffensivePlay'].unique():
            play_data = vs_opponent_defense[vs_opponent_defense['OffensivePlay'] == play]
            
            if len(play_data) < min_attempts:
                continue
            
            attempts = len(play_data)
            avg_yards = play_data['YardsGained'].mean()
            total_yards = play_data['YardsGained'].sum()
            
            # Calculate ANY/A components
            touchdowns = len(play_data[play_data['Text'].str.contains('TOUCHDOWN', na=False)]) if 'Text' in play_data.columns else 0
            interceptions = len(play_data[play_data['Text'].str.contains('INTERCEPTED', na=False)]) if 'Text' in play_data.columns else 0
            sacks = len(play_data[play_data['Text'].str.contains('sacked', na=False)]) if 'Text' in play_data.columns else 0
            sack_yards = abs(play_data[play_data['Text'].str.contains('sacked', na=False)]['YardsGained'].sum()) if 'Text' in play_data.columns else 0
            
            # ANY/A calculation
            any_a = (total_yards + 20*touchdowns - 60*interceptions - sack_yards) / attempts
            
            # Success rate
            play_type = play_data['OffPlayType'].iloc[0] if 'OffPlayType' in play_data.columns else 'Unknown'
            success_threshold = 4.0 if play_type in ['Inside Run', 'Outside Run'] else 6.0
            successful = len(play_data[play_data['YardsGained'] >= success_threshold])
            success_rate = (successful / attempts) * 100
            
            effectiveness[play] = {
                'cnt': attempts,
                'ypp': round(avg_yards, 2),
                'any_a': round(any_a, 2),
                'success_rate': round(success_rate, 1),
                'OffPlayType': play_type,
                'OffPersonnel': play_data['OffPersonnel'].mode().iloc[0] if 'OffPersonnel' in play_data.columns and not play_data['OffPersonnel'].empty else 'Unknown'
            }
        
        # Convert to DataFrame and get top plays
        effectiveness_df = pd.DataFrame.from_dict(effectiveness, orient='index')
        
        if effectiveness_df.empty:
            print(f"❌ No plays with {min_attempts}+ attempts found")
            return {}
        
        # Sort by ANY/A to get the most effective plays
        top_plays = effectiveness_df.sort_values('any_a', ascending=False)
        
        print(f"✅ Found {len(top_plays)} plays with {min_attempts}+ attempts")
        print(f"📈 Top 15 most effective plays by ANY/A:")
        
        for rank, (play, stats) in enumerate(top_plays.head(15).iterrows(), 1):
            print(f"   {rank:2d}. {play[:50]:<50} ANY/A: {stats['any_a']:5.1f} ({stats['cnt']} att)")
        
        return top_plays
    
    def load_all_playbooks(self):
        """Load all available playbooks from Google Sheets."""
        
        if not SHEETS_AVAILABLE or self.sheets_connector is None:
            print("❌ Cannot load playbooks - Google Sheets not available")
            return {}
        
        try:
            sheet_id = Config.GAMEPLAN_SHEET_ID
            spreadsheet = self.sheets_connector.get_sheet(sheet_id)
            
            # Get all worksheet names
            worksheets = spreadsheet.worksheets()
            
            # Filter for playbook sheets (exclude analysis tabs and other sheets)
            playbook_sheets = []
            excluded_patterns = ['_Analysis_', 'analysis', 'data', 'temp', 'summary', 'reference']
            
            for ws in worksheets:
                sheet_name = ws.title.lower()
                if not any(pattern in sheet_name for pattern in excluded_patterns):
                    playbook_sheets.append(ws.title)
            
            print(f"🔍 Found {len(playbook_sheets)} potential playbook sheets:")
            for sheet in playbook_sheets:
                print(f"   • {sheet}")
            
            # Load plays from each playbook
            all_playbooks = {}
            
            for playbook_name in playbook_sheets:
                try:
                    playbook_worksheet = spreadsheet.worksheet(playbook_name)
                    playbook_data = playbook_worksheet.get_all_values()
                    
                    if not playbook_data:
                        continue
                    
                    # Find header row with 'Play Name'
                    header_row = None
                    for i, row in enumerate(playbook_data):
                        if any('play name' in cell.lower() for cell in row):
                            header_row = i
                            break
                    
                    if header_row is None:
                        continue
                    
                    headers = playbook_data[header_row]
                    play_col_idx = None
                    for i, header in enumerate(headers):
                        if 'play name' in header.lower():
                            play_col_idx = i
                            break
                    
                    if play_col_idx is None:
                        continue
                    
                    # Extract plays
                    plays = []
                    for row in playbook_data[header_row + 1:]:
                        if len(row) > play_col_idx and row[play_col_idx].strip():
                            play_name = row[play_col_idx].strip()
                            # Remove numbering if present
                            if '. ' in play_name:
                                play_name = play_name.split('. ', 1)[1]
                            plays.append(play_name)
                    
                    if plays:
                        all_playbooks[playbook_name] = plays
                        print(f"📋 {playbook_name}: {len(plays)} plays")
                    
                except Exception as e:
                    print(f"⚠️  Could not load {playbook_name}: {e}")
                    continue
            
            print(f"\n✅ Successfully loaded {len(all_playbooks)} playbooks")
            return all_playbooks
            
        except Exception as e:
            print(f"❌ Error loading playbooks: {e}")
            return {}
    
    def analyze_playbook_effectiveness(self, top_plays, csv_playbooks):
        """Score and rank playbooks based on effectiveness against opponent using CSV data."""
        
        if top_plays.empty or not csv_playbooks:
            print("❌ Cannot analyze playbook effectiveness - missing data")
            return {}
        
        print(f"\n💡 PLAYBOOK EFFECTIVENESS vs {self.opponent}")
        print("=" * 60)
        
        # Get top N plays to evaluate
        top_n = min(15, len(top_plays))
        top_plays_subset = top_plays.head(top_n)
        
        print(f"📈 Evaluating 5 playbooks against top {top_n} most effective plays:")
        
        # Score each playbook
        playbook_scores = {}
        
        for playbook_name, plays in csv_playbooks.items():
            # Find which top plays are in this playbook
            matching_plays = []
            total_any_a = 0
            total_ypp = 0
            
            for play in top_plays_subset.index:
                if play in plays:
                    matching_plays.append(play)
                    total_any_a += top_plays_subset.loc[play, 'any_a']
                    total_ypp += top_plays_subset.loc[play, 'ypp']
            
            coverage_count = len(matching_plays)
            coverage_percent = (coverage_count / top_n) * 100
            
            # Calculate average effectiveness of available top plays
            avg_any_a = total_any_a / coverage_count if coverage_count > 0 else 0
            avg_ypp = total_ypp / coverage_count if coverage_count > 0 else 0
            
            # Create composite score: (coverage% * 0.6) + (avg_any_a * 4) 
            # This weights both coverage and quality of available plays
            composite_score = (coverage_percent * 0.6) + (avg_any_a * 4)
            
            playbook_scores[playbook_name] = {
                'matching_plays': matching_plays,
                'coverage_count': coverage_count,
                'coverage_percent': coverage_percent,
                'avg_any_a': round(avg_any_a, 2),
                'avg_ypp': round(avg_ypp, 2),
                'composite_score': round(composite_score, 1),
                'total_plays': len(plays)
            }
        
        # Sort by composite score
        sorted_playbooks = sorted(playbook_scores.items(), key=lambda x: x[1]['composite_score'], reverse=True)
        
        print(f"\n📊 PLAYBOOK EFFECTIVENESS RANKINGS:")
        print(f"{'Rank':<4} {'Playbook':<18} {'Coverage':<10} {'Avg ANY/A':<10} {'Avg YPP':<9} {'Score':<7} {'Total'}")
        print("-" * 85)
        
        for rank, (playbook_name, scores) in enumerate(sorted_playbooks, 1):
            coverage_str = f"{scores['coverage_count']}/{top_n}"
            any_a_str = f"{scores['avg_any_a']:.1f}" if scores['avg_any_a'] > 0 else "N/A"
            ypp_str = f"{scores['avg_ypp']:.1f}" if scores['avg_ypp'] > 0 else "N/A"
            
            print(f"{rank:<4} {playbook_name:<18} {coverage_str:<10} {any_a_str:<10} {ypp_str:<9} {scores['composite_score']:<7} {scores['total_plays']}")
        
        # Get best recommendation
        best_playbook = sorted_playbooks[0] if sorted_playbooks else None
        
        print(f"\n🎯 RECOMMENDATION vs {self.opponent}:")
        
        if best_playbook:
            best_name, best_scores = best_playbook
            print(f"   🏆 USE '{best_name}' playbook")
            print(f"   📊 Effectiveness: {best_scores['coverage_count']}/{top_n} top plays available")
            print(f"   💪 Average ANY/A of available plays: {best_scores['avg_any_a']}")
            print(f"   🎯 Composite Score: {best_scores['composite_score']}")
            
            print(f"\n   ✨ TOP PLAYS YOU'D HAVE ACCESS TO:")
            for i, play in enumerate(best_scores['matching_plays'][:5], 1):
                play_rank = list(top_plays_subset.index).index(play) + 1
                play_any_a = top_plays_subset.loc[play, 'any_a']
                print(f"      {i}. #{play_rank} {play} (ANY/A: {play_any_a})")
            
            if len(best_scores['matching_plays']) > 5:
                print(f"      ... and {len(best_scores['matching_plays']) - 5} more")
        
        # Show comparison with other top playbooks
        if len(sorted_playbooks) > 1:
            print(f"\n   📈 COMPARISON:")
            for rank, (name, scores) in enumerate(sorted_playbooks[:3], 1):
                status = "👑" if rank == 1 else f"{rank}."
                print(f"      {status} {name}: {scores['coverage_count']}/{top_n} plays, {scores['avg_any_a']} ANY/A, Score: {scores['composite_score']}")
        
        return {
            'rankings': sorted_playbooks,
            'top_plays_analyzed': top_n,
            'recommendation': best_playbook[0] if best_playbook else None,
            'best_score': best_playbook[1] if best_playbook else {}
        }
    
    def analyze_defensive_success_vs_opponent(self):
        """Find the most successful defensive plays against the opponent's offense."""
        
        print(f"\n🛡️ DEFENSIVE PLAYS vs {self.opponent} OFFENSE")
        print("=" * 50)
        
        # Find games where opponent was on offense (opponent HasBall)
        opponent_games = self.df.groupby('Game ID')['HasBall'].unique()
        games_with_opponent = [game_id for game_id, teams in opponent_games.items() 
                              if self.opponent in teams]
        
        # Filter for plays against opponent's offense
        vs_opponent_offense = self.df[
            (self.df['Game ID'].isin(games_with_opponent)) &
            (self.df['HasBall'] == self.opponent) &
            (self.df['DefensivePlay'].notna()) &
            (~self.df['DefensivePlay'].isin(['Punt Return', 'Kick Return', 'FG Block']))
        ].copy()
        
        if vs_opponent_offense.empty:
            print(f"❌ No defensive plays found against {self.opponent} offense")
            return {}
        
        print(f"📊 Analyzing {len(vs_opponent_offense)} plays against {self.opponent} offense")
        
        # Calculate defensive success metrics
        def_success = vs_opponent_offense.groupby('DefensivePlay').agg({
            'YardsGained': ['count', 'mean', 'sum', 'std'],
            'OffPlayType': lambda x: x.mode().iloc[0] if not x.empty else 'Mixed'  # Most common off play type faced
        }).round(2)
        
        # Flatten column names
        def_success.columns = ['Attempts', 'Avg_Yards_Allowed', 'Total_Yards_Allowed', 'Std_Dev', 'Primary_OffType']
        
        # Filter by minimum attempts
        def_success = def_success[def_success['Attempts'] >= self.min_attempts]
        
        if def_success.empty:
            print(f"❌ No defensive plays with {self.min_attempts}+ attempts found")
            return {}
        
        # Sort by yards allowed (ascending = better defense)
        def_sorted = def_success.sort_values('Avg_Yards_Allowed', ascending=True)
        
        print(f"\n🛡️ BEST DEFENSIVE PLAYS vs {self.opponent}")
        print(f"   (Min {self.min_attempts} attempts, sorted by fewest yards allowed)")
        
        for defense, stats in def_sorted.head(10).iterrows():
            stop_rate = self._calculate_defensive_stop_rate(vs_opponent_offense, defense)
            disruption_rate = self._calculate_disruption_rate(vs_opponent_offense, defense)
            print(f"   {defense}")
            print(f"     {stats['Avg_Yards_Allowed']:.1f} yds allowed/play, {stats['Attempts']} attempts, {stop_rate:.1f}% stop rate, {disruption_rate:.1f}% disruption rate")
            print(f"     Primary vs: {stats['Primary_OffType']}")
        
        # Recommendations
        print(f"\n💡 DEFENSIVE RECOMMENDATIONS vs {self.opponent}")
        print("=" * 45)
        
        best_overall_def = def_sorted.index[0]
        best_overall_stats = def_sorted.iloc[0]
        
        print(f"   🛡️ Best Overall Defense: {best_overall_def}")
        print(f"     ({best_overall_stats['Avg_Yards_Allowed']:.1f} yards allowed per play)")
        
        # Find best vs run and pass separately
        run_defenses = vs_opponent_offense[vs_opponent_offense['OffPlayType'].isin(['Inside Run', 'Outside Run'])]
        pass_defenses = vs_opponent_offense[vs_opponent_offense['OffPlayType'].isin(['Short Pass', 'Medium Pass', 'Long Pass'])]
        
        if not run_defenses.empty:
            best_vs_run = run_defenses.groupby('DefensivePlay')['YardsGained'].mean().sort_values().head(3)
            print(f"   🏃‍♂️ Best vs Run: {', '.join([f'{play} ({yards:.1f})' for play, yards in best_vs_run.items()])}")
        
        if not pass_defenses.empty:
            best_vs_pass = pass_defenses.groupby('DefensivePlay')['YardsGained'].mean().sort_values().head(3)
            print(f"   🎯 Best vs Pass: {', '.join([f'{play} ({yards:.1f})' for play, yards in best_vs_pass.items()])}")
        
        return def_sorted.to_dict('index')
    
    def _calculate_success_rate(self, data, play_name, success_threshold):
        """Calculate success rate for an offensive play."""
        play_data = data[data['OffensivePlay'] == play_name]
        if len(play_data) == 0:
            return 0.0
        successful_plays = len(play_data[play_data['YardsGained'] >= success_threshold])
        return (successful_plays / len(play_data)) * 100
    
    def _calculate_completion_rate(self, data, play_name):
        """
        Calculate completion rate for a passing play.
        This is an estimate, as we can't definitively determine incomplete passes from the data.
        We are assuming a pass is incomplete if YardsGained is 0, which is an educated guess.
        A completed pass for 0 yards will be incorrectly marked as incomplete.
        """
        play_data = data[data['OffensivePlay'] == play_name]
        if len(play_data) == 0:
            return 0.0
        # Assume incomplete passes result in 0 yards.
        completed_passes = len(play_data[play_data['YardsGained'] != 0])
        return (completed_passes / len(play_data)) * 100
    
    def _calculate_defensive_stop_rate(self, data, defense_name):
        """
        Calculate stop rate for a defensive play, using different criteria for run and pass plays.
        - Run play stop: < 4 yards gained
        - Pass play stop: < 6 yards gained
        """
        defense_data = data[data['DefensivePlay'] == defense_name]
        if len(defense_data) == 0:
            return 0.0

        run_plays = defense_data[defense_data['OffPlayType'].isin(['Inside Run', 'Outside Run'])]
        pass_plays = defense_data[defense_data['OffPlayType'].isin(['Short Pass', 'Medium Pass', 'Long Pass'])]

        run_stops = len(run_plays[run_plays['YardsGained'] < 4])
        pass_stops = len(pass_plays[pass_plays['YardsGained'] < 6])

        total_stops = run_stops + pass_stops
        total_plays = len(run_plays) + len(pass_plays)

        if total_plays == 0:
            return 0.0
        
        return (total_stops / total_plays) * 100
    
    def _calculate_disruption_rate(self, data, defense_name):
        """Calculate disruption rate for a defensive play (yards gained < 0)."""
        defense_data = data[data['DefensivePlay'] == defense_name]
        if len(defense_data) == 0:
            return 0.0
        disruptions = len(defense_data[defense_data['YardsGained'] < 0])
        return (disruptions / len(defense_data)) * 100
    
    def create_sheets_tab(self, off_results, def_results, top_plays=None, playbook_recommendations=None):
        """Create a new tab in Google Sheets with results."""
        if not SHEETS_AVAILABLE or self.sheets_connector is None:
            print("⚠️  Google Sheets not available - skipping export")
            return
        
        try:
            sheet_id = Config.GAMEPLAN_SHEET_ID
            spreadsheet = self.sheets_connector.get_sheet(sheet_id)
            
            # Create tab name
            tab_name = f"{self.opponent}_Analysis_{self.season}"
            
            # Delete existing tab if it exists
            try:
                existing_tab = spreadsheet.worksheet(tab_name)
                spreadsheet.del_worksheet(existing_tab)
                print(f"🗑️  Deleted existing {tab_name} tab")
            except:
                pass
            
            # Create new worksheet
            worksheet = spreadsheet.add_worksheet(title=tab_name, rows=200, cols=15)
            
            # Prepare data for export
            export_data = []
            
            # Title and header section
            export_data.append([f"TEAM ANALYSIS vs {self.opponent} ({self.league} {self.season})"])
            export_data.append([])
            
            # Offensive section - ALL PLAYBOOK PLAYS
            export_data.append(["OFFENSIVE PLAYS (ALL PLAYBOOK PLAYS)"])
            export_data.append(["Rank", "Play Name", "Cnt", "YPP", "ANY/A", "Success Rate %", "Comp Rate %", "TD Rate %", "INT Rate %", "Personnel", "Play Type"])
            
            # Add ALL qualifying plays (not just top 15)
            if 'all_plays' in off_results and off_results['all_plays']:
                all_plays_df = pd.DataFrame.from_dict(off_results['all_plays'], orient='index')
                all_plays_sorted = all_plays_df.sort_values('any_a', ascending=False)
                
                for rank, (play, stats) in enumerate(all_plays_sorted.iterrows(), 1):
                    export_data.append([
                        rank,
                        play,
                        int(stats['cnt']),
                        round(stats['ypp'], 1),
                        round(stats['any_a'], 1),
                        round(stats['success_rate'], 1),
                        round(stats['completion_rate'], 1) if stats['OffPlayType'] in ['Short Pass', 'Medium Pass', 'Long Pass'] else 'N/A',
                        round(stats['td_rate'], 1),
                        round(stats['int_rate'], 1),
                        stats.get('OffPersonnel', 'Unknown'),
                        stats.get('OffPlayType', 'Unknown')
                    ])
            
            # Playbook effectiveness section
            if playbook_recommendations and playbook_recommendations.get('rankings'):
                export_data.append([""])
                export_data.append([""])
                export_data.append(["PLAYBOOK EFFECTIVENESS ANALYSIS"])
                export_data.append(["Rank", "Playbook Name", "Coverage", "Avg ANY/A", "Avg YPP", "Score", "Total Plays"])
                
                for rank, (playbook_name, scores) in enumerate(playbook_recommendations['rankings'], 1):
                    top_n = playbook_recommendations.get('top_plays_analyzed', 15)
                    coverage_ratio = f"{scores['coverage_count']}/{top_n}"
                    avg_any_a = f"{scores['avg_any_a']:.1f}" if scores['avg_any_a'] > 0 else "N/A"
                    avg_ypp = f"{scores['avg_ypp']:.1f}" if scores['avg_ypp'] > 0 else "N/A"
                    
                    export_data.append([
                        rank,
                        playbook_name,
                        coverage_ratio,
                        avg_any_a,
                        avg_ypp,
                        scores['composite_score'],
                        scores['total_plays']
                    ])
                
                # Add recommendation summary
                export_data.append([""])
                if playbook_recommendations.get('recommendation'):
                    recommended = playbook_recommendations['recommendation']
                    best_score = playbook_recommendations.get('best_score', {})
                    
                    export_data.append(["RECOMMENDATION", f"USE '{recommended}' playbook"])
                    if best_score:
                        export_data.append(["EFFECTIVENESS", f"{best_score.get('coverage_count', 0)}/{playbook_recommendations.get('top_plays_analyzed', 15)} top plays available"])
                        export_data.append(["AVG ANY/A", f"{best_score.get('avg_any_a', 0):.1f}"])
                        export_data.append(["SCORE", f"{best_score.get('composite_score', 0):.1f}"])
            
            # Top all plays section (if available)
            if top_plays is not None and not top_plays.empty:
                export_data.append([""])
                export_data.append([""])
                export_data.append(["TOP PLAYS vs OPPONENT (ALL PLAYBOOKS)"])
                export_data.append(["Rank", "Play Name", "Cnt", "YPP", "ANY/A", "Success Rate %", "Personnel", "Play Type"])
                
                for rank, (play, stats) in enumerate(top_plays.head(15).iterrows(), 1):
                    export_data.append([
                        rank,
                        play,
                        int(stats['cnt']),
                        round(stats['ypp'], 1),
                        round(stats['any_a'], 1),
                        round(stats['success_rate'], 1),
                        stats.get('OffPersonnel', 'Unknown'),
                        stats.get('OffPlayType', 'Unknown')
                    ])
            
            # Defensive section
            export_data.append([""])
            export_data.append([""])
            export_data.append(["DEFENSIVE PLAYS"])
            export_data.append(["Rank", "Defense Name", "Attempts", "Avg Yards Allowed", "Stop Rate %", "Disruption Rate %", "Primary vs"])
            
            if def_results:
                def_df = pd.DataFrame.from_dict(def_results, orient='index')
                def_sorted = def_df.sort_values('Avg_Yards_Allowed', ascending=True)
                
                for rank, (defense, stats) in enumerate(def_sorted.head(15).iterrows(), 1):
                    stop_rate = 50.0  # Placeholder
                    disruption_rate = 10.0  # Placeholder
                    export_data.append([
                        rank,
                        defense,
                        int(stats['Attempts']),
                        round(stats['Avg_Yards_Allowed'], 1),
                        stop_rate,
                        disruption_rate,
                        stats.get('Primary_OffType', 'Mixed')
                    ])
            
            # Write to sheet
            worksheet.update('A1', export_data)
            
            # Format header rows
            worksheet.format('A1', {
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 1.0},
                'textFormat': {'bold': True, 'fontSize': 14}
            })
            
            worksheet.format('A3:K3', {
                'backgroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8},
                'textFormat': {'bold': True}
            })
            
            worksheet.format('A4:K4', {
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9},
                'textFormat': {'bold': True}
            })
            
            print(f"✅ Created {tab_name} tab in Google Sheets")
            print(f"🔗 View at: https://docs.google.com/spreadsheets/d/{sheet_id}")
            
        except Exception as e:
            print(f"❌ Error creating Google Sheets tab: {e}")
    
    def generate_full_report(self):
        """Generate complete offensive and defensive analysis with playbook recommendations."""
        print(f"🏈 TEAM-SPECIFIC SUCCESS ANALYSIS WITH PLAYBOOK OPTIMIZATION")
        print(f"Target: {self.opponent} ({self.league} {self.season})")
        print(f"Minimum attempts: {self.min_attempts}")
        print("=" * 70)
        
        # Step 1: Analyze ALL plays vs opponent to find top performers
        top_plays = self.analyze_all_plays_vs_opponent()
        
        # Step 2: Load CSV-based playbooks (the real ones)
        csv_playbooks = self.load_csv_playbooks()
        
        # Step 3: Analyze playbook effectiveness using CSV data
        playbook_recommendations = {}
        if not top_plays.empty and csv_playbooks:
            playbook_recommendations = self.analyze_playbook_effectiveness(top_plays, csv_playbooks)
        
        # Step 4: Analyze current playbook vs opponent (original functionality)
        off_results = self.analyze_offensive_success_vs_opponent()
        
        # Step 5: Analyze defensive plays
        def_results = self.analyze_defensive_success_vs_opponent()
        
        # Step 6: Export to Google Sheets
        self.create_sheets_tab(off_results, def_results, top_plays, playbook_recommendations)
        
        return {
            'offensive': off_results,
            'defensive': def_results,
            'top_plays_all': top_plays,
            'playbook_recommendations': playbook_recommendations
        }

def main():
    """Main function to run team-specific analysis."""
    parser = argparse.ArgumentParser(description='Analyze successful plays against a specific opponent')
    parser.add_argument('--opponent', required=True, help='Opponent team abbreviation (e.g., MIC)')
    parser.add_argument('--league', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--season', type=int, required=True, help='Season year (e.g., 2018)')
    parser.add_argument('--min-attempts', type=int, default=1, help='Minimum attempts required for analysis (default: 1)')
    
    args = parser.parse_args()
    
    try:
        analyzer = TeamSuccessAnalyzer(args.league, args.season, args.opponent, args.min_attempts)
        results = analyzer.generate_full_report()
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())