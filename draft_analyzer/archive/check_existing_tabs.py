#!/usr/bin/env python3
"""
Check existing tabs in the Google Sheets to see format of Draft-Prioritized Multi-Position Analysis
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from sheets_connector import SheetsConnector

def check_existing_tabs():
    """Check what tabs exist and what the Draft-Prioritized tab looks like."""
    
    sheet_id = "1rkE1PpGezNeltSMIU7XLXjhxi1sSbWhfIbrDi4LKh9A"
    
    connector = SheetsConnector(verbose=False)
    spreadsheet = connector.client.open_by_key(sheet_id)
    
    print("🔍 CHECKING EXISTING TABS")
    print("=" * 50)
    
    # List all worksheets
    worksheets = spreadsheet.worksheets()
    print(f"\nFound {len(worksheets)} tabs:")
    for i, ws in enumerate(worksheets, 1):
        print(f"  {i}. {ws.title}")
    
    # Look for the Draft-Prioritized tab
    draft_prioritized_tab = None
    for ws in worksheets:
        if "Draft-Prioritized" in ws.title or "Multi-Position" in ws.title:
            draft_prioritized_tab = ws
            break
    
    if draft_prioritized_tab:
        print(f"\n📋 ANALYZING TAB: {draft_prioritized_tab.title}")
        print("=" * 60)
        
        # Get header row
        headers = draft_prioritized_tab.row_values(1)
        print(f"\nHeaders ({len(headers)} columns):")
        for i, header in enumerate(headers, 1):
            print(f"  {i}. {header}")
        
        # Get first few data rows
        print(f"\nFirst 5 data rows:")
        for row_num in range(2, 7):  # Rows 2-6
            try:
                row_data = draft_prioritized_tab.row_values(row_num)
                if row_data:
                    # Show first 8 columns to avoid too much output
                    row_preview = row_data[:8]
                    print(f"  Row {row_num}: {row_preview}")
                else:
                    break
            except:
                break
    else:
        print("\n❌ Could not find 'Draft-Prioritized Multi-Position Analysis' tab")
        print("Available tabs:")
        for ws in worksheets:
            print(f"  - {ws.title}")

if __name__ == "__main__":
    check_existing_tabs()