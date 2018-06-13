from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.externals import joblib
import math
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
import sys
import matplotlib.pyplot as plt

def main():

    # t0 = time.time()

    # SQL snippet for reading data into dataframe
    import pyodbc
    cnxn = pyodbc.connect("""Driver={SQL Server Native Client 11.0};Server=UT-EDWDEV;
    Database=Epic;Trusted_Connection=yes;""")
    #
    df = pd.read_sql(
            sql="""select PatientEncounterID, PredictedProbNBR, LOS, Predicted, Actual, LastLoadDTS
            from (select h.patientEncounterID, h.PredictedProbNBR, h.LastLoadDTS,
            DATEDIFF(HOUR, p.HospitalAdmitDTS, p.HospitalDischargeDTS) AS LOS,
            CASE WHEN DATEDIFF(HOUR, p.HospitalAdmitDTS, p.HospitalDischargeDTS) >= 120 THEN 1 ELSE 0 END AS Actual,
            CASE WHEN PredictedProbNBR >= 0.3 THEN 1 ELSE 0 END AS Predicted,
            ROW_NUMBER() over(partition by h.patientencounterid order by h.LastLoadDTS desc) as rn
            from [SAM].[dbo].[HCPyDeployClassificationLOS_NewBASE] h
            join epic.Encounter.PatientEncounterBASE p on h.patientencounterID = p.PatientEncounterID
            join epic.Finance.HospitalAccountBASE f on p.HospitalAccountID = f.HospitalAccountID) as r
            where r.rn = 1
            and r.LOS IS NOT NULL
            order by PredictedProbNBR desc""",
            con=cnxn)

    # Set None string to be None type
    # df.replace(['None'], [None], inplace=True)
    df['PredictedProbNBR'] = df['PredictedProbNBR'].astype('float')
    df['Actual'] = df['Actual'].astype('int')

    # Look at data that's been pulled in
    # print(df.head())
    # print(df.dtypes)

    # Drop columns that won't help machine learning
    # df.drop(['LOS', 'EncounterTypeCD'], axis=1, inplace=True)
    # print(df['Predicted'])
    # print(df['Actual'])

    # print(roc_auc_score(df['Actual'], df['PredictedProbNBR']))

    auc = GenerateAUC(df['PredictedProbNBR'], df['Actual'], aucType='SS', plotFlg=True, allCutoffsFlg=False)


def GenerateAUC(predictions, labels, aucType='SS', plotFlg=False, allCutoffsFlg=False):
    """
    This function creates an ROC or PR curve and calculates the area under it.
    Parameters
    ----------
    predictions (list) : predictions coming from an ML algorithm of length n.
    labels (list) : true label values corresponding to the predictions. Also length n.
    aucType (str) : either 'SS' for ROC curve or 'PR' for precision recall curve. Defaults to 'SS'
    plotFlg (bol) : True will return plots. Defaults to False.
    allCutoffsFlg (bol) : True will return plots. Defaults to False.
    Returns
    -------
    AUC (float) : either AU_ROC or AU_PR
    """
    # Error check for uneven length predictions and labels
    if len(predictions) != len(labels):
        raise Exception('Data vectors are not equal length!')

    # make AUC type upper case.
    aucType = aucType.upper()

    # check to see if AUC is SS or PR. If not, default to SS
    if aucType != 'SS' and aucType != 'PR':
        print('Drawing ROC curve with Sensitivity/Specificity')
        aucType = 'SS'

    # Compute ROC curve and ROC area
    if aucType == 'SS':
        fpr, tpr, thresh = roc_curve(labels, predictions)
        area = auc(fpr, tpr)
        print('Area under ROC curve (AUC): %0.2f' % area)
        # get ideal cutoffs for suggestions
        d = (fpr - 0)**2 + (tpr - 1)**2
        ind = np.where(d == np.min(d))
        bestTpr = tpr[ind]
        bestFpr = fpr[ind]
        cutoff = thresh[ind]
        print("Ideal cutoff is %0.2f, yielding TPR of %0.2f and FPR of %0.2f" % (cutoff, bestTpr, bestFpr))
        if allCutoffsFlg is True:
            print('%-7s %-6s %-5s' % ('Thresh', 'TPR', 'FPR'))
            for i in range(len(thresh)):
                print('%-7.2f %-6.2f %-6.2f' % (thresh[i], tpr[i], fpr[i]))

        # plot ROC curve
        if plotFlg is True:
            plt.figure()
            plt.plot(fpr, tpr, color='darkorange',
                     lw=2, label='ROC curve (area = %0.2f)' % area)
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Receiver operating characteristic curve')
            plt.legend(loc="lower right")
            plt.show()
        return ({'AU_ROC': area,
                 'BestCutoff': cutoff[0],
                 'BestTpr': bestTpr[0],
                 'BestFpr': bestFpr[0]})
    # Compute PR curve and PR area
    else: # must be PR
        # Compute Precision-Recall and plot curve
        precision, recall, thresh = precision_recall_curve(labels, predictions)
        area = average_precision_score(labels, predictions)
        print('Area under PR curve (AU_PR): %0.2f' % area)
        # get ideal cutoffs for suggestions
        d = (precision - 1) ** 2 + (recall - 1) ** 2
        ind = np.where(d == np.min(d))
        bestPre = precision[ind]
        bestRec = recall[ind]
        cutoff = thresh[ind]
        print( "Ideal cutoff is %0.2f, yielding TPR of %0.2f and FPR of %0.2f"
               % (cutoff, bestPre, bestRec))
        if allCutoffsFlg is True:
            print('%-7s %-10s %-10s' % ('Thresh', 'Precision', 'Recall'))
            for i in range(len(thresh)):
                print('%5.2f %6.2f %10.2f' %(thresh[i],precision[i], recall[i]))

        # plot PR curve
        if plotFlg is True:
            # Plot Precision-Recall curve
            plt.figure()
            plt.plot(recall, precision, lw=2, color='darkred',
                     label='Precision-Recall curve' % area)
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.ylim([0.0, 1.05])
            plt.xlim([0.0, 1.0])
            plt.title('Precision-Recall AUC={0:0.2f}'.format(
                area))
            plt.legend(loc="lower right")
            plt.show()
        return({'AU_PR':area,
                'BestCutoff':cutoff[0],
                'BestPrecision':bestPre[0],
                'BestRecall':bestRec[0]})


if __name__ == "__main__":
    main()