import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


for x in range(0, 50):
    csv = '..//healthcareai/tests/fixtures/dtest2.csv'
    patients = pandas.read_csv(csv)
    patients = patients.dropna(axis=0)
    patients.drop(['PatientID', 'InTestWindowFLG'], axis=1, inplace=True)
    # print patients.corr()["ThirtyDayReadmitFLG"]
    good_columns = patients._get_numeric_data()
    # good_columns = patients.select_dtypes(include=['int64', 'float64'])
    columns = patients.columns.tolist()
    columns = [c for c in good_columns if c not in ["ThirtyDayReadmitFLG", "InTestWindowFLG", "PatientID"]]
    target = "ThirtyDayReadmitFLG"
    # print columns
    train = patients.sample(frac=0.5, random_state=random.seed())
    test = patients.loc[~patients.index.isin(train.index)]
    # print train.shape
    # print test.shape
    # model = LinearRegression()
    # model = svm.LinearSVC()
    # model = RandomForestClassifier(n_estimators=100, min_samples_leaf=10, random_state=1)
    model = tree.DecisionTreeClassifier()
    # model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
    model.fit(train[columns], train[target])
    predictions = model.predict(test[columns])
    # print mean_squared_error(predictions, test[target])
    print 'accuracy:', accuracy_score(test[target], predictions), '%'
# corr = patients.corr()
# g = sns.heatmap(corr,
#                 xticklabels=corr.columns.values,
#                 yticklabels=corr.columns.values, annot=True, cmap="winter", linewidths=0.5)
# for item in g.get_xticklabels():
#     item.set_rotation(45)
# for item in g.get_yticklabels():
#     item.set_rotation(0)
# sns.plt.show()
# g = list(columns)
# tree.export_graphviz(decision_tree=model,feature_names=g, out_file='..//healthcareai/tests/fixtures/tree2.dot')
