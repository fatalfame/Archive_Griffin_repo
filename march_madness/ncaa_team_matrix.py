import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import *
import csv as csv
from sklearn.ensemble import *
from sklearn.tree import *
from sklearn.neighbors import *
from sklearn.feature_selection import RFE
from sklearn import *


players = '..//Code/Griffin_repo/march_madness/team_stats.csv'
input_file = open(players, 'rb')
reader = csv.DictReader(input_file)
targets = []
features = []
x_2015 = []
for row in reader:
    x = row['OFF']
    print row['School']
    print row['Season']
    row['W'] = float(row['W'])
    print 'W', type(row['W'])
    row['L'] = float(row['L'])
    print 'L', type(row['L'])
    row['Percent'] = float(row['Percent'])
    print '%', type(row['Percent'])
    if row['SOS']:
            row['SOS'] = float(row['SOS'])
    else:
        row['SOS'] = None
    print 'SOS', type(row['SOS'])
    row['OFF'] = float(row['OFF'])
    print 'OFF', type(row['OFF'])
    row['DEF'] = float(row['DEF'])
    print 'DEF', type(row['DEF'])
    row['AP High'] = float(row['AP High'])
    print 'AP High', type(row['AP High'])
    row['AP Final'] = float(row['AP Final'])
    print 'AP Final', type(row['AP Final'])
    if '2015-16' not in row['Season']:
        features.append([row['W'],
        row['L'],
        row['Percent'],
        row['SOS'],
        row['OFF'],
        row['DEF'],
        row['AP High'],
        row['AP Final']])
        targets.append(row['NCAA'])
    else:
        x_2015.append([row['W'],
        row['L'],
        row['Percent'],
        row['SOS'],
        row['OFF'],
        row['DEF'],
        row['AP High'],
        row['AP Final']])


def convert(val):
    if val:
        for k in val:
            val = float(val)
            return val
    else:
        val = None
        return val

# print 'features:', features
# print 'targets:', targets

classifier = RandomForestClassifier()
classifier.fit(features, targets)
predictions = classifier.predict([i[1:] for i in x_2015])
final_result = zip(predictions, x_2015)
for row in sorted(final_result, reverse=True):
    print row
