import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, f1_score, make_scorer, roc_curve, roc_auc_score
from sklearn.externals import joblib
import xgboost as xgb


dataset= pd.read_csv('../data/PeMS/Incidents/work_folder/windows.csv')

def grd_srch_boost(dataset, drop_features=[], cv=5):
    drop_cols = ['y', 'Timestamp', 'ID_Next', 'ID_Prev', 'Latitude_Next', 'Longitude_Next', 'Latitude_Prev', 'Longitude_Prev'] + drop_features #, 'Longitude', 'Latitude'
    tr_X, te_X, tr_y, te_y = train_test_split(dataset.drop(columns=drop_cols), dataset['y'], stratify=dataset.y, test_size=.2, random_state=442)
    scaler = StandardScaler()
    tr_X = scaler.fit_transform(tr_X)
    te_X = scaler.transform(te_X)
        
    print('XGBoost')
    param_grid = {'objective': ['binary:logistic'], 
              'learning_rate': [1.0, .1],
              'n_estimators': [500],
             'min_child_weight' : [.1, 1, 10],
             'max_depth': [3, 6, 10],
             'gamma': [0, .1],
             'subsample': [.5, 1],
              'colsample_bytree': [.5, 1],
              'reg_lambda': [1]
             }

    clf = xgb.XGBClassifier()
    grdCV = GridSearchCV(clf, param_grid, 'roc_auc', cv=cv, n_jobs=-1, refit=True)
    grdCV.fit(tr_X, tr_y)
    joblib.dump(grdCV, 'pickle_wo_loc.pkl')
    return 
    predict = clf.predict(te_X)
    print('example CM =', confusion_matrix(te_y, predict))
    proba = clf.predict_proba(te_X)
    fpr, tpr, thresholds = roc_curve(te_y, proba[:,1])
    print()
      
    plt.plot(fpr, tpr)
    plt.plot([0,1], [0,1])
    plt.grid()
    plt.show()
    
    print()
    
grd_srch_boost(dataset)