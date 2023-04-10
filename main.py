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


def adj_ev(dd, grouper, plays=all_plays, sort='desc', col_to_sum='YardsGained', column_to_check='Text'):
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
    yards_per_play = dx.groupby(grouper)[col_to_sum].sum() / dx.groupby(grouper).size()
    interception_rate = dx.loc[dx[column_to_check].str.contains('.*INTERCEPTED.*', regex=True)].groupby(
        grouper).size() / dx.groupby(grouper).size() * 100
    sack_rate = dx.loc[dx[column_to_check].str.contains('.*sacked.*', regex=True)].groupby(grouper).size() / dx.groupby(
        grouper).size() * 100

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
                                 'cnt': c,
                                 'ypp': round(yards_per_play[p], 3),
                                 'int_rate': round(interception_rate[p], 2),
                                 'sack_rate': round(sack_rate[p], 2),
                                 'ev_adj': round(g, 3)
                                 }]
    sort_map = {'asc': True, 'desc': False}
    return pd.DataFrame(rows).sort_values('ypp', ascending=sort_map[sort]).reset_index(drop=True)


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
    dd.h_pts_lb.replace(0, np.nan, inplace=True)
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
df = format_df(pd.concat((Config.load_feather(k, y) for k, v in Config.ls_dictionary.items() for y in v))).reset_index(
    drop=True)

df = Config.load_feather('pfl', 2027)

# Scouting
scout('norig', 2030, 'KCC')

# download_all_logs()

path = '/Users/jamesjones/game_logs/moguls/2044/moguls_2044.csv'

gdl = GameLogDownloader()
gdl.set_league_season('moguls', 2044)
gdl.download_season(path)

# Compile a season
SeasonCompiler.compile('qad', 2039)
SeasonCompiler.compile('norig', 2027, players=True)
# specify path to game logs
SeasonCompiler.compile('qad', 2044, override_path='/Users/jamesjones/game_logs/qad/2044/qad_2044.csv')
SeasonCompiler.compile('norig', 2030, override_path='/Users/jamesjones/game_logs/norig/2030/norig_2030.csv')
SeasonCompiler.compile('paydirt', 1997, override_path='/Users/jamesjones/game_logs/paydirt/1997/paydirt_1997.csv')
SeasonCompiler.compile('USFL', 2003, override_path='/Users/jamesjones/game_logs/USFL/2003/USFL_2003.csv')
SeasonCompiler.compile('pfl', 2027, override_path='/Users/jamesjones/game_logs/pfl/2027/pfl_2027.csv')
SeasonCompiler.compile('lol', 2118, override_path='/Users/jamesjones/game_logs/lol/2118/lol_2118.csv')
SeasonCompiler.compile('xfl', 2044, override_path='/Users/jamesjones/game_logs/xfl/2044/xfl_2044.csv')
SeasonCompiler.compile('moguls', 2044, override_path='/Users/jamesjones/game_logs/moguls/2044/moguls_2044.csv')

###########################################

# EV - Best Overall Plays
off_play_adj_ev = adj_ev(df, 'OffensivePlay', all_plays, 'desc')

off_play_adj_ev.to_csv(Config.root + '/off_play_adj_ev.csv', index=False)

# Best Defensive Calls
formations = {
    '113': {
        'pass': ['Singleback Normal TE Quick Out', 'Shotgun Normal HB Flare', 'Singleback Normal WR Quick In',
                 'Singleback Normal HB Release Mid', 'Singleback Normal FL Post'],
        'run': ['Singleback Normal Dive Weak', 'Singleback Normal HB Inside Weak', 'Singleback Normal HB Dive Strong',
                'Singleback Normal HB Counter Weak']
    },
    '122': {
        'pass': ['Singleback Big WR Deep', 'Singleback Big Ins and Out'],
        'run': ['Singleback Big HB Inside Strong']
    },
    '203': {
        'pass': ['I Formation 3WR Slot Corner Short', 'I Formation 3WR Slot Short WR Deep', 'I Formation 3WR WR Out',
                 'I Formation 3WR FL Post', 'Split Backs 3 Wide Slot Post'],
        'run': ['Split Backs 3 Wide Dive Left', 'I Formation 3WR HB Inside Strong', 'I Formation 3WR HB Inside Weak',
                'Split Backs 3 Wide Off Tackle Strong']
    },
    '212': {
        'pass': ['Weak I Normal WR Corner TE Middle', 'I Formation Normal FL Hitch', 'I Formation Twin WR Hard Slants',
                 'I Formation Twin WR Quick Outs', 'Strong I Normal WR Post TE Out', 'I Formation Normal Max Protect'],
        'run': ['I Formation Normal HB Blast', 'I Formation Normal HB Dive', 'Strong I Normal HB Off Tackle Strong',
                'Weak I Normal HB Inside Weak', 'I Formation Normal HB Counter']
    },
    '221': {
        'pass': ['Strong I Big TE Post', 'Strong I Big Backfield Drag']
    },
    '311': {
        'pass': ['I Formation Power Play Action HB Downfield', 'I Formation Power PA Flats'],
        'run': ['I Formation Power HB Strong Outside']
    },
    '104': {
        'pass': ['Singleback 4 Wide Quick Outs']
    },
}

# Calculate adjusted expected value for each formation and play type
for formation in formations:
    form_pass = formations[formation]['pass']
    if 'run' in formations[formation]:
        form_run = formations[formation]['run']
    else:
        []
    form_plays = form_pass + form_run

    globals()[f"def_plays_pass_{formation}"] = adj_ev(df.loc[df.OffensivePlay.isin(form_pass)], 'DefensivePlay',
                                                      all_plays, 'asc')
    globals()[f"def_plays_run_{formation}"] = adj_ev(df.loc[df.OffensivePlay.isin(form_run)], 'DefensivePlay',
                                                     all_plays, 'asc')
    globals()[f"def_plays_total_{formation}"] = adj_ev(df.loc[df.OffensivePlay.isin(form_plays)], 'DefensivePlay',
                                                       all_plays, 'asc')

# Best Offensive Calls
def_formations = {
    '113': ['3-4 Normal Man Cover 1', '4-3 Normal WLB Outside Blitz', '4-3 Normal Double WR1'],
    '203': ['Dime Normal Man Cover 1', '3-4 Normal Man Cover 1'],
    '212': ['3-4 Normal Man Cover 1'],
    '311': ['Dime Normal Man Cover 1', '4-3 Under Crash Right'],
    '221': ['3-4 Normal Man Cover 1'],
    '023': ['Goal Line Attack #2']
}

for formation in def_formations:
    globals()[f"off_plays_{formation}"] = adj_ev(df.loc[df.DefensivePlay.isin(def_formations[formation])],
                                                 'OffensivePlay', all_plays, 'desc')


#######################################################


ypp = df.groupby(['OffensivePlay', 'DefensivePlay']).agg({'YardsGained': ['mean', 'count']})
ypp = ypp.reset_index()
ypp.to_csv('/Users/jamesjones/game_logs/ypp_off_def_3.csv')

ypp_offense = df.groupby('OffensivePlay', as_index=False).agg({'YardsGained': ['mean', 'count']})
ypp_defense = df.groupby('DefensivePlay', as_index=False).agg({'YardsGained': ['mean', 'count']})
ypp_offense.to_csv('/Users/jamesjones/game_logs/ypp_off.csv')
ypp_defense.to_csv('/Users/jamesjones/game_logs/ypp_def.csv')

ypp_offense = df.groupby('OffensivePlay', as_index=False)['YardsGained'].mean() \
    .sort_values('YardsGained', ascending=False)
ypp_defense = df.groupby('DefensivePlay', as_index=False)['YardsGained'].mean() \
    .sort_values('YardsGained', ascending=True)

off_plays_113 = ['Shotgun Normal HB Flare', 'Singleback Normal TE Quick Out', 'Singleback Normal HB Release Mid',
                 'Singleback Normal SE Quick Hit', 'Singleback Normal WR Quick In', 'Singleback Normal FL Post']
def_ypp_113 = df.loc[df.OffensivePlay.isin(off_plays_113)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_113.columns[0]])

off_plays_122 = ['Singleback Big WR Deep']
def_ypp_122 = df.loc[df.OffensivePlay.isin(off_plays_122)].groupby('DefensivePlay').agg(
    {'YardsGained': ['mean', 'count']}) \
    .sort_values(by=[def_ypp_122.columns[0]])

def_plays_113 = ['Dime Normal Double WR1 WR2']
off_ypp_113 = df.loc[df.DefensivePlay.isin(def_plays_113)].groupby('OffensivePlay').agg(
    {'YardsGained': ['mean', 'count']})
off_ypp_113.sort_values(('b', 'Yards Per Play'))

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
    {'YardsGained': {'ypp_mean': 'mean', 'ypp_count': 'count'}})

def_plays_113 = ['Dime Normal Double WR1 WR2']
off_ypp_113 = df.loc[df.DefensivePlay.isin(def_plays_113)].groupby('OffensivePlay').agg \
    (yards_per_play=pd.NamedAgg(column='YardsGained', aggfunc='mean')).agg \
    (count=pd.NamedAgg(column='YardsGained', aggfunc='count')).sort_values(by='yards_per_play')
