from GameLogDownloader import GameLogDownloader
from util import Config
from glob import iglob
import pandas as pd


class SeasonCompiler:
    cols1 = ['HasBall', 'Game Clock', 'Ball @', 'Quarter',
             'Down', 'YTG', 'OffensivePlay', 'DefensivePlay',
             'YardsGained', 'Home Score', 'Away Score', 'Text']
    cols2 = ['Game ID', 'Season', 'Type', 'Week',
             'Home Team', 'H Score', 'Away Team', 'A Score', 'Win']

    @classmethod
    def compile(cls, league, season, players=False, override_path=False):
        log = pd.read_csv(override_path)[cls.cols2]
        dfs, k = [], len(f'{Config.root}/{league}/{season}/')
        for f in iglob(f'{Config.root}/{league}/{season}/*.csv'):
            if f != f'{Config.root}/{league}/{season}/{league}_{season}.csv':
                gid = f[k:-4]
                dfs[len(dfs):] = (pd.read_csv(f)[cls.cols1],)
                dfs[-1].insert(0, 'gid', gid)
                dfs[-1].insert(1, 'League', league)
                log.loc[:, 'Game ID'] = log.loc[:, 'Game ID'].astype(str)
                dfs[-1] = dfs[-1].merge(log, how='left', left_on='gid', right_on='Game ID')
                dfs[-1].drop('gid', axis=1, inplace=True)
        pd.concat(dfs).reset_index().to_feather(f'{Config.root}/{league}/{league}_{season}.feather')
