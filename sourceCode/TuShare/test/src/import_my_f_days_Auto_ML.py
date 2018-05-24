import xgboost as xgb 
import numpy as np
import pandas as pd
import getStockData as gsd
import os
import pickle
# from sklearn.metrics import accuracy_score
from auto_ml import Predictor
# from auto_ml.utils import get_boston_dataset
from auto_ml.utils_models import load_ml_model

# 基础参数配置
class conf:
#     today = '2017-06-02'
#     today = '2017-04-13'
#     today = '2017-09-22'
    today = '2017-01-10'
#     today = '2017-01-04'
#     today = '2017-08-11'
#     file = "d:/xgb.h"
    days = 12
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

colums = []
for c in pd.DataFrame(train_x).columns :
    colums.append("x" + str(int(c/6))+str(c%6))
    
colums.append("y")

df_train = pd.DataFrame(train_x)
df_train["y"] = train_y

df_test = pd.DataFrame(test_x)
df_test["y"] = test_y

df_train.columns =colums
df_test.columns =colums

file_name = "d:/automl.saved"

if __name__ == '__main__':
    # Tell auto_ml which column is 'output'
    # Also note columns that aren't purely numerical
    # Examples include ['nlp', 'date', 'categorical', 'ignore']
    column_descriptions = {
      'y': 'output' ,
#       'CHAS': 'categorical'
    }
    
    ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)
    
    model_names = ['LGBMRegressor',"AdaBoostRegressor","XGBRegressor","ExtraTreesRegressor","RANSACRegressor",]
    model_names = ["GradientBoostingRegressor","DeepLearningRegressor","RandomForestRegressor","SGDRegressor","PassiveAggressiveRegressor"]
#     ml_predictor.train(df_train , model_names = model_names )
    ml_predictor.train(df_train  )
    
    # Score the model on test data
    test_score = ml_predictor.score(df_test, df_test.y)
    
    # auto_ml is specifically tuned for running in production
    # It can get predictions on an individual row (passed in as a dictionary)
    # A single prediction like this takes ~1 millisecond
    # Here we will demonstrate saving the trained model, and loading it again
    file_name = ml_predictor.save(file_name="d:/automl.saved")  
    test_score = ml_predictor.score(df_test, df_test.y)
    print(test_score)
    
    

    trained_model = load_ml_model(file_name)
    
    # .predict and .predict_proba take in either:
    # A pandas DataFrame
    # A list of dictionaries
    # A single dictionary (optimized for speed in production evironments)
    predictions = trained_model.predict(df_test)
    print(df_test)
    print(predictions)
    print("test:",len(df_test))
    print("train:",len(df_train))      
    
    
    f = open('d:/test.csv','w')    
    #     for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , test_y , test_code ,test_shi_jian,test_return):
    for pre , test_y_ , test_code_ ,test_return_ in zip(predictions , test_y , test_code ,test_return):
    #         f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_ +","+test_shi_jian_ + "\n")
        f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_  + "\n")
    #     print(pre[0] , test_y_ , test_code_ ,test_shi_jian_)    
    f.close()      
    print("finished")
