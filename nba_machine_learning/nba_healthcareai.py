import numpy as np
import pandas
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


def main():

    players = pandas.read_csv("..//nba_machine_learning/outputs/all_star_predictions_2017.csv")
    players.drop(['ID', 'Team', 'Season', 'Player'], axis=1, inplace=True)
    players = players.dropna(axis=0)
    plt.style.use('ggplot')
    # players.plot.scatter(x="Points", y="Rebounds")
    # sns.FacetGrid(players, hue="All Star").map(plt.scatter, "Points", "Rebounds")
    x = (players.corr()["All Star"])
    plt.show(players.corr())
    # plt.show(players.corr()["All Star"])
    X = players.values[:, 1:24]
    Y = players.values[:, 25]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)
    clf_gini = DecisionTreeClassifier(criterion="gini", random_state= 100, max_depth=3, min_samples_leaf=5)
    clf_gini.fit(X_train, y_train)
    DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=3, max_features=None, max_leaf_nodes=None,
                           min_samples_leaf=5, min_samples_split=2, min_weight_fraction_leaf=0.0, presort=False,
                           random_state=100, splitter='best')
    y_pred = clf_gini.predict(X_test)
    print(accuracy_score(y_test, y_pred)*100)


if __name__ == "__main__":
    main()