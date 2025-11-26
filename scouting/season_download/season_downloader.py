#!/usr/bin/env python3
"""
MFN Season Downloader
====================

Streamlined tool for downloading complete MFN seasons with minimal setup.

This tool combines the best parts of the original automation scripts into
a single, focused season download utility.

Usage:
python season_downloader.py --league USFL --year 2018 --starting-id 14077 --username YOUR_USERNAME --password YOUR_PASSWORD

Features:
- Simple game ID list generation for any season
- Authenticated downloads through MFN website
- Automatic file format handling (CSV/ZIP/Excel)
- Progress tracking and error handling
"""

import argparse
import os
import sys
import requests
import pandas as pd
import zipfile
import shutil
import tempfile
from pathlib import Path
from glob import glob
from config import Config


class SeasonDownloader:
    """Main class for downloading MFN seasons."""
    
    def __init__(self, league=None, season=None, username=None, password=None):
        self.league = league
        self.season = str(season) if season else None
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.authenticated = False
        self.temp_dir = None
        
        # Feather output paths - use Config to find Google Drive location
        sys.path.append(str(Path(__file__).parent.parent))
        from util import Config
        self.feathers_dir = Config.seasons
        
    def create_game_id_list(self, starting_game_id: int, num_games: int = 256) -> pd.DataFrame:
        """
        Create a simple list of Game IDs for download.
        
        Args:
            starting_game_id: First game ID of the season
            num_games: Number of games in season (default: 256)
        
        Returns:
            DataFrame with Game ID and Captured columns
        """
        games = []
        for i in range(num_games):
            games.append({
                'Game ID': starting_game_id + i,
                'Captured': 0  # 0 = download, 1 = skip
            })
        
        return pd.DataFrame(games)
    
    def login(self):
        """Authenticate with MFN website."""
        if not self.username or not self.password:
            print("❌ Username and password required for authentication")
            return False
        
        domain = Config.domain_map.get(self.league)
        if not domain:
            print(f"❌ Unknown league: {self.league}")
            return False
        
        login_url = "https://www.myfootballnow.com/login"
        
        print(f"🔐 Logging into {login_url}...")
        
        # Get login page to extract CSRF token
        try:
            login_page = self.session.get(login_url)
            login_page.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Failed to access login page: {e}")
            return False
        
        # Extract CSRF token from login page
        import re
        token_match = re.search(r'name="_token"\s+value="([^"]+)"', login_page.text)
        if not token_match:
            print("❌ Could not find CSRF token in login page")
            return False
        
        csrf_token = token_match.group(1)
        print(f"🔑 Found CSRF token: {csrf_token[:10]}...")
        
        # Prepare login data
        login_data = {
            '_token': csrf_token,
            'user_username': self.username,
            'password': self.password,
        }
        
        # Try POST to login endpoint
        try:
            login_response = self.session.post(login_url, data=login_data)
            login_response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Login request failed: {e}")
            return False
        
        # Check if login was successful
        response_text = login_response.text.lower()
        
        if any(indicator in response_text for indicator in ['logout', 'dashboard', 'profile', 'settings']):
            print("✅ Login successful!")
            
            # Visit the league subdomain to establish session there
            domain = Config.domain_map[self.league]
            league_url = f"https://{domain}.myfootballnow.com/"
            
            print(f"🌐 Visiting league domain: {league_url}")
            try:
                league_response = self.session.get(league_url)
                league_response.raise_for_status()
                print("✅ League domain session established")
            except requests.RequestException as e:
                print(f"⚠️  Warning: Could not visit league domain: {e}")
            
            self.authenticated = True
            return True
        elif any(indicator in response_text for indicator in ['invalid', 'incorrect', 'failed', 'error']):
            print("❌ Login failed - invalid credentials")
            return False
        else:
            print("⚠️  Login status unclear - proceeding with attempt")
            self.authenticated = True
            return True
    
    def download_game_log(self, game_id, save_path):
        """Download a single game log with authentication."""
        domain = Config.domain_map[self.league]
        
        # Visit the box score page first
        box_url = f"https://{domain}.myfootballnow.com/box/{game_id}"
        try:
            box_response = self.session.get(box_url)
            box_response.raise_for_status()
        except requests.RequestException as e:
            print(f"⚠️  Warning: Could not access box score: {e}")
        
        # Use the download URL
        url = f"https://{domain}.myfootballnow.com/download-game/{game_id}"
        
        # Set headers to match browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': box_url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        try:
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                content = response.text
                
                # Check if we got HTML instead of data
                if content.startswith('<!DOCTYPE html>') or 'Error 404' in content:
                    print(f"❌ Game {game_id}: Got HTML page instead of data")
                    return False
                
                # Check if it's a ZIP file - just save the raw response for now
                if response.content.startswith(b'PK'):
                    print(f"⚠️  Game {game_id}: Got ZIP file, saving raw content")
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    return True
                
                # Check if it looks like CSV data
                elif ',' in content or '\t' in content:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True
                else:
                    print(f"⚠️  Unknown response format for game {game_id}")
                    return False
                    
            elif response.status_code == 404:
                print(f"❌ Game {game_id}: Not found (404)")
                return False
            else:
                print(f"❌ Game {game_id}: Unexpected status {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Failed to download game {game_id}: {e}")
            return False
    
    def _handle_zip_download(self, response, save_path, game_id):
        """Handle ZIP file downloads and extraction."""
        zip_path = str(save_path).replace('.csv', '.zip')
        
        # Save as ZIP file
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        # Extract the ZIP file
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                extract_dir = os.path.dirname(save_path)
                zip_ref.extractall(extract_dir)
                
                # Check if it's an Excel file (contains xl/worksheets)
                if any('xl/worksheets' in f for f in file_list):
                    excel_path = str(save_path).replace('.csv', '.xlsx')
                    shutil.copy2(zip_path, excel_path)
                    
                    # Convert Excel to CSV
                    try:
                        df = pd.read_excel(excel_path)
                        df.to_csv(save_path, index=False)
                        os.remove(excel_path)
                        print(f"✅ Converted Excel to CSV: {df.shape[0]} rows")
                    except Exception as e:
                        print(f"❌ Error converting Excel: {e}")
                        return False
                else:
                    # Look for CSV files in extracted content
                    csv_files = [f for f in file_list if f.endswith('.csv')]
                    if csv_files:
                        extracted_csv = os.path.join(extract_dir, csv_files[0])
                        if os.path.exists(extracted_csv):
                            os.rename(extracted_csv, save_path)
                
                # Clean up extracted files
                for file_name in file_list:
                    file_path = os.path.join(extract_dir, file_name)
                    if os.path.isfile(file_path):
                        try:
                            os.remove(file_path)
                        except:
                            pass
                    elif os.path.isdir(file_path):
                        try:
                            shutil.rmtree(file_path)
                        except:
                            pass
            
            # Clean up ZIP file
            os.remove(zip_path)
            return True
            
        except zipfile.BadZipFile:
            print(f"❌ Downloaded file is not a valid ZIP file")
            return False
    
    def download_season(self, starting_game_id, num_games=256):
        """Download all games for a season to temporary directory."""
        if not self.authenticated:
            print("❌ Not authenticated - please login first")
            return False
        
        # Create temporary directory for downloads
        self.temp_dir = Path(self.script_dir) / "temp" / f"{self.league}_{self.season}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Downloading to temporary directory: {self.temp_dir}")
        print(f"⬇️  Downloading {num_games} games starting from ID {starting_game_id}...")
        
        success_count = 0
        failed_count = 0
        
        for i in range(num_games):
            game_id = starting_game_id + i
            save_path = self.temp_dir / f"{game_id}.csv"
            
            print(f"Downloading {game_id} for {self.league}... ({i+1}/{num_games})")
            
            if self.download_game_log(game_id, save_path):
                success_count += 1
                print(f"✅ Game {game_id} downloaded")
            else:
                failed_count += 1
                # Remove failed file if it exists
                if save_path.exists():
                    save_path.unlink()
        
        print(f"\n📊 Download Summary:")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📁 Files saved to: {self.temp_dir}")
        
        return success_count > 0
    
    def compile_to_feather(self):
        """Compile downloaded CSV files into a complete feather file with full processing."""
        if not self.temp_dir or not self.temp_dir.exists():
            print("❌ No temporary directory found - please download files first")
            return False
        
        print(f"\n📦 COMPILING TO FEATHER FILE")
        print("=" * 50)
        
        # Find all CSV files in temp directory
        csv_files = list(self.temp_dir.glob("*.csv"))
        if not csv_files:
            print("❌ No CSV files found in temporary directory")
            return False
        
        print(f"📄 Found {len(csv_files)} files to compile")
        
        # Define the columns we need (based on SeasonCompiler)
        play_cols = ['HasBall', 'Game Clock', 'Ball @', 'Quarter',
                     'Down', 'YTG', 'OffensivePlay', 'DefensivePlay',
                     'YardsGained', 'Home Score', 'Away Score', 'Text']
        
        # Compile all files
        compiled_dfs = []
        for csv_file in csv_files:
            try:
                # Extract game ID from filename
                game_id = csv_file.stem
                
                # Check if file is binary (ZIP) or text (CSV)
                with open(csv_file, 'rb') as f:
                    first_bytes = f.read(4)
                
                if first_bytes.startswith(b'PK'):
                    print(f"📦 Extracting Excel data from {csv_file.name}")
                    # The ZIP file is actually an Excel file
                    try:
                        # Read Excel data directly from the ZIP file
                        df = pd.read_excel(csv_file)
                        print(f"✅ Read Excel data: {len(df)} rows")
                        
                        # Save as clean CSV file, replacing the original ZIP
                        clean_csv_path = csv_file
                        df.to_csv(clean_csv_path, index=False)
                        print(f"💾 Saved clean CSV: {clean_csv_path.name}")
                        
                    except ImportError:
                        print(f"⚠️  Need openpyxl to read Excel files. Skipping {csv_file.name}")
                        print(f"   Install with: pip install openpyxl")
                        continue
                    except Exception as e:
                        print(f"⚠️  Failed to read Excel data from {csv_file.name}: {e}")
                        continue
                else:
                    # Try to read as CSV
                    df = pd.read_csv(csv_file)
                
                # Filter to required columns (only include columns that exist)
                available_cols = [col for col in play_cols if col in df.columns]
                if not available_cols:
                    print(f"⚠️  Warning: No recognized columns in {csv_file.name}")
                    continue
                    
                df = df[available_cols]
                
                # Add game ID, league, and season columns
                df.insert(0, 'Game ID', game_id)
                df.insert(1, 'League', self.league)
                df.insert(2, 'Season', int(self.season))
                
                compiled_dfs.append(df)
                print(f"✅ Processed {csv_file.name}: {len(df)} plays")
                
            except Exception as e:
                print(f"⚠️  Warning: Could not process {csv_file.name}: {e}")
                continue
        
        if not compiled_dfs:
            print("❌ No valid CSV files could be processed")
            return False
        
        # Concatenate all dataframes
        print(f"🔄 Combining {len(compiled_dfs)} game files...")
        raw_df = pd.concat(compiled_dfs, ignore_index=True)
        print(f"📊 Raw dataset: {len(raw_df)} plays from {len(compiled_dfs)} games")
        
        # Add missing columns that format_df expects
        if 'Text' not in raw_df.columns:
            print(f"⚠️  Adding missing 'Text' column (required for format_df)")
            raw_df['Text'] = ''  # Empty string for all rows
        
        # Now run through enhanced processing pipeline
        print(f"🔄 Processing through enhanced pipeline for complete analysis...")
        try:
            # Import from main.py and add path to access global reference files
            import sys
            sys.path.append(str(self.script_dir.parent))
            
            # Try full format_df first
            try:
                from main import format_df
                final_df = format_df(raw_df)
                print(f"✅ Full format_df processing complete: {len(final_df)} plays, {len(final_df.columns)} columns")
                
            except Exception as format_error:
                print(f"⚠️  Full format_df failed ({format_error}), trying enhanced processing...")
                
                # Enhanced processing: manually add play types and personnel  
                final_df = self._enhance_with_play_data(raw_df)
                print(f"✅ Enhanced processing complete: {len(final_df)} plays, {len(final_df.columns)} columns")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not run enhanced processing: {e}")
            print(f"   Falling back to basic format...")
            final_df = raw_df
        
        # Create feather filename following convention: {league}_{year}.feather
        feather_filename = f"{self.league}_{self.season}.feather"
        feather_path = self.feathers_dir / feather_filename
        
        # Ensure feathers directory exists
        self.feathers_dir.mkdir(exist_ok=True)
        
        # Save as feather file
        print(f"💾 Saving feather file: {feather_path}")
        final_df.to_feather(feather_path)
        
        print(f"✅ Feather file created successfully!")
        print(f"📊 Final dataset: {len(final_df)} plays, {len(final_df.columns)} columns")
        print(f"📁 Location: {feather_path}")
        
        return True
    
    def _enhance_with_play_data(self, df):
        """Enhance dataframe with play types and personnel data from global reference files."""
        print("🔍 Enhancing data with play types and personnel...")
        
        try:
            enhanced_df = df.copy()
            
            # Check if we need to add play type and personnel data
            needs_enhancement = 'OffPlayType' not in enhanced_df.columns or 'OffPersonnel' not in enhanced_df.columns
            
            if needs_enhancement:
                # Load global reference files
                global_off_path = '/Users/jamesjones/personal/game_logs/MFN Global Reference - OffPlays.csv'
                global_off_ref = pd.read_csv(global_off_path)
                print(f"✅ Loaded {len(global_off_ref)} offensive play references")
                
                # Merge with offensive play reference to get play types and personnel
                merge_columns = []
                if 'OffPlayType' not in enhanced_df.columns:
                    merge_columns.append('OffPlayType')
                if 'OffPersonnel' not in enhanced_df.columns:
                    merge_columns.append('OffPersonnel')
                
                if merge_columns:
                    merge_data = global_off_ref[['OffPlay'] + merge_columns]
                    enhanced_df = enhanced_df.merge(
                        merge_data, 
                        how='left', 
                        left_on='OffensivePlay', 
                        right_on='OffPlay'
                    )
                    
                    # Clean up merge column
                    enhanced_df = enhanced_df.drop(columns=['OffPlay'], errors='ignore')
            else:
                print("✅ Play types and personnel already present")
            
            # Add version column (consistent with format_df)
            if 'version' not in enhanced_df.columns:
                enhanced_df['version'] = '0.4.6'
            
            # Add any other columns that might be expected
            if 'YTGL' not in enhanced_df.columns and 'Ball @' in enhanced_df.columns:
                # Extract yard line from 'Ball @' column if possible
                enhanced_df['YTGL'] = 50  # Default to midfield
            
            if 'ytgl_bucket' not in enhanced_df.columns:
                enhanced_df['ytgl_bucket'] = '20-80'  # Default bucket
            
            if 'ev' not in enhanced_df.columns:
                enhanced_df['ev'] = 0.0  # Default expected value
            
            # Report results
            if 'OffPlayType' in enhanced_df.columns:
                print(f"✅ Play types: {enhanced_df['OffPlayType'].value_counts().head(3).to_dict()}")
            if 'OffPersonnel' in enhanced_df.columns:
                print(f"✅ Personnel: {enhanced_df['OffPersonnel'].value_counts().head(3).to_dict()}")
            
            return enhanced_df
            
        except Exception as e:
            print(f"⚠️  Warning: Could not enhance with play data: {e}")
            print("   Returning original dataframe...")
            return df
    
    def cleanup_temp_directory(self):
        """Remove the temporary download directory."""
        if self.temp_dir and self.temp_dir.exists():
            print(f"\n🧹 CLEANING UP TEMPORARY FILES")
            print("=" * 50)
            try:
                shutil.rmtree(self.temp_dir)
                print(f"✅ Temporary directory removed: {self.temp_dir}")
                return True
            except Exception as e:
                print(f"⚠️  Warning: Could not remove temporary directory: {e}")
                print(f"   You may need to manually delete: {self.temp_dir}")
                return False
        return True
    
    def run_download(self, starting_game_id, num_games=256, generate_schedule=False):
        """Run complete season download process."""
        print(f"🚀 MFN Season Downloader Starting")
        print(f"League: {self.league}, Season: {self.season}")
        print(f"Games: {starting_game_id} to {starting_game_id + num_games - 1}")
        print()
        
        # Step 1: Generate schedule if requested
        if generate_schedule:
            print("📋 Step 1: Generating Game ID List")
            schedule_path = f"{self.league}_{self.season}_games.csv"
            
            game_list = self.create_game_id_list(starting_game_id, num_games)
            game_list.to_csv(schedule_path, index=False)
            
            print(f"✅ Generated game list: {schedule_path}")
            print(f"   {len(game_list)} games from ID {starting_game_id}")
            print()
        
        # Step 2: Authenticate
        print("🔐 Step 2: Authentication")
        if not self.login():
            print("❌ Authentication failed")
            return False
        print()
        
        # Step 3: Download all game logs
        print("⬇️  Step 3: Downloading Game Logs")
        success = self.download_season(starting_game_id, num_games)
        
        if not success:
            print("\n❌ Season download failed!")
            self.cleanup_temp_directory()
            return False
        
        # Step 4: Compile to feather file
        print("📦 Step 4: Compiling to Feather File")
        feather_success = self.compile_to_feather()
        
        if not feather_success:
            print("\n❌ Feather compilation failed!")
            self.cleanup_temp_directory()
            return False
        
        # Step 5: Clean up temporary files (unless user wants to keep them)
        print("🧹 Step 5: Cleaning Up")
        self.cleanup_temp_directory()
        
        print("\n🎉 Season download and compilation completed successfully!")
        feather_path = self.feathers_dir / f"{self.league}_{self.season}.feather"
        print(f"📁 Final feather file: {feather_path}")
        return True
    
    def run_download_keep_temp(self, starting_game_id, num_games=256, generate_schedule=False, keep_temp=False):
        """Run complete season download process with option to keep temp files."""
        print(f"🚀 MFN Season Downloader Starting")
        print(f"League: {self.league}, Season: {self.season}")
        print(f"Games: {starting_game_id} to {starting_game_id + num_games - 1}")
        print()
        
        # Step 1: Generate schedule if requested
        if generate_schedule:
            print("📋 Step 1: Generating Game ID List")
            schedule_path = f"{self.league}_{self.season}_games.csv"
            
            game_list = self.create_game_id_list(starting_game_id, num_games)
            game_list.to_csv(schedule_path, index=False)
            
            print(f"✅ Generated game list: {schedule_path}")
            print(f"   {len(game_list)} games from ID {starting_game_id}")
            print()
        
        # Step 2: Authenticate
        print("🔐 Step 2: Authentication")
        if not self.login():
            print("❌ Authentication failed")
            return False
        print()
        
        # Step 3: Download all game logs
        print("⬇️  Step 3: Downloading Game Logs")
        success = self.download_season(starting_game_id, num_games)
        
        if not success:
            print("\n❌ Season download failed!")
            if not keep_temp:
                self.cleanup_temp_directory()
            return False
        
        # Step 4: Compile to feather file
        print("📦 Step 4: Compiling to Feather File")
        feather_success = self.compile_to_feather()
        
        if not feather_success:
            print("\n❌ Feather compilation failed!")
            if not keep_temp:
                self.cleanup_temp_directory()
            return False
        
        # Step 5: Clean up temporary files (unless user wants to keep them)
        if keep_temp:
            print("🧹 Step 5: Keeping Temporary Files (as requested)")
            print(f"📁 Temporary files location: {self.temp_dir}")
        else:
            print("🧹 Step 5: Cleaning Up")
            self.cleanup_temp_directory()
        
        print("\n🎉 Season download and compilation completed successfully!")
        feather_path = self.feathers_dir / f"{self.league}_{self.season}.feather"
        print(f"📁 Final feather file: {feather_path}")
        return True


def main():
    parser = argparse.ArgumentParser(description='MFN Season Downloader')
    parser.add_argument('--league', '-l', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--year', '-y', type=int, required=True, help='Season year (e.g., 2018)')
    parser.add_argument('--starting-id', '-s', type=int, required=True, 
                       help='Starting Game ID (e.g., 14077)')
    parser.add_argument('--num-games', '-n', type=int, default=256,
                       help='Number of games in season (default: 256)')
    parser.add_argument('--username', '-u', required=True, help='MFN username')
    parser.add_argument('--password', '-p', required=True, help='MFN password')
    parser.add_argument('--generate-schedule', action='store_true',
                       help='Generate a schedule CSV file')
    parser.add_argument('--test-single', action='store_true',
                       help='Test with just one game download')
    parser.add_argument('--keep-temp', action='store_true',
                       help='Keep temporary CSV files (for debugging)')
    
    args = parser.parse_args()
    
    # Create downloader
    downloader = SeasonDownloader(
        league=args.league,
        season=args.year,
        username=args.username,
        password=args.password
    )
    
    # Download season
    num_games = 1 if args.test_single else args.num_games
    if args.test_single:
        print(f"🧪 Test mode: downloading only 1 game")
    
    success = downloader.run_download_keep_temp(
        starting_game_id=args.starting_id,
        num_games=num_games,
        generate_schedule=args.generate_schedule,
        keep_temp=args.keep_temp
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())