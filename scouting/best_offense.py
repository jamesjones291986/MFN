from main import adj_ev
import pandas as pd

# Best Offensive Calls
def_formations = {
    '113': ['Quarter Normal Man Short Zone', '3-4 Normal Man Cover 1', 'Dime Flat Man Cover 1'],
    '122': ['Quarter Normal Man Short Zone', '3-4 Normal Man Cover 1', 'Goal Line Attack #2'],
    '203': ['Dime Flat 2 Deep Man Under', 'Dime Flat MLB SS Blitz'],
    '212': ['3-4 Normal Man Cover 1', 'Dime Flat 2 Deep Man Under', 'Goal Line Attack #3'],
    '311': ['Dime Normal Double WR1 WR2', '3-4 Normal Man Cover 1'],
    '221': ['Nickel Normal Double WR3', 'Goal Line Attack #1'],
    '104': ['Dime Flat 2 Deep Man Under']
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

