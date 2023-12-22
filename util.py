"""
utility functions and global configuration
"""

import pandas as pd


class Config:
    root = r'/Users/jamesjones/personal/game_logs/'
    seasons = r'/Users/jamesjones/personal/game_logs/feathers'
    global_file = r'/Users/jamesjones/personal/game_logs/'
    ls_dictionary = {
        'qad': [2043, 2044, 2045, 2046],
        'xfl': [2043, 2044, 2045],
        'paydirt': [1996, 1997, 1998, 1999],
        'USFL': [2002, 2003, 2004, 2005],
        'moguls': [2042, 2043, 2044, 2045],
    }
    sheet_lookup = {
        'qad': '1Nab-IckGA6tG19TOxEu_fYgbNl_7dCZ9hzrTtqcrOO8',
        'xfl': '141ZIAR5ubelkZ4tO7C2QTVFHodlSXNPZQ6i6toVlIRQ',
        'paydirt': '1lRu3yMe7D1j0oJxqVlpPFzh6Dv9JGi2xS6sXzIS-FlY',
        'USFL': '1uhpNHxeXe5xeXR93bAGU6_-vXaTvWvgmRLEd_3Z984s',
    }
    domain_map = {
        'qad': 'fantasy-league',
        'xfl': 'xfl',
        'paydirt': 'paydirt',
        'USFL': 'usflwfl',
        'moguls': 'moguls',
    }
    version_map = {
        'qad': {
            2043: '0.4.6',
            2044: '0.4.6',
            2045: '0.4.6',
            2046: '0.4.6',
        },
        'xfl': {
            2043: '0.4.6',
            2044: '0.4.6',
            2045: '0.4.6',
        },
        'paydirt': {
            1996: '0.4.6',
            1997: '0.4.6',
            1998: '0.4.6',
            1999: '0.4.6',
        },
        'USFL': {
            2002: '0.4.6',
            2003: '0.4.6',
            2004: '0.4.6',
            2005: '0.4.6',
        },
        'moguls': {
            2042: '0.4.6',
            2043: '0.4.6',
            2044: '0.4.6',
            2045: '0.4.6',
        },
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

