import pandas as pd
from main import format_df, adj_ev
from util import Config

# Scouting

# Set Variables
league_mfn = 'USFL'
season_year = "2011"
defenses_to_scout = ['NYS']  # Example list of defenses

file_name = f"{league_mfn}_{season_year}.feather"

# Load the specific file
df = format_df(Config.load_specific_feather(file_name)).reset_index(drop=True)

# Function to scout defensive plays
def def_scouting(defenses, league, season, df):
    scouting_results = {}  # Dictionary to store scouting results for each defense

    for defense in defenses:
        defense_results = {}  # Dictionary to store results for each personnel group for this defense

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

            # Store the scouting results for this personnel group
            defense_results[p] = top_30.apply(lambda x: f'{x:.1f}%')

        # Store the scouting results for this defense
        scouting_results[defense] = defense_results

    return scouting_results

# Call def_scouting to get defensive plays
scouting_results = def_scouting(defenses_to_scout, league_mfn, season_year, df)

# Extract the top defensive plays for each offensive personnel group
def_formations = {}
for defense, personnel_results in scouting_results.items():
    for personnel, percentages in personnel_results.items():
        top_defensive_plays = percentages.index.tolist()  # Get the top plays
        personnel_key = [key for key, value in off_personnel_values.items() if value == personnel]
        if personnel_key:
            def_formations[personnel_key[0]] = top_defensive_plays

# Function to get best offensive plays
def get_best_offensive_plays(def_formations, df):
    off_plays_combined = pd.DataFrame()  # DataFrame to store the combined results

    for formation, defensive_plays in def_formations.items():
        off_personnel_value = off_personnel_values.get(formation)

        if off_personnel_value is not None:
            filtered_df = df.loc[df.DefensivePlay.isin(defensive_plays)]
            off_plays = adj_ev(filtered_df, 'OffensivePlay', all_plays, 'desc')
            filtered_plays = off_plays.loc[off_plays.OffPersonnel == off_personnel_value]
            off_plays_combined = pd.concat([off_plays_combined, filtered_plays])

    # Sort the DataFrame by 'ypp'
    off_plays_combined = off_plays_combined.sort_values(by='ypp', ascending=False)

    return off_plays_combined

# Get the best offensive plays based on scouted defensive plays
off_plays_combined = get_best_offensive_plays(def_formations, df)

# Separate into pass and run DataFrames
pass_plays = off_plays_combined[off_plays_combined['OffPlayType'].str.contains('pass', case=False)] \
    .sort_values('any/a', ascending=False)
run_plays = off_plays_combined[off_plays_combined['OffPlayType'].str.contains('run', case=False)]

# Print the results
print("Best Offensive Pass Plays:")
print(pass_plays)

print("\nBest Offensive Run Plays:")
print(run_plays)

# Uncomment to save results
# pass_plays.to_csv(Config.root + '/plays/pass_plays.csv', index=False)
# run_plays.to_csv(Config.root + '/plays/run_plays.csv', index=False)
