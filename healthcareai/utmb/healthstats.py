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
        sql="""select h.PatientEncounterID, ADTPatientClassificationCD, h.AdmitSourceCD, HospitalAdmitTypeCD,
        HospitalServiceCD, MeansOfArrivalCD, AcuityLevelCD, p.SexCD,
        DATEDIFF(YEAR,p.BirthDTS, h.InpatientAdmitDTS) AS PatientAge, f.MSDRG,
        DATEDIFF(HOUR, h.InpatientAdmitDTS, h.HospitalDischargeDTS) AS LOS,
        CASE WHEN DATEDIFF(HOUR, h.InpatientAdmitDTS, h.HospitalDischargeDTS) > 120 THEN 'Y'
        WHEN DATEDIFF(HOUR, h.InpatientAdmitDTS, h.HospitalDischargeDTS) IS NULL THEN NULL
        ELSE 'N' END AS ExtendedLOSFLG,
        CASE WHEN h.HospitalDischargeDTS IS NOT NULL THEN 'N' ELSE 'Y' END AS InTestWindowFLG
        from epic.Encounter.PatientEncounterHospitalBASE h
        join epic.Patient.Patient p on h.PatientID = p.PatientID
        join shared.clinical.facilityaccount f on h.hospitalaccountID = f.facilityaccountID
        where h.InpatientAdmitDTS > '2015-01-01' and h.InpatientAdmitDTS < GETDATE()
        --and h.HospitalDischargeDTS IS NOT NULL
        and ADTPatientClassificationCD NOT IN (4, 6, 7, 9)""",
            con=cnxn)

    # Set None string to be None type
    df.replace(['None'], [None], inplace=True)
    df.replace(['NULL'], [None], inplace=True)

    # Drop columns that won't help machine learning
    df.drop(['LOS'], axis=1, inplace=True)
    # Convert columns to appropriate data types
    df['PatientEncounterID'] = df['PatientEncounterID'].astype('int')
    df['ADTPatientClassificationCD'] = df['ADTPatientClassificationCD'].astype('object')
    df['AdmitSourceCD'] = df['AdmitSourceCD'].astype('object')
    df['HospitalAdmitTypeCD'] = df['HospitalAdmitTypeCD'].astype('object')
    df['HospitalServiceCD'] = df['HospitalServiceCD'].astype('object')
    df['MeansOfArrivalCD'] = df['MeansOfArrivalCD'].astype('object')
    df['AcuityLevelCD'] = df['AcuityLevelCD'].astype('object')
    df['SexCD'] = df['SexCD'].astype('object')
    df['MSDRG'] = df['MSDRG'].astype('object')
    df['ExtendedLOSFLG'] = df['ExtendedLOSFLG'].astype('object')
    print(df.dtypes)

    # Step 1: compare two models
    # o = DevelopSupervisedModel(modeltype='classification',
    #                            df=df,
    #                            predictedcol='ExtendedLOSFLG',
    #                            graincol='PatientEncounterID',  #OPTIONAL
    #                            impute=True,
    #                            debug=True)

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
                              graincol='PatientEncounterID',
                              windowcol='InTestWindowFLG',
                              predictedcol='ExtendedLOSFLG',
                              impute=True,
                              debug=False)

    p.deploy(method='linear',
             cores=4,
             server='UT-EDWDEV',
             dest_db_schema_table='[SAM].[dbo].[HCPyDeployClassificationFinalBASE]',
             use_saved_model=True,
             debug=False)

    print('\nTime:\n', time.time() - t0)

if __name__ == "__main__":
    main()
