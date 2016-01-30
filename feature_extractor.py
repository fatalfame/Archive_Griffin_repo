import csv as csv

az = '../Code/ncaa_machine_learning/inputs/arizona.csv'
Opp = '../Code/ncaa_machine_learning/inputs/az_state.csv'


fieldnames = ['Season', 'W-L%', 'OFF', 'DEF', 'OppSeason', 'OppW-L', 'OppOFF', 'OppDEF']
writer = csv.DictWriter(open('..//Code/ncaa_machine_learning/outputs/team_features.csv', 'wb'),
                        fieldnames=fieldnames)

writer.writeheader()
input_file = open(az, 'rt')
input_file2 = open(Opp, 'rt')
reader = csv.DictReader(input_file)
reader2 = csv.DictReader(input_file2)
for row in reader:
    writer.writerow({'Season': row['Season'], 'W-L%': row['W-L%'], 'OFF': row['OFF'], 'DEF': row['DEF']})
for row in reader2:
    writer.writerow({'OppSeason': row['Season'], 'OppW-L': row['W-L%'], 'OppOFF': row['OFF'],
                     'OppDEF': row['DEF']})

