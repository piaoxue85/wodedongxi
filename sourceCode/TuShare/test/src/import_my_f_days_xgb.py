import xgboost as xgb 
import numpy as np
import pandas as pd
import getStockData as gsd
import os
import pickle
# from sklearn.metrics import accuracy_score

# 基础参数配置
class conf:
#     today = '2017-06-02'
#     today = '2017-04-13'
#     today = '2017-09-22'
#     today = '2017-01-10'
    today = '2017-01-04'
#     today = '2017-08-11'
#     file = "d:/xgb.h"
    days = 24
    total_days = 144
    train_file = "d:/train.h"
    test_file  = "d:/test.h"
    file = "d:/xgb.h"
    
def get_data(time=[],days=5):
    x        = []
    y        = []
    code     = []
    shi_jian = []  
    ret      = []
    ret_std  = []
    ret_hot  = []       
    
    for i in range(0,len(time)) :
        if i+days > len(time) :
            break
        
        end   = time[i]
        begin = time[i+days-1]
        _,data = gsd.get_101_data_train1_my_f_lstm(start = begin , end = end)
        x,y,code,ret,ret_std,ret_hot =genLstmData (data,x,y,code,days,ret,ret_std , ret_hot)
        shi_jian.append(end)
        
        data = { "x"       :  x        ,
                 "y"       :  y        ,
                 "code"    :  code     ,
                 "return"  :  ret      ,
                 "ret_std" :  ret_std  ,
                 "shi_jian":  shi_jian ,
                 "ret_hot" :  ret_hot         
                }

    return data
   
def genLstmData( df,x,y,pcode,days,ret = [] , ret_std = [] , ret_hot = [] ):
    codes = pd.DataFrame()
    codes["code"] = df["code"]
    codes = codes.drop_duplicates() 
    
    print(len(codes))
    
    for code in codes["code"].values :
        c_data = df[df["code"] == code] 
        if len(c_data) != days :
            continue 
        
        pcode.append(code)
        
        y_  = c_data["ret_hot"].values[-1] 
        ret_hot.append(y_)
                     
        if y_ == 0 :
            y_= [0,1]
        else :
            y_= [1,0]            
        y.append(y_)
        
        ret.append(c_data["return"].values[-1])
        ret_std.append(c_data["ret_std"].values[-1] )
        
        c_data = c_data.drop('code', 1)
        c_data = c_data.drop('shi_jian', 1)
        c_data = c_data.drop('return', 1)
        c_data = c_data.drop('ret_std', 1)
        c_data = c_data.drop('ret_hot', 1) 
        c_data = np.array(c_data).tolist()

        x.append(c_data)      
    
    return x,y,pcode,ret,ret_std,ret_hot

train_time , test_time  = gsd.get_my_f_lstm_times( today=conf.today ,lenth=conf.total_days,days = conf.days)
conf.train_file += test_time[0]  
conf.test_file  += test_time[0]

if os.path.isfile(conf.train_file) == False :    
    train_data  = get_data(train_time , conf.days)    
    ftrain = open(conf.train_file, "wb")
    pickle.dump(train_data, ftrain)
    ftrain.close()
    print("train data saved")
else :
    ftrain = open(conf.train_file, "rb")
    train_data = pickle.load(ftrain)
    ftrain.close()    
    print("train data loaded")    
    
if os.path.isfile(conf.test_file) == False :  
    test_data   = get_data(test_time , conf.days)   
    ftest  = open(conf.test_file , "wb")    
    pickle.dump(test_data, ftest)
    ftest.close()    
    print("test data saved")    
else :
    ftest = open(conf.test_file, "rb")
    test_data  = pickle.load(ftest)
    ftest.close()    
    print("test data loaded")


train_x        = np.array( train_data["x"]       )
# train_y        = np.array( train_data["y"]       ) 
train_y        = np.array( train_data["ret_std"]       )
train_return   = np.array( train_data["return"]  )
train_ret_std  = np.array( train_data["ret_std"] )
train_shi_jian = np.array( train_data["shi_jian"])
train_code     = np.array( train_data["code"    ])

test_x        = np.array( test_data["x"]       )
# test_y        = np.array( test_data["y"]       )
test_y        = np.array( test_data["ret_std"]       )
test_return   = np.array(test_data["return"]   )
test_ret_std  = np.array(test_data["ret_std"]  )
test_shi_jian = np.array(test_data["shi_jian"] )
test_code     = np.array(test_data["code"    ] )


train_x = train_x.reshape(-1,6*conf.days)
test_x  = test_x.reshape(-1,6*conf.days)

# Specify sufficient boosting iterations to reach a minimum
# num_round = 61
num_round = 3348

#模型参数设置XGBRegressor
xlf = xgb.XGBRegressor(learning_rate=0.5, 
                        n_estimators=55,
                        max_depth=5,  
                        min_child_weight=3, 
                        silent=True, 
                        objective='reg:linear', 
                        nthread=-1, 
                        gamma=0,                        
                        max_delta_step=0, 
                        subsample= 1, 
                        colsample_bytree= 1, 
                        colsample_bylevel=1, 
                        reg_alpha=0.0001, 
                        reg_lambda= 0.2,   
                        scale_pos_weight=0, 
                        seed=1024, 
                        missing=None)

# python Z:\StockAnalysis\sourceCode\TuShare\test\src\importAlpha101_train_xgb.py 

train = True

if train :
#     xlf.fit(train_x, train_y, eval_metric='logloss', verbose = True, eval_set = [(test_x, test_y)],early_stopping_rounds=50)
    xlf.fit(train_x, train_y, eval_metric='auc',  eval_set = [(test_x, test_y)],verbose = True ,early_stopping_rounds=50)
    # xlf._Booster.save_model(conf.file)
    pickle.dump(xlf, open(conf.file, "wb"))
    print("model saved")
else :
    # load data
    bExists = os.path.isfile(conf.file)
    if bExists :
    #     xlf._Booster = xgb.Booster()
    #     xlf._Booster.load_model(conf.file)
        xlf = pickle.load(open(conf.file, "rb"))
        print("model loaded")

# 计算 auc 分数、预测
# predictions = xlf.predict(train_x)
predictions = xlf.predict(test_x)

# accuracy = accuracy_score(test_y, predictions)

f = open('d:/test.csv','w')    
#     for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , test_y , test_code ,test_shi_jian,test_return):
for pre , test_y_ , test_code_ ,test_return_ in zip(predictions , test_y , test_code ,test_return):
#         f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_ +","+test_shi_jian_ + "\n")
    f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_  + "\n")
#     print(pre[0] , test_y_ , test_code_ ,test_shi_jian_)    
f.close()      
print("finished")




