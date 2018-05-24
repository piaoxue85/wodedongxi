'''
Created on 2017年9月30日

@author: moonlit
'''
import xgboost as xgb 
import getStockData as gsd
import pickle
from xgboost.sklearn import XGBRegressor

def get_data(train_begin="",train_end="", test_begin="", test_end=""):
    train_data = gsd.get_101_data_train1(start=train_begin, end = train_end)
    test_data  = gsd.get_101_data_test1(start=test_begin , end = test_end )
#     test_data  = gsd.get_101_data_test(start="2017-08-24" , end = "2017-08-25" )
    return train_data , test_data

# 基础参数配置
class conf:
#     today = '2017-06-02'
#     today = '2017-04-13'
#     today = '2017-09-22'
#     today = '2017-01-10'
#     today = '2017-01-04'
    today = '2017-08-11'
    file = "d:/xgb.h"

# 035,

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

#模型参数设置XGBRegressor
xlf = xgb.XGBRegressor(learning_rate=0.5, 
                        n_estimators=20000,
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

# python Z:\StockAnalysis\sourceCode\TuShare\test\src\importAlpha101_train_xgb.py 

train = True



if train :
    xlf.fit(train_x, train_y, eval_metric='auc', verbose = True, eval_set = [(test_x, test_y)],early_stopping_rounds=50)
    # xlf.fit(train_x, train_y, eval_metric='mae',  eval_set = [(train_x, train_y)],verbose = True ,early_stopping_rounds=20)
    # xlf._Booster.save_model(conf.file)
    pickle.dump(xlf, open(conf.file, "wb"))
    print("model saved")
else :
    # load data
    import os
    bExists = os.path.isfile(conf.file)
    if bExists :
    #     xlf._Booster = xgb.Booster()
    #     xlf._Booster.load_model(conf.file)
        xlf = pickle.load(open(conf.file, "rb"))
        print("model loaded")

# 计算 auc 分数、预测
# predictions = xlf.predict(train_x)
predictions = xlf.predict(test_x)

print(train_begin , train_end , test_begin,test_end) 

f = open('d:/test.csv','w')
# for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , train_y , train_code ,train_shi_jian,train_return):
for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , test_y , test_code ,test_shi_jian,test_return):
    f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_ +","+test_shi_jian_ + "\n")
#     print(pre[0] , test_y_ , test_code_ ,test_shi_jian_)
    
f.close()    
print("finished")


    