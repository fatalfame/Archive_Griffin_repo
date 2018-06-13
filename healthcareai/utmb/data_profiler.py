import pandas as pd
import pandas_profiling
import numpy as np
import pyodbc


def main():

    cnxn = pyodbc.connect("""Driver={SQL Server Native Client 11.0};Server=UT-EDWDEV;
    Database=Epic;Trusted_Connection=yes;""")
    #
    df = pd.read_sql(
        sql="""select h.PatientEncounterID, ADTPatientClassificationCD, f.MSDRG, f.APRDRG, h.AdmitSourceCD,
        HospitalAdmitTypeCD, HospitalServiceCD, h.MeansOfArrivalCD,
        AcuityLevelCD, AccommodationCD, p.SexCD, fh.AdmissionTypeCD,
        CASE WHEN s.SpecialtyCD IS NOT NULL THEN s.SpecialtyCD
        ELSE ss.SpecialtyCD END AS ProviderSpecialtyCD,
        fh.DRGExpectedReimbursementAMT, fh.FinalDRG,
        fh.DRGMajorDiagnosticCategoryCD, DATEPART(dw, fh.AdmitDTS) AS AdmitDayOfWeekNBR,
        DATEDIFF(YEAR,p.BirthDTS, fh.AdmitDTS) AS PatientAge, f.MSDRG,
        DATEDIFF(HOUR, fh.AdmitDTS, fh.DischargeDTS) AS LOS,
        CASE WHEN DATEDIFF(HOUR, fh.AdmitDTS, fh.DischargeDTS) > 120 THEN 'Y'
        WHEN DATEDIFF(HOUR, fh.AdmitDTS, fh.DischargeDTS) IS NULL THEN NULL
        ELSE 'N' END AS ExtendedLOSFLG,
        CASE WHEN fh.DischargeDTS IS NOT NULL THEN 'N' ELSE 'Y' END AS InTestWindowFLG,
        f.AdmitDiagnosisCD, /*f.PrimaryDiagnosisCD,*/ f.PrimaryBenefitPlanCD
        from epic.Encounter.PatientEncounterHospitalBASE h
        join epic.Patient.Patient p on h.PatientID = p.PatientID
        join shared.clinical.facilityaccount f on h.hospitalaccountID = f.facilityaccountID
        join epic.Finance.HospitalAccountBASE fh on h.hospitalAccountID = fh.HospitalAccountID
        left join epic.Reference.ProviderSpecialtyBASE s on fh.AdmittingProviderID = s.ProviderID
        left join epic.Reference.ProviderSpecialtyBASE ss on fh.AttendingProviderID = ss.ProviderID
        left join epic.Finance.HospitalAccountSingleBillingOfficeBalanceBASE SBO
        ON fh.HospitalAccountID = SBO.HospitalAccountID
        where fh.AdmitDTS > '2015-01-01' and fh.AdmitDTS < GETDATE()
        AND fh.hospitalaccountBaseClassCD = 1
        AND fh.BillStatusCD NOT IN (40, 99)
        AND SBO.SingleBillingOfficeHospitalAccountRecordTypeCD = 0
        AND COALESCE (fh.TotalChargeAMT, 0) <> 0""",
        con=cnxn)

    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(outputfile="C:\\Users\griffin.hoopes\Desktop/testfile.html")

if __name__ == "__main__":
    main()