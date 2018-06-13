import numpy as np
import pandas
import random
# from sklearn.svm import *
import csv as csv
from sklearn.ensemble import *
from sklearn.tree import *
# from sklearn.neighbors import *
# from sklearn.feature_selection import RFE
# from sklearn import *
# import pydot_ng
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score

players = '..//march_madness/team_stats2.csv'
df = pandas.read_csv(players)
targets = []
features = []
x_2017 = []
# for y in df:
#     print(y)
for d in df['Season']:
    if '2017-18' in d:
        x_2017.append(d)

df.drop(['School', 'Season', 'Conf', 'W', 'L'], axis=1, inplace=True)
columns = df.columns.tolist()
columns = [c for c in columns if c not in ["NCAA"]]
target = "NCAA"
train = df.sample(frac=0.7, random_state=random.seed())
test = df.loc[~df.index.isin(train.index)]
# print(columns)
model = RandomForestClassifier()
model.fit(train[columns], train[target])
predictions = model.predict(test[columns])
print('roc_auc_score: ', roc_auc_score(test[target], predictions))
print('Accuracy:', round(accuracy_score(test[target], predictions), 3), '%')
fi = model.feature_importances_
fi = ([round(f, 3) for f in fi])
fa = ([i for i in columns])
features = zip(fi, fa)
print('-------------------')
print('Feature Importance:')
print('-------------------')
for row in sorted(features, reverse=True):
    print(row)
    # row['W'] = float(row['W'])
    # row['L'] = float(row['L'])
#     row['Percent'] = float(row['Percent'])
#     if row['SOS']:
#             row['SOS'] = float(row['SOS'])
#     if row['OFF']:
#             row['OFF'] = float(row['OFF'])
#     if row['DEF']:
#             row['DEF'] = float(row['DEF'])
#     if row['AP High']:
#             row['AP High'] = float(row['AP High'])
#     if row['AP Final']:
#             row['AP Final'] = float(row['AP Final'])
#     if '2016-17' not in row['Season']:
#         features.append(
#         # [row['W'],
#         # row['L'],
#         [row['Percent'],
#         row['SOS'],
#         row['OFF'],
#         row['DEF'],
#         row['AP High']]),
#         # row['AP Final']])
#         targets.append(row['NCAA'])
#     else:
#         x_2016.append(
#         [row['School'],
#         # row['W'],
#         # row['L'],
#         row['Percent'],
#         row['SOS'],
#         row['OFF'],
#         row['DEF'],
#         row['AP High']])
#         # row['AP Final']])
#
#
# def convert(val):
#     if val == 'Lost First Four':
#         val = 0
#     if val:
#         val = float(val)
#         return val
#     else:
#         val = None
#         return val
#
# feat_names = ['Win %', 'SOS', 'OFF', 'DEF', 'AP High']
# model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10)
# model.fit(features, targets)
# mi = model.feature_importances_
# pred = ([i for i in feat_names])
# mii = []
# for m in mi:
#     mii.append(round(m, 2))
# fr = zip(mii, pred)
# classifier = RandomForestRegressor(n_estimators=100, min_samples_leaf=10)
# # classifier = DecisionTreeClassifier()
# # classifier = RandomForestClassifier(n_estimators=100)
# classifier.fit(features, targets)
# predictions = classifier.predict([i[1:] for i in x_2016])
# final_result = zip(predictions, x_2016)
# for row in sorted(final_result, reverse=True):
#     print(row)
# for row in sorted(fr, reverse=True):
#     print(row)

# classifier = classifier.fit(features, targets)
# tree.export_graphviz(classifier, out_file='tree.dot')
# graph = pydot_ng.graph_from_dot_file('tree.dot')
# graph.write_png('newtree.png')
# check_call(['dot','-Tpng','tree.dot','-o','tree_done.png'])
