import pandas
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn import svm
from sklearn.neighbors import *
# from ggplot import *
from sklearn.tree import *
from itertools import product
from sklearn.metrics import accuracy_score
from sklearn import tree

players = pandas.read_csv("..//nba_machine_learning/outputs/all_players_2017.csv")
# plt.hist(players["Rebounds"])
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
# print(so)
columns = players.columns.tolist()
columns = [c for c in columns if c not in ["Player", "Rk", "Season", "Pos", "Team", "All Star"]]
target = "All Star"
train = players.sample(frac=0.3, random_state=2)
test = players.loc[~players.index.isin(train.index)]
# model = LinearRegression()
# model = KNeighborsClassifier()
# model = MLPClassifier()
# model = MLPRegressor(solver='adam', activation='relu')
# model = DecisionTreeClassifier()
model = RandomForestClassifier(min_samples_leaf=10)
# model = DecisionTreeRegressor(min_samples_leaf=10)
# model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
# model = svm.LinearSVR()
model = model.fit(train[columns], train[target])
predictions = model.predict(test[columns])
# print([p for p in predictions]), print([y for y in test[columns]])
# print mean_squared_error(predictions, test[target])
# print(model.feature_importances_)
# for z in product(players["Player"], players["Season"], test[target], predictions):
#     print(z)
fr = zip(test["Player"], test["Season"], predictions, test[target])
for f in fr:
    print(f)
print(accuracy_score(predictions, test[target]))
x = list(good_columns)
# export_graphviz(decision_tree=model,feature_names=x, out_file='..//nba_machine_learning/allstar.dot')

