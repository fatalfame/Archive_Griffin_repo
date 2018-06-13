import pandas as pd
import random
from sklearn.ensemble import *
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import *
from scipy.stats import uniform as sp_rand
from sklearn.tree import *
from sklearn.svm import SVC


def main():

    csv = '..//healthcareai/tests/fixtures/LOS3.csv'
    df = pd.read_csv(csv)
    df = df.dropna(axis=0)
    # df['AdmitDiagnosisCD'] = df['AdmitDiagnosisCD'].str.replace(r'[^0-9\\.]', '').astype('float')
    # df['AdmitDiagnosisCD'].replace(teamindex, inplace=True)
    # x = df[df['LongLOS'] == 1]
    # PatientClassCD is Inpatient/Outpatient/Emergency/etc..
    # HospitalAdmitTypeCD is Routine/Emergency/Urgent/etc...
    feat_names = ['ZipCD', 'Age', 'HospitalAdmitTypeCD', 'PatientClassCD',
                  'MaritalStatusCD', 'EmploymentStatusCD', 'MeansofArrivalCD', 'AcuityLevelCD']
    df.drop(['LOS', 'EthnicGroupCD', 'SexCD', 'AdmitDiagnosisCD'], axis=1, inplace=True)
    columns = df.columns.tolist()
    columns = [c for c in columns if c not in ["LongLOS"]]
    target = "LongLOS"
    train = df.sample(frac=0.5, random_state=random.seed())
    test = df.loc[~df.index.isin(train.index)]
    model = RandomForestClassifier(min_samples_leaf=10, n_estimators=100)
    # model = DecisionTreeClassifier()
    # model = SVC()
    # model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
    model.fit(train[columns], train[target])
    predictions = model.predict(test[columns])
    # print mean_squared_error(predictions, test[target])
    print('Accuracy:', round(accuracy_score(test[target], predictions), 3), '%')
    # x = round(accuracy_score(test[target], predictions), 3), '%'
    print('-------------------')
    fi = model.feature_importances_
    fa = ([i for i in feat_names])
    features = zip(fi, fa)
    print('Feature Importance:')
    print('-------------------')
    for row in sorted(features, reverse=True):
        print(row)


if __name__ == "__main__":
    main()
