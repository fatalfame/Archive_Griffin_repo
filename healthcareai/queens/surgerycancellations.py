from healthcareai import DevelopSupervisedModel
from healthcareai import DeploySupervisedModel
import pandas as pd
import time


def main():

    t0 = time.time()

    # SQL snippet for reading data into dataframe
    import pyodbc
    cnxn = pyodbc.connect("""Driver={SQL Server Native Client 11.0};Server=QU-EDWDEV;
    Database=Epic;Trusted_Connection=yes;""")
    df = pd.read_sql(
    sql="""with x as (SELECT
    sc.PatientID, ScheduledDTS, 1 AS CancelCNT
    FROM Epic.Surgery.SurgicalCase AS SC
    WHERE 1 = 1
    AND sc.CaseTypeCD = 1
    and sc.SchedulingStatusCD = 2
    and sc.surgerydts > '2013-01-01')
    ,y as (SELECT DISTINCT
    SC.CaseID
    ,sc.PatientID
    ,CASE
    WHEN SC.CancelReasonDSC IS NOT NULL
    AND SchedulingStatusCD = 2 THEN SC.CancelReasonDSC
    ELSE NULL
    END AS CancelReasonDSC
    ,CASE
    WHEN SchedulingStatusDSC = 'Canceled' THEN SC.CancelDTS
    ELSE NULL
    END AS CancelDTS
    ,sc.SchedulingStatusDSC
    ,CASE
    WHEN SC.CancelDTS IS NOT NULL
    AND SchedulingStatusCD = 2
    AND CONCAT(DATEPART(MM,SC.CancelDTS),DATEPART(DD,SC.CancelDTS)) =
    CONCAT(DATEPART(MM,SC.SurgeryDTS),DATEPART(DD,SC.SurgeryDTS)) THEN 1
    ELSE 0
    END AS SameDayCancelFLG,
    DATEDIFF(YEAR, p.BirthDTS, sc.ScheduledDTS) AS PatientAge,
    CASE WHEN DATEDIFF(YEAR, p.BirthDTS, sc.ScheduledDTS) > 60 THEN 5
    WHEN DATEDIFF(YEAR, p.BirthDTS, sc.ScheduledDTS) BETWEEN 40 AND 60 THEN 4
    WHEN DATEDIFF(YEAR, p.BirthDTS, sc.ScheduledDTS) BETWEEN 18 AND 40 THEN 3
    WHEN DATEDIFF(YEAR, p.BirthDTS, sc.ScheduledDTS) BETWEEN 5 AND 18 then 2
    WHEN DATEDIFF(YEAR, p.BirthDTS, sc.ScheduledDTS) < 5 THEN 1 END AS PatientAgeGroup,
    sc.PatientAgeNBR,
    p.SexCD,
    sc.CaseTypeCD,
    sc.CaseClassCD,
    sc.PatientClassCD,
    sc.ServiceCD,
    sc.TotalTimeNeededMinutesNBR,
    sc.LocationID,
    sc.AddOnCaseFLG,
    sc.PatientLevelCD,
    p.PrimaryFinancialClassCD,
    sc.surgeryDTS,
    sc.schedulingstatuscd,
    p.EmploymentStatusCD,
    p.StateCD,
    sp.ProcedureID,
    sp.BodyRegionCD,
    sc.ScheduledDTS,
	sc.CaseTypeDSC,
    CASE WHEN SchedulingStatusCD = 2 and CancelDTS IS NOT NULL THEN 1
    WHEN sc.SchedulingStatusCD IN (1, 3, 8) AND SurgeryDTS < GETDATE() THEN 0 ELSE NULL END AS CancelFLG
    FROM Epic.Surgery.SurgicalCase AS SC
    LEFT JOIN epic.Surgery.Room AS r
    ON sc.OperatingRoomID = r.ProviderID
    left join epic.Patient.Patient p on sc.PatientID = p.PatientID
    left join epic.Surgery.LogAllProcedureBASE sp on sc.CaseID = sp.LogID and ProcedureOrdinalSEQ=1
    WHERE 1 = 1
    and sc.SurgeryDTS > '2013-01-01'
    AND sc.CaseTypeCD = 1
    and sc.SchedulingStatusDSC NOT IN ('Voided'))
    select distinct y.CaseID, CASE WHEN y.SurgeryDTS < GETDATE() AND SchedulingStatusCD IN (8) THEN 'N'
    WHEN y.SurgeryDTS > GETDATE() AND SchedulingStatusCD IN (1, 3) THEN 'Y' ELSE 'N' END AS InTestWindowFLG,
    CASE WHEN y.PatientID IN (SELECT patientID from X)
    THEN (SELECT SUM(CancelCNT) FROM x where x.PatientID = y.PatientID and x.scheduledDTS <= y.scheduledDTS) ELSE 0
    END AS PriorCancellationAMT
    ,CASE WHEN y.CancelFLG = 1 THEN 'Y' WHEN CancelFLG = 0 THEN 'N' ELSE NULL END AS CancelFLG,
    DATEPART(dw, y.SurgeryDTS) AS DayOfSurgeryNBR, y.EmploymentStatusCD,
    y.SameDayCancelFLG, y.PatientAge, y.PatientAgeGroup, y.SexCD,
    y.PatientClassCD, y.ServiceCD, y.TotalTimeNeededMinutesNBR,
    y.LocationID, CASE WHEN y.AddOnCaseFLG = 'Y' THEN 1 ELSE 0 END AS AddOnCaseFLG,
    y.PrimaryFinancialClassCD,
    DATEPART(mm, y.SurgeryDTS) AS MonthOfSurgeryNBR,
    y.BodyRegionCD
    from y left join x on y.patientID = x.PatientID
    WHERE SurgeryDTS < GETDATE() + 1095""",
    con=cnxn)

    # Set None string to be None type
    df.replace(['None'], [None], inplace=True)
    df.replace(['NULL'], [None], inplace=True)
    # df.dropna(axis=1, inplace=True)
    # print(df.dtypes)

    # Drop columns that won't help machine learning
    df.drop(['SameDayCancelFLG', 'PatientAgeGroup', 'TotalTimeNeededMinutesNBR',
             'EmploymentStatusCD'], axis=1, inplace=True)
    # Convert columns to appropriate data types
    df['LocationID'] = df['LocationID'].astype('object')
    df['PatientClassCD'] = df['PatientClassCD'].astype('object')
    df['ServiceCD'] = df['ServiceCD'].astype('object')
    df['AddOnCaseFLG'] = df['AddOnCaseFLG'].astype('object')
    df['DayOfSurgeryNBR'] = df['DayOfSurgeryNBR'].astype('object')
    df['SexCD'] = df['SexCD'].astype('object')
    df['PrimaryFinancialClassCD'] = df['PrimaryFinancialClassCD'].astype('object')
    # df['EmploymentStatusCD'] = df['EmploymentStatusCD'].astype('object')
    df['MonthOfSurgeryNBR'] = df['MonthOfSurgeryNBR'].astype('object')
    df['BodyRegionCD'] = df['BodyRegionCD'].astype('object')
    df['CancelFLG'] = df['CancelFLG'].astype('object')
    print(df.dtypes)

    # Step 1: compare two models
    # o = DevelopSupervisedModel(modeltype='classification',
    #                            df=df,
    #                            predictedcol='CancelFLG',
    #                            graincol='CaseID',  #OPTIONAL
    #                            impute=True,
    #                            debug=False)

    # Run the linear model
    # o.linear(cores=4)

    # Run the random forest model
    # o.random_forest(cores=4, trees=100,
    #                 tune=False)

    # Look at the RF feature importance rankings
    # o.plot_rffeature_importance(save=False)

    # Create ROC plot to compare the two models
    # o.plot_roc(debug=False,
    #            save=False)

    p = DeploySupervisedModel(modeltype='classification',
                              df=df,
                              graincol='CaseID',
                              windowcol='InTestWindowFLG',
                              predictedcol='CancelFLG',
                              impute=True,
                              debug=False)

    p.deploy(method='linear',
             cores=4,
             server='QU-EDWDEV',
             dest_db_schema_table='[SAM].[dbo].[HCPyDeployClassificationSurgeryCancelBASE]',
             use_saved_model=True,
             debug=False)

    print('\nTime:\n', time.time() - t0)

if __name__ == "__main__":
    main()
