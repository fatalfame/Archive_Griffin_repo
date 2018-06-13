import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import SGDRegressor
import numpy as np


csvfile = '..//machine_learning/titanic.csv'
players = pandas.read_csv(csvfile)
# print the names of the columns in games.
# print(patients.columns)
# print patients.shape
# plt.hist(patients["MaritalStatusCD"])
# plt.show()
# print(patients[patients["SexCD"] == 1].iloc[10100])
# Remove any rows without Procedure ID's.
# patients = patients[patients["All Star"] > 0]
# Remove any rows with missing values.
players = players.dropna(axis=0)
# kmeans_model = KMeans(n_clusters=5, random_state=1)  # n_clusters defines how many clusters of patients we want
good_columns = players._get_numeric_data()
# kmeans_model.fit(good_columns)
# labels = kmeans_model.labels_
# pca_2 = PCA(2)
# plot_columns = pca_2.fit_transform(good_columns)
# plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=labels)
# plt.show()
# print players.corr()["Pos"]
columns = players.columns.tolist()
# columns = [c for c in good_columns if c not in ["Rk", "Age", "FTA", "BLK", "FT", "2PA", "Pos"]]
columns = [c for c in good_columns if c in ["PassengerId", "Pclass", "Sex", "Age", "Parch", "Fare"]]
target = "Survived"
train = players.sample(frac=0.40, random_state=np.random.seed(seed=None))
test = players.loc[~players.index.isin(train.index)]
print(train.shape)
print(test.shape)
# model = LinearRegression()
# model = svm.LinearSVC
# model = RandomForestRegressor(n_estimators=10)
# model = RandomForestClassifier(n_estimators=100, min_samples_leaf=10, random_state=1)
# model = linear_model.SGDRegressor(shuffle=True, random_state=1, fit_intercept=True)
model = tree.DecisionTreeClassifier(min_samples_leaf=10)
# model = linear_model.Lasso()
# model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
# print train[columns]
# print test[target]
# print players["Player"]
# sel = VarianceThreshold(threshold=(.5 * (1 - .5)))
model.fit(train[columns], train[target])
predictions = model.predict(test[columns])
# print mean_squared_error(predictions, test[target])
# print model.score(predictions, test[target])
print(accuracy_score(test[target], predictions))
# print model.score(test[target], predictions)
# Instantiate the visualizer
