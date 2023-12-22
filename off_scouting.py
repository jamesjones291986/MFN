import pandas as pd
from main import format_df
from util import Config


# Scouting

# Set Variables
league_mfn = 'qad'
season_year = '2049'
offenses_to_scout = ['SGR']  # Example list of offenses

# Bring in the league to scout
df = format_df(Config.load_feather(league_mfn, season_year)).reset_index(drop=True)


##############

def off_scouting(offense_teams, league, season):
    scouting_results = {}  # Create a dictionary to store scouting results for each offense

    for offense_team in offense_teams:
        offense_results = {}  # Create a dictionary to store results for each personnel group for this offense

        for personnel_set in df.OffPersonnel.unique():  # Iterate through personnel sets
            filtered_df = df.loc[
                df.HasBall.eq(offense_team) &  # Query the team with the ball as the offensive team
                df.League.eq(league) &
                df.OffPersonnel.eq(personnel_set) &  # Use personnel set as a filter
                df.Season.astype(str).eq(season)
            ]
            grouped_data = filtered_df.groupby('OffensivePlay').size().sort_values(ascending=False).head(30)
            percentages = grouped_data / grouped_data.sum() * 100
            top_30 = percentages.head(30)

            # Store the scouting results for this personnel set
            offense_results[personnel_set] = top_30.apply(lambda x: f'{x:.1f}%')

        # Store the scouting results for this offense
        scouting_results[offense_team] = offense_results

    return scouting_results


# Call off_scouting with multiple offenses
scouting_results = off_scouting(offenses_to_scout, league_mfn, season_year)

######################

import pandas as pd

# Assuming you have already obtained scouting_results as shown in your previous code

# Create an empty DataFrame to store the combined results
combined_results_df = pd.DataFrame(columns=['Personnel', 'OffensivePlay', 'Usage'])

data_to_append = []

# Iterate through the scouting results for each defense and personnel group
for defense, personnel_results in scouting_results.items():
    for personnel, percentages in personnel_results.items():
        for play, usage in percentages.items():
            # Extract the percentage value as a float
            usage_float = float(usage.strip('%'))

            # Append the data to the list
            data_to_append.append({'Personnel': personnel, 'OffensivePlay': play, 'Usage': usage_float})

# Create a DataFrame from the list of data
combined_results_df = pd.DataFrame(data_to_append)

# Group the combined results by 'DefensiveTeam' and 'OffensivePlay' and sum the 'Usage'
combined_results_grouped = combined_results_df.groupby(['Personnel', 'OffensivePlay'])['Usage'].sum().reset_index()

# Filter the combined results to include only plays with 20% or higher combined usage
threshold_percentage = 10
filtered_results = combined_results_grouped[combined_results_grouped['Usage'] >= threshold_percentage]

# Sort the filtered results first by 'DefensiveTeam' and then by 'Usage' in descending order
filtered_results_sorted = filtered_results.sort_values(by=['Personnel', 'Usage'], ascending=[True, False])

# Print the filtered results
print(filtered_results_sorted)





