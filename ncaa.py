import csv as csv
import numpy as np
import itertools

with open('../Downloads/arizona.csv', 'rt') as f:    # Load in the csv file
    reader = csv.reader(f)
    next(reader)
    offense_features = []
    win_loss_features = []
    defense_features = []
    for row in reader:
        rk = row[0]
        season = row[1]
        conf = row[2]
        wins = row[3]
        losses = row[4]
        percentage = row[5]
        srs = row[6]
        sos = row[7]
        offense = row[8]
        defense = row[9]
        ap_pre = row[10]
        ap_high = row[11]
        ap_final = row[12]
        tournament = row[13]
        coaches = row[14]
        offense_features.append(offense)
        defense_features.append(defense)
        win_loss_features.append(percentage)
    print 'az', offense_features
    print 'az', defense_features
    print 'az', win_loss_features
with open('../Downloads/duke.csv', 'rt') as d:    # Load in the csv file
    reader = csv.reader(d)
    next(reader)
    offense2_features = []
    win_loss2_features = []
    defense2_features = []
    for row in reader:
        rk = row[0]
        season = row[1]
        conf = row[2]
        wins = row[3]
        losses = row[4]
        percentage = row[5]
        srs = row[6]
        sos = row[7]
        offense = row[8]
        defense = row[9]
        ap_pre = row[10]
        ap_high = row[11]
        ap_final = row[12]
        tournament = row[13]
        coaches = row[14]
        offense2_features.append(offense)
        defense2_features.append(defense)
        win_loss2_features.append(percentage)
    print 'dk', offense2_features
    print 'dk', defense2_features
    print 'dk', win_loss2_features


output = open('../Downloads/team_features.csv', "wb")
mywriter = csv.writer(output)
mywriter.writerow(offense_features)
output.close()