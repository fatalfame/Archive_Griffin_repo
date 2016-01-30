import csv as csv

az = '../Code/ncaa_machine_learning/inputs/arizona.csv'
duke = '../Code/ncaa_machine_learning/inputs/duke.csv'


fieldnames = ['Season', 'W-L%', 'OFF', 'DEF', 'DukeSeason', 'DukeW-L', 'DukeOFF', 'DukeDEF']
writer = csv.DictWriter(open('..//Code/ncaa_machine_learning/outputs/team_features.csv', 'wb'),
                        fieldnames=fieldnames)

writer.writeheader()
input_file = open(az, 'rt')
input_file2 = open(duke, 'rt')
reader = csv.DictReader(input_file)
reader2 = csv.DictReader(input_file2)
for row in reader:
    writer.writerow({'Season': row['Season'], 'W-L%': row['W-L%'], 'OFF': row['OFF'], 'DEF': row['DEF']})
for row in reader2:
    writer.writerow({'DukeSeason': row['Season'], 'DukeW-L': row['W-L%'], 'DukeOFF': row['OFF'],
                     'DukeDEF': row['DEF']})

