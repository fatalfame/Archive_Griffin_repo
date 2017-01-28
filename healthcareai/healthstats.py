from healthcareai import DevelopSupervisedModel
import pandas as pd
import time


def main():

    t0 = time.time()

    # CSV snippet for reading data into dataframe
    df = pd.read_csv('..//healthcareai/tests/fixtures/HCPyDiabetesClinical.csv',
                     na_values=['None'])

    # SQL snippet for reading data into dataframe
    # import pyodbc
    # cnxn = pyodbc.connect("""SERVER=localhost;
    #                         DRIVER={SQL Server Native Client 11.0};
    #                         Trusted_Connection=yes;
    #                         autocommit=True""")
    #
    # df = pd.read_sql(
    #     sql="""SELECT *
    #         FROM [SAM].[dbo].[HCPyDiabetesClinical]
    #         -- In this step, just grab rows that have a target
    #         WHERE ThirtyDayReadmitFLG is not null""",
    #     con=cnxn)

    # Set None string to be None type
    df.replace(['None'], [None], inplace=True)

    # Look at data that's been pulled in
    print(df.head())
    print(df.dtypes)

    # Drop columns that won't help machine learning
    df.drop(['PatientID', 'InTestWindowFLG'], axis=1, inplace=True)

    # Step 1: compare two models
    o = DevelopSupervisedModel(modeltype='classification',
                               df=df,
                               predictedcol='ThirtyDayReadmitFLG',
                               # graincol='PatientEncounterID',  #OPTIONAL
                               impute=True,
                               debug=False)

    # Run the linear model
    o.linear(cores=5)

    # Run the random forest model
    o.random_forest(cores=100,
                    tune=False)

    # Look at the RF feature importance rankings
    o.plot_rffeature_importance(save=False)

    # Create ROC plot to compare the two models
    o.plot_roc(debug=False,
               save=False)

    df = pd.read_csv('..//healthcareai/tests/fixtures/HCPyDiabetesClinical.csv',
                     na_values=['None'])

    df.drop(['PatientID'], axis=1, inplace=True)


    print('\nTime:\n', time.time() - t0)

if __name__ == "__main__":
    main()
