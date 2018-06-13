from healthcareai import DevelopSupervisedModel
import pandas as pd
import time


def main():

    t0 = time.time()

    # CSV snippet for reading data into dataframe
    df = pd.read_csv('..//healthcareai/tests/fixtures/LOSQHSTEST.csv', na_values=['NULL'])

    # SQL snippet for reading data into dataframe
    # import pyodbc
    # cnxn = pyodbc.connect("""Driver={SQL Server Native Client 11.0};Server=HCS-DEV0004;
    # Database=Epic;Trusted_Connection=yes;""")
    #
    # df = pd.read_sql(
    #     sql="""with x as (select distinct e.PatientEncounterID, e.PatientID, p.ZipCD, e.ContactDTS,
    # DATEDIFF(yy, p.BirthDTS, GetDate()) AS Age, SexCD, EthnicGroupCD,e.HospitalAdmitTypeCD,
    #     e.HospitalAdmitTypeDSC, p.MaritalStatusCD, p.EmploymentStatusCD, h.MeansOfArrivalCD, h.MeansOfArrivalDSC,
    # f.AdmitDiagnosisCD, f.AdmitDiagnosisDSC,
    #     f.LengthOfStayDaysNBR, f.LengthOfStayHoursNBR, h.AcuityLevelCD, e.EncounterTypeCD, e.FinancialClassCD,
		# r.SpecialtyCD AS PCPSpecialty, h.AdmitSourceCD, h.HospitalServiceCD, rp.SpecialtyCD AS AttendingSpecialty, f.InpatientReadmit30FLG, f.InpatientReadmit90FLG
    #     FROM [Epic].[Encounter].[PatientEncounterBASE] e join epic.Patient.Patient p on e.patientid = p.patientid
    #     left join epic.encounter.patientencounterhospital h on e.patientencounterid = h.patientencounterid
    #     left join [Shared].[Clinical].[EncounterLinkBASE] l on e.PatientEncounterID = l.PatientEncounterID
    #     left join shared.Clinical.FacilityAccount f on l.FacilityAccountID = f.FacilityAccountID
		# left join [Epic].[Reference].[ProviderSpecialtyBASE] r on h.AdmissionProviderID = r.ProviderID
		# left join [Epic].[Reference].[ProviderSpecialtyBASE] rp on f.AttendingProviderID = rp.ProviderID)
    #     ,y as (select PatientEncounterID, min(EventDTS) AS MinEvent, Max(EventDTS) AS MaxEvent, PatientClassCD,
    # PatientClassDSC
    #     from epic.Encounter.ADT
    #     group by patientencounterid, PatientClassCD, PatientClassDSC)
    #     select CASE WHEN DATEPART(dw,x.ContactDTS) IN (1,7) THEN 1 ELSE 0 END AS Weekend,
		# x.ZipCD, x.Age, x.SexCD, x.EthnicGroupCD, x.HospitalAdmitTypeCD, y.PatientClassCD, x.MaritalStatusCD,
		# CASE WHEN x.EmploymentStatusCD IS NULL THEN 0 ELSE x.EmploymentStatusCD END AS EmploymentStatusCD,
    #     x.EncounterTypeCD, x.FinancialClassCD,
		# x.PCPSpecialty, x.AdmitSourceCD, x.HospitalServiceCD, x.AttendingSpecialty, x.InpatientReadmit30FLG, x.InpatientReadmit90FLG,
    #     CASE WHEN x.MeansOfArrivalCD IS NULL THEN 0 ELSE x.MeansOfArrivalCD END AS MeansofArrivalCD,
    #     x.AcuityLevelCD,
    #     CASE WHEN x.LengthOfStayHoursNBR< 0 THEN DATEDIFF(dd,y.MinEvent, y.MaxEvent) ELSE x.LengthOfStayHoursNBR END AS LOS,
    #     CASE WHEN x.LengthOfStayHoursNBR > 36 THEN 'Y' else 'N' END AS LongLOS
		# --CASE WHEN x.LengthOfStayHoursNBR > 36 THEN 1 else 0 END AS LongLOS
    #     from x join y on x.PatientEncounterID = y.PatientEncounterID""",
    #     con=cnxn)

    # Set None string to be None type
    df.replace(['None'], [None], inplace=True)
    df.replace(['NULL'], [None], inplace=True)


    # Look at data that's been pulled in
    # print(df.head())
    # print(df.dtypes)

    # Drop columns that won't help machine learning
    df.drop(['ZipCD', 'InTestWindowFLG', 'EthnicGroupCD', 'FinancialClassCD', 'PatientClassCD',
             'EmploymentStatusCD', 'AdmitSourceCD', 'HospitalAdmitTypeCD', 'MaritalStatusCD',
             'ADTPatientClassificationCD'], axis=1, inplace=True)
    # Convert categorical columns to 'object' type
    # df['MaritalStatusCD'] = df['MaritalStatusCD'].astype('object')
    df['SexCD'] = df['SexCD'].astype('object')
    # df['HospitalAdmitTypeCD'] = df['HospitalAdmitTypeCD'].astype('object')
    df['AdmissionSourceCD'] = df['AdmissionSourceCD'].astype('object')
    # df['EmploymentStatusCD'] = df['EmploymentStatusCD'].astype('object')
    # df['PatientClassCD'] = df['PatientClassCD'].astype('object')
    # df['HospitalAdmitTypeCD'] = df['HospitalAdmitTypeCD'].astype('object')
    df['CurrentPCP'] = df['CurrentPCP'].astype('object')
    df['AdmittingSpecialtyCD'] = df['AdmittingSpecialtyCD'].astype('object')
    df['AttendingSpecialtyCD'] = df['AttendingSpecialtyCD'].astype('object')
    df['MeansofArrivalCD'] = df['MeansofArrivalCD'].astype('object')
    # df['AdmitSourceCD'] = df['AdmitSourceCD'].astype('object')
    # df['FinancialClassCD'] = df['FinancialClassCD'].astype('object')
    # df['ADTPatientClassificationCD'] = df['ADTPatientClassificationCD'].astype('object')

    # Step 1: compare two models
    o = DevelopSupervisedModel(modeltype='classification',
                               df=df,
                               predictedcol='ExtendedLOS',
                               graincol='PatientEncounterID',  #OPTIONAL
                               impute=True,
                               debug=False)

    # Run the linear model
    # o.linear(cores=1)

    # Run the random forest model
    o.random_forest(cores=1, trees=20,
                    tune=False)

    # Look at the RF feature importance rankings
    # o.plot_rffeature_importance(save=False)

    # Create ROC plot to compare the two models
    # o.plot_roc(debug=False,
    #            save=False)

    # df = pd.read_csv('..//healthcareai/tests/fixtures/LOS2.csv', na_values=['None'])
    #
    print('\nTime:\n', time.time() - t0)


if __name__ == "__main__":
    main()
