import pandas
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


players = pandas.read_csv("..//nba_machine_learning/outputs/all_players_2017.csv")
players = players.dropna(axis=0)
# good_columns = players._get_numeric_data()
# star = players[players["All Star"] > 0]
# corr = star.corr()
corr = players.corr()
# corr = corr.sortlevel(level=0, ascending=True)
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values, annot=True, linewidths=.5, cmap='coolwarm', robust=True,
            fmt=".2f", mask=mask)
plt.show()
# sns.show()
# sns.heatmap(corr,
#             xticklabels=corr.columns.values,
#             yticklabels=corr.columns.values, annot=True, cmap="YlGnBu", cbar_kws={"orientation": "horizontal"},
#             linewidths=.5)
# plt.show()


