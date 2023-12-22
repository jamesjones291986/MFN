import os

import pandas as pd
import requests
#from SheetsRef import SheetsRef
from util import Config


class GameLogDownloader:
    sheet_lookup = Config.sheet_lookup

    def __init__(self, league=None, season=None):
        self.league, self.season = league, season
        self.root = Config.root
        self.ls_sheet = None

    def set_league_season(self, league, season):
        self.league, self.season = league, str(season)
        return True

    def get_game_log(self):
        return SheetsRef(self.sheet_lookup[self.league], str(self.season)).get_dataframe()

    @staticmethod
    def save_log(url, save_loc):
        with open(save_loc, 'wb') as f, requests.get(url) as r:
            for line in r.iter_lines():
                f.write(line + '\n'.encode())

    def download_season(self, override_path=False):
        f = f'{self.root}/{self.league}/{self.season}'
        if not os.path.isdir(f):
            os.makedirs(f)
        r = f'https://{Config.domain_map[self.league]}.myfootballnow.com/log/download/'
        if override_path:
            if '.xls' in override_path:
                self.ls_sheet = pd.read_excel(override_path)
            elif '.csv' in override_path:
                self.ls_sheet = pd.read_csv(override_path)
            elif '.feather' in override_path:
                self.ls_sheet = pd.read_feather(override_path)
        else:
            self.ls_sheet = self.get_game_log()
        for gid in self.ls_sheet['Game ID']:
            if self.ls_sheet.loc[self.ls_sheet['Game ID'].eq(gid), 'Captured'].isin([0, '0']).item():
                print(f'Downloading {gid} for {self.league}...')
                self.save_log(f'{r}{gid}', f + f'/{gid}.csv')
        return True
