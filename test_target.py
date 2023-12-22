import csv
import io
import gdown

def download_csv_from_drive(file_url):
    # Download the CSV file from Google Drive using gdown
    response = gdown.download(file_url, quiet=False)
    with open(response, 'r', encoding='utf-8') as file:
        csv_data = io.StringIO(file.read())
    return csv_data

def get_totals(input_values, csv_data):
    # Parse CSV data
    reader = csv.DictReader(csv_data)

    # Initialize a dictionary to store the total values for each column B value
    totals = {}

    # Loop through each row in the CSV file
    for row in reader:

        # If the value in column A matches any of the input values
        if row['OffensivePlay'] in input_values:

            # Add the value in column C to the total for this column B value
            if row['target'] in totals:
                totals[row['target']] += int(float(row['tgt %'].replace('%', '')))
            else:
                totals[row['target']] = int(float(row['tgt %'].replace('%', '')))

    # Sort the totals in descending order
    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    # Return the sorted totals as a list of tuples
    return sorted_totals

# Google Drive File URL of the CSV file
drive_file_url = 'https://docs.google.com/spreadsheets/d/1FraQWCNpatVlQvMDrGeTrWkITgX3I_yp/edit#gid=1532934773'

# Example usage for play_dict_rf
play_dict_rf = {'Singeback 4 Wide': [],
                'Singeback Empty 4': [],
                'Singleback Normal': ['Singleback Normal TE Quick Out'],
                'Singleback Slot Strong': [],
                'Singleback Big': [],
                'I Formation 3 WR': [],
                'Split Backs 3 Wide': [],
                'Strong I Normal': [],
                'Weak I Normal': [],
                'I Formation Twin WR': [],
                'I Formation Normal': [],
                'Strong I Big': [],
                'I Formation Power': [],
                }

csv_data = download_csv_from_drive(drive_file_url)

for formation, plays in play_dict_rf.items():
    print(f'{formation}:')
    for position, total_value in get_totals(plays, csv_data):
        print(f'Total for {position} is {total_value}')
    print('')

# Example usage for play_dict_pf
play_dict_pf = {'Shotgun Normal': [],
                'Singleback Normal': [],
                'Singleback Big': [],
                'Split Backs 3 Wide': [],
                'Strong I Normal': [],
                'Weak I Normal': [],
                'I Formation Twin WR': [],
                'I Formation Normal': [],
                'Strong I Big': [],
                'I Formation Power': [],
                }

csv_data = download_csv_from_drive(drive_file_url)

for formation, plays in play_dict_pf.items():
    print(f'{formation}:')
    for position, total_value in get_totals(plays, csv_data):
        print(f'Total for {position} is {total_value}')
    print('')
