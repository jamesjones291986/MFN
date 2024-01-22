import pandas as pd
import re

# Assuming df is your DataFrame

# Exclude NaN, 'Special Teams', and 'Victory' from 'OffPersonnel' column
df_filtered = df.dropna(subset=['OffPersonnel'])
df_filtered = df_filtered[(df_filtered['OffPersonnel'] != 'Special Teams') & (df_filtered['OffPersonnel'] != 'Victory')]

# Get unique values in 'OffPersonnel' column
unique_off_personnel_values = df_filtered['OffPersonnel'].unique()

# Create a dictionary to store DataFrames for each unique value
dfs_by_off_personnel = {}


# Function to clean names by removing all non-alphanumeric characters
def clean_name(value):
    return re.sub(r'[^a-zA-Z0-9_]', '', str(value))


# Loop through unique values and apply the function
for off_personnel_value in unique_off_personnel_values:
    # Filter DataFrame based on the current 'OffPersonnel' value
    subset_df = df_filtered[df_filtered['OffPersonnel'] == off_personnel_value].copy()

    # Apply the adj_ev function
    overall_def_play_adj_ev = adj_ev(subset_df, 'DefensivePlay', all_plays, 'desc')

    # Clean the name using the custom function
    df_name = f"{clean_name(off_personnel_value)}_adj_ev"

    # Store the result in the dictionary with the cleaned name
    dfs_by_off_personnel[df_name] = overall_def_play_adj_ev

# Now dfs_by_off_personnel is a dictionary where keys are cleaned 'OffPersonnel' values
# (appended with '_adj_ev') and values are DataFrames resulting from applying adj_ev to the corresponding subset.
