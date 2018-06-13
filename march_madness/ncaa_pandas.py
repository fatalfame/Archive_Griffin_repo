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
import seaborn as sns

players = pandas.read_csv('..//march_madness/team_stats2.csv')
# plt.hist(players["NCAA"])
# plt.show()
# print(players[players["Season"] == '2017-18'])
# players = players[players["G"] > 10]
x = players.corr()
plt.show(sns.heatmap(x, xticklabels=x.columns, yticklabels=x.columns))
players = players.dropna(axis=0)
good_columns = players._get_numeric_data()
# x = players.corr()["NCAA"]
# plt.show(players.corr()["NCAA"])
# so = x.sort_values(kind="quicksort", ascending=False)
# print(so)
# columns = players.columns.tolist()
# columns = [c for c in columns if c not in ["School", "Season", "Percent", "SRS", "SOS", "OFF", "DEF", "AP High",
#                                            "AP Final", "NCAA"]]
# target = "NCAA"
# train = players.sample(frac=0.3, random_state=2)
# test = players.loc[~players.index.isin(train.index)]
# model = RandomForestClassifier(min_samples_leaf=10)
# model = model.fit(train[columns], train[target])
# predictions = model.predict(test[columns])
# fr = zip(test["School"], test["Season"], predictions, test[target])
# for f in fr:
#     print(f)
# print(accuracy_score(predictions, test[target]))
# x = list(good_columns)

