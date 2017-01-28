import pandas
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn.neighbors import *
from ggplot import *
from sklearn.tree import *
from sklearn.metrics import accuracy_score
from sklearn import tree

players = pandas.read_csv("..//nba_machine_learning/2016-17_players.csv")
# plt.hist(players["GS"])
# plt.show()
# print players[players["GS"] == 27]
# players = players[players["G"] > 10]
players = players.dropna(axis=0)
# kmeans_model = KMeans(n_clusters=5, random_state=1)
good_columns = players._get_numeric_data()
# kmeans_model.fit(good_columns)
# labels = kmeans_model.labels_
# pca_2 = PCA(2)
# plot_columns = pca_2.fit_transform(good_columns)
# plt.scatter(x=plot_columns[:, 0], y=plot_columns[:, 1], c=labels)
# plt.show()
# x = players.corr()["All Star"]
# plt.matshow(players.corr()["All Star"])
# so = x.sort_values(kind="quicksort", ascending=False)
# print so
columns = players.columns.tolist()
columns = [c for c in columns if c not in ["Player", "Rk", "Tm", "Pos"]]
target = "Pos"
train = players.sample(frac=0.5, random_state=1)
test = players.loc[~players.index.isin(train.index)]
# model = LinearRegression()
# model = KNeighborsClassifier()
model = DecisionTreeClassifier(min_samples_leaf=10)
# model = DecisionTreeRegressor(min_samples_leaf=10)
# model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
# model = svm.LinearSVR()
model = model.fit(train[columns], train[target])
predictions = model.predict(test[columns])
# print mean_squared_error(predictions, test[target])
# print model.feature_importances_
print accuracy_score(predictions, test[target])
x = list(good_columns)
export_graphviz(decision_tree=model,feature_names=x, out_file='..//nba_machine_learning/allstar.dot')

