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


play_dict_rf = {'Singeback 4 Wide': ['Singleback 4 Wide Quick Outs'],
             'Singleback Normal': ['Singleback Normal TE Quick Out'],
             'Singleback Slot Strong': ['Singleback Slot Strong HB Checkdown'],
             'Singleback Big': [],
             'I Formation 3 WR': ['I Formation 3WR WR Out', 'I Formation 3WR Backfield Flats',
                                  'I Formation 3WR FL Post', 'I Formation 3WR Slot Short WR Deep'],
             'Split Backs 3 Wide': [],
             'Strong I Normal': [],
             'Weak I Normal': ['Weak I Normal WR Corner TE Middle', 'Weak I Normal Skinny Posts'],
             'I Formation Twin WR': ['I Formation Twin WR Hard Slants', 'I Formation Twin WR Quick Outs'],
             'I Formation Normal': ['I Formation Normal FL Hitch', 'I Formation Normal Max Protect'],
             'Strong I Big': ['Strong I Big Backfield Drag'],
             'I Formation Power': ['I Formation Power Play Action HB Downfield', 'I Formation Power PA Flats'],
             }
for formation, plays in play_dict_rf.items():
    print(f'{formation}:')
    for position, total_value in get_totals(plays):
        print(f'Total for {position} is {total_value}')
    print('')


play_dict_pf = {'Shotgun Normal': ['Shotgun Normal HB Flare'],
             'Singleback Normal': ['Singleback Normal TE Quick Out', 'Singleback Normal WR Quick In'],
             'Singleback Big': ['Singleback Big Ins and Outs'],
             'Split Backs 3 Wide': [],
             'Strong I Normal': ['Strong I Normal Short Attack'],
             'Weak I Normal': ['Weak I Normal WR Corner TE Middle', 'Weak I Normal Skinny Posts'],
             'I Formation Twin WR': ['I Formation Twin WR Hard Slants', 'I Formation Twin WR Quick Outs'],
             'I Formation Normal': ['I Formation Normal PA Fullback Flat', 'I Formation Normal FL Hitch'],
             'Strong I Big': [],
             'I Formation Power': ['I Formation Power PA Flats', 'I Formation Power Play Action HB Downfield'],
             }
for formation, plays in play_dict_pf.items():
    print(f'{formation}:')
    for position, total_value in get_totals(plays):
        print(f'Total for {position} is {total_value}')
    print('')

