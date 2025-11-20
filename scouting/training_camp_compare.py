import pandas as pd

def compare_and_create_diff_csv(file1, file2, output_csv):
    # Read CSV files into pandas DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Merge DataFrames based on "PlayerID"
    merged_df = pd.merge(df1, df2, on="PlayerID", suffixes=('_csv1', '_csv2'), how='outer')

    # Create a new DataFrame to store differences
    diff_df = pd.DataFrame()

    # Iterate through all columns excluding the merging column
    for column in df1.columns:
        if column == "PlayerID":
            continue  # Skip the merging column

        # Ensure both columns are numeric
        if (pd.api.types.is_numeric_dtype(merged_df[f"{column}_csv1"]) and
                pd.api.types.is_numeric_dtype(merged_df[f"{column}_csv2"])):
            try:
                # Compare the columns and add differences to the new DataFrame
                column_diff = merged_df[f"{column}_csv1"].equals(merged_df[f"{column}_csv2"])
                if not column_diff:
                    diff_df[f"{column}"] = merged_df[f"{column}_csv1"]
                    diff_df[f"{column}_diff"] = merged_df[f"{column}_csv1"] - merged_df[f"{column}_csv2"]
            except ValueError:
                print(f"Unable to compare numerical values for column '{column}' due to a structure mismatch.")
        else:
            # If the column is not numeric, add it as it is
            diff_df[f"{column}"] = merged_df[f"{column}_csv1"]

    # Write the differences to a new CSV file
    diff_df.to_csv(output_csv, index=False)

# Replace the file paths with your actual file paths
compare_and_create_diff_csv('/Users/jamesjones/game_logs/draft/Post-TC XFL 2048.csv',
                            '/Users/jamesjones/game_logs/draft/Pre-TC XFL 2048.csv',
                            '/Users/jamesjones/game_logs/draft/differences.csv')
