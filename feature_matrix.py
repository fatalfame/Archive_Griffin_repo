import csv as csv

matchup = '../Code/ncaa_machine_learning/inputs/matchup.csv'
features = '../Code/ncaa_machine_learning/outputs/team_features.csv'


fieldnames = ['Year', 'Outcome', 'OFF', 'DEF', 'Season', 'W-L%', 'SeasonOFF', 'SeasonDEF']
writer = csv.DictWriter(open('..//Code/ncaa_machine_learning/outputs/feature_matrix.csv', 'wb'),
                        fieldnames=fieldnames)

writer.writeheader()
input_file = open(matchup, 'rt')
input_file2 = open(features, 'rt')
reader = csv.DictReader(input_file)
reader2 = csv.DictReader(input_file2)
for row in reader:
    writer.writerow({'Year': row['Year'], 'Outcome': row['Outcome'], 'OFF': row['OFF'], 'DEF': row['DEF']})
for row in reader2:
    writer.writerow({'W-L%': row['W-L%'], 'Season': row['Season'], 'SeasonOFF': row['OFF'], 'SeasonDEF': row['DEF']})

