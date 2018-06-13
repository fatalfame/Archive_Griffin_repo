import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import *
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
import csv as csv
from sklearn.ensemble import *
from sklearn.tree import *
from sklearn.neighbors import *
from sklearn.feature_selection import RFE
from sklearn.svm import LinearSVC
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.svm import LinearSVC
from ggplot import *
import random
from sklearn import linear_model
from sklearn.datasets import make_classification
from sklearn.datasets import make_blobs
from sklearn.datasets import make_gaussian_quantiles
from sklearn.feature_extraction.text import CountVectorizer


players = '..//nba_machine_learning/outputs/all_star_predictions_2017.csv'
input_file = open(players, 'r')
reader = csv.DictReader(input_file)


def main():

    targets = []
    features = []
    feat_names = ['Points', 'Rebounds', 'Assists', 'Mins', 'Blocks', 'FGA', 'FGM', 'EFG%', 'TS%', 'FTA', '3p%', 'Age']
    x_2017 = []
    pts = []
    ast = []
    for row in reader:
        if '2017-18' not in row['Season']:
            pts.append(convert(row['Points']))
            ast.append(convert(row['Assists']))
            features.append([convert(row['Points']),
            convert(row['Rebounds']),
            convert(row['Assists']),
            convert(row['Mins']),
            convert(row['Blocks']),
            # convert(row['Fouls']),
            convert(row['FGA']),
            convert(row['FGM']),
            # convert(row['Steals']),
            # convert(row['Turnovers']),
            # convert(row['ft%']),
            convert(row['EFG%']),
            convert(row['TS%']),
            # convert(row['Games']),
            convert(row['3p%']),
            # convert(row['3pa']),
            convert(row['Age']),
            # convert(row['Games Started']),
            convert(row['FTA'])]),
            targets.append(bool(int(row['All Star'])))
        else:
            x_2017.append([row['Player'],
            convert(row['Points']),
            convert(row['Rebounds']),
            convert(row['Assists']),
            convert(row['Mins']),
            convert(row['Blocks']),
            # convert(row['Fouls']),
            convert(row['FGA']),
            convert(row['FGM']),
            # convert(row['Steals']),
            # convert(row['Turnovers']),
            # convert(row['ft%']),
            convert(row['EFG%']),
            convert(row['TS%']),
            # convert(row['Games']),
            convert(row['3p%']),
            # convert(row['3pa']),
            convert(row['Age']),
            # convert(row['Games Started']),
            convert(row['FTA'])])

    # model = MLPClassifier()
    # model.fit(features, targets)
    # mi = model.feature_importances_
    # pred = ([i for i in feat_names])
    # mii = []
    # for m in mi:
    #     mii.append(round(m, 2))
    # fr = zip(mii, pred)
    # plt.plot(mi)
    # plt.ylabel(pred)
    # plt.show()
    # features = float([f for f in features])
    # targets = float([t for t in targets])
    classifier = MLPClassifier()
    # classifier = SVC()
    # classifier = SVC()
    # classifier = svm.SVC(kernel='linear', C=1.0)
    classifier.fit(features, targets)
    predictions = classifier.predict([i[1:] for i in x_2017])
    y = []
    for x in x_2017:
        y.append(x[0])
    final_result = zip(predictions, y)
    for row in sorted(final_result, reverse=False):
        print(row)
    # for row in sorted(fr, reverse=True):
    #     print(row)


def convert(item):
    try:
        float(item)
        return item
    except ValueError:
        return 0


if __name__ == '__main__':
    main()
