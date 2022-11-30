import pandas as pd
import numpy as np
from util import Config
from SheetsRef import SheetsRef
from GameLogDownloader import GameLogDownloader
from SeasonCompiler import SeasonCompiler
from glob import iglob

"""
Down 6 = kickoff
Down 7 = extra point / 2pt attempt
"""

# Configuration
buckets = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29',
           '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
           '60-64', '65-69', '70-74', '75-79', '80-84', '85-89',
           '90-94', '95-99']

# global_off_ref = SheetsRef(Config.sheet_lookup['global'], 'OffPlays').get_dataframe()
# global_def_ref = SheetsRef(Config.sheet_lookup['global'], 'DefPlays').get_dataframe()

global_off = '/Users/jamesjones/game_logs/MFN Global Reference - OffPlays.csv'
global_def = '/Users/jamesjones/game_logs/MFN Global Reference - DefPlays.csv'
global_off_ref = pd.read_csv(global_off)
global_def_ref = pd.read_csv(global_def)

run_plays = ('Inside Run', 'Outside Run')
pass_plays = ('Short Pass', 'Medium Pass', 'Long Pass')
all_plays = run_plays + pass_plays
def_excludes = (None, 'FG Block', 'Punt Return', 'Kick Return', 'Onsides Kick Return Onside Kick Return')
off_excludes = (None, 'Field Goal', 'Punt', 'Victory', 'Kickoff', 'Onsides Kick Onside Kick')


def download_all_logs():
    gdl = GameLogDownloader()

    for k, v in Config.ls_dictionary.items():
        for y in v:
            if not gdl.set_league_season(k, y):
                print(f'ERROR! {k} {y} not set!')
            if not gdl.download_season():
                print(f'ERROR! {k} {y} not downloaded!')


def adj_ev(dd, grouper, plays=all_plays, sort='desc'):
    dx = dd.loc[dd.YTGL.ge(20) & dd.YTGL.lt(80) & dd.Down.isin([1, 2, 3])].copy()
    dx = dx.loc[dx.OffPlayType.isin(plays) &
                ~dx.DefensivePlay.isin(def_excludes) &
                ~dx.OffensivePlay.isin(off_excludes)]

    sit_score = dx.groupby(['ytgl_bucket', 'Down', 'YTG']).ev.mean()
    dx['ev_adj'] = dx.ev - dx.merge(sit_score, how='left',
                                    left_on=['ytgl_bucket', 'Down', 'YTG'],
                                    right_index=True)['ev_y']

    ev_adj_count = dx.groupby(grouper).ev_adj.count()
    ev_adj_score = dx.groupby(grouper).ev_adj.mean()

    rows = []
    for p in dx[grouper].unique():
        try:
            g = ev_adj_score[p]
        except KeyError:
            g = np.nan
        try:
            c = ev_adj_count[p]
        except KeyError:
            c = np.nan
        if c > 50:
            rows[len(rows):] = [{grouper: p,
                                 'ev_adj': round(g, 3),
                                 'cnt': c
                                 }]
    sort_map = {'asc': True, 'desc': False}
    return pd.DataFrame(rows).sort_values('ev_adj', ascending=sort_map[sort]).reset_index(drop=True)


def format_df(dd):
    # Set versions
    dd['version'] = pd.concat([dd.League, dd.Season.astype(str)], axis=1).apply(
        lambda x: Config.version_map[x['League']][int(x['Season'])], axis=1)

    # Offensive Play Type and personnel
    dd[['OffPlayType', 'OffPersonnel']] = dd.merge(
        global_off_ref, how='left', left_on='OffensivePlay', right_on='OffPlay')[['OffPlayType', 'OffPersonnel']]

    # OPTIONAL 0.4.6 only
    dd = dd.loc[dd.version.eq('0.4.6')]

    # Convert home/away teams into acronyms
    # A two-minute warning on a touchdown play will cause a bug without this
    dd.HasBall.mask(dd.Text.eq('Timeout for two minute warning.'),
                    dd.HasBall.shift(-1), inplace=True)

    # Use FG plays or touchdowns to discern who is which acronym
    dd.drop('hh', axis=1, inplace=True, errors='ignore')
    dd.insert(0, 'hh', '')
    dd['hh'].mask(dd['OffensivePlay'].eq('Field Goal') &
                  dd['Home Score'].eq(dd['Home Score'].shift() + 3),
                  dd.HasBall, inplace=True)
    dd['hh'].mask(dd.Down.shift(-1).eq(7) &
                  dd['Home Score'].eq(dd['Home Score'].shift() + 6),
                  dd.HasBall.shift(-1), inplace=True)
    dd.drop('home_ac', axis=1, inplace=True, errors='ignore')
    dd.insert(0, 'home_ac', '')
    dd['home_ac'] = dd.merge(dd.groupby(['League', 'Game ID'])['hh'].max(),
                             how='left', left_on=['League', 'Game ID'], right_index=True)['hh_y']

    dd.drop('aa', axis=1, inplace=True, errors='ignore')
    dd.insert(0, 'aa', '')
    dd['aa'].mask(dd['OffensivePlay'].eq('Field Goal') &
                  dd['Away Score'].eq(dd['Away Score'].shift() + 3),
                  dd.HasBall, inplace=True)
    dd['aa'].mask(dd.Down.shift(-1).eq(7) &
                  dd['Away Score'].eq(dd['Away Score'].shift() + 6),
                  dd.HasBall.shift(-1), inplace=True)
    dd.drop('away_ac', axis=1, inplace=True, errors='ignore')
    dd.insert(0, 'away_ac', '')
    dd['away_ac'] = dd.merge(dd.groupby(['League', 'Game ID'])['aa'].max(),
                             how='left', left_on=['League', 'Game ID'], right_index=True)['aa_y']

    # dealing with one team getting shut out
    dd.HasBall.fillna('', inplace=True)
    dd['hh'].mask(dd.home_ac.eq('') & dd.HasBall.ne(dd.away_ac),
                  dd.HasBall, inplace=True)
    dd['home_ac'] = dd.merge(dd.groupby(['League', 'Game ID'])['hh'].max(),
                             how='left', left_on=['League', 'Game ID'], right_index=True)['hh_y']
    dd['aa'].mask(dd.away_ac.eq('') & dd.HasBall.ne(dd.home_ac),
                  dd.HasBall, inplace=True)
    dd['away_ac'] = dd.merge(dd.groupby(['League', 'Game ID'])['aa'].max(),
                             how='left', left_on=['League', 'Game ID'], right_index=True)['aa_y']

    # testing and cleanup
    if ((dd.away_ac.eq('') | dd.home_ac.eq('')) | dd.away_ac.eq(dd.home_ac)).sum():
        # Only prints if away/home teams are equal or unresolved
        a = dd.loc[
            (dd.away_ac.eq('') | dd.home_ac.eq('')) | dd.away_ac.eq(dd.home_ac), ['League', 'Game ID']].value_counts()
        print(f'ERROR! Game IDs with unresolved home/away teams: {a}')
    else:
        dd.drop(['aa', 'hh'], axis=1, inplace=True)

    # Set defending team
    dd['DefTeam'] = dd.loc[:, 'away_ac']
    dd.loc[:, 'DefTeam'].mask(dd.DefTeam.eq(dd.HasBall), dd.home_ac, inplace=True)
    dd.loc[:, 'DefTeam'].mask(dd.HasBall.eq(''), '', inplace=True)

    # Scoring Plays (for possession)
    dd.drop('score', axis=1, inplace=True, errors='ignore')
    dd.insert(14, 'score', 0)
    dd['score'].mask(dd['Game ID'].eq(dd['Game ID'].shift()) &
                     dd.Down.ne(7) &  # don't count extra points/2pt conversions
                     (dd['Home Score'].ne(dd['Home Score'].shift()) |
                      dd['Away Score'].ne(dd['Away Score'].shift())),
                     1, inplace=True)

    # Value of scoring play to home team
    dd.drop('h_pts', axis=1, inplace=True, errors='ignore')
    dd.insert(15, 'h_pts', 0)
    dd['h_pts'].mask(dd['score'].eq(1),
                     dd['Home Score'] - dd['Home Score'].shift(), inplace=True)
    dd['h_pts'].mask(dd['score'].eq(1) & dd['h_pts'].eq(0),
                     dd['Away Score'].shift() - dd['Away Score'], inplace=True)

    # Roll values back

    dd.drop('h_pts_lb', axis=1, inplace=True, errors='ignore')
    dd.insert(16, 'h_pts_lb', dd.h_pts)
    dd.h_pts_lb.replace(0, pd.NA, inplace=True)
    dd.h_pts_lb.mask(dd.Text.isin(['End of half.',
                                   'End of fourth quarter.',
                                   'End of OT 1.',
                                   'End of OT 2.',
                                   'End of OT 3.']),
                     0, inplace=True)
    dd.h_pts_lb.fillna(method='bfill', inplace=True)
    dd.h_pts_lb = dd.h_pts_lb.astype('Int64')

    # Expected values
    dd.drop('ev', axis=1, inplace=True, errors='ignore')
    dd.insert(17, 'ev', dd.h_pts_lb)
    dd.ev.mask(dd.home_ac.ne(dd.HasBall),
               -dd.ev, inplace=True)

    # Value TD correctly and roll to EV
    temp = dd.loc[dd.Down.eq(7) & dd.OffensivePlay.eq('Field Goal')]
    xp_value = 1 - temp.Text.str.contains('NO GOOD').sum() / temp.shape[0]
    temp = dd.loc[dd.Down.eq(7) & dd.OffensivePlay.ne('Field Goal')]
    twopt_value = 2 * temp.Text.str.contains('CONVERSION GOOD').sum() / temp.shape[0]
    m = (xp_value + twopt_value) / 2
    dd.loc[:, 'ev'] = dd.ev.astype('float64')
    dd.ev.replace({6: 6 + m, -6: -6 - m}, inplace=True)

    # Yards to Goal Line
    dd.drop('YTGL', axis=1, inplace=True, errors='ignore')
    dd.insert(6, 'YTGL', dd['Ball @'].str.partition(' ')[2].astype('Int64'))
    dd.YTGL.mask(dd.HasBall.eq(dd['Ball @'].str.partition(' ')[0]),
                 100 - dd['Ball @'].str.partition(' ')[2].astype('Int64'), inplace=True)
    dd.YTGL.mask(dd.Down.isin([6, 7]), pd.NA, inplace=True)

    # Bucket YTGL
    bucket_size = 5
    dd.drop('ytgl_bucket', axis=1, inplace=True, errors='ignore')
    dd.insert(7, 'ytgl_bucket', dd.YTGL.floordiv(bucket_size).mul(bucket_size))
    dd.loc[:, 'ytgl_bucket'] = dd.ytgl_bucket.astype(str) + \
                               pd.Series('-', index=dd.index) + \
                               (dd.ytgl_bucket.add(4)).astype(str)

    # Play flags
    dd['punt'] = dd.OffensivePlay.eq('Punt')
    dd['fg'] = dd.OffensivePlay.eq('Field Goal')
    dd['gfi'] = ~dd.OffensivePlay.isin([None, 'Punt', 'Field Goal', 'Kickoff',
                                        'Onsides Kick Onside Kick', 'Victory'])
    dd['fb_dive'] = dd.OffensivePlay.eq('Goal Line Normal FB Dive')

    no_0 = dd.loc[dd.ev.ne(0)]
    return no_0


def scout_off_def(temp_df, team):
    d1 = temp_df.loc[temp_df.away_ac.eq(team) | temp_df.home_ac.eq(team)]
    do = d1.loc[d1.HasBall.eq(team)]
    dd = d1.loc[d1.HasBall.ne(team) & ~d1.HasBall.isna()]

    d_off = do.loc[~do.OffensivePlay.isin(off_excludes)].groupby('OffensivePlay').OffensivePlay.count()
    d_def = dd.loc[~dd.DefensivePlay.isin(def_excludes)].groupby('DefensivePlay').DefensivePlay.count()

    off_pp = (100 * d_off / do.loc[~do.OffensivePlay.isin(off_excludes), 'OffensivePlay'].count()).round(
        2).sort_values(ascending=False)
    def_pp = (100 * d_def / dd.loc[~dd.DefensivePlay.isin(def_excludes), 'DefensivePlay'].count()).round(
        2).sort_values(ascending=False)

    print(f'\nOffensive plays called by {team} at least 2% of the time')
    print((off_pp.loc[off_pp.ge(2)].astype(str) + '%').to_string().replace('OffensivePlay\n', ''))
    print(f'\nDefensive plays called by {team} at least 2% of the time')
    print((def_pp.loc[def_pp.ge(2)].astype(str) + '%').to_string().replace('DefensivePlay\n', ''))


def scout_run_vs_pass_downs(temp_df, team):
    d1 = temp_df.loc[temp_df.away_ac.eq(team) | temp_df.home_ac.eq(team)]
    do = d1.loc[d1.HasBall.eq(team)]
    # dd = d1.loc[d1.HasBall.ne(team) & ~d1.HasBall.isna()]
    do['dist'] = '0-2'
    do.dist.mask(do.YTG.ge(3), '3-5', inplace=True)
    do.dist.mask(do.YTG.ge(6), '6-9', inplace=True)
    do.dist.mask(do.YTG.ge(10), '10-14', inplace=True)
    do.dist.mask(do.YTG.ge(15), '15+', inplace=True)

    c = ['Down', 'dist', 'OffPlayType']
    r = ['Inside Run', 'Outside Run']
    p = ['Short Pass', 'Medium Pass', 'Long Pass']
    gb = do.groupby(c).OffPlayType.count()
    gb.index.to_frame().reset_index().merge(gb, how='left', left_on=c, right_index=True)


def def_against_personnel():
    pass


def scout(league, season, team):
    tdf = format_df(Config.load_feather(league, season))
    print(f'Scouting Report for {team} in {league} {season}')
    scout_off_def(tdf, team)
    scout_run_vs_pass_downs(tdf, team)


# Load all seasons
df = Config.load_feather('qad', 2039)
df.Season.isna().sum()
df = pd.concat((pd.read_feather(f) for f in iglob(Config.seasons + '/*.feather')))
df = format_df(pd.concat((pd.read_feather(f) for f in iglob(Config.seasons + '/*.feather'))))
df = format_df(pd.concat((Config.load_feather(k, y) for k, v in Config.ls_dictionary.items() for y in v)).reset_index
               (drop=True))
df = pd.concat((Config.load_feather(k, y) for k, v in Config.ls_dictionary.items() for y in v)).reset_index(drop=True)
df = format_df(df)

# Scouting
scout('pfl', 2024, 'HOU')

# download_all_logs()

path = '/Users/jamesjones/game_logs/qad/2039/qad_2039.csv'

gdl = GameLogDownloader()
gdl.set_league_season('qad', 2039)
gdl.download_season(path)

# Compile a season
SeasonCompiler.compile('qad', 2039)
SeasonCompiler.compile('norig', 2027, players=True)
# specify path to game logs
SeasonCompiler.compile('qad', 2039, override_path='/Users/jamesjones/game_logs/qad/2039/qad_2039.csv')
SeasonCompiler.compile('xfl', 2042, override_path='/Users/jamesjones/game_logs/xfl/2042/xfl_2042.csv')

"""
for k, v in Config.ls_dictionary.items():
    for y in v:
        print(k, y)
        compile_season_players(k, y)
"""

#################

# Set versions
# df['version'] = df[['League', 'Season']].apply(
#     lambda x: Config.version_map[x['League']][int(x['Season'])], axis=1)

# Scouting
scout(df, 'NYK')

# Best defensive plays
off_play_adj_ev = adj_ev(df, 'OffensivePlay', all_plays, 'desc')
flat_zone = df.loc[df.DefensivePlay.eq('4-3 Normal Man Under 1')]
off_play_adj_ev_flat_zone = adj_ev(flat_zone, 'OffensivePlay', all_plays, 'desc')
off_play_adj_ev_no_zone = adj_ev(df.loc[df.DefensivePlay.ne('4-3 Normal Man Under 1')],
                                 'OffensivePlay', all_plays, 'desc')

# Moving feather files to csv
df = pd.read_feather('/Users/jamesjones/game_logs/xfl/xfl_2042.feather')
df.to_csv('/Users/jamesjones/game_logs/xfl/xfl_2042.feather')

cols2 = ['Game ID', 'Season', 'Type', 'Week',
         'Home Team', 'H Score', 'Away Team', 'A Score', 'Win']

df = pd.read_csv('/Users/jamesjones/game_logs/qad/2039/qad_2039.csv')[cols2]



##############################################################################################

# Aggregate!!!
r = df.groupby(['Down', 'YTG', 'ytgl_bucket']).ev.mean()
r2 = df.groupby(['Down']).ev.mean()

print('Down and distance, anywhere on the field:')
print('Positive means go for it, negative means punt')
r3 = df.loc[df.Down.eq(4)].groupby(['YTG', 'punt']).ev.mean()
for i in range(1, 11):
    print(f'4th and {i}: {r3[i][False] - r3[i][True]}')

print('Down and distance, 35-55 yards from goal line:')
print('Positive means go for it, negative means punt')
r4 = df.loc[df.Down.eq(4) & df.YTGL.ge(35) & df.YTGL.le(55)].groupby(['YTG', 'punt']).ev.mean()
for i in range(1, 11):
    print(f'4th and {i}: {r4[i][False] - r4[i][True]}')

print('Kick FG or punt?')
print('Positive means kick FG, negative means punt')
r5 = df.loc[df.Down.eq(4) & df.YTGL.ge(25) & df.YTGL.le(40)].groupby(['YTGL', 'punt']).ev.mean()
r6 = df.loc[df.Down.eq(4) & df.YTGL.ge(25) & df.YTGL.le(40)].groupby(['YTGL', 'fg']).ev.mean()
for i in range(16):
    print(f'From the {25 + i}: {r5[25 + i][True] - r6[25 + i][True]}')

print('Kick FG or go for it?')
r7 = df.loc[df.Down.eq(4) & df.YTGL.le(35)].groupby(['YTG', 'YTGL', 'gfi']).ev.mean()
r8 = df.loc[df.Down.eq(4) & df.YTGL.le(35)].groupby(['YTG', 'YTGL', 'fg']).ev.mean()
for j in range(5, 9):
    for i in range(1, 36):
        if j <= i:
            try:
                m = r8[j][i][True] - r7[j][i][True]
                if m >= 0:
                    print(f'4th and {j} from the {i}: Kick FG')
                else:
                    print(f'4th and {j} from the {i}: Go for it!')
            except KeyError:
                pass

print('Kick FG, punt, or go for it?')
r10 = df.loc[df.Down.eq(4)].groupby(['YTG', 'ytgl_bucket', 'gfi']).ev.mean()
r11 = df.loc[df.Down.eq(4)].groupby(['YTG', 'ytgl_bucket', 'fg']).ev.mean()
r12 = df.loc[df.Down.eq(4)].groupby(['YTG', 'ytgl_bucket', 'punt']).ev.mean()
for i in range(1, 9):
    for b in buckets:
        try:
            g = r10[i][b][True]
        except KeyError:
            g = -99
        try:
            f = r11[i][b][True]
        except KeyError:
            f = -99
        try:
            p = r12[i][b][True]
        except KeyError:
            p = -99
        if g > f and g > p:
            m = f'Go for it ({round(g - max(f, p), 3)} over {("FG" if f == max(f, p) else "Punt")})'
        if f > g and f > p:
            m = f'Kick FG ({round(f - max(g, p), 3)} over {("Punt" if p == max(g, p) else "Go for it")})'
        if p > f and p > g:
            m = f'Punt ({round(p - max(f, g), 3)} over {("FG" if f == max(f, g) else "Go for it")})'
        print(f'4th and {i}, yards to GL {b}: {m}')

rows = []
for b in buckets:
    for i in range(1, 9):
        try:
            g = r10[i][b][True]
        except KeyError:
            g = -99
        try:
            f = r11[i][b][True]
        except KeyError:
            f = -99
        try:
            p = r12[i][b][True]
        except KeyError:
            p = -99
        rows[len(rows):] = [{'down': 4,
                             'distance': i,
                             'ytgl': b,
                             'gfi': round(g, 3),
                             'fg': round(f, 3),
                             'punt': round(p, 3)}]
d = pd.DataFrame(rows)
d.to_csv(Config.root + '/4th_dd.csv', index=False)

# Downs 1-3
r13_a = df.loc[df.Down.isin([1, 2, 3])].groupby(['ytgl_bucket', 'Down', 'YTG']).ev.count()
r13 = df.loc[df.Down.isin([1, 2, 3])].groupby(['ytgl_bucket', 'Down', 'YTG']).ev.mean()
r14 = df.loc[df.Down.isin([1, 2, 3]) & df.YTG.ge(15)].groupby(['ytgl_bucket', 'Down']).ev.mean()
rows = []
for b in buckets:
    for down in range(1, 4):
        for i in range(1, 15):
            try:
                g = r13[b][down][i]
            except KeyError:
                g = np.nan
            rows[len(rows):] = [{'down': down,
                                 'distance': str(i),
                                 'ytgl': b,
                                 'ev': round(g, 3)
                                 }]
        try:
            g = r14[b][down]
        except KeyError:
            g = np.nan
        rows[len(rows):] = [{'down': down,
                             'distance': '15+',
                             'ytgl': b,
                             'ev': round(g, 3)
                             }]
d = pd.DataFrame(rows)
d.to_csv(Config.root + '/1st_thru_3rd_dd.csv', index=False)
dd_1_10 = d.loc[d.down.eq(1) & d.distance.eq('10')]
dds = {}
dds[1]['10'] = dd_1_10

# 4th and 1 FB Dive
print('Kick FG, punt, or FB Dive?')
r15 = df.loc[df.Down.eq(4) & df.YTG.eq(1)].groupby(['ytgl_bucket', 'fb_dive']).ev.mean()
r16 = df.loc[df.Down.eq(4) & df.YTG.eq(1)].groupby(['ytgl_bucket', 'fg']).ev.mean()
r17 = df.loc[df.Down.eq(4) & df.YTG.eq(1)].groupby(['ytgl_bucket', 'punt']).ev.mean()
rows = []
for b in buckets:
    try:
        g = r15[b][True]
    except KeyError:
        g = np.nan
    try:
        f = r16[b][True]
    except KeyError:
        f = np.nan
    try:
        p = r17[b][True]
    except KeyError:
        p = np.nan
    rows[len(rows):] = [{'down': 4,
                         'distance': 1,
                         'ytgl': b,
                         'fb_dive': round(g, 3),
                         'fg': round(f, 3),
                         'punt': round(p, 3)}]
d = pd.DataFrame(rows)

# 4th and 2 FB Dive
print('Kick FG, punt, or FB Dive?')
r15 = df.loc[df.Down.eq(4) & df.YTG.eq(2)].groupby(['ytgl_bucket', 'fb_dive']).ev.mean()
r16 = df.loc[df.Down.eq(4) & df.YTG.eq(2)].groupby(['ytgl_bucket', 'fg']).ev.mean()
r17 = df.loc[df.Down.eq(4) & df.YTG.eq(2)].groupby(['ytgl_bucket', 'punt']).ev.mean()
rows = []
for b in buckets:
    try:
        g = r15[b][True]
    except KeyError:
        g = np.nan
    try:
        f = r16[b][True]
    except KeyError:
        f = np.nan
    try:
        p = r17[b][True]
    except KeyError:
        p = np.nan
    rows[len(rows):] = [{'down': 4,
                         'distance': 2,
                         'ytgl': b,
                         'fb_dive': round(g, 3),
                         'fg': round(f, 3),
                         'punt': round(p, 3)}]
d = pd.DataFrame(rows)

# 4th and 3 FG vs punt vs GFI
print('Kick FG, punt, or FB Dive?')
r15 = df.loc[df.Down.eq(4) & df.YTG.eq(3)].groupby(['ytgl_bucket', 'gfi']).ev.mean()
r16 = df.loc[df.Down.eq(4) & df.YTG.eq(3)].groupby(['ytgl_bucket', 'fg']).ev.mean()
r17 = df.loc[df.Down.eq(4) & df.YTG.eq(3)].groupby(['ytgl_bucket', 'punt']).ev.mean()
rows = []
for b in buckets:
    try:
        g = r15[b][True]
    except KeyError:
        g = np.nan
    try:
        f = r16[b][True]
    except KeyError:
        f = np.nan
    try:
        p = r17[b][True]
    except KeyError:
        p = np.nan
    rows[len(rows):] = [{'down': 4,
                         'distance': 1,
                         'ytgl': b,
                         'gfi': round(g, 3),
                         'fg': round(f, 3),
                         'punt': round(p, 3)}]
d = pd.DataFrame(rows)

# best plays? 1st and 10 at your own 25
r18_a = df.loc[df.Down.eq(1) & df.YTG.eq(10) & df.YTGL.eq(75)].groupby(['OffensivePlay']).ev.count()
r18 = df.loc[df.Down.eq(1) & df.YTG.eq(10) & df.YTGL.eq(75)].groupby(['OffensivePlay']).ev.mean()
rows = []
for p in df.OffensivePlay.unique():
    try:
        g = r18[p]
    except KeyError:
        g = np.nan
    try:
        c = r18_a[p]
    except KeyError:
        c = np.nan
    if c > 50:
        rows[len(rows):] = [{'off_play': p,
                             'ev': round(g, 3),
                             'cnt': c
                             }]
first_and_10_own_25 = pd.DataFrame(rows)
first_and_10_own_25.sort_values('ev', ascending=False, inplace=True)

##########################################################
# plays between the 20s, normalized for position on field

off_play_adj_ev = adj_ev(df, 'OffensivePlay', all_plays, 'desc')
flat_zone = df.loc[df.DefensivePlay.eq('4-3 Normal Man Under 1')]
off_play_adj_ev_flat_zone = adj_ev(flat_zone, 'OffensivePlay', all_plays, 'desc')

off_play_adj_ev_no_zone = adj_ev(df.loc[df.DefensivePlay.ne('4-3 Normal Man OLB Flat Zone')],
                                 'OffensivePlay', all_plays, 'desc')

# Offensive playbook
pbs = ['GenBal', 'PassFoc', 'RunFoc', 'PossOff', 'WestCoast']
combine = ['OffPlayType', 'OffFormation', 'OffPersonnel'] + pbs
off_play_adj_ev_no_zone[combine] = off_play_adj_ev_no_zone.merge(
    global_off_ref, how='left', left_on='OffensivePlay', right_on='OffPlay')[combine]
off_play_adj_ev_no_zone[pbs] = off_play_adj_ev_no_zone[pbs].astype('Int64')

e = off_play_adj_ev_no_zone
j = 15
pb_scores = [{k: e.loc[e[k].eq(1)].head(i).ev_adj.mean().round(3) for k in pbs} for i in range(j, 41)]
for i in pb_scores:
    print(f'{j}: {i} {max(i.values())}')
    j += 1

pbs = ['GenBal', 'PassFoc', 'RunFoc', 'PossOff', 'WestCoast']
off_play_adj_ev_no_zone[pbs] = off_play_adj_ev_no_zone.merge(
    global_off_ref, how='left', left_on='OffensivePlay', right_on='OffPlay')[pbs]
off_play_adj_ev_no_zone[pbs] = off_play_adj_ev_no_zone[pbs].astype('Int64')

# Zone killers
zone_merge = off_play_adj_ev_flat_zone.merge(off_play_adj_ev, how='inner', on='OffensivePlay')
zone_killers = pd.concat([zone_merge['OffensivePlay'],
                          zone_merge['ev_adj_y'],
                          zone_merge['ev_adj_x'],
                          zone_merge['ev_adj_x'] - zone_merge['ev_adj_y']], axis=1)
zone_killers.rename({'ev_adj_y': 'against_all', 'ev_adj_x': 'against_zone', 0: 'improvement'}, axis=1, inplace=True)
zone_killers.sort_values('improvement', ascending=False, inplace=True)
zone_killers.reset_index(drop=True, inplace=True)

# Exporting
off_play_adj_ev.to_csv(Config.root + '/off_play_adj_ev_no_0.csv', index=False)
off_play_adj_ev_flat_zone.to_csv(Config.root + '/off_play_adj_ev_flat_zone_no_0.csv', index=False)

##########################################
# Defensive Plays
####
def_play_scores = {k: adj_ev(df.loc[df.DefensivePlay.eq(k)], 'OffPersonnel',
                             all_plays, 'asc') for k in ['4-3 Normal Man OLB Flat Zone', ]}
def_play_scores.copy()
#####

def_play_scores = {k: adj_ev(df.loc[df.DefensivePlay.eq(k)], 'OffPersonnel',
                             all_plays, 'asc') for k in df.DefensivePlay.unique() if k not in def_excludes}
def_play_scores_run = {k: adj_ev(df.loc[df.DefensivePlay.eq(k)], 'OffPersonnel',
                                 run_plays, 'asc') for k in df.DefensivePlay.unique()}
def_play_scores_pass = {k: adj_ev(df.loc[df.DefensivePlay.eq(k)], 'OffPersonnel',
                                  pass_plays, 'asc') for k in df.DefensivePlay.unique()}

def_play_adj_ev = adj_ev(df, 'DefensivePlay', all_plays, 'asc')
def_play_adj_ev_runs = adj_ev(df, 'DefensivePlay', run_plays, 'asc')
def_play_adj_ev_passes = adj_ev(df, 'DefensivePlay', pass_plays, 'asc')
def_play_adj_ev_fb_dive = adj_ev(df.loc[df.fb_dive], 'DefensivePlay', all_plays, 'asc')

dime_norm_man_cover_1 = adj_ev(df.loc[df.DefensivePlay.eq('Dime Normal Man Cover 1')],
                               'OffPersonnel', all_plays, 'asc')
dime_norm_man_cover_1_run = adj_ev(df.loc[df.DefensivePlay.eq('Dime Normal Man Cover 1')],
                                   'OffPersonnel', run_plays, 'asc')
dime_norm_man_cover_1_pass = adj_ev(df.loc[df.DefensivePlay.eq('Dime Normal Man Cover 1')],
                                    'OffPersonnel', pass_plays, 'asc')

olb_flat_zone = adj_ev(df.loc[df.DefensivePlay.eq('4-3 Normal Man OLB Flat Zone')],
                       'OffPersonnel', all_plays, 'asc')
olb_flat_zone_run = adj_ev(df.loc[df.DefensivePlay.eq('4-3 Normal Man OLB Flat Zone')],
                           'OffPersonnel', run_plays, 'asc')
olb_flat_zone_pass = adj_ev(df.loc[df.DefensivePlay.eq('4-3 Normal Man OLB Flat Zone')],
                            'OffPersonnel', pass_plays, 'asc')

attack_2 = adj_ev(df.loc[df.DefensivePlay.eq('Goal Line Attack #2')],
                  'OffPersonnel', all_plays, 'asc')
attack_2_run = adj_ev(df.loc[df.DefensivePlay.eq('Goal Line Attack #2')],
                      'OffPersonnel', run_plays, 'asc')
attack_2_pass = adj_ev(df.loc[df.DefensivePlay.eq('Goal Line Attack #2')],
                       'OffPersonnel', pass_plays, 'asc')

# Defensive Plays by Personnel
def_play_adj_ev = adj_ev(df, 'DefensivePlay', all_plays, 'asc')

######################################################
# best plays against OLB Flat Zone? 1st and 10 at your own 25
r19_a = df.loc[df.Down.eq(1) &
               df.YTG.eq(10) &
               df.YTGL.eq(75) &
               df.DefensivePlay.eq('4-3 Normal Man OLB Flat Zone')].groupby(['OffensivePlay']).ev.count()
r19 = df.loc[df.Down.eq(1) &
             df.YTG.eq(10) &
             df.YTGL.eq(75) &
             df.DefensivePlay.eq('4-3 Normal Man OLB Flat Zone')].groupby(['OffensivePlay']).ev.mean()
rows = []
for p in df.OffensivePlay.unique():
    try:
        g = r19[p]
    except KeyError:
        g = np.nan
    try:
        c = r19_a[p]
    except KeyError:
        c = np.nan
    if c > 50:
        rows[len(rows):] = [{'off_play': p,
                             'ev': round(g, 3),
                             'cnt': c
                             }]
d = pd.DataFrame(rows)
d.sort_values('ev', ascending=False, inplace=True)

# Quarter Normal Man Short Zone
dn = df.loc[df.YTGL.ge(20) & df.YTGL.lt(80) & df.Down.isin([1, 2, 3]) &
            ~df.OffensivePlay.isin(off_excludes)].copy()
sit_score = dn.groupby(['ytgl_bucket', 'Down', 'YTG']).ev.mean()
dn['ev_adj'] = dn.ev - dn.merge(sit_score, how='left',
                                left_on=['ytgl_bucket', 'Down', 'YTG'],
                                right_index=True)['ev_y']
qn = dn.loc[dn.DefensivePlay.eq('Quarter Normal Man Short Zone')]
qn_run = qn.loc[qn.OffPlayType.isin(run_plays)]
qn_run.ev_adj.mean()

# Interception Rate
dn = df.loc[df.YTGL.ge(20) & df.YTGL.lt(80) & df.Down.isin([1, 2, 3]) &
            ~df.OffensivePlay.isin(off_excludes) &
            df.OffPlayType.isin(pass_plays)].copy()
dn['INT'] = False
dn.INT.mask(dn.Text.str.contains('INTERCEPT'), True, inplace=True)
interception_rates = 100 * dn.loc[dn.INT.eq(True)].groupby('DefensivePlay').DefensivePlay.count(
) / dn.groupby('DefensivePlay').DefensivePlay.count()
interception_rates = 100 * dn.loc[dn.INT.eq(True)].groupby('OffensivePlay').DefensivePlay.count(
) / dn.groupby('OffensivePlay').DefensivePlay.count()
interception_rates.sort_values(ascending=False, inplace=True)

#######################################################
# Download a single season
gdl = GameLogDownloader()
if gdl.set_league_season('norig', '2025'):
    gdl.download_season()

""""
Overuse
This is what happens when you keep calling the same offensive play.
I think the offense is starting to overuse that play.
The offense has gone to that play a few too many times.
The defense seems to be getting familiar with that play.
The offense seems to be calling that play a lot.
"""

# Convert player feathers to CSV
pd.concat(
    (Config.load_feather_with_players(league, season) for league, seasons in Config.ls_dictionary.items() for season in
     seasons)).to_csv(Config.root + '/big_data.csv')

# Blitzing
df['DefSecondary'] = df.merge(global_def_ref, left_on='DefensivePlay',
                              right_on='DefPlay', how='left')['DefSecondary']
df['DefLinebackers'] = df.merge(global_def_ref, left_on='DefensivePlay',
                                right_on='DefPlay', how='left')['DefLinebackers']
df['blitz'] = 0
df.loc[:, 'blitz'].mask(df.DefLinebackers.isin(['Blitz 2', 'Blitz 1', 'Blitz 2+']) |
                        df.DefSecondary.isin(['Corner Blitz', 'Safety Blitz']),
                        1, inplace=True)

# chances of getting 2+ yards on a play
df.loc[:, 'YardsGained'].fillna(0, inplace=True)
df['2plus'] = df.YardsGained.ge(2)
a = (1 - df.loc[df.blitz.eq(1) & ~df.OffensivePlay.isin(off_excludes)].groupby('OffensivePlay')[
    '2plus'].mean().sort_values(ascending=False)) / (
                1 - df.loc[df.blitz.eq(1) & df.OffensivePlay.eq('Goal Line Normal FB Dive')]['2plus'].mean())

gb = df.loc[df.Down.eq(4) & ~df.OffensivePlay.isin(off_excludes)].groupby('OffensivePlay')
f = gb.filter(lambda x: x['OffensivePlay'].count() >= 30)
aa = df.loc[f.index].groupby('OffensivePlay')['2plus'].mean().sort_values(ascending=False)

d = df.loc[df.DefensivePlay.eq('Goal Line Attack #2') & ~df.OffensivePlay.isin(off_excludes)]
ab = (1 - d.groupby('OffensivePlay')['2plus'].mean().sort_values(ascending=False)) / (
            1 - d.loc[d.OffensivePlay.eq('Goal Line Normal FB Dive')]['2plus'].mean())

df = pd.read_feather('/Users/jamesjones/game_logs/xfl/xfl_2042.feather')
df.to_csv('/Users/jamesjones/game_logs/xfl/xfl_2042.feather')
