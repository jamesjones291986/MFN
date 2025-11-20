#!/usr/bin/env python3
"""
Update Live Rookies CSV
Downloads the latest draft-eligible players from Google Sheets and saves to live_rookies.csv
"""

import sys
import csv
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from sheets_connector import SheetsConnector

def update_live_rookies_csv():
    """Extract latest rookie data from Google Sheets and save to live_rookies.csv."""
    sheet_id = "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"
    
    print("🔄 UPDATING LIVE ROOKIES DATA")
    print("=" * 50)
    print(f"📊 Source: Google Sheets (Sheet ID: {sheet_id})")
    
    try:
        # Connect to Google Sheets
        print("🔗 Connecting to Google Sheets...")
        connector = SheetsConnector(verbose=False)
        
        if not connector.client:
            print("❌ Failed to connect to Google Sheets")
            return False
        
        spreadsheet = connector.client.open_by_key(sheet_id)
        print("✅ Connected successfully")
        
        # Check available worksheets
        worksheets = spreadsheet.worksheets()
        print(f"📋 Available worksheets: {[ws.title for ws in worksheets]}")
        
        # Try different possible worksheet names for current data
        possible_sheets = ['Player Import', 'Players Cur', 'MaxDraft', 'CurFormulas']
        current_data = None
        source_sheet = None
        
        for sheet_name in possible_sheets:
            try:
                ws = spreadsheet.worksheet(sheet_name)
                data = ws.get_all_records()
                
                # Filter to rookies (draft-eligible players)
                rookies = []
                for player in data:
                    # Check for rookie indicators
                    exp = player.get('Exp', player.get('Experience', ''))
                    team = player.get('Team', '')
                    
                    if (exp == 'R' or 'Draft Eligible' in str(team) or 
                        'Rookie' in str(team) or len(str(exp)) == 0):
                        rookies.append(player)
                
                if rookies:
                    print(f"✅ Found {len(rookies)} rookies in '{sheet_name}'")
                    current_data = rookies
                    source_sheet = sheet_name
                    break
                else:
                    print(f"⚠️  No rookies found in '{sheet_name}'")
                    
            except Exception as e:
                print(f"❌ Could not access '{sheet_name}': {e}")
        
        if not current_data:
            print("❌ No rookie data found in any worksheet")
            return False
        
        # Save to CSV
        csv_file = Path(__file__).parent / "live_rookies.csv"
        
        print(f"💾 Saving to {csv_file}...")
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            if current_data:
                # Use all available fields
                fieldnames = list(current_data[0].keys())
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(current_data)
        
        print(f"✅ Successfully updated live_rookies.csv")
        print(f"📈 Total players: {len(current_data)}")
        print(f"📊 Source worksheet: '{source_sheet}'")
        
        # Show sample of what was saved
        print(f"\\n📋 Sample of saved data:")
        for i, player in enumerate(current_data[:3], 1):
            name_parts = []
            if player.get('FirstName'):
                name_parts.append(player['FirstName'])
            if player.get('LastName'):
                name_parts.append(player['LastName'])
            name = " ".join(name_parts) if name_parts else "Unknown"
            
            pos = player.get('Pos', player.get('Position', 'N/A'))
            vol = player.get('Volatility', player.get('Vol', 'N/A'))
            exp = player.get('Exp', player.get('Experience', 'N/A'))
            
            print(f"  {i}. {name} ({pos}) - Vol: {vol}, Exp: {exp}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating live rookies: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to update live rookies data."""
    print("🚀 LIVE ROOKIES DATA UPDATER")
    print("=" * 60)
    
    success = update_live_rookies_csv()
    
    if success:
        print(f"\\n🎉 SUCCESS!")
        print(f"📁 Updated file: live_rookies.csv")
        print(f"🔧 Next steps:")
        print(f"   1. Run: python3 live_rookies_analyzer.py")
        print(f"   2. Or:  python3 draft_prioritized_analyzer.py")
    else:
        print(f"\\n❌ FAILED to update live rookies data")

if __name__ == "__main__":
    main()