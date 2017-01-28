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
from sklearn import tree
from tqdm import tqdm
from matplotlib import *
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error



csvfile = '..//healthcareai/tests/fixtures/test4.csv'
input_file = open(csvfile, 'r')
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
        features.append([int(row['PatientAge']),
        # int(row['LateStartFLG']),
        # int(row['PediatricFLG']),
        # int(row['AddOnCaseFLG']),
        # int(row['FirstCaseFLG']),
        # int(row['PrimaryTimeBlockFLG']),
        # int(row['OperatingRoomMinuteQTY']),
        # int(row['ProcedureID']),
        # int(row['StateCD']),
        # int(row['CountyCD']),
        int(row['PatZip']),
        int(row['EthnicGroupCD']),
        # int(row['MaritalStatusCD']),
        int(row['ReligionCD']),
        int(row['LanguageCD']),
        int(row['PrimaryFinancialClassCD']),
        int(row['EmploymentStatusCD']),
        # int(row['PatientStatusCD']),
        int(row['CountyCD'])]),
        targets.append(int(row['SexCD']))
    else:
        # this is a list of features for your set you want to test and predict
        test_set.append([int(row['SexCD']),
        # int(row['LateStartFLG']),
        # int(row['PediatricFLG']),
        # int(row['AddOnCaseFLG']),
        # int(row['FirstCaseFLG']),
        # int(row['PrimaryTimeBlockFLG']),
        # int(row['OperatingRoomMinuteQTY']),
        # int(row['ProcedureID']),
        # int(row['StateCD']),
        # int(row['CountyCD']),
        int(row['PatZip']),
        int(row['EthnicGroupCD']),
        # int(row['MaritalStatusCD']),
        int(row['ReligionCD']),
        int(row['LanguageCD']),
        int(row['PrimaryFinancialClassCD']),
        int(row['PatientAge']),
        # int(row['PatientStatusCD']),
        int(row['EmploymentStatusCD']),
        int(row['CountyCD'])]),
        answers.append(int(row['SexCD']))


# print 'features:', features
# print 'targets:', targets

classifier = LinearSVC()
classifier.fit(features, targets)
predictions = classifier.predict([i[1:] for i in test_set])
final_result = zip(predictions, test_set)
# for row in sorted(final_result, reverse=True):
#     print row
print accuracy_score(answers, predictions)
# print classifier.feature_importances_







