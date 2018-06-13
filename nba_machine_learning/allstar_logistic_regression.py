import pandas
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

players = pandas.read_csv('..//NBA_machine_learning/outputs/all_star_roster2.csv')
players = players[players["Seas"] >= 1980]
players = players.dropna(axis=0)
x = pandas.DataFrame()
x['Points'] = players["Points"]
x['Rebounds'] = players["Rebounds"]
x['Assists'] = players["Assists"]
x['fta'] = players["FTA"]
x['All Star'] = players["All Star"]
x = x.dropna(axis=0)
y = x['All Star']
x = x.drop(['All Star'], axis=1)
scaler = StandardScaler()
x = scaler.fit_transform(x)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=20)
model = LogisticRegression(penalty='l2', C=1)
model.fit(x_train, y_train)
print('accuracy', accuracy_score(y_test, model.predict(x_test)))
logit_roc_auc = roc_auc_score(y_test, model.predict(x_test))
print('log auc', logit_roc_auc)
print(classification_report(y_test, model.predict(x_test)))
fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(x_test)[:, 1])
plt.plot(fpr, tpr, label='ROC Curve (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiveer operating characteristic example')
plt.legend(loc='lower right')
plt.show()