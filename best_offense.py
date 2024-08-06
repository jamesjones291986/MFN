from main import adj_ev
import pandas as pd

# Best Offensive Calls
def_formations = {
    '113': ['Nickel 3-3-5 Cover 2 Man Under', 'Dime Normal Double WR1 WR2', 'Dime Flat 2 Deep Man Under', 'Dime Flat MLB SS Blitz', 'Dime Normal Man Cover 1'],
    '122': ['3-4 Normal 2 Deep Man', '4-3 Normal Man QB Spy', '4-3 Normal Man Under 1', '4-3 Normal WLB Outside Blitz'],
    '203': ['Dime Flat 2 Deep Man Under', 'Dime Normal Man Cover 1', 'Nickel Normal SS Blitz', 'Dime Flat MLB SS Blitz'],
    '212': ['4-3 Normal WLB Outside Blitz', '4-3 Normal Man Under 1', '4-3 Under Crash Right', '4-3 Normal Man QB Spy'],
    '311': ['4-3 Normal Man Under 1', '4-3 Under Crash Right', '3-4 Normal Man Cover 1', '4-3 Normal Man QB Spy'],
    '221': ['3-4 Normal 2 Deep Man', '3-4 Normal Man Cover 1', '4-3 Normal Man QB Spy', '4-3 Normal WLB Outside Blitz'],
    '104': ['Dime Normal Man Cover 1', 'Quarter Normal Man Short Zone']
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

# pass_plays.to_csv(Config.root + '/plays/pass_plays.csv', index=False)
# run_plays.to_csv(Config.root + '/plays/run_plays.csv', index=False)

