#!/usr/bin/env python3
"""
Authenticated MFN Game Log Downloader
=====================================

Enhanced downloader that handles MFN website authentication for automatic game log downloads.

Usage:
python authenticated_downloader.py --league USFL --year 2018 --starting-id 14077 --username YOUR_USERNAME --password YOUR_PASSWORD
"""

import requests
import os
import pandas as pd
import argparse
from pathlib import Path
from util import Config


class AuthenticatedGameLogDownloader:
    """Enhanced GameLogDownloader with MFN website authentication support."""
    
    def __init__(self, league=None, season=None, username=None, password=None):
        self.league = league
        self.season = str(season) if season else None
        self.root = Config.root
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.authenticated = False
    
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
        
        # Prepare login data with correct field names
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
        # Common indicators: redirect, absence of login form, presence of logout link
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
            self.authenticated = True  # Optimistic assumption
            return True
    
    def download_game_log(self, game_id, save_path):
        """Download a single game log with authentication."""
        domain = Config.domain_map[self.league]
        
        # First visit the box score page (as per the Referer in your browser)
        box_url = f"https://{domain}.myfootballnow.com/box/{game_id}"
        print(f"📊 Visiting box score: {box_url}")
        try:
            box_response = self.session.get(box_url)
            box_response.raise_for_status()
            print("✅ Box score page accessed")
            
            # Check if box score page contains any download links or tokens
            if 'download' in box_response.text.lower():
                print("🔍 Found download reference in box score page")
                
                # Extract download links from the page
                import re
                download_links = re.findall(r'href="([^"]*download[^"]*)"', box_response.text, re.IGNORECASE)
                if download_links:
                    print(f"🔗 Found download links: {download_links}")
                else:
                    # Look for any URLs containing the game ID
                    game_id_links = re.findall(r'href="([^"]*' + str(game_id) + r'[^"]*)"', box_response.text)
                    print(f"🔗 Found game ID links: {game_id_links[:5]}")  # Show first 5
                    
                # Let's also see if there are any form actions or JavaScript URLs
                form_actions = re.findall(r'action="([^"]*)"', box_response.text, re.IGNORECASE)
                if form_actions:
                    print(f"📝 Found form actions: {form_actions[:3]}")  # Show first 3
            
        except requests.RequestException as e:
            print(f"⚠️  Warning: Could not access box score: {e}")
        
        # Use the correct download URL format found from the box score page
        url = f"https://{domain}.myfootballnow.com/download-game/{game_id}"
        
        # Set headers to match browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0',
            'Referer': box_url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        }
        
        print(f"🍪 Current cookies: {len(self.session.cookies)} cookies")
        for cookie in self.session.cookies:
            print(f"   {cookie.name}: domain={cookie.domain}, value={cookie.value[:20]}...")
        
        print(f"🔄 Trying download URL: {url}")
        try:
            response = self.session.get(url, headers=headers)
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                # Check if we got actual CSV data or an error page
                content = response.text
                if content.startswith('<!DOCTYPE html>') or 'Error 404' in content:
                    print(f"❌ Game {game_id}: Got HTML page instead of CSV")
                    print(f"First 200 chars: {content[:200]}")
                    return False
                
                # Check if it's a ZIP file (starts with "PK")
                if content.startswith('PK'):
                    print(f"✅ Found ZIP file! Saving as .zip")
                    # Save as ZIP file
                    zip_path = str(save_path).replace('.csv', '.zip')
                    with open(zip_path, 'wb') as f:
                        f.write(response.content)
                    
                    # Extract the ZIP file to get the CSV
                    import zipfile
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            # List files in the zip
                            file_list = zip_ref.namelist()
                            print(f"📦 ZIP contains: {file_list}")
                            
                            # Extract all files to the same directory
                            extract_dir = os.path.dirname(save_path)
                            zip_ref.extractall(extract_dir)
                            
                            # Look for Excel structure - if we see xl/worksheets, it's an Excel file
                            if any('xl/worksheets' in f for f in file_list):
                                print("📊 Detected Excel file structure, converting to CSV")
                                
                                # The extracted files form an Excel file, let's read it using pandas
                                # Save the zip as a .xlsx file first
                                excel_path = str(save_path).replace('.csv', '.xlsx')
                                
                                # Copy the zip as Excel file (don't move, we need to clean it up later)
                                import shutil
                                shutil.copy2(zip_path, excel_path)
                                
                                # Read Excel file and convert to CSV
                                try:
                                    import pandas as pd
                                    df = pd.read_excel(excel_path)
                                    df.to_csv(save_path, index=False)
                                    print(f"✅ Converted Excel to CSV: {df.shape[0]} rows, {df.shape[1]} columns")
                                    
                                    # Clean up Excel file and extracted files
                                    os.remove(excel_path)
                                    
                                except Exception as e:
                                    print(f"❌ Error converting Excel to CSV: {e}")
                                    return False
                            else:
                                # Try to find a CSV file in the extracted files
                                csv_files = [f for f in file_list if f.endswith('.csv')]
                                if csv_files:
                                    # Rename the first CSV file to our expected name
                                    extracted_csv = os.path.join(extract_dir, csv_files[0])
                                    if os.path.exists(extracted_csv):
                                        os.rename(extracted_csv, save_path)
                                        print(f"✅ Extracted and renamed CSV: {csv_files[0]} -> {os.path.basename(save_path)}")
                            
                            # Clean up any remaining extracted files
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
                            
                        # Clean up the ZIP file
                        os.remove(zip_path)
                        return True
                        
                    except zipfile.BadZipFile:
                        print(f"❌ Downloaded file is not a valid ZIP file")
                        return False
                        
                # Check if it looks like CSV data
                elif ',' in content or '\t' in content:
                    print(f"✅ Found CSV data! First 100 chars: {content[:100]}")
                    # Save the CSV file
                    with open(save_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True
                else:
                    print(f"⚠️  Response doesn't look like CSV or ZIP: {content[:100]}")
                    return False
                    
            elif response.status_code == 404:
                print(f"❌ 404 Not Found")
                return False
            else:
                print(f"❌ Unexpected status: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Failed to download game {game_id}: {e}")
            return False
    
    def download_season(self, starting_game_id, num_games=256):
        """Download all games for a season."""
        if not self.authenticated:
            print("❌ Not authenticated - please login first")
            return False
        
        # Create output directory
        output_dir = Path(self.root) / self.league / self.season
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Saving to: {output_dir}")
        print(f"⬇️  Downloading {num_games} games starting from ID {starting_game_id}...")
        
        success_count = 0
        failed_count = 0
        
        for i in range(num_games):
            game_id = starting_game_id + i
            save_path = output_dir / f"{game_id}.csv"
            
            print(f"Downloading {game_id} for {self.league}...")
            
            if self.download_game_log(game_id, save_path):
                success_count += 1
            else:
                failed_count += 1
                # Remove failed file if it exists
                if save_path.exists():
                    save_path.unlink()
        
        print(f"\n📊 Download Summary:")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📁 Files saved to: {output_dir}")
        
        return success_count > 0


def main():
    parser = argparse.ArgumentParser(description='Authenticated MFN Game Log Downloader')
    parser.add_argument('--league', '-l', required=True, help='League name (e.g., USFL)')
    parser.add_argument('--year', '-y', type=int, required=True, help='Season year (e.g., 2018)')
    parser.add_argument('--starting-id', '-s', type=int, required=True, 
                       help='Starting Game ID (e.g., 14077)')
    parser.add_argument('--num-games', '-n', type=int, default=256,
                       help='Number of games in season (default: 256)')
    parser.add_argument('--username', '-u', required=True, help='MFN username')
    parser.add_argument('--password', '-p', required=True, help='MFN password')
    parser.add_argument('--test-single', action='store_true',
                       help='Test with just one game download')
    
    args = parser.parse_args()
    
    # Create downloader
    downloader = AuthenticatedGameLogDownloader(
        league=args.league,
        season=args.year,
        username=args.username,
        password=args.password
    )
    
    # Login
    if not downloader.login():
        print("❌ Authentication failed")
        return 1
    
    # Download games
    num_games = 1 if args.test_single else args.num_games
    if args.test_single:
        print(f"🧪 Test mode: downloading only 1 game")
    
    success = downloader.download_season(args.starting_id, num_games)
    
    if success:
        print("✅ Download completed!")
        return 0
    else:
        print("❌ Download failed!")
        return 1


if __name__ == "__main__":
    exit(main())