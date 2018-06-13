import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import *
import csv as csv
from sklearn.ensemble import *
from sklearn.tree import *
from sklearn.neighbors import *
from sklearn.feature_selection import RFE
from sklearn.svm import LinearSVC
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import pandas
from sklearn import svm
from sklearn.svm import LinearSVC
from ggplot import *
import random
from sklearn import linear_model
from sklearn.datasets import make_classification
from sklearn.datasets import make_blobs
from sklearn.datasets import make_gaussian_quantiles
from sklearn.feature_extraction.text import CountVectorizer


players = '..//nba_machine_learning/outputs/all_star_roster2.csv'
input_file = open(players, 'r')
reader = csv.DictReader(input_file)


def main():

    targets = []
    features = []
    feat_names = ['Points', 'Rebounds', 'Assists', 'Mins', 'Blocks', 'FGA', 'FGM', 'EFG%', 'TS%', 'FTA']
    x_2016 = []
    pts = []
    ast = []
    for row in reader:
        if '2016-17' not in row['Season']:
            pts.append(float(row['Points']))
            ast.append(float(row['Assists']))
            features.append([float(row['Points']),
            float(row['Rebounds']),
            float(row['Assists']),
            float(row['Mins']),
            float(row['Blocks']),
            # float(row['Fouls']),
            float(row['FGA']),
            convert(row['FGM']),
            # float(row['Steals']),
            # float(row['Turnovers']),
            # convert(row['ft%']),
            convert(row['EFG%']),
            convert(row['TS%']),
            # float(row['Games']),
            # convert(row['3p%']),
            # convert(row['3pa']),
            # convert(row['Age']),
            # convert(row['Games Started']),
            float(row['FTA'])]),
            targets.append(bool(int(row['All Star'])))
        else:
            x_2016.append([row['Player'],
            float(row['Points']),
            float(row['Rebounds']),
            float(row['Assists']),
            float(row['Mins']),
            float(row['Blocks']),
            # float(row['Fouls']),
            float(row['FGA']),
            convert(row['FGM']),
            # float(row['Steals']),
            # float(row['Turnovers']),
            # convert(row['ft%']),
            convert(row['EFG%']),
            convert(row['TS%']),
            # float(row['Games']),
            # convert(row['3p%']),
            # convert(row['3pa']),
            # convert(row['Age']),
            # convert(row['Games Started']),
            float(row['FTA'])])

    model = DecisionTreeClassifier(min_samples_leaf=10)
    model.fit(features, targets)
    mi = model.feature_importances_
    pred = ([i for i in feat_names])
    mii = []
    for m in mi:
        mii.append(round(m, 2))
    fr = zip(mii, pred)
    # plt.plot(mi)
    # plt.ylabel(pred)
    # plt.show()
    # classifier = DecisionTreeClassifier(min_samples_leaf=10)
    # classifier = SVC()
    classifier = svm.SVC(kernel='linear', C=1.0)
    classifier.fit(features, targets)
    predictions = classifier.predict([i[1:] for i in x_2016])
    y = []
    for x in x_2016:
        y.append(x[0])
    final_result = zip(predictions, y)
    for row in sorted(final_result, reverse=False):
        print(row)
    for row in sorted(fr, reverse=True):
        print(row)

    # X = np.array(features)
    # y = np.array(targets)
    # w = classifier.coef_[0]
    # print w
    # a = -w[0] / w[1]
    # xx = np.linspace(0, 50)
    # yy = a * xx - classifier.intercept_[0] / w[1]
    # h0 = plt.plot(xx, yy, 'k-', label="non weighted div")
    # plt.scatter(X[:, 0], X[:, 1], c=y)
    # plt.legend()
    # plt.show()
    # plt.scatter(pts, ast, c=y)
    # plt.xlabel('points')
    # plt.ylabel('assists')
    # plt.show()


def convert(item):
    try:
        float(item)
        return item
    except ValueError:
        return 0


if __name__ == '__main__':
    main()
