'''
Created on 2017年9月30日

@author: moonlit
'''
import xgboost as xgb 
import getStockData as gsd
import pickle

def get_data(train_begin="",train_end="", test_begin="", test_end=""):
    train_data = gsd.get_101_data_train1(start=train_begin, end = train_end)
    test_data  = gsd.get_101_data_test1(start=test_begin , end = test_end )
#     test_data  = gsd.get_101_data_test(start="2017-08-24" , end = "2017-08-25" )
    return train_data , test_data

# 基础参数配置
class conf:
    today = '2017-07-25'
#     today = '2017-04-13'
#     today = '2017-09-19'
#     today = '2017-01-10'
    file = "d:/xgb.h"


train_begin , train_end , test_begin,test_end  = gsd.get_101_data_4_times(today=conf.today )
train_data , test_data                         = get_data(train_begin , train_end , test_begin,test_end )  

# test_data = train_data

train_x        = train_data["data_101"]
train_y        = train_data["CodeRetStd"] 
train_return   = train_data["CodeReturn"]
train_shi_jian = train_data["shi_jian"]
train_code     = train_data["code"    ]

# train_y = train_return

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

# Specify sufficient boosting iterations to reach a minimum
# num_round = 61
num_round = 3348

# Leave most parameters as default
# param = {
#             "learning_rate"         : 0.2,                   
#             "n_estimators"          : 13430,                 
#             "max_depth"             : 7,                     
#             "min_child_weight"      : 5,                     
#             "silent"                : True,                  
#             "objective"             : 'reg:linear',          
#             "nthread"               : -1,                    
#             "gamma"                 : 0.1,                   
#             "max_delta_step"        : 0,                     
#             "subsample"             : 0.9,                   
#             "colsample_bytree"      : 0.9,                   
#             "colsample_bylevel"     : 1,                     
#             "reg_alpha"             : 1e-05,                 
#             "reg_lambda"            : 0.01,                  
#             "scale_pos_weight"      : 0,                     
#             "seed"                  : 30,                    
#             "missing"               : None,     
#             "gpu_id"                : 0  ,
#             "tree_method"           : "gpu_hist" ,
#             "eval_metric"           : "mae" ,
#             "early_stopping_rounds" : 50   ,
#             "verbose"               : True ,                       
#         }

param = {
            "learning_rate"         : 0.0001,                   
            "n_estimators"          : 13430,                 
            "max_depth"             : 15,                     
            "min_child_weight"      : 5,                     
            "silent"                : True,                  
            "objective"             : 'reg:linear',          
            "nthread"               : -1,                    
            "gamma"                 : 0.1,                   
            "max_delta_step"        : 0,                     
            "subsample"             : 0.8,                   
            "colsample_bytree"      : 0.9,                   
            "colsample_bylevel"     : 1,                     
            "reg_alpha"             : 1e-05,                 
            "reg_lambda"            : 0.01,                  
            "scale_pos_weight"      : 0,                     
            "seed"                  : 100,                    
            "missing"               : None,     
            "gpu_id"                : 0  ,
            "tree_method"           : "gpu_hist" ,
            "eval_metric"           : "mae" ,
            "early_stopping_rounds" : 50   ,
            "verbose"               : True ,                       
        }


# Convert input data from numpy to XGBoost format
dtrain = xgb.DMatrix(train_x, label=train_y)
dtest  = xgb.DMatrix(test_x , label=test_y )
gpu_res = {} 

# bst = xgb.train(params = param,dtrain = dtrain,num_boost_round =num_round , evals=[(dtrain, 'dtrain')], evals_result=gpu_res ,early_stopping_rounds = 50 )
bst = xgb.train(params = param,dtrain = dtrain,num_boost_round =num_round , evals=[(dtest, 'dtest')], evals_result=gpu_res ,early_stopping_rounds = 50 )
predictions = bst.predict(dtest)

print(train_begin , train_end , test_begin,test_end) 

f = open('d:/test.csv','w')
# for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , train_y , train_code ,train_shi_jian,train_return):
for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , test_y , test_code ,test_shi_jian,test_return):
    f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_ +","+test_shi_jian_ + "\n")
#     print(pre[0] , test_y_ , test_code_ ,test_shi_jian_)
    
f.close()    
print("finished")


    