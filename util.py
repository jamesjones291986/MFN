import os
import pandas as pd

class Config:
    root = r'/Users/jamesjones/personal/game_logs'
    seasons = r'/Users/jamesjones/personal/MFN/feathers'
    global_file = r'/Users/jamesjones/personal/game_logs'
    ls_dictionary = {
        'qad': [2043, 2044, 2045, 2046, 2047, 2048, 2049],
        'xfl': [2043, 2044, 2045, 2046, 2047, 2048],
        'paydirt': [1996, 1997, 1998, 1999, 2000, 2001, 2002],
        'USFL': [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010],
        'moguls': [2042, 2043, 2044, 2045, 2046, 2047],
        'norig': [2028, 2029, 2030, 2031, 2032],
        'pfl': [2026, 2027, 2028, 2029],
        'lol': [2117, 2118, 2119, 2120],
        'nba': [2000, 2001],
    }
    sheet_lookup = {
        'qad': '1Nab-IckGA6tG19TOxEu_fYgbNl_7dCZ9hzrTtqcrOO8',
        'xfl': '141ZIAR5ubelkZ4tO7C2QTVFHodlSXNPZQ6i6toVlIRQ',
        'norig': '1jeVorER82DR-xB81wez2t4tuN1HpJvhmMaihh-8gpnI',
        'paydirt': '1lRu3yMe7D1j0oJxqVlpPFzh6Dv9JGi2xS6sXzIS-FlY',
        'USFL': '1uhpNHxeXe5xeXR93bAGU6_-vXaTvWvgmRLEd_3Z984s',
    }
    domain_map = {
        'qad': 'fantasy-league',
        'xfl': 'xfl',
        'norig': 'norig',
        'paydirt': 'paydirt',
        'USFL': 'usflwfl',
        'pfl': 'pfl',
        'lol': 'lol',
        'moguls': 'moguls',
        'nba': 'nba-league',
    }
    version_map = {
        'qad': {
            2043: '0.4.6',
            2044: '0.4.6',
            2045: '0.4.6',
            2046: '0.4.6',
            2047: '0.4.6',
            2048: '0.4.6',
            2049: '0.4.6',
        },
        'xfl': {
            2043: '0.4.6',
            2044: '0.4.6',
            2045: '0.4.6',
            2046: '0.4.6',
            2047: '0.4.6',
            2048: '0.4.6',
        },
        'paydirt': {
            1996: '0.4.6',
            1997: '0.4.6',
            1998: '0.4.6',
            1999: '0.4.6',
            2000: '0.4.6',
            2001: '0.4.6',
            2002: '0.4.6',
        },
        'USFL': {
            2002: '0.4.6',
            2003: '0.4.6',
            2004: '0.4.6',
            2005: '0.4.6',
            2006: '0.4.6',
            2007: '0.4.6',
            2008: '0.4.6',
            2009: '0.4.6',
            2010: '0.4.6',
        },
        'moguls': {
            2042: '0.4.6',
            2043: '0.4.6',
            2044: '0.4.6',
            2045: '0.4.6',
            2046: '0.4.6',
            2047: '0.4.6',
        },
        'norig': {
            2028: '0.4.6',
            2029: '0.4.6',
            2030: '0.4.6',
            2031: '0.4.6',
            2032: '0.4.6',
        },
        'pfl': {
            2026: '0.4.6',
            2027: '0.4.6',
            2028: '0.4.6',
            2029: '0.4.6',
        },
        'lol': {
            2117: '0.4.6',
            2118: '0.4.6',
            2119: '0.4.6',
            2120: '0.4.6',
        },
        'nba': {
            2000: '0.4.6',
            2001: '0.4.6',
        },
    }

    @classmethod
    def load_feather(cls, league, season):
        try:
            file_path = next(
                file for file in os.listdir(cls.seasons) if f"{league}_{season}" in file and file.endswith(".feather"))
            return pd.read_feather(os.path.join(cls.seasons, file_path)).drop('index', axis=1)
        except (StopIteration, FileNotFoundError):
            # Handle the case where the file is not found
            pass

    @classmethod
    def load_feather_with_players(cls, league, season):
        try:
            file_path = next(file for file in os.listdir(cls.seasons) if
                             f"{league}_{season}_with_players" in file and file.endswith(".feather"))
            return pd.read_feather(os.path.join(cls.seasons, file_path)).drop('index', axis=1)
        except (StopIteration, FileNotFoundError):
            # Handle the case where the file is not found
            pass

    @classmethod
    def load_all_seasons(cls):
        all_seasons_df = pd.concat(
            (cls.load_feather(league, year) for league, years in cls.ls_dictionary.items() for year in years),
            ignore_index=True)
        return all_seasons_df

    @classmethod
    def load_specific_feather(cls, file_name):
        try:
            return pd.read_feather(os.path.join(cls.seasons, file_name)).reset_index(drop=True)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # Handle the case where the file is not found or is empty by returning an empty DataFrame
            return pd.DataFrame()



