import numpy as np
from sklearn.svm import *
import csv as csv
from sklearn.ensemble import *
from sklearn.tree import *
from sklearn.neighbors import *
from sklearn.feature_selection import RFE
from sklearn import *
from subprocess import check_call
import pydot_ng

weather = '..//Griffin_repo/weather/724242.csv'
input_file = open(weather, 'rb')
reader = csv.DictReader(input_file)
targets = []
features = []
x_2016 = []
for row in reader:
    row['MEDIAN'] = float(row['MEDIAN'])
    if row['PRCP']:
            row['PRCP'] = float(row['PRCP'])
    if row['TMAX']:
            row['TMAX'] = float(row['TMAX'])
    if row['TMIN']:
            row['TMIN'] = float(row['TMIN'])
    # if row['MONTH']:
    #         row['MONTH'] = float(row['MONTH'])
    if '2016' not in row['YEAR']:
        features.append(
        [row['MEDIAN'],
        row['TMIN'],
        row['TOBS'],
        row['YEAR'],
        row['MONTH'],
        row['PRCP'],
        row['DAY']])
        targets.append(row['TMAX'])
    else:
        x_2016.append(
        [row['DATE'],
        row['MEDIAN'],
        row['TMIN'],
        row['TOBS'],
        row['YEAR'],
        row['MONTH'],
        row['PRCP'],
        row['DAY']])


def convert(val):
    if val:
        val = float(val)
        return val
    else:
        val = None
        return val


classifier = RandomForestClassifier(n_estimators=100)
classifier.fit(features, targets)
predictions = classifier.predict([i[1:] for i in x_2016])
final_result = zip(predictions, x_2016)
for row in sorted(final_result):
    print row


# classifier = classifier.fit(features, targets)
# tree.export_graphviz(classifier, out_file='tree.dot')
# graph = pydot_ng.graph_from_dot_file('tree.dot')
# graph.write_png('newtree.png')
# check_call(['dot','-Tpng','tree.dot','-o','tree_done.png'])
