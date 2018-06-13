from healthcareai import DevelopSupervisedModel
from healthcareai import DeploySupervisedModel
import pandas as pd
import time


def main():

    t0 = time.time()

    # SQL snippet for reading data into dataframe
    import pyodbc
    cnxn = pyodbc.connect("""Driver={SQL Server Native Client 11.0};Server=UT-EDWDEV;
    Database=Epic;Trusted_Connection=yes;""")
    df = pd.read_sql(
        sql="""with x as (select sc.CaseID, sc.ScheduledDTS, sc.CaseTypeCD, sc.CaseClassCD, sc.PatientClassCD,
        sc.ServiceCD,
            sc.TotalTimeNeededMinutesNBR, sc.SchedulingStatusCD,
            sc.ProgressCD,
            SchedulingStatusDSC, sc.ProgressDSC,
            DATEDIFF(YEAR, p.BirthDTS, ep.ContactDTS) AS PatientAge, sc.PatientLevelCD,
            rsn.DelayReasonCD, rsn.DelayReasonDSC,
            sc.LocationID, p.ZipCD, p.SexCD, p.EthnicGroupCD,
            p.MaritalStatusCD, p.ReligionCD, p.PrimaryFinancialClassCD, p.EmploymentStatusCD, OperatingRoomID
            from epic.Surgery.SurgicalCaseBASE sc
            LEFT JOIN Epic.Surgery.LogDelay AS D
                      ON SC.CaseID = D.LogID
            LEFT JOIN Epic.Surgery.LogDelayReasonLog AS RSN
                      ON D.LogRecordID = RSN.RecordID
            LEFT JOIN epic.Patient.Patient p on sc.PatientID = p.PatientID
            LEFT JOIN epic.Encounter.PatientEncounter EP on sc.PatientEncounterID = ep.PatientEncounterID
            where SurgeryDTS < '2020-01-01'
            and SchedulingStatusCD NOT IN (2, 5, 3, 4))
            ,y as (select s.CaseID, t.TrackingEventDSC, t.TimeOutDTS from epic.Surgery.SurgicalCaseBASE s
            left join epic.Surgery.LogEventTimeTrackingBASE t on s.CaseID = t.LogID
            WHERE t.TrackingEventCD = 2)
            select x.CaseID, x.CaseTypeCD, x.CaseClassCD, x.PatientClassCD, x.ServiceCD, x.TotalTimeNeededMinutesNBR,
            x.SchedulingStatusCD, x.SchedulingStatusCD, x.SchedulingStatusDSC, y.TimeOutDTS, x.ProgressCD,
            x.ProgressDSC,
            CASE WHEN TimeOutDTS IS NULL AND x.ScheduledDTS > GETDATE() THEN 'N' ELSE 'Y' END AS InTestWindowFLG,
            x.PatientAge, x.PatientLevelCD, x.DelayReasonDSC,
            CASE WHEN TimeOutDTS IS NOT NULL AND DelayReasonCD <> 44 AND DelayReasonCD IS NOT NULL THEN 'Y'
            WHEN x.SchedulingStatusCD = 8 AND TimeOutDTS IS NOT NULL AND DelayReasonCD IS NULL THEN 'N'
            WHEN x.SchedulingStatusCD = 8 AND TimeOutDTS IS NOT NULL AND DelayReasonCD = 44 THEN 'N'
            WHEN x.SchedulingStatusCD = 8 AND TimeOutDTS IS NULL AND DelayReasonCD IS NULL THEN 'N' ELSE NULL
            END AS DelayFLG,
            x.LocationID, x.ZipCD, x.SexCD, x.EthnicGroupCD, x.MaritalStatusCD, x.ReligionCD,
            x.PrimaryFinancialClassCD, x.EmploymentStatusCD, x.OperatingRoomID
            from x left join y on x.CaseID = y.CaseID
            where 1 = 1
            and TimeOutDTS is not null and SchedulingStatusCD = 8""",
        con=cnxn)

    # Set None string to be None type
    df.replace(['None'], [None], inplace=True)
    df.replace(['NULL'], [None], inplace=True)
    # df.dropna(axis=1, inplace=True)
    # print(df.dtypes)

    # Drop columns that won't help machine learning
    df.drop(['SchedulingStatusCD', 'SchedulingStatusDSC', 'TimeOutDTS', 'ProgressCD', 'ProgressDSC',
             'InTestWindowFLG', 'DelayReasonDSC', 'ReligionCD', 'EthnicGroupCD', 'ZipCD',
             'LocationID', 'PrimaryFinancialClassCD', 'EmploymentStatusCD', 'OperatingRoomID'], axis=1, inplace=True)
    # Convert columns to appropriate data types
    df['CaseTypeCD'] = df['CaseTypeCD'].astype('object')
    df['CaseClassCD'] = df['CaseClassCD'].astype('object')
    df['PatientClassCD'] = df['PatientClassCD'].astype('object')
    df['ServiceCD'] = df['ServiceCD'].astype('object')
    df['PatientLevelCD'] = df['PatientLevelCD'].astype('object')
    # df['LocationID'] = df['LocationID'].astype('object')
    # df['ZipCD'] = df['ZipCD'].astype('object')
    # df['EthnicGroupCD'] = df['EthnicGroupCD'].astype('object')
    df['MaritalStatusCD'] = df['MaritalStatusCD'].astype('object')
    # df['ReligionCD'] = df['ReligionCD'].astype('object')
    # df['PrimaryFinancialClassCD'] = df['PrimaryFinancialClassCD'].astype('object')
    # df['EmploymentStatusCD'] = df['EmploymentStatusCD'].astype('object')
    # df['OperatingRoomID'] = df['OperatingRoomID'].astype('object')
    df['SexCD'] = df['SexCD'].astype('object')
    print(df.dtypes)

    # Step 1: compare two models
    o = DevelopSupervisedModel(modeltype='classification',
                               df=df,
                               predictedcol='DelayFLG',
                               graincol='CaseID',  #OPTIONAL
                               impute=True,
                               debug=False)

    # Run the linear model
    # o.linear(cores=2)

    # Run the random forest model
    o.random_forest(cores=2,
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
    #
    # p.deploy(method='linear',
    #          cores=2,
    #          server='UT-EDWDEV',
    #          dest_db_schema_table='[SAM].[dbo].[HCPyDeployClassificationBASE]',
    #          use_saved_model=True,
    #          debug=False)

    print('\nTime:\n', time.time() - t0)

if __name__ == "__main__":
    main()
