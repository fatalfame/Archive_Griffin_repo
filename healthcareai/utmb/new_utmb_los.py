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
    cnxn = pyodbc.connect("""Driver={SQL Server Native Client 11.0};Server=UT-EDWDEV;
    Database=Epic;Trusted_Connection=yes;""")
    df = pd.read_sql(
        sql="""with ad as (SELECT DISTINCT
        adt.PatientEncounterID
        ,first_value
        (dep.DepartmentID) OVER(PARTITION BY adt.PatientEncounterID ORDER BY adt.effectiveDTS ASC) AS AdmitDepartmentID
        FROM epic.Encounter.ADTBASE adt
        JOIN epic.Reference.Department AS dep
        ON adt.DepartmentID = dep.DepartmentID
        JOIN epic.Encounter.PatientEncounterHospital ph on adt.patientencounterid = ph.patientencounterid
        WHERE adt.ADTEventTypeCD IN(1,3,5)
        AND adt.ADTEventSubtypeCD IN(1,3)
        AND ph.ADTPatientClassificationCD =1
        AND ph.InpatientAdmitDTS > '2015-01-01'
        AND ph.InpatientAdmitDTS < GETDATE()
        AND ph.PatientEncounterID NOT IN(26179574,49957093)
        --and ph.HospitalDischargeDTS IS null
        and ph.DeliveryTypeCD IS NULL
        and ph.HospitalAdmitTypeCD NOT IN (1, 4) -- Routine or Pregnancy
        )
        , x as (SELECT DISTINCT
        a.PatientEncounterID
        --,ph.HospitalAdmitDTS
        --,ph.InpatientAdmitDTS
        --,ph.HospitalDischargeDTS
        ,f.AdmitTypeCD
        ,ph.AdmitSourceCD
        ,f.FinancialClassCD
        ,f.AdmitAgeNBR
        ,f.InpatientLengthOfStayHoursNBR AS LOS
        ,CASE WHEN f.InpatientLengthOfStayHoursNBR > 120 THEN 1
        WHEN f.InpatientLengthOfStayHoursNBR IS NULL THEN NULL
        ELSE 0 END AS ExtendedLOS
        ,CASE WHEN f.InpatientLengthOfStayHoursNBR > 120 THEN 'Y'
        WHEN f.InpatientLengthOfStayHoursNBR IS NULL THEN NULL
        ELSE 'N' END AS ExtendedLOSFLG
        ,f.InpatientReadmissionCNT
        ,f.InpatientDaysToReadmitNBR
        ,f.InpatientReadmit30FLG
        ,f.InpatientReadmit90FLG
        ,f.CharlsonDeyoRiskScoreGroupingNBR
        ,f.ElixhauserScoreNBR
        ,ph.AcuityLevelCD
        ,ph.AccommodationCD
        ,ph.EDDispositionCD
        ,ph.HospitalServiceCD
        ,ph.MeansOfArrivalCD
        ,DATEPART(DW, ph.InpatientAdmitDTS) AS AdmitDay
        ,DATEPART(hh, ph.InpatientAdmitDTS) AS AdmitHour
        ,DATEPART(mm, ph.InpatientAdmitDTS) AS AdmitMonth
        ,a.BloodPressureSystolicNBR
        ,a.BloodPressureDiastolicNBR
        ,a.TemperatureFahrenheitNBR
        ,a.HeartRateNBR
        --,a.WeightNBR * 0.0625 AS PatWeightNBR
        ,a.BodyMassIndexNBR
        ,a.RespirationRateNBR
        ,CASE WHEN a.AdmittedForSurgeryFLG = 'Y' THEN 1 ELSE 0 END AS AdmittedForSurgeryFLG
        ,pat.EmploymentStatusCD
        ,pat.EthnicGroupCD
        ,pat.MaritalStatusCD
        ,pat.SexCD AS GenderCD
        ,sp.PrimarySpecialtyCD
        ,CASE
        WHEN fh.FinancialClassDSC = 'Correctional Care' THEN 1
        ELSE 0
        END AS TDCJFLG
        FROM epic.encounter.patientEncounterBASE AS a
        JOIN epic.Encounter.PatientEncounterHospitalBASE AS ph ON a.patientencounterID = ph.patientEncounterID
        LEFT JOIN epic.Patient.Patient AS pat
        ON a.PatientID = pat.PatientID
        join Shared.Clinical.FacilityAccount f on f.facilityAccountID = ph.HospitalAccountID
        join epic.Finance.HospitalAccount fh on a.hospitalAccountID = fh.hospitalAccountID
        left join Shared.Person.Provider sp on fh.AdmittingProviderID = sp.EDWProviderID
        WHERE 1 = 1
        AND ph.ADTPatientClassificationCD =1
        AND ph.InpatientAdmitDTS > '2015-01-01'
        AND ph.InpatientAdmitDTS < GETDATE()
        AND a.PatientEncounterID NOT IN(26179574,49957093)
        --and ph.HospitalDischargeDTS IS null
        and ph.DeliveryTypeCD IS NULL
        and ph.HospitalAdmitTypeCD NOT IN (1, 4) -- Routine or Pregnancy
        )
select x.*, ad.AdmitDepartmentID from x left join ad on x.PatientEncounterID = ad.PatientEncounterID""",
        con=cnxn)

    # Set None string to be None type
    df.replace(['None'], [None], inplace=True)
    df.replace(['NULL'], [None], inplace=True)
    df.replace([''], [None], inplace=True)
    df.replace([' '], [None], inplace=True)
    # df = df.dropna(axis=0)

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
    df.drop(['LOS', 'ExtendedLOS', 'InpatientReadmit30FLG', 'InpatientReadmit90FLG'], axis=1, inplace=True)
    # Convert columns to appropriate data types
    df['PatientEncounterID'] = df['PatientEncounterID'].astype('int')
    df['AdmitTypeCD'] = df['AdmitTypeCD'].astype('object')
    df['AdmitSourceCD'] = df['AdmitSourceCD'].astype('object')
    df['FinancialClassCD'] = df['FinancialClassCD'].astype('object')
    df['AdmitDay'] = df['AdmitDay'].astype('object')
    df['AdmitMonth'] = df['AdmitMonth'].astype('object')
    df['AdmitHour'] = df['AdmitHour'].astype('object')
    df['AdmitDepartmentID'] = df['AdmitDepartmentID'].astype('object')
    df['TDCJFLG'] = df['TDCJFLG'].astype('object')
    df['PrimarySpecialtyCD'] = df['PrimarySpecialtyCD'].astype('object')
    # df['InpatientReadmit30FLG'] = df['InpatientReadmit30FLG'].astype('object')
    # df['InpatientReadmit90FLG'] = df['InpatientReadmit90FLG'].astype('object')
    df['CharlsonDeyoRiskScoreGroupingNBR'] = df['CharlsonDeyoRiskScoreGroupingNBR'].astype('object')
    df['ElixhauserScoreNBR'] = df['ElixhauserScoreNBR'].astype('object')
    df['AcuityLevelCD'] = df['AcuityLevelCD'].astype('object')
    df['AccommodationCD'] = df['AccommodationCD'].astype('object')
    df['EDDispositionCD'] = df['EDDispositionCD'].astype('object')
    df['HospitalServiceCD'] = df['HospitalServiceCD'].astype('object')
    df['MeansOfArrivalCD'] = df['MeansOfArrivalCD'].astype('object')
    df['AdmittedForSurgeryFLG'] = df['AdmittedForSurgeryFLG'].astype('object')
    df['EmploymentStatusCD'] = df['EmploymentStatusCD'].astype('object')
    df['EthnicGroupCD'] = df['EthnicGroupCD'].astype('object')
    df['MaritalStatusCD'] = df['MaritalStatusCD'].astype('object')
    df['GenderCD'] = df['GenderCD'].astype('object')
    print(df.dtypes)

    # Step 1: compare two models
    o = DevelopSupervisedModel(modeltype='classification',
                               df=df,
                               predictedcol='ExtendedLOSFLG',
                               graincol='PatientEncounterID',  #OPTIONAL
                               impute=True,
                               debug=False)

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
    #          server='UT-EDWDEV',
    #          dest_db_schema_table='[SAM].[dbo].[HCPyDeployClassificationLOS_NewBASE]',
    #          use_saved_model=False,
    #          debug=False)

    print('\nTime:\n', time.time() - t0)

if __name__ == "__main__":
    main()
