import pandas as pd
from main import format_df, adj_ev
from util import Config

# Set Variables
league_mfn = 'USFL'
season_year = '2011'
offenses_to_scout = ['NYS']
file_name = f"{league_mfn}_{season_year}.feather"

# Load the specific file
df = format_df(Config.load_specific_feather(file_name)).reset_index(drop=True)

def off_scouting(offense_teams, league, season):
    scouting_results = {}

    for offense_team in offense_teams:
        offense_results = {}
        for personnel_set in df.OffPersonnel.unique():
            filtered_df = df.loc[
                (df.HasBall == offense_team) &
                (df.League == league) &
                (df.OffPersonnel == personnel_set) &
                (df.Season.astype(str) == season)
            ]
            grouped_data = filtered_df.groupby('OffensivePlay').size().sort_values(ascending=False).head(30)
            percentages = grouped_data / grouped_data.sum() * 100
            top_30 = percentages.head(30)

            offense_results[personnel_set] = top_30.apply(lambda x: f'{x:.1f}%')

        scouting_results[offense_team] = offense_results

    return scouting_results

# Call off_scouting with multiple offenses
scouting_results = off_scouting(offenses_to_scout, league_mfn, season_year)

# Combine scouting results into a DataFrame
data_to_append = []
for defense, personnel_results in scouting_results.items():
    for personnel, percentages in personnel_results.items():
        for play, usage in percentages.items():
            data_to_append.append({'Personnel': personnel, 'OffensivePlay': play, 'Usage': float(usage.strip('%'))})

combined_results_df = pd.DataFrame(data_to_append)

# Group and filter the combined results
threshold_percentage = 10
filtered_results = combined_results_df.groupby(['Personnel', 'OffensivePlay'])['Usage'].sum().reset_index()
filtered_results = filtered_results[filtered_results['Usage'] >= threshold_percentage]

# Generate formations dictionary dynamically
formations = {}
for personnel in filtered_results['Personnel'].unique():
    formations[personnel] = {
        'pass': filtered_results[filtered_results['Personnel'] == personnel]['OffensivePlay'].tolist(),
        'run': []  # Placeholder; you can add logic to populate run plays if needed
    }

print("Generated formations dictionary:")
print(formations)

# Calculate adjusted expected value for each formation and play type
pass_threshold = 7
run_threshold = 6
exclude_columns = ['OffPlayType', 'OffPersonnel']
exclude_columns_run = ['OffPlayType', 'OffPersonnel', 'any/a', 'int_rate', 'sack_rate']

for formation, plays in formations.items():
    form_pass = plays['pass']
    form_run = plays.get('run', [])
    form_plays = form_pass + form_run

    print(f"Processing formation: {formation}")
    print(f"Pass plays: {form_pass}")
    print(f"Run plays: {form_run}")

    # Pass plays EV
    if form_pass:
        try:
            globals()[f"def_plays_pass_{formation}"] = adj_ev(
                df.loc[df.OffensivePlay.isin(form_pass)], 'DefensivePlay', all_plays, 'asc'
            ).sort_values(by='any/a').drop(exclude_columns, axis=1)
        except KeyError as e:
            print(f"Error processing pass plays for formation {formation}: {e}")
            print(df.columns)
            continue

    # Run plays EV
    if form_run:
        try:
            globals()[f"def_plays_run_{formation}"] = adj_ev(
                df.loc[df.OffensivePlay.isin(form_run)], 'DefensivePlay', all_plays, 'asc'
            ).drop(exclude_columns_run, axis=1)
        except KeyError as e:
            print(f"Error processing run plays for formation {formation}: {e}")
            print(df.columns)
            continue

    # Combined plays EV
    if form_plays:
        try:
            globals()[f"def_plays_total_{formation}"] = adj_ev(
                df.loc[df.OffensivePlay.isin(form_plays)], 'DefensivePlay', all_plays, 'asc'
            ).drop(exclude_columns_run, axis=1)
        except KeyError as e:
            print(f"Error processing combined plays for formation {formation}: {e}")
            print(df.columns)
            continue

# New code to find matches between run and pass plays with 'ypp' < thresholds for each formation
for formation in formations:
    if f"def_plays_pass_{formation}" in globals() and f"def_plays_run_{formation}" in globals():
        pass_plays_df = globals()[f"def_plays_pass_{formation}"]
        run_plays_df = globals()[f"def_plays_run_{formation}"]

        try:
            matched_df = pass_plays_df[pass_plays_df['ypp'] < pass_threshold].merge(
                run_plays_df[run_plays_df['ypp'] < run_threshold],
                on='DefensivePlay',
                suffixes=('_pass', '_run')
            )

            globals()[f"combined_matched_result_{formation}"] = matched_df
        except KeyError as e:
            print(f"Error matching pass and run plays for formation {formation}: {e}")
            print(pass_plays_df.columns)
            print(run_plays_df.columns)

# Print results
print("Formations results:")
for formation in formations:
    if f"combined_matched_result_{formation}" in globals():
        print(f"Combined matched result for formation {formation}:")
        print(globals()[f"combined_matched_result_{formation}"])
