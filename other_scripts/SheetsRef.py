import os.path

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError


class SheetsRef:
    def __init__(self, sheet_id, sheet_name):
        self.sheet_id, self.sheet_name, self.df = sheet_id, sheet_name, None
        self.data = self.get_sheet_data()

    def get_sheet_data(self):
        creds = None
        # If modifying these scopes, delete the file token.json.
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            # if creds and creds.expired and creds.refresh_token:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
            except RefreshError:
                creds.refresh(Request())
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheet_id,
                                        range=self.sheet_name).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
                return

            return values
        except HttpError as err:
            print(err)

    def create_dataframe(self):
        if not self.data:
            self.data = self.get_sheet_data()
        self.df = pd.DataFrame(columns=self.data[0], data=self.data[1:])

    def get_dataframe(self):
        if self.df is None:
            self.create_dataframe()
        return self.df
