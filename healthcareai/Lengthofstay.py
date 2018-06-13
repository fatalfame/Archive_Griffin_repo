import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import *
from sklearn.model_selection import *
from scipy.stats import uniform as sp_rand
from sklearn.tree import *
from sklearn.metrics import *
from sklearn import model_selection
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import *
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
import time

def main():

    csv = '..//healthcareai/tests/fixtures/LOS7.csv'
    df = pd.read_csv(csv)
    df = df.dropna(axis=0)
    # df['MaritalStatusCD'] = df['MaritalStatusCD'].astype('category')
    df['SexCD'] = df['SexCD'].astype('category')
    df['PatientClassCD'] = df['PatientClassCD'].astype('category')
    df['EthnicGroupCD'] = df['EthnicGroupCD'].astype('category')
    df['CurrentPCP'] = df['CurrentPCP'].astype('category')
    df['AdmitTypeCD'] = df['AdmitTypeCD'].astype('category')
    df['AdmittingSpecialtyCD'] = df['AdmittingSpecialtyCD'].astype('category')
    df['AttendingSpecialtyCD'] = df['AttendingSpecialtyCD'].astype('category')
    # df['AdmitDiagnosisCD'] = df['AdmitDiagnosisCD'].str.replace(r'[^0-9\\.]', '').astype('float')
    # df['AdmitDiagnosisCD'].replace(teamindex, inplace=True)
    # PatientClassCD is Inpatient/Outpatient/Emergency/etc..
    # HospitalAdmitTypeCD is Routine/Emergency/Urgent/etc...

    feat_names = ['Age', 'EthnicGroupCD', 'SexCD', 'HospitalAdmitTypeCD', 'AdmitTypeCD', 'CurrentPCP']
    df.drop(['PatientEncounterID', 'ZipCD', 'HospitalAdmitTypeCD', 'FinancialClassCD',
             'MeansofArrivalCD', 'LengthOfStayDaysNBR', 'InTestWindowFLG', 'EmploymentStatusCD',
             'MaritalStatusCD', 'PatientClassCD'], axis=1, inplace=True)

    # df = df.astype('category')
    print(df.dtypes)
    columns = df.columns.tolist()
    columns = [c for c in columns if c not in ["ExtendedLOSFLG"]]
    target = "ExtendedLOSFLG"
    train = df.sample(frac=0.5, random_state=random.seed())
    test = df.loc[~df.index.isin(train.index)]
    # model = RandomForestClassifier(n_estimators=50, min_samples_leaf=10)
    # model = KNeighborsClassifier(n_neighbors=3)
    # model = SVC()
    model = DecisionTreeClassifier()
    # model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
    # model = LinearRegression()
    model.fit(train[columns], train[target])
    predictions = model.predict(test[columns])
    # print mean_squared_error(test[target], predictions)
    # print mean_absolute_error(test[target], predictions)
    # print('roc_auc_score: ', roc_auc_score(test[target], predictions))
    print('Accuracy:', round(accuracy_score(test[target], predictions), 3), '%')
    print('-------------------')
    fi = model.feature_importances_
    fa = ([i for i in feat_names])
    features = zip(fi, fa)
    print('Feature Importance:')
    print('-------------------')
    for row in sorted(features, reverse=True):
        print(row)
    # class_report = classification_report(test[target], predictions)
    # print class_report
    # matrix = confusion_matrix(test[target], predictions)
    # print matrix
    """ HYPERPARAMETER TUNING """
    # params = {'n_estimators': [5, 20, 50, 100, 200], 'criterion': ['gini', 'entropy'], 'min_samples_leaf': [1, 2, 3],
    #           'min_samples_split': [2, 3, 4, 5], 'max_features': [1, 2, 3, 4, 5], 'max_depth': [1, 2, 3, 4, 5],
    #           'min_weight_fraction_leaf': [0, 0.5], 'max_leaf_nodes': [-2, 2, 4], 'min_impurity_split': [0, 1, 5]}
    # grid = RandomizedSearchCV(model, params)
    # start = time.time()
    # grid.fit(train[columns], train[target])
    # acc = grid.score(train[columns], train[target])
    # print("[INFO] grid search took {:.2f} seconds".format(	time.time() - start))
    # print("[INFO] grid search accuracy: {:.2f}%".format(acc * 100))
    # print("[INFO] grid search best parameters: {}".format(	grid.best_params_))

if __name__ == "__main__":
    main()
