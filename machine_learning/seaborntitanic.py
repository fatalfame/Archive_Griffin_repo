import pandas
import seaborn as sns

patients = pandas.read_csv("..//machine_learning/titanic.csv")
patients = patients.dropna(axis=0)
good_columns = patients._get_numeric_data()
corr = patients.corr()
g = sns.heatmap(corr,
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values, annot=True, cmap="winter", linewidths=0.5)
for item in g.get_xticklabels():
    item.set_rotation(45)
for item in g.get_yticklabels():
    item.set_rotation(0)
sns.plt.show()