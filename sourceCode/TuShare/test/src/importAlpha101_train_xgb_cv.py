'''
Created on 2017年9月30日

@author: moonlit
'''
import xgboost as xgb 
import getStockData as gsd
from xgboost.sklearn import XGBRegressor
from sklearn import cross_validation, metrics   #Additional     scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search
import matplotlib.pylab as plt
# %matplotlib inline
from matplotlib.pylab import rcParams
import pandas as pd

def get_data(train_begin="",train_end="", test_begin="", test_end=""):
    train_data = gsd.get_101_data_train1(start=train_begin, end = train_end)
    test_data  = gsd.get_101_data_test1(start=test_begin , end = test_end )
#     test_data  = gsd.get_101_data_test(start="2017-08-24" , end = "2017-08-25" )
    return train_data , test_data

# 基础参数配置
class conf:

    today = '2017-04-13'
#     today = '2017-09-11'
    file = "d:/xgb.h"

train_begin , train_end , test_begin,test_end  = gsd.get_101_data_4_times(today=conf.today )
train_data , test_data                         = get_data(train_begin , train_end , test_begin,test_end )  

train_x        = train_data["data_101"]
train_y        = train_data["CodeRetStd"] 
train_return   = train_data["CodeReturn"]
train_shi_jian = train_data["shi_jian"]
train_code     = train_data["code"    ]

train_y = train_return

# print(train_x)
# print(train_y)
# print(train_return)
# print(train_shi_jian)
# print(train_code)

test_x        = test_data["data_101"]
test_y        = test_data["CodeRetStd"] 
test_return   = test_data["CodeReturn"]
test_shi_jian = test_data["shi_jian"]
test_code     = test_data["code"    ]

xlf =      XGBRegressor(learning_rate=0.5, 
                        n_estimators=30000,
                        max_depth=4,  
                        min_child_weight=3, 
                        silent=True, 
                        objective='reg:linear', 
                        nthread=-1, 
                        gamma=0.0,                        
                        max_delta_step=0, 
                        subsample= 0.95, 
                        colsample_bytree= 0.8, 
                        colsample_bylevel=1, 
                        reg_alpha=0.0001, 
                        reg_lambda= 0.2,   
                        scale_pos_weight=0, 
                        seed=30, 
                        missing=None)

def modelfit(alg, train_x,train_y,test_x,test_y, useTrainCV = True, cv_folds = 5, early_stopping_rounds = 50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(train_x, label = train_y)
        cvresult = xgb.cv(xgb_param, 
                          xgtrain, 
                          num_boost_round = alg.get_params()['n_estimators'],
                          nfold = cv_folds, 
                          metrics = 'mae', 
                          early_stopping_rounds = early_stopping_rounds,
                          verbose_eval=True
                          )
#         print("cvresult",cvresult)
        n_estimators = cvresult.shape[0]
        alg.set_params(n_estimators = n_estimators)

#     alg.fit(train_x, train_y, eval_set = [(test_x, test_y)], eval_metric = 'mae',verbose = False)

#     dtrain_predictions = alg.predict(test_x)
    print("n_estimators:",n_estimators)
    return []

#step 1 :
#n_estimators: 1487
predictions = modelfit(xlf, train_x,train_y,test_x,test_y)

'''
#step 2 :
# {'max_depth': 7, 'min_child_weight': 5} -0.054415238503889476
param_test1 = {
#     'max_depth':list(range(2,10,2)),
#     'min_child_weight':list(range(1,6,2))
    'max_depth':[3,4,5],
    'min_child_weight':[2,3,4]
}
gsearch1 = GridSearchCV(estimator = xlf ,
                        param_grid = param_test1,     
                        scoring='neg_mean_absolute_error',
                        n_jobs=1,
                        iid=False, 
                        cv=5
                        )
gsearch1.fit(train_x,train_y)
print(
      gsearch1.grid_scores_, 
      gsearch1.best_params_,     
      gsearch1.best_score_
      )

'''
'''
#step 3 :
# {'gamma': 0.0} -0.035413255155249825
param_test3 = {
 'gamma':[i/10.0 for i in range(0,10)]
}
gsearch3 = GridSearchCV(estimator = xlf , 
                        param_grid = param_test3, 
                        scoring='neg_mean_absolute_error',
                        n_jobs=1,
                        iid=False, 
                        cv=5
                        )
gsearch3.fit(train_x,train_y)
print(gsearch3.grid_scores_, 
      gsearch3.best_params_, 
      gsearch3.best_score_)    
'''    

'''
#step 4 :
# {'subsample': 0.9, 'colsample_bytree': 0.6} -0.03540104614593826
param_test4 = {
#     'subsample':[i/10.0 for i in range(1,10)],
#     'colsample_bytree':[i/10.0 for i in range(1,10)]
    'subsample':[i/100.0 for i in range(80,100,5)],
    'colsample_bytree':[i/100.0 for i in range(80,100,5)]
}

gsearch4 = GridSearchCV(estimator = xlf, 
                        param_grid = param_test4, 
                        scoring='neg_mean_absolute_error',
                        n_jobs=1,
                        iid=False, cv=5
                        )

gsearch4.fit(train_x,train_y)
print(gsearch4.grid_scores_,
      gsearch4.best_params_, 
      gsearch4.best_score_)       
'''

'''
#step 5 :
# {'reg_alpha': 0.0001, 'reg_lambda': 0.001} -0.035370866058153046
param_test6 = {
#         'reg_alpha':  [1e-04,1e-05,1e-06 ],
#         "reg_lambda": [1e-01,1e-02,1e-03,1e-04,1e-05] ,
    'reg_alpha':  [0.01,0.001,0.0001] ,
    "reg_lambda": [0.01],
#         'seed':  [25,30,35] ,
}

gsearch6 = GridSearchCV(estimator = xlf, 
                        param_grid = param_test6, 
                        scoring='neg_mean_absolute_error',
                        n_jobs=1,
                        iid=False, 
                        cv=5)
gsearch6.fit(train_x,train_y)
print(gsearch6.grid_scores_,
      gsearch6.best_params_, 
      gsearch6.best_score_)
'''

'''
#step 5 :
#{'seed': 30, 'scale_pos_weight': 0} -0.037503434379181314
param_test6 = {
    'seed':  [25,30,35] ,
    "scale_pos_weight":[0], 
}
gsearch6 = GridSearchCV(estimator = xlf, 
param_grid = param_test6, scoring='neg_mean_absolute_error',n_jobs=1,iid=False, cv=5)
gsearch6.fit(train_x,train_y)
print(gsearch6.grid_scores_,
      gsearch6.best_params_, 
      gsearch6.best_score_)  
''' 
