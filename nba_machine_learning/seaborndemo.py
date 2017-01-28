import pandas
import seaborn as sns

players = pandas.read_csv("..//nba_machine_learning/2016-17_players.csv")
players = players.dropna(axis=0)
good_columns = players._get_numeric_data()
corr = players.corr()
sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values, annot=True, cmap="spectral_r")
sns.plt.show()
sns.heatmap(corr,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values, annot=True, cmap="YlGnBu", cbar_kws={"orientation": "horizontal"},
            linewidths=.5)
sns.plt.show()


