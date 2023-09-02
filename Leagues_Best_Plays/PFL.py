import pandas as pd
from util import Config
from main import format_df
from main import adj_ev

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

# Load all seasons
df = format_df(pd.concat((Config.load_feather(k, y) for k, v in Config.ls_dictionary.items() for y in v))).reset_index(
    drop=True)

# Best Defensive Calls
formations = {
    '113': {
        'pass': ['Singleback Normal HB Release Mid', 'Singleback Normal WR Quick In', 'Singleback Normal TE Quick Out',
                 'Singleback Normal Quick Slant', 'Shotgun Normal HB Flare'],
        'run': ['Singleback Normal HB Counter Weak', 'Singleback Slot Strong HB Counter',
                'Singleback Normal HB Inside Weak']
    },
    '122': {
        'pass': ['Singleback Big WR Deep', 'Singleback Big Ins and Outs'],
        'run': ['Singleback Big Off Tackle Strong']
    },
    '203': {
        'pass': ['I Formation 3WR FL Post', 'I Formation 3WR WR Out', 'I Formation 3WR Slot Short WR Deep',
                 'I Formation 3WR Backfield Flats', 'Split Backs 3 Wide WR WR Quick Out'],
        'run': ['Split Backs 3 Wide Dive Left', 'I Formation 3WR HB Inside Weak']
    },
    '212': {
        'pass': ['I Formation Twin WR Hard Slants', 'Weak I Normal WR Corner TE Middle', 'Weak I Normal Skinny Posts'
                 'I Formation Twin WR Quick Outs', 'I Formation Normal Max Protect', 'I Formation Normal FL Hitch'],
        'run': ['Strong I Normal HB Off Tackle', 'Weak I Normal Fullback Counter Weak', 'I Formation Normal HB Draw']
    },
    '221': {
        'pass': ['Strong I Big TE Post', 'Strong I Big Backfield Drag'],
        'run': ['Strong I Big HB Dive Strong']
    },
    '311': {
        'pass': ['I Formation Power Play Action HB Downfield', 'I Formation Power PA Flats'],
        'run': ['I Formation Power HB Strong Outside', 'I Formation Power HB Sweep Weak']
    },
    '104': {
        'pass': ['Singleback 4 Wide Quick Outs'],
    },
    '105': {
        'pass': ['Shotgun 5 Wide Parallel Slants'],
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

# Existing code to calculate adjusted expected values for run and pass plays

# New code to find matches between run and pass plays with 'ypp' < 6 for each formation
for formation in formations:
    if f"def_plays_pass_{formation}" in globals() and f"def_plays_run_{formation}" in globals():
        pass_plays_df = globals()[f"def_plays_pass_{formation}"]
        run_plays_df = globals()[f"def_plays_run_{formation}"]

        matched_df = pass_plays_df[pass_plays_df['ypp'] < 6].merge(
            run_plays_df[run_plays_df['ypp'] < 5],
            on='DefensivePlay',
            suffixes=('_pass', '_run')
        )

        globals()[f"combined_matched_result_{formation}"] = matched_df

# Best Offensive Calls
def_formations = {
    '113': ['4-3 Normal Man Under 1', '3-4 Normal Man Cover 1', '4-3 Normal Double WR3'],
    '122': ['Nickel Normal Double WR3', 'Nickel Normal CB3 LB Blitz'],
    '203': ['3-4 Normal Man Cover 1', '4-3 Under Double LB Blitz', '4-3 Normal Double WR3', '4-3 Normal Man Under 1'],
    '212': ['Goal Line Attack #3', '3-4 Normal Man Cover 1', 'Dime Normal Man Cover 1'],
    '311': ['3-4 Normal Man Cover 1', 'Dime Normal Man Cover 1', '4-3 Normal Man Under 1'],
    '221': ['Dime Normal Man Cover 1'],
    '104': ['Dime Normal Man Cover 1']
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

pass_plays.to_csv(Config.root + '/pass_plays.csv', index=False)
run_plays.to_csv(Config.root + '/run_plays.csv', index=False)
