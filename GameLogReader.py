"""
class GameLogReader

Collection of various functions for GameLog objects
"""

import pandas as pd
from util import Config
from SheetsRef import SheetsRef


class GameLogReader:
    sheet_lookup = Config.sheet_lookup

    def __init__(self, league, season, gid, home=None, away=None):
        self.league, self.season, self.gid = league, season, gid
        self.gdf = self.load_log()
        if not home or not away:
            team_map = SheetsRef(self.sheet_lookup['global'], 'TeamMap').get_dataframe()
            game = SheetsRef(self.sheet_lookup[self.league], str(self.season)).get_dataframe()
            game = game.loc[game['Game ID'].astype('int64').eq(gid)]
            self.game = game
            home = team_map.loc[team_map.League.eq(league) &
                                team_map.Ssn.eq(str(season)) &
                                team_map.Long.eq(game['Home Team'])].Abb
            away = team_map.loc[team_map.League.eq(league) &
                                team_map.Ssn.eq(str(season)) &
                                team_map.Long.eq(game['Away Team'])].Abb
        self.home, self.away = home, away

    def load_log(self):
        return pd.read_csv(f'{Config.root}\\{self.league}\\{self.season}\\{self.gid}.csv')

    def create_possessions(self):
        if not self.gdf:
            self.gdf = self.load_log()
        self.gdf.insert(self.gdf.shape[1] - 1, 'poss', 0)


glr = GameLogReader('norig', 2024, 1000)
backup = glr.gdf.copy()

glr.gdf = backup.copy()

# Setup
glr.gdf.HasBall.mask(glr.gdf.OffensivePlay.eq('Kickoff'), pd.NA, inplace=True)
glr.gdf.dropna(subset='HasBall', inplace=True)
glr.gdf.YardsGained.fillna(0, inplace=True)
glr.gdf.YardsGained.mask(glr.gdf.OffensivePlay.eq('Field Goal'), 0, inplace=True)
glr.gdf.YardsGained.mask(glr.gdf.OffensivePlay.eq('Punt'), 0, inplace=True)

# Yards to Goal Line (YTGL)
glr.gdf.insert(glr.gdf.shape[1], 'YTGL',
               glr.gdf['Ball @'].str.partition(' ')[2].astype('int64'))
glr.gdf.YTGL.mask(glr.gdf.HasBall.eq(glr.gdf['Ball @'].str.partition(' ')[0]),
                  100 - glr.gdf['Ball @'].str.partition(' ')[2].astype('int64'), inplace=True)

# Create possession table
glr.gdf.insert(glr.gdf.shape[1], 'poss_chg',
               glr.gdf.HasBall.ne(glr.gdf.HasBall.shift()) &
               ~glr.gdf.HasBall.isna() &
               ~glr.gdf.HasBall.shift().isna() |
               (glr.gdf.Quarter.isin((3, 5)) & glr.gdf.Quarter.shift().isin((2, 4))))
glr.gdf.insert(glr.gdf.shape[1], 'poss',
               glr.gdf.poss_chg.cumsum())
glr.gdf.drop('poss_chg', axis=1, inplace=True)
gb = glr.gdf.groupby('poss')
gb_nxp = glr.gdf.loc[glr.gdf.Down.lt(5)].groupby('poss')  # possessions without extra point plays
glr.pdf = pd.DataFrame(index=gb.indices.keys())

# possession start
glr.pdf.insert(glr.pdf.shape[1], 'start',
               gb['YTGL'].first())

# possession yards gained
glr.pdf.insert(glr.pdf.shape[1], 'yards_gained',
               (gb['YTGL'].first() - gb_nxp['YTGL'].last() + gb_nxp['YardsGained'].last()).astype('int64'))

# possession points
glr.pdf.insert(glr.pdf.shape[1], 'points',
               pd.NA  # safety -2
              )

# possession turnover

# possession sacks

# possession penalties against offense

# possession penalty yards against offense

# possession penalties against defense

# possession penalty yards against defense

a = glr.gdf[['HasBall', 'Quarter', 'Game Clock', 'HasBall',
             'Ball @', 'YTGL', 'Down', 'YTG', 'YardsGained', 'poss',
             'OffensivePlay', 'DefensivePlay',
             'Text']]
