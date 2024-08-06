# EV - Best Overall Plays
# overall_off_play_adj_ev = adj_ev(df, 'OffensivePlay', all_plays, 'desc')
#
# overall_off_play_adj_ev.to_csv(Config.root + '/off_play_adj_ev.csv', index=False)

pass_threshold = 7
run_threshold = 6

# Best Defensive Calls
formations = {
    '113': {
        'pass': ['Singleback Normal TE Quick Out'],
        'run': ['Singleback Slot Strong HB Counter', 'Singleback Normal HB Counter Weak', 'Singleback Normal HB Inside Weak']
    },
    '122': {
        'pass': ['Singleback Big Ins and Outs'],
        'run': ['Singleback Big HB Inside Strong', 'Singleback Big Off Tackle Strong']
    },
    '203': {
        'pass': ['I Formation 3WR WR Out', 'I Formation 3WR FL Post', 'Split Backs 3 Wide WR Quick Out'],
        'run': ['I Formation 3WR HB Inside Weak', 'I Formation 3WR HB Inside Strong', 'Split Backs 3 Wide Dive Left']
    },
    '212': {
        'pass': ['I Formation Twin WR Hard Slants', 'I Formation Twin WR Quick Outs'],
        'run': ['I Formation Normal HB Blast']
    },
    '221': {
        'pass': ['Strong I Big TE Post', 'Strong I Big WR Quick In'],
        'run': ['Strong I Big HB Dive Strong']
    },
    '311': {
        'pass': ['I Formation Power Play Action HB Downfield'],
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

        matched_df = pass_plays_df[pass_plays_df['ypp'] < pass_threshold].merge(
            run_plays_df[run_plays_df['ypp'] < run_threshold],
            on='DefensivePlay',
            suffixes=('_pass', '_run')
        )

        globals()[f"combined_matched_result_{formation}"] = matched_df
