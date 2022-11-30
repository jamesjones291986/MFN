
####################################
# Power Rankings
####################################

from GameLogDownloader import GameLogDownloader
from SheetsRef import SheetsRef
from util import Config
import pandas as pd

# config
league = 'gfl'
season = '2500'
week = None

# logic
gdl = GameLogDownloader()
gdf = None
if gdl.set_league_season(league, season):
    gdf = gdl.get_game_log()
tdf = pd.DataFrame(gdf['Away Team'].unique(), columns=('team',))
if not week:
    week = int(gdf.Week.astype('Int64').max())
else:
    gdf = gdf.loc[gdf.Week.astype('Int64').le(week)]

# wins
tdf = tdf.merge(gdf.loc[gdf.Win.eq('A')].groupby('Away Team').Season.count().astype('Int64'),
                how='left', left_on='team', right_index=True).fillna(0)
tdf.rename(mapper={'Season': 'awins'}, axis=1, inplace=True)
tdf = tdf.merge(gdf.loc[gdf.Win.eq('H')].groupby('Home Team').Season.count().astype('Int64'),
                how='left', left_on='team', right_index=True).fillna(0)
tdf.rename(mapper={'Season': 'hwins'}, axis=1, inplace=True)
tdf.loc[:, 'Wins'] = tdf.loc[:, 'awins'] + tdf.loc[:, 'hwins']
tdf.drop(['awins', 'hwins'], axis=1, inplace=True)

# ties
tdf = tdf.merge(gdf.loc[gdf.Win.eq('T')].groupby('Away Team').Season.count().astype('Int64'),
                how='left', left_on='team', right_index=True).fillna(0)
tdf.rename(mapper={'Season': 'aties'}, axis=1, inplace=True)
tdf = tdf.merge(gdf.loc[gdf.Win.eq('T')].groupby('Home Team').Season.count().astype('Int64'),
                how='left', left_on='team', right_index=True).fillna(0)
tdf.rename(mapper={'Season': 'hties'}, axis=1, inplace=True)
tdf.loc[:, 'Ties'] = tdf.loc[:, 'aties'] + tdf.loc[:, 'hties']
tdf.drop(['aties', 'hties'], axis=1, inplace=True)

# losses
tdf.loc[:, 'Losses'] = week - tdf.loc[:, 'Wins'] - tdf.loc[:, 'Ties']

# win% (1/2 point for ties)
tdf.loc[:, 'Win%'] = (tdf.loc[:, 'Wins'] + 0.5 * tdf.loc[:, 'Ties']) / week

# yards from scrimmage
yfs = SheetsRef(Config.sheet_lookup[league], f'YFS {season}').get_dataframe().loc[0:31, ['Team', 'OYds', 'DYds']]

# combine
tdf = tdf.merge(yfs, how='inner', left_on='team', right_on='Team').drop('Team', axis=1)

# yards and wtl to games
gdf = gdf.merge(tdf, how='left', left_on='Away Team', right_on='team')
m = {'Wins': 'awins',
     'Ties': 'aties',
     'Losses': 'alosses',
     'OYds': 'aoyds',
     'DYds': 'adyds',
     'Win%': 'awinp'
     }
gdf.rename(mapper=m, axis=1, inplace=True)
gdf.drop('team', axis=1, inplace=True)

gdf = gdf.merge(tdf, how='left', left_on='Home Team', right_on='team')
m = {'Wins': 'hwins',
     'Ties': 'hties',
     'Losses': 'hlosses',
     'OYds': 'hoyds',
     'DYds': 'hdyds',
     'Win%': 'hwinp'
     }
gdf.rename(mapper=m, axis=1, inplace=True)
gdf.drop('team', axis=1, inplace=True)

# numerical conversions
tps = ['aoyds', 'adyds', 'hoyds', 'hdyds']
for t in tps:
    gdf.loc[:, t] = gdf.loc[:, t].astype('float64')
tdf.loc[:, 'OYds'] = tdf.loc[:, 'OYds'].astype('float64')
tdf.loc[:, 'DYds'] = tdf.loc[:, 'DYds'].astype('float64')

# opp yds to teams
tdf.sort_values('team', inplace=True)
tdf = tdf.merge(gdf.groupby('Away Team').hoyds.mean(),
                left_on='team', right_index=True)
tdf = tdf.merge(gdf.groupby('Away Team').hdyds.mean(),
                left_on='team', right_index=True)
tdf = tdf.merge(gdf.groupby('Away Team').hwinp.mean(),
                left_on='team', right_index=True)
tdf = tdf.merge(gdf.groupby('Home Team').aoyds.mean(),
                left_on='team', right_index=True)
tdf = tdf.merge(gdf.groupby('Home Team').adyds.mean(),
                left_on='team', right_index=True)
tdf = tdf.merge(gdf.groupby('Home Team').awinp.mean(),
                left_on='team', right_index=True)
ag = gdf.groupby('Away Team').Season.count().reset_index(drop=True)
hg = gdf.groupby('Home Team').Season.count().reset_index(drop=True)
tdf.loc[:, 'opp_avg_yds_gained'] = (tdf.loc[:, 'hoyds'] * hg + tdf.loc[:, 'aoyds'] * ag) / (hg + ag)
tdf.loc[:, 'opp_avg_yds_allowed'] = (tdf.loc[:, 'hdyds'] * hg + tdf.loc[:, 'adyds'] * ag) / (hg + ag)
tdf.loc[:, 'opp_avg_winp'] = (tdf.loc[:, 'hwinp'] * hg + tdf.loc[:, 'awinp'] * ag) / (hg + ag)
tdf.drop(tps + ['awinp', 'hwinp'], axis=1, inplace=True)

# comparisons
tdf.loc[:, 'oyds_over_avg'] = tdf.loc[:, 'OYds'] - tdf.loc[:, 'opp_avg_yds_allowed']
tdf.loc[:, 'dyds_under_avg'] = tdf.loc[:, 'opp_avg_yds_gained'] - tdf.loc[:, 'DYds']

# z-scores
tdf = tdf.merge((tdf.loc[:, 'oyds_over_avg'] - tdf.loc[:, 'oyds_over_avg'].mean()) / tdf.loc[:, 'oyds_over_avg'].std(),
                left_index=True, right_index=True, suffixes=('', '_y'))
tdf.rename({'oyds_over_avg_y': 'z_off'}, axis=1, inplace=True)
tdf = tdf.merge((tdf.loc[:, 'dyds_under_avg'] - tdf.loc[:, 'dyds_under_avg'].mean()) / tdf.loc[:, 'dyds_under_avg'].std(),
                left_index=True, right_index=True, suffixes=('', '_y'))
tdf.rename({'dyds_under_avg_y': 'z_def'}, axis=1, inplace=True)

tdf = tdf.merge((tdf.loc[:, 'Win%'] - tdf.loc[:, 'Win%'].mean()) / tdf.loc[:, 'Win%'].std(),
                left_index=True, right_index=True, suffixes=('', '_y'))
tdf.rename({'Win%_y': 'z_winp'}, axis=1, inplace=True)
tdf = tdf.merge((tdf.loc[:, 'opp_avg_winp'] - tdf.loc[:, 'opp_avg_winp'].mean()) / tdf.loc[:, 'opp_avg_winp'].std(),
                left_index=True, right_index=True, suffixes=('', '_y'))
tdf.rename({'opp_avg_winp_y': 'z_opp_winp'}, axis=1, inplace=True)

# power rankings
z_mult = {'z_winp': 85,
          'z_opp_winp': 20,
          'z_off': 30,
          'z_def': 35,
          }

raw = 'pwr_raw'
tdf.loc[:, raw] = z_mult['z_winp'] * tdf.loc[:, 'z_winp'] +\
                  z_mult['z_opp_winp'] * tdf.loc[:, 'z_opp_winp'] +\
                  z_mult['z_off'] * tdf.loc[:, 'z_off'] +\
                  z_mult['z_def'] * tdf.loc[:, 'z_def']
rnk = 'pwr_rank'
try:
    tdf.drop(rnk, axis=1, inplace=True)
except KeyError:
    pass
tdf.insert(1, rnk, tdf.loc[:, raw].rank(ascending=False).astype('Int64'))
tdf.sort_values(rnk, inplace=True)

# pretty up
pretty = 'pwr_raw_pretty'
try:
    tdf.drop(pretty, axis=1, inplace=True)
except KeyError:
    pass
tdf.insert(2, pretty, tdf.loc[:, raw].round().astype('Int64'))

# print weight %ages
for z in z_mult:
    print(f'{z}: {round(100 * z_mult[z] / sum(z_mult.values()), 1)}%')

# save to CSV
csv_name = f'{Config.root}/pwr_rnk_{league}_{season}_{week}.csv'
tdf[['team', 'pwr_rank', 'pwr_raw_pretty']].to_csv(csv_name, index=False)

"""
tdf.loc[:, 'tyds_over_avg'] = tdf.loc[:, 'oyds_over_avg'] + tdf.loc[:, 'dyds_under_avg']
tdf.sort_values('tyds_over_avg', ascending=False, inplace=True)
tdf[['team', 'tyds_over_avg']]
"""

pass
