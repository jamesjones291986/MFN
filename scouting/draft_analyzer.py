import os
import pandas as pd

def import_and_analyze_trend(directory_path):
    # Get a list of CSV files in the specified directory
    csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

    # Create an empty DataFrame to store the concatenated differences
    concatenated_df = pd.DataFrame()

    # Iterate through each CSV file
    for csv_file in csv_files:
        file_path = os.path.join(directory_path, csv_file)

        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Print column names for debugging
        print(f"Columns for {csv_file}: {df.columns}")

        # Concatenate DataFrames
        concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

    # Continue with the rest of the script...

# Replace the directory path with the actual path to your CSV files
import_and_analyze_trend('/Users/jamesjones/game_logs/draft/Differences/')
