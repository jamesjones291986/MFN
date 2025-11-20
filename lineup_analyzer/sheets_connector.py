#!/usr/bin/env python3
"""
Google Sheets Connector for MFN Lineup Analyzer
Handles authentication and data retrieval from Google Sheets.
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from pathlib import Path


class LineupSheetsConnector:
    """Connects to Google Sheets for lineup analysis."""
    
    def __init__(self, credentials_path: str = None, verbose: bool = True):
        """Initialize the Google Sheets connector."""
        self.verbose = verbose
        
        # Set up credentials path
        if credentials_path is None:
            credentials_path = Path(__file__).parent / "credentials.json"
        
        # Define the scope for Google Sheets API
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        try:
            # Load credentials and authorize
            creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
            self.client = gspread.authorize(creds)
            
            if self.verbose:
                print("✅ Successfully connected to Google Sheets")
                
        except Exception as e:
            print(f"❌ Failed to connect to Google Sheets: {e}")
            raise
            
    def get_sheet(self, sheet_id: str):
        """Get a specific Google Sheet by ID."""
        try:
            spreadsheet = self.client.open_by_key(sheet_id)
            if self.verbose:
                print(f"📋 Opened sheet: {spreadsheet.title}")
            return spreadsheet
        except Exception as e:
            print(f"❌ Failed to open sheet {sheet_id}: {e}")
            raise
            
    def get_worksheet_data(self, sheet_id: str, worksheet_name: str) -> pd.DataFrame:
        """Get data from a specific worksheet as a pandas DataFrame."""
        try:
            spreadsheet = self.get_sheet(sheet_id)
            worksheet = spreadsheet.worksheet(worksheet_name)
            
            # Get all values
            data = worksheet.get_all_values()
            
            if not data:
                if self.verbose:
                    print(f"⚠️ Worksheet '{worksheet_name}' is empty")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            
            if self.verbose:
                print(f"📊 Loaded {len(df)} rows from '{worksheet_name}'")
                
            return df
            
        except Exception as e:
            print(f"❌ Failed to get data from '{worksheet_name}': {e}")
            raise