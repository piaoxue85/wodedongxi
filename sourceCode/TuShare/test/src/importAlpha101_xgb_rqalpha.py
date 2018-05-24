'''
Created on 2017年9月30日

@author: moonlit
'''
import pandas as pd
import getStockData as gsd
import pickle

def get_data(train_begin="",train_end="", test_begin="", test_end=""):
    train_data = gsd.get_101_data_train1(start=train_begin, end = train_end)
    test_data  = gsd.get_101_data_test1 (start=test_begin , end = test_end )
#     test_data  = gsd.get_101_data_test(start="2017-08-24" , end = "2017-08-25" )
    return train_data , test_data

# 基础参数配置
class conf:
    file = "d:/xgb.h"

def get_buy_list(today="" , buy_count = 20):
    print("now:" + today )
    train_begin , train_end , test_begin,test_end  = gsd.get_101_data_4_times(today=today )
    train_data , test_data                         = get_data(train_begin , train_end , test_begin,test_end ) 
    
    train_x        = train_data["data_101"]
    train_y        = train_data["CodeRetStd"] 
    train_return   = train_data["CodeReturn"]        

#     train_y = train_return

    test_x        = test_data["data_101"]
#     test_y        = test_data["CodeRetStd"] 
    test_return   = test_data["CodeReturn"]
#     test_shi_jian = test_data["shi_jian"]
    test_code     = test_data["code"    ]
        
    import xgboost as xgb 
    
    #模型参数设置XGBRegressor
    xlf = xgb.XGBRegressor(learning_rate=0.5, 
                            n_estimators=50,
                            max_depth=100,  
                            min_child_weight=3, 
                            silent=True, 
                            objective='reg:linear', 
                            nthread=-1, 
                            gamma=0.3,                        
                            max_delta_step=0, 
                            subsample= 0.7, 
                            colsample_bytree= 0.8, 
                            colsample_bylevel=1, 
                            reg_alpha=0.0001, 
                            reg_lambda= 0.2,   
                            scale_pos_weight=0, 
                            seed=1024, 
                            missing=None)
      
    xlf.fit(train_x, train_y, eval_metric='auc', verbose = True, eval_set = [(train_x, train_y)],early_stopping_rounds=50)                  
    
    #预测
    predictions = xlf.predict(test_x)
    predictions = predictions.reshape(-1)
    
    data                = pd.DataFrame()
    data["pre"]         = predictions
    data["code"]        = test_code
    data["test_return"] = test_return
    data                = data.sort_values(by = "pre", ascending =False)
#     print(data)
    buy_list  = data["code"].values
    buy_list  = buy_list[:buy_count]
    
    buy_list_ = pd.DataFrame()
    
    returns = data["test_return"].values
    returns = returns[:buy_count]
    
    buy_list_["code"] = buy_list
    
#     f = open('d:/test.txt','a')
#     for code,ret in zip(buy_list,returns):
#         f.writelines(today +"," + code +"," + str( ret) +"\n")
    
    return buy_list_ ,buy_list,returns

# ret = get_buy_list("2017-09-22")





    