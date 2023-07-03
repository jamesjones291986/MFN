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
    touchdown_rate = dx.loc[dx[column_to_check].str.contains('.*TOUCHDOWN.*', regex=True)].groupby(
        grouper).size() / dx.groupby(grouper).size() * 100
    yards_per_play_100 = yards_per_play * 100
    any_a = (yards_per_play_100 + (20 * yards_per_play) - (60 * interception_rate) - (sack_rate * 20)) / 100

    results = []
    for p in dx[grouper].unique():
        try:
            g = ev_adj_score[p]
        except KeyError:
            g = np.nan
        try:
            c = ev_adj_count[p]
        except KeyError:
            c = np.nan
        if c > 30:
            off_play_type = dx.loc[dx[grouper] == p, 'OffPlayType'].iloc[0]
            off_personnel_type = dx.loc[dx[grouper] == p, 'OffPersonnel'].iloc[0]
            results.append({
                grouper: p,
                'OffPlayType': off_play_type,
                'OffPersonnel': off_personnel_type,
                'ypp': round(yards_per_play[p], 2),
                'cnt': c,
                'any/a': round(any_a[p], 2),
                'int_rate': round(interception_rate[p], 2),
                'sack_rate': round(sack_rate[p], 2),
                'td_rate': round(touchdown_rate[p], 2),
                'ev_adj': round(g, 3),
            })

    sort_map = {'asc': True, 'desc': False}
    return pd.DataFrame(results).sort_values('ypp', ascending=sort_map[sort]).reset_index(drop=True)


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

    # Create a new column 'dist' instead of modifying the existing one
    do.loc[:, 'dist'] = '0-2'
    do.loc[do.YTG.ge(3), 'dist'] = '3-5'
    do.loc[do.YTG.ge(6), 'dist'] = '6-9'
    do.loc[do.YTG.ge(10), 'dist'] = '10-14'
    do.loc[do.YTG.ge(15), 'dist'] = '15+'

    c = ['Down', 'dist', 'OffPlayType']
    r = ['Inside Run', 'Outside Run']
    p = ['Short Pass', 'Medium Pass', 'Long Pass']
    gb = do.groupby(c).OffPlayType.count()

    result = gb.index.to_frame().reset_index()
    result.rename(columns={0: 'PlayCount'}, inplace=True)
    result = result.merge(gb, how='left', left_on=c, right_index=True)

    print("Result DataFrame:")
    print(result)


def def_against_personnel():
    pass


def scout(league, season, team):
    tdf = format_df(Config.load_feather(league, season))
    print(f'Scouting Report for {team} in {league} {season}')
    scout_off_def(tdf, team)
    # scout_run_vs_pass_downs(tdf, team)


# Load all seasons
df = format_df(pd.concat((Config.load_feather(k, y) for k, v in Config.ls_dictionary.items() for y in v))).reset_index(
    drop=True)

df = format_df(Config.load_feather('norig', 2031)).reset_index(drop=True)

#####################################

# Scouting
scout('norig', 2030, 'KCC')

# download_all_logs()

league = 'nba'
year = '2000'
path = f'/Users/jamesjones/game_logs/{league}/{year}/{league}_{year}.csv'

gdl = GameLogDownloader()
gdl.set_league_season(league, int(year))
gdl.download_season(path)

# Compile into a feather file

SeasonCompiler.compile(league, int(year), override_path=path)

###########################################

# EV - Best Overall Plays
off_play_adj_ev = adj_ev(df, 'OffensivePlay', all_plays, 'desc')

off_play_adj_ev.to_csv(Config.root + '/off_play_adj_ev.csv', index=False)

# Best Defensive Calls
formations = {
    '113': {
        'pass': ['Shotgun Normal HB Flare', 'Singleback Normal TE Quick Out'],
        'run': ['Singleback Normal HB Inside Weak', 'Singleback Normal HB Dive Weak',
                'Singleback Slot Strong HB Strong Inside', 'Singleback Slot Strong HB Counter',
                'Singleback Normal HB Dive Strong']
    },
    '122': {
        'pass': ['Singleback Big Ins and Outs'],
        'run': ['Singleback Big HB Inside Strong']
    },
    '203': {
        'pass': ['I Formation 3WR Slot Short WR Deep', 'I Formation 3WR FL Post', 'I Formation 3WR WR Out'],
        'run': ['Split Backs 3 Wide Dive Left', 'I Formation 3WR HB Inside Weak', 'Shotgun 2 RB 3 WR Shotgun Sweep']
    },
    '212': {
        'pass': ['I Formation Twin WR Hard Slants', 'I Formation Twin WR Quick Outs', 'I Formation Normal FL Hitch',
                 'Weak I Normal WR Corner TE Middle'],
        'run': ['Weak I Normal HB Inside Weak', 'I Formation Normal HB Dive', 'I Formation Normal HB Blast',
                'Weak I Normal FB Inside Weak']
    },
    '221': {
        'pass': ['Strong I Big TE Post', 'Strong I Big Backfield Drag'],
        'run': ['Strong I Big HB Dive Strong']
    },
    '311': {
        'pass': ['I Formation Power Play Action HB Downfield', 'I Formation Power PA Flats'],
        'run': ['I Formation Power HB Strong Outside']
    },
    '104': {
        'pass': ['Singleback 4 Wide Quick Outs'],
    },
}

# Calculate adjusted expected value for each formation and play type

exclude_columns = ['OffPlayType', 'OffPersonnel']
exclude_columns_run = ['OffPlayType', 'OffPersonnel', 'any/a', 'int_rate',
                       'sack_rate']  # Specify the columns to exclude

for formation in formations:
    form_pass = formations[formation]['pass']
    if 'run' in formations[formation]:
        form_run = formations[formation]['run']
    else:
        []
    form_plays = form_pass + form_run

    globals()[f"def_plays_pass_{formation}"] = adj_ev(df.loc[df.OffensivePlay.isin(form_pass)], 'DefensivePlay',
                                                      all_plays, 'asc').sort_values(by='any/a').drop(exclude_columns,
                                                                                                     axis=1)
    globals()[f"def_plays_run_{formation}"] = adj_ev(df.loc[df.OffensivePlay.isin(form_run)], 'DefensivePlay',
                                                     all_plays, 'asc').drop(exclude_columns_run, axis=1)
    globals()[f"def_plays_total_{formation}"] = adj_ev(df.loc[df.OffensivePlay.isin(form_plays)], 'DefensivePlay',
                                                       all_plays, 'asc').drop(exclude_columns_run, axis=1)

# Best Offensive Calls
def_formations = {
    '113': ['4-3 Normal Man Under 1', 'Dime Flat Man Cover 1', '3-4 Normal Man Cover 1', '4-3 Normal Double WR1'],
    '122': ['4-3 Normal Man Under 1', 'Dime Flat Man Cover 1', '3-4 Normal Man Cover 1', '4-3 Normal Double WR3'],
    '203': ['4-3 Normal Man Under 1', 'Dime Flat Man Cover 1', '3-4 Normal Man Cover 1', '4-3 Under Crash Right'],
    '212': ['4-3 Normal Man Under 1', 'Dime Flat Man Cover 1', '3-4 Normal Man Cover 1', '4-3 Normal Double WR3'],
    '311': ['4-3 Normal Man Under 1', 'Dime Flat Man Cover 1', '3-4 Normal Man Cover 1', '4-3 Under Crash Right'],
    '221': ['4-3 Normal Man Under 1', 'Dime Flat Man Cover 1', '3-4 Normal Man Cover 1', '4-3 Under Crash Right'],
    '104': ['Quarter Normal Man Short Zone']
}

off_personnel_values = {
    '113': '1RB/1TE/3WR',
    '122': '1RB/2TE/2WR',
    '203': '2RB/3WR',
    '212': '2RB/1TE/2WR',
    '311': '3RB/1TE/1WR',
    '221': '2RB/2TE/1WR',
    '104': '1RB/4WR',
}

off_plays_combined = pd.DataFrame()  # DataFrame to store the combined results

for formation in def_formations:
    off_personnel_value = off_personnel_values.get(formation)

    if off_personnel_value is not None:
        filtered_df = df.loc[df.DefensivePlay.isin(def_formations[formation])]
        off_plays = adj_ev(filtered_df, 'OffensivePlay', all_plays, 'desc')
        filtered_plays = off_plays.loc[off_plays.OffPersonnel == off_personnel_value]
        off_plays_combined = pd.concat([off_plays_combined, filtered_plays])

# Sort the DataFrame by 'ypp'
off_plays_combined = off_plays_combined.sort_values(by='ypp', ascending=False)

# Separate into pass and run DataFrames
pass_plays = off_plays_combined[off_plays_combined['OffPlayType'].str.contains('pass', case=False)] \
    .sort_values('any/a', ascending=False)
run_plays = off_plays_combined[off_plays_combined['OffPlayType'].str.contains('run', case=False)]

#######################################################

# Scouting

# Bring in the league to scout
df = format_df(Config.load_feather('USFL', 2005)).reset_index(drop=True)


def scouting(defense, league, season):
    for p in df.OffPersonnel.unique():
        filtered_df = df.loc[
            df.DefTeam.eq(defense) &
            df.League.eq(league) &
            df.OffPersonnel.eq(p) &
            df.Season.astype(str).eq(season)
            ]
        grouped_data = filtered_df.groupby('DefensivePlay').size().sort_values(ascending=False).head(30)
        percentages = grouped_data / grouped_data.sum() * 100
        top_30 = percentages.head(30)
        print(p)
        print(top_30.apply(lambda x: f'{x:.1f}%'))
        print('')


scouting('PHI', 'USFL', '2005')

##################################################

# Testing
