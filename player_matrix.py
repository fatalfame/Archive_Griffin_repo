import numpy as np
from sklearn.svm import SVC
import csv as csv

players = '../Code/ncaa_machine_learning/outputs/nba_players.csv'
input_file = open(players, 'rb')
reader = csv.DictReader(input_file)

points = []
minutes = []
targets = []
stars = []
x_2015 = []
features = []
for row in reader:
    if '2015-16' not in row['Season']:
        points.append(float(row['Points']))
        minutes.append(float(row['Minutes']))
        stars.append(bool(int(row['All Star'])))
    else:
        x_2015.append(float(row['Points']))
        x_2015.append(float(row['Minutes']))

x = zip(points, minutes, stars)
feat = []
tar = []
for data in x:
    feat.append(data[:-1])
    tar.append(data[-1])

print 'features:', feat
print 'targets:', tar

a = np.array(feat)

classifier = SVC()
classifier.fit(feat, tar)
print classifier.predict(a)


# some_data = [(1, 2, 3), (4, 5, 6)]
# features = []
# targets = []
# for data in some_data:
#     features.append(data[:-1])
#     targets.append(data[-1])
#
# print 'features:', features
# print 'targets:', targets
#
# a = np.array(features)
# print a, type(a)
#
# classifier = SVC()
# classifier.fit(features, targets)
# print 'prediction:', classifier.predict([(1, 2)])
# print "You don't have to use numpy"

# x_known = np.matrix('1 1; 0 1')
# y_known = [1, 0]
# x_unknown = np.matrix('1 0; 0 0')
# classifier = SVC()
# classifier.fit(x_known, y_known)
# print classifier.predict(x_unknown)
#
# x_2014 = np.matrix('20 30; 2 4')
# y_2014 = [1, 0]
# x_2015 = np.matrix('13 25; 22 35; 3 2')
# classifier = SVC()
# classifier.fit(x_2014, y_2014)
# print classifier.predict(x_2015)


