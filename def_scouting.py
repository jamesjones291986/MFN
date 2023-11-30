import pandas as pd
from main import format_df
from util import Config


# Scouting

# Set Variables
league_mfn = 'xfl'
season_year = '2047'
defenses_to_scout = ['PRI']  # Example list of offenses

# Bring in the league to scout
df = format_df(Config.load_feather(league_mfn, season_year)).reset_index(drop=True)


##############

def def_scouting(defenses, league, season):
    scouting_results = {}  # Create a dictionary to store scouting results for each defense

    for defense in defenses:
        defense_results = {}  # Create a dictionary to store results for each personnel group for this defense

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

# Call def_scouting with multiple defenses
scouting_results = def_scouting(defenses_to_scout, league_mfn, season_year)

######################

import pandas as pd

# Assuming you have already obtained scouting_results as shown in your previous code

# Create an empty DataFrame to store the combined results
combined_results_df = pd.DataFrame(columns=['Personnel', 'DefensivePlay', 'Usage'])

# Iterate through the scouting results for each defense and personnel group
for defense, personnel_results in scouting_results.items():
    for personnel, percentages in personnel_results.items():
        for play, usage in percentages.items():
            # Extract the percentage value as a float
            usage_float = float(usage.strip('%'))

            # Append the data to the combined_results_df DataFrame
            combined_results_df = combined_results_df.append(
                {'Personnel': personnel, 'DefensivePlay': play, 'Usage': usage_float}, ignore_index=True)

# Group the combined results by 'Personnel' and 'DefensivePlay' and sum the 'Usage'
combined_results_grouped = combined_results_df.groupby(['Personnel', 'DefensivePlay'])['Usage'].sum().reset_index()

# Filter the combined results to include only plays with 20% or higher combined usage
threshold_percentage = 7
filtered_results = combined_results_grouped[combined_results_grouped['Usage'] >= threshold_percentage]

# Sort the filtered results first by 'Personnel' and then by 'Usage' in descending order
filtered_results_sorted = filtered_results.sort_values(by=['Personnel', 'Usage'], ascending=[True, False])

# Print the filtered results
print(filtered_results_sorted)




