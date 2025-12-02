from main import adj_ev
import pandas as pd

# Best Offensive Calls
def_formations = {
    '113': ['Quarter Normal Man Short Zone', '3-4 Normal Man Cover 1', 'Dime Flat Man Cover 1'],
    '122': ['Quarter Normal Man Short Zone', '3-4 Normal Man Cover 1', 'Goal Line Attack #2'],
    '203': ['Nickel Normal Double WR1'],
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

# Best Offensive Calls by Personnel Set
personnel_sets = ['113', '122', '203', '212', '311', '221', '104']

exclude_columns = ['OffPlayType', 'OffPersonnel']

for personnel in personnel_sets:
    personnel_value = off_personnel_values.get(personnel)
    
    if personnel_value is not None:
        # Get all plays for this personnel set
        filtered_df_personnel = df.loc[df.OffPersonnel == personnel_value]
        
        if not filtered_df_personnel.empty:
            # Get best offensive plays for this personnel set
            off_plays_personnel = adj_ev(filtered_df_personnel, 'OffensivePlay', all_plays, 'desc')
            
            # Separate into pass and run plays for this personnel set
            pass_plays_personnel = off_plays_personnel[off_plays_personnel['OffPlayType'].str.contains('pass', case=False)].sort_values('any/a', ascending=False)
            run_plays_personnel = off_plays_personnel[off_plays_personnel['OffPlayType'].str.contains('run', case=False)]
            
            # Create global variables for each personnel set
            globals()[f"off_plays_pass_{personnel}"] = pass_plays_personnel.drop(exclude_columns, axis=1, errors='ignore')
            globals()[f"off_plays_run_{personnel}"] = run_plays_personnel.drop(exclude_columns, axis=1, errors='ignore')
            globals()[f"off_plays_total_{personnel}"] = off_plays_personnel.drop(exclude_columns, axis=1, errors='ignore')

# Combine all personnel set data into one summary table
all_personnel_plays = []

for personnel in personnel_sets:
    if f"off_plays_total_{personnel}" in globals():
        personnel_df = globals()[f"off_plays_total_{personnel}"].copy()
        if not personnel_df.empty:
            personnel_df['Personnel'] = off_personnel_values.get(personnel, personnel)
            all_personnel_plays.append(personnel_df)

if all_personnel_plays:
    # Combine all DataFrames
    combined_personnel_plays = pd.concat(all_personnel_plays, ignore_index=True)
    
    # Sort by YPP (descending)
    combined_personnel_plays = combined_personnel_plays.sort_values(by='ypp', ascending=False).reset_index(drop=True)
    
    print("ALL OFFENSIVE PLAYS BY PERSONNEL SET (Sorted by YPP)")
    print("=" * 70)
    print(combined_personnel_plays.to_string(index=False))

