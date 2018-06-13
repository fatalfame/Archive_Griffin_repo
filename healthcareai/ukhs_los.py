from healthcareai import DevelopSupervisedModel
from healthcareai import DeploySupervisedModel
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.stats import pearsonr
from sklearn.feature_selection import RFE
from sklearn.model_selection import *
from sklearn.metrics import accuracy_score
from sklearn.ensemble import *

def main():

    t0 = time.time()

    # SQL snippet for reading data into dataframe
    import pyodbc
    cnxn = pyodbc.connect("""Driver={SQL Server Native Client 11.0};Server=KU-EDWDEV;
    Database=Epic;Trusted_Connection=yes;""")
    df = pd.read_sql(
        sql="""SELECT DISTINCT
        ph.HospitalAccountID
        ,ph.PatientEncounterID
        ,DATEDIFF(YEAR, pat.BirthDTS, ph.HospitalAdmitDTS) AS PatEncounterAge
        ,pat.SexCD AS GenderCD
        ,left(pat.zipCD, 5) as PatZipCD
        ,pat.EthnicGroupCD
        ,pat.MaritalStatusCD
        ,pat.EmploymentStatusCD
        ,CASE WHEN pat.CurrentPCPProviderID IS NOT NULL THEN 1 ELSE 0 END AS CurrentProviderFLG
        ,pat.PrimaryFinancialClassCD
        ,ph.AdmitSourceCD
        ,ph.HospitalAdmitTypeCD
        ,ph.HospitalServiceCD
        ,ph.MeansOfArrivalCD
        ,ph.AcuityLevelCD
        ,p.BloodPressureSystolicNBR
        ,p.BloodPressureDiastolicNBR
        ,p.TemperatureFahrenheitNBR
        ,p.HeartRateNBR
        ,p.BodyMassIndexNBR
        ,p.VisitFinancialClassID
        --,ph.HospitalAdmitDTS
        --,ph.InpatientAdmitDTS
        --,ph.HospitalDischargeDTS
        ,DATEPART(dw, ph.InpatientAdmitDTS) AS WeekdayNM
        ,DATEDIFF(HOUR, ph.HospitalAdmitDTS, ph.InpatientAdmitDTS) AS ArrivalToInpatientHRS
        ,DATEDIFF(HOUR, ph.InpatientAdmitDTS, ph.HospitalDischargeDTS) AS AdmitToDischargeHRS
        ,CASE WHEN DATEDIFF(DAY, ph.InpatientAdmitDTS, ph.HospitalDischargeDTS) < 1 THEN 1
        ELSE DATEDIFF(DAY, ph.InpatientAdmitDTS, ph.HospitalDischargeDTS) END AS AdmitToDischargeDays
        ,CASE WHEN DATEDIFF(HOUR, ph.InpatientAdmitDTS, ph.HospitalDischargeDTS) > 120 THEN 'Y'
        WHEN DATEDIFF(HOUR, ph.InpatientAdmitDTS, ph.HospitalDischargeDTS) IS NULL THEN NULL ELSE 'N' END AS ExtendedLOS
        ,CASE WHEN ph.ADTPatientStatusCD = 2 THEN 0 ELSE 1 END AS TrainingFLG
        FROM epic.Encounter.PatientEncounter p
        JOIN epic.Encounter.PatientEncounterHospitalBASE AS ph ON p.patientencounterID = ph.patientEncounterID
        JOIN epic.Patient.PatientBASE AS pat
        ON ph.PatientID = pat.PatientID
        JOIN epic.Finance.HospitalAccountBASE h on ph.HospitalAccountID = h.HospitalAccountID
        JOIN Epic.Reference.HospitalProfileBaseClassMapBASE cm
        on ph.ADTPatientClassificationCD = cm.AccountClassMappingCD
        WHERE 1 = 1
        AND ph.ADTPatientClassificationCD IN(101, 110, 103, 104, 127)
        AND ph.HospitalAdmitDTS between datetimefromparts( datepart( year, CURRENT_TIMESTAMP ) - 3, 7, 1, 0, 0, 0, 0 )
        and current_timestamp /* past three years */
        and cm.BaseClassMappingDSC = 'Inpatient'
        and ph.HospitalAdmitTypeCD NOT IN (1, 3) --Pregnancy or Routine elective admission""",
        con=cnxn)

    # Set None string to be None type
    # df.replace(['None'], [None], inplace=True)
    # df.replace(['NULL'], [None], inplace=True)
    # df.replace([''], [None], inplace=True)
    # df.replace([' '], [None], inplace=True)
    # df = df.fillna('')
    df = df.dropna(axis=0, how='any', inplace=False)
    # print(df.shape)

    # import random
    from sklearn.linear_model import LogisticRegression
    # columns = df.columns.tolist()
    # columns = [c for c in columns if c not in ["ExtendedLOS", "LOS", "PatientEncounterID"]]
    # target = "ExtendedLOS"
    # train = df.sample(frac=0.7, random_state=random.seed())
    # test = df.loc[~df.index.isin(train.index)]
    # model = SVC()
    # model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
    # model = RandomForestClassifier(min_samples_leaf=20, n_estimators=200)
    # rfe = RFE(model, 8)
    # rfe = rfe.fit(train[columns], train[target])
    # model.fit(train[columns], train[target])
    # fi = model.feature_importances_.round(2)
    # features = zip([c for c in columns], fi)
    # for row in sorted(features, reverse=True):
    #     print(row)
    # model.fit(train[columns], train[target])
    # predictions = model.predict(test[columns])
    # print('Accuracy:', round(accuracy_score(test[target], predictions), 3), '%')
    # for m in model.feature_importances_:
    #     print(round(m, 3))

    # plt.style.use('ggplot')
    # plt.scatter(x, y)
    # plt.show()

    # calculate the correlation matrix
    # corr = df.corr()
    # sns.heatmap(corr, annot=False)
    # plt.xticks(rotation=90)
    # plt.yticks(rotation=0)
    # plt.show()

    # Drop columns that won't help machine learning
    df.drop(['AdmitToDischargeHRS',
             'AdmitToDischargeDays',
             'HospitalAccountID'
             # 'TrainingFLG',
             # 'HospitalAdmitTypeCD',
             # 'HospitalServiceCD',
             # 'PatZipCD',
             # 'MaritalStatusCD',
             # 'EmploymentStatusCD',
             # 'CurrentProviderFLG',
             # 'PrimaryFinancialClassCD',
             # 'AdmitSourceCD',
             # 'MeansOfArrivalCD',
             # 'AcuityLevelCD',
             # 'BloodPressureSystolicNBR',
             # 'BloodPressureDiastolicNBR',
             # 'TemperatureFahrenheitNBR',
             # 'HeartRateNBR',
             # 'BodyMassIndexNBR',
             # 'VisitFinancialClassID',
             # 'WeekdayNM',
             # 'ArrivalToInpatientHRS'
             ], axis=1, inplace=True)
    # Convert columns to appropriate data types
    df['PatientEncounterID'] = df['PatientEncounterID'].astype('int')
    df['GenderCD'] = df['GenderCD'].astype('object')
    df['PatZipCD'] = df['PatZipCD'].astype('object')
    df['EthnicGroupCD'] = df['EthnicGroupCD'].astype('object')
    df['MaritalStatusCD'] = df['MaritalStatusCD'].astype('object')
    df['EmploymentStatusCD'] = df['EmploymentStatusCD'].astype('object')
    df['CurrentProviderFLG'] = df['CurrentProviderFLG'].astype('object')
    df['PrimaryFinancialClassCD'] = df['PrimaryFinancialClassCD'].astype('object')
    df['AdmitSourceCD'] = df['AdmitSourceCD'].astype('object')
    df['HospitalAdmitTypeCD'] = df['HospitalAdmitTypeCD'].astype('object')
    df['HospitalServiceCD'] = df['HospitalServiceCD'].astype('object')
    df['MeansOfArrivalCD'] = df['MeansOfArrivalCD'].astype('object')
    df['AcuityLevelCD'] = df['AcuityLevelCD'].astype('object')
    df['VisitFinancialClassID'] = df['VisitFinancialClassID'].astype('object')
    df['WeekdayNM'] = df['WeekdayNM'].astype('object')
    print(df.dtypes)

    # Step 1: compare two models
    o = DevelopSupervisedModel(modeltype='classification',
                               df=df,
                               predictedcol='ExtendedLOS',
                               graincol='PatientEncounterID',  #OPTIONAL
                               impute=True,
                               debug=True)

    # Run the linear model
    # o.linear(cores=4)

    # Run the random forest model
    o.random_forest(cores=4, trees=200,
                    tune=False)

    # Look at the RF feature importance rankings
    # o.plot_rffeature_importance(save=False)

    # Create ROC plot to compare the two models
    # o.plot_roc(debug=False,
    #            save=False)

    # p = DeploySupervisedModel(modeltype='classification',
    #                           df=df,
    #                           graincol='PatientEncounterID',
    #                           windowcol='InTestWindowFLG',
    #                           predictedcol='ExtendedLOSFLG',
    #                           impute=True,
    #                           debug=False)
    # #
    # p.deploy(method='rf',
    #          cores=4,
    #          server='KU-EDWDEV',
    #          dest_db_schema_table='[SAM].[dbo].[HCPyDeployClassificationLOS_NewBASE]',
    #          use_saved_model=False,
    #          debug=False)

    print('\nTime:\n', time.time() - t0)

if __name__ == "__main__":
    main()
