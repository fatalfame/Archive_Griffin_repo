import numpy as np
from sklearn.svm import *
import csv as csv
from sklearn.ensemble import *
from sklearn.tree import *
from sklearn.neighbors import *
from sklearn.feature_selection import RFE
from sklearn import *
from subprocess import check_call
# import pydot_ng

players = '..//march_madness/team_stats.csv'
input_file = open(players, 'rb')
reader = csv.DictReader(input_file)
targets = []
features = []
x_2016 = []
for row in reader:
    row['W'] = float(row['W'])
    row['L'] = float(row['L'])
    row['Percent'] = float(row['Percent'])
    if row['SOS']:
            row['SOS'] = float(row['SOS'])
    if row['OFF']:
            row['OFF'] = float(row['OFF'])
    if row['DEF']:
            row['DEF'] = float(row['DEF'])
    if row['AP High']:
            row['AP High'] = float(row['AP High'])
    if row['AP Final']:
            row['AP Final'] = float(row['AP Final'])
    if '2016-17' not in row['Season']:
        features.append(
        [row['W'],
        row['L'],
        row['Percent'],
        row['SOS'],
        row['OFF'],
        row['DEF'],
        row['AP High'],
        row['AP Final']])
        targets.append(row['NCAA'])
    else:
        x_2016.append(
        [row['School'],
        row['W'],
        row['L'],
        row['Percent'],
        row['SOS'],
        row['OFF'],
        row['DEF'],
        row['AP High'],
        row['AP Final']])


def convert(val):
    if val == 'Lost First Four':
        val = 0
    if val:
        val = float(val)
        return val
    else:
        val = None
        return val


classifier = RandomForestRegressor(n_estimators=100)
classifier.fit(features, targets)
predictions = classifier.predict([i[1:] for i in x_2016])
final_result = zip(predictions, x_2016)
for row in sorted(final_result, reverse=True):
    print row


# classifier = classifier.fit(features, targets)
# tree.export_graphviz(classifier, out_file='tree.dot')
# graph = pydot_ng.graph_from_dot_file('tree.dot')
# graph.write_png('newtree.png')
# check_call(['dot','-Tpng','tree.dot','-o','tree_done.png'])
