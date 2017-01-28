from healthcareai import DevelopSupervisedModel
import pandas as pd
import time


def main():

    t0 = time.time()

    # CSV snippet for reading data into dataframe
    df = pd.read_csv('..//healthcareai/tests/fixtures/HCPyDiabetesClinical.csv',
                     na_values=['None'])


    # Set None string to be None type
    df.replace(['None'], [None], inplace=True)

    # Look at data that's been pulled in
    # print(df.head())
    # print(df.dtypes)

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
