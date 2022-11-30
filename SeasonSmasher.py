import pandas as pd
from util import Config
from glob import iglob


class SeasonSmasher:
    """
    Combine all CSVs for a season into a single CSV
    Makes running analytics much faster
    """
    cols = ['HasBall', 'Game Clock', 'Ball @', 'Quarter',
            'Down', 'YTG', 'OffensivePlay', 'DefensivePlay',
            'YardsGained', 'Home Score', 'Away Score', 'Text']

    def __init__(self):
        self.root = Config.root

    def smash(self, league, season):
        print(f'Hulk smash {league} {season}!')
        r = f'{self.root}\\{league}\\{season}'
        pd.concat((pd.read_csv(f) for f in iglob(f'{r}\\*.csv'))).to_csv(f'{r}.csv', index=False)
        print('Smashed!')

    def playerless(self, league, season):
        """ Take a smashed CSV and create a version without player data """
        print(f'Creating player-less {league} {season}...')
        r = f'{self.root}\\{league}\\{season}'
        pd.read_csv(f'{r}.csv')[self.cols].to_csv(f'{r}_pl.csv', index=False)


if __name__ == '__main__':
    ls_dictionary = {
        'mfn1': [2051, 2052, 2053],
        'lol': [2109, 2110, 2111],
        'ukaf': [1960, 1961, 1962, 1963, 1964],
        'football': [2021, 2022, 2023],
        'norig': [2021, 2022, 2023, 2024],
    }

    ss = SeasonSmasher()

    # one season
    ss.smash('football', 2021)

    # all seasons
    for ll, s in ls_dictionary.items():
        for a in s:
            ss.smash(ll, a)
            ss.playerless(ll, a)
