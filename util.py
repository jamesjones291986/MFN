"""
utility functions and global configuration
"""

import pandas as pd


class Config:
    root = r'/Users/jamesjones/game_logs/'
    seasons = r'/Users/jamesjones/game_logs/feathers'
    ls_dictionary = {
        'qad': [2039],
        'xfl': [2042],
    }
    sheet_lookup = {
        'qad': '1Nab-IckGA6tG19TOxEu_fYgbNl_7dCZ9hzrTtqcrOO8',
        'xfl': '141ZIAR5ubelkZ4tO7C2QTVFHodlSXNPZQ6i6toVlIRQ',
    }
    domain_map = {
        'qad': 'fantasy-league',
        'xfl': 'xfl',
    }
    version_map = {
        'qad': {
            2039: '0.4.6',
        },
        'xfl': {
            2042: '0.4.6',
        }
    }

    @classmethod
    def load_feather(cls, league, season):
        try:
            return pd.read_feather(f'{cls.root}/{league}/{league}_{season}.feather').drop('index', axis=1)
        except KeyError:
            return pd.read_feather(f'{cls.root}/{league}/{league}_{season}.feather')

    @classmethod
    def load_feather_with_players(cls, league, season):
        try:
            return pd.read_feather(f'{cls.root}/{league}/{league}_{season}_with_players.feather').drop('index', axis=1)
        except KeyError:
            return pd.read_feather(f'{cls.root}/{league}/{league}_{season}_with_players.feather')

