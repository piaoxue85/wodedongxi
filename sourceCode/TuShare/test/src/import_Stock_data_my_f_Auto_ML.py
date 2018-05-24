'''
Created on 2017年9月30日

@author: moonlit
'''
 
import getStockData as gsd
import pandas as pd
import numpy as np
from auto_ml import Predictor
# from auto_ml.utils import get_boston_dataset
from auto_ml.utils_models import load_ml_model
from sklearn import preprocessing

def get_data(train_begin="",train_end="", test_begin="", test_end=""):
    train_data,_ = gsd.get_101_data_train1_my_f(start=train_begin, end = train_end)
    test_data,_  = gsd.get_101_data_test1_my_f (start=test_begin , end = test_end )
#     test_data  = gsd.get_101_data_test(start="2017-08-24" , end = "2017-08-25" )
    return train_data , test_data

# 基础参数配置
class conf:
#     today = '2017-07-17'    
#     today = '2017-06-02'
#     today = '2017-04-13'
#     today = '2017-09-22'
    today = '2017-01-10'
#     today = '2017-01-04'
#     today = '2017-08-11'
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

cols = [
        "x1",
        "x2",
        "x3",
        "x4",
        "x5",
        "x6",
        "x7",
        "x8",
        "x9",
        "x10",
        "x11",
        "x12",
        "x13",
        "x14",
        "x15",
        "x16",
        ]

clos_need = [
            "x9" ,
            "x8" ,
            "x14",
            "x12",
            "x11",
            "x10", 
            "x15",                           
            ]

clos_need = cols

def del_not_deed(df,cols = [] ,needed=[]):
    
    for col in cols:
        if col not in needed :
            df = df.drop(col,1)
    
    return df 

df_train = pd.DataFrame(train_x)
df_train.columns = cols
df_train = del_not_deed(df_train, cols, clos_need)
cols_ = df_train.columns 
df_train = preprocessing.scale(df_train.as_matrix().astype(float) , axis =1 )
df_train = pd.DataFrame(df_train)
df_train.columns = cols_
df_train["y"] = train_y*10


df_test = pd.DataFrame(test_x)
df_test.columns =cols
df_test = del_not_deed(df_test, cols, clos_need)
cols_ = df_test.columns 
df_test = preprocessing.scale(df_test.as_matrix().astype(float) , axis =1 )
df_test = pd.DataFrame(df_test)
df_test.columns = cols_
df_test["y"] = test_y*10

print(df_train.corr())
print(df_test.corr())


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
    model_names = ['LGBMRegressor',"AdaBoostRegressor","XGBRegressor","ExtraTreesRegressor","RANSACRegressor","GradientBoostingRegressor","DeepLearningRegressor","RandomForestRegressor","SGDRegressor","PassiveAggressiveRegressor"]
#     ml_predictor.train(df_train , model_names = model_names )    
    ml_predictor.train(df_train)
    
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
    
    
    f = open('d:/' + conf.today + '.csv','w')    
    #     for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , test_y , test_code ,test_shi_jian,test_return):
    for pre , test_y_ , test_code_ ,test_return_ in zip(predictions , test_y , test_code ,test_return):
    #         f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_ +","+test_shi_jian_ + "\n")
        f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_  + "\n")
    #     print(pre[0] , test_y_ , test_code_ ,test_shi_jian_)    
    f.close()      
    print("finished")
    