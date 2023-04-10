import csv


def get_totals(input_values):
    # Open the CSV file
    with open('/Users/jamesjones/game_logs/MFN-Targets.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

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


play_dict = {'Singeback 4 Wide': ['Singleback 4 Wide Quick Outs'],
             'Singleback Normal': ['Singleback Normal TE Quick Out', 'Singleback Normal Quick Slant'],
             'Singleback Slot Strong': [],
             'Singleback Big': [],
             'I Formation 3 WR': ['I Formation 3WR WR Out', 'I Formation 3WR PA Fullback Flat'],
             'Split Backs 3 Wide': ['Split Backs 3 Wide WR Quick Out'],
             'Strong I Normal': [],
             'Weak I Normal': [],
             'I Formation Twin WR': ['I Formation Twin WR Hard Slants', 'I Formation Twin WR Quick Outs'],
             'I Formation Normal': ['I Formation Normal FL Hitch'],
             'Strong I Big': ['Strong I Big Backfield Drag'],
             'I Formation Power': ['I Formation Power PA Flats', 'I Formation Power Play Action HB Downfield'],
             }
for formation, plays in play_dict.items():
    print(f'{formation}:')
    for position, total_value in get_totals(plays):
        print(f'Total for {position} is {total_value}')
    print('')