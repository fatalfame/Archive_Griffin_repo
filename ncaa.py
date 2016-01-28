import csv as csv

files = ('../Code/ncaa_machine_learning/inputs/arizona.csv', '../Code/ncaa_machine_learning/inputs/duke.csv')

for file_names in files:
    input_file = open(file_names, 'rt')
    reader = csv.DictReader(input_file)
    fieldnames = ['W-L%', 'PTS', 'SOS', 'Season']
    writer = csv.DictWriter(open('..//Code/ncaa_machine_learning/outputs/team_features.csv', 'wb'),
                            fieldnames=fieldnames)
    for row in reader:
        print row
        row = {k: v for k, v in row.iteritems()}
        writer.writeheader()
        for value in row.iteritems():
            writer.writerow({'Season': row['Season'], 'W-L%': row['W-L%'], 'PTS': row['PTS'], 'SOS': row['SOS']})

