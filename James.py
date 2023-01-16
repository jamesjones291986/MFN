import pandas as pd
import numpy as np
from glob import iglob
from util import Config
from GameLogDownloader import GameLogDownloader
from SeasonCompiler import SeasonCompiler

df = pd.concat((Config.load_feather(k, y) for k, v in Config.ls_dictionary.items() for y in v)).fillna(0)

# df = pd.read_feather('/Users/jamesjones/game_logs/xfl/xfl_2043.feather').fillna(0)

# download_all_logs()

path = '/Users/jamesjones/game_logs/xfl/2043/xfl_2043.csv'

gdl = GameLogDownloader()
gdl.set_league_season('xfl', 2043)
gdl.download_season(path)

# Compile a season
SeasonCompiler.compile('qad', 2039)
SeasonCompiler.compile('norig', 2027, players=True)
# specify path to game logs
SeasonCompiler.compile('qad', 2043, override_path='/Users/jamesjones/game_logs/qad/2043/qad_2043.csv')
SeasonCompiler.compile('norig', 2028, override_path='/Users/jamesjones/game_logs/norig/2028/norig_2028.csv')
SeasonCompiler.compile('paydirt', 1996, override_path='/Users/jamesjones/game_logs/paydirt/1996/paydirt_1996.csv')
SeasonCompiler.compile('USFL', 2002, override_path='/Users/jamesjones/game_logs/USFL/2002/USFL_2002.csv')
SeasonCompiler.compile('pfl', 2026, override_path='/Users/jamesjones/game_logs/pfl/2026/pfl_2026.csv')
SeasonCompiler.compile('lol', 2117, override_path='/Users/jamesjones/game_logs/lol/2117/lol_2117.csv')
SeasonCompiler.compile('xfl', 2043, override_path='/Users/jamesjones/game_logs/xfl/2043/xfl_2043.csv')

global_off = '/Users/jamesjones/game_logs/MFN Global Reference - OffPlays.csv'
global_def = '/Users/jamesjones/game_logs/MFN Global Reference - DefPlays.csv'
global_off_ref = pd.read_csv(global_off)
global_def_ref = pd.read_csv(global_def)

run_plays = ('Inside Run', 'Outside Run')
pass_plays = ('Short Pass', 'Medium Pass', 'Long Pass')
all_plays = run_plays + pass_plays
def_excludes = (None, 'FG Block', 'Punt Return', 'Kick Return', 'Onsides Kick Return Onside Kick Return')
off_excludes = (None, 'Field Goal', 'Punt', 'Victory', 'Kickoff', 'Onsides Kick Onside Kick')

df = pd.concat((pd.read_feather(f) for f in iglob(Config.seasons + '/*.feather'))).fillna(0)
df = pd.concat((Config.load_feather(k, y) for k, v in Config.ls_dictionary.items() for y in v)).fillna(0)

# This works
ypp = df.groupby(['OffensivePlay', 'DefensivePlay']).agg({'YardsGained': ['mean', 'count']})
ypp = ypp.reset_index()
ypp.to_csv('/Users/jamesjones/game_logs/ypp_off_def_3.csv')

ypp_offense = df.groupby('OffensivePlay', as_index=False).agg({'YardsGained': ['mean', 'count']})
ypp_defense = df.groupby('DefensivePlay', as_index=False).agg({'YardsGained': ['mean', 'count']})
ypp_offense.to_csv('/Users/jamesjones/game_logs/ypp_off3.csv')
ypp_defense.to_csv('/Users/jamesjones/game_logs/ypp_def3.csv')

ypp_offense = df.groupby('OffensivePlay', as_index=False)['YardsGained'].mean() \
    .sort_values('YardsGained', ascending=False)
ypp_defense = df.groupby('DefensivePlay', as_index=False)['YardsGained'].mean() \
    .sort_values('YardsGained', ascending=True)

################################################################


# Below are new projects

off_plays_113 = ['Shotgun Normal HB Flare', 'Singleback Normal TE Quick Out', 'Singleback Normal HB Release Mid',
                 'Singleback Normal SE Quick Hit', 'Singleback Normal WR Quick In', 'Singleback Normal FL Post']
def_ypp_113 = df.loc[df.OffensivePlay.isin(off_plays_113)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_113.columns[0]])

def_plays_113 = ['Dime Normal Double WR1 WR2']
off_ypp_113 = df.loc[df.DefensivePlay.isin(def_plays_113)].groupby('OffensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[off_ypp_113.columns[0]], ascending=False)


team = ['HOU']
off_plays = ['Singleback Normal TE Quick Out', 'Singleback Normal HB Release Mid',
             'Singleback Normal SE Quick Hit', 'Singleback Normal WR Quick In', 'Singleback Normal FL Post']
def_plays = ['play2']
off_ypp = df.loc[df.DefensivePlay.isin(def_plays)].groupby('OffensivePlay').agg({'YardsGained': ['mean', 'count']})
def_ypp = df.loc[df.OffensivePlay.isin(off_plays)].groupby('DefensivePlay').agg({'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp.columns[0]])

off_ypp = df.loc[df.DefensivePlay.isin(def_plays) & df.HasBall.isin(team)].groupby('OffensivePlay').agg(
    {'YardsGained': ['mean', 'count']})
def_ypp = df.loc[df.OffensivePlay.isin(off_plays) & df.HasBall.isin(team)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']})
