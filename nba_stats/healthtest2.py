import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.svm import *
import csv as csv
from sklearn.ensemble import *
from sklearn.tree import *
from sklearn.neighbors import *
from sklearn.feature_selection import RFE
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split



players = '..//healthcareai/tests/fixtures/HCPyDiabetesClinical2.csv'
input_file = open(players, 'r')
reader = csv.DictReader(input_file)

# # CSV snippet for reading data into dataframe
# df = pd.read_csv('..//healthcareai/tests/fixtures/HCPyDiabetesClinical2.csv')


targets = []
features = []
test_set = []
answers = []
# X, y = np.arange(10).reshape((5, 2)), range(5)
# print X
# print y
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
# print X_train
# print y_train
# print X_test
# print y_test

for row in reader:
    if 'N' not in row['trainFLG']:
        # this is a list of features and targets for a training set
        features.append([int(row['SystolicBPNBR']),
        int(row['A1CNBR']),
        int(row['GenderFLG']),
        int(row['LDLNBR'])]),
        targets.append(int(row['ThirtyDayReadmitFLG']))
    else:
        # this is a list of features for your set you want to test and predict
        test_set.append([int(row['PatientID']),
        int(row['SystolicBPNBR']),
        int(row['A1CNBR']),
        int(row['GenderFLG']),
        int(row['LDLNBR'])]),
        answers.append(int(row['ThirtyDayReadmitFLG']))


# print 'features:', features
# print 'targets:', targets

classifier = RandomForestClassifier(n_estimators=500)
classifier.fit(features, targets)
predictions = classifier.predict([i[1:] for i in test_set])
final_result = zip(predictions, test_set)
# for row in final_result:
#     print row
print accuracy_score(answers, predictions)

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
