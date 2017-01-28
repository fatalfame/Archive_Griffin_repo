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
from sklearn.linear_model import RandomizedLasso
import matplotlib.pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import make_classification
import matplotlib as plot
import pandas
from ggplot import *
import random



players = '..//nba_machine_learning/outputs/all_star_roster2.csv'
input_file = open(players, 'r')
reader = csv.DictReader(input_file)


def main():

    targets = []
    features = []
    feat_names = ['Points', 'Rebounds', 'Assists', 'Mins', 'Blocks', 'FGA', 'FGM', 'EFG%', 'TS%', 'FTA']
    x_2015 = []
    for row in reader:
        if '2016-17' not in row['Season']:
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
            x_2015.append([row['Player'],
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

    model = ExtraTreesClassifier()
    model.fit(features, targets)
    mi = model.feature_importances_
    pred = ([i for i in feat_names])
    fr = zip(mi, pred)
    # plt.plot(mi)
    # plt.ylabel(pred)
    # plt.show()
    classifier = DecisionTreeClassifier(min_samples_leaf=8)
    classifier.fit(features, targets)
    predictions = classifier.predict([i[1:] for i in x_2015])
    final_result = zip(predictions, x_2015)
    for row in sorted(final_result, reverse=False):
        print(row)
    for row in sorted(fr, reverse=True):
        print(row)


def convert(item):
    try:
        float(item)
        return item
    except ValueError:
        return 0


if __name__ == '__main__':
    main()
