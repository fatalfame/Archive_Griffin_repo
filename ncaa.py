import csv as csv

files = ('../Code/ncaa_machine_learning/inputs/arizona.csv', '../Code/ncaa_machine_learning/inputs/duke.csv')

for file_names in files:
    input_file = open(file_names, 'rt')
    reader = csv.DictReader(input_file)
    for row in reader:
        row = {k: v for k, v in row.iteritems()}
        print row
        fieldnames = ['Rk', 'W-L%', 'SOS']
        writer = csv.DictWriter(open('..//Code/ncaa_machine_learning/outputs/team_features.csv', 'wb'),
                                fieldnames=row)
        writer.writeheader()
        writer.writerow(row)
