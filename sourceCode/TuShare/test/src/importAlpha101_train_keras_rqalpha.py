'''
Created on 2017年9月30日

@author: moonlit
'''

from keras.layers import Input, Dense
from keras.models import Model
from keras.models import load_model
# from keras.optimizers import SGD,Adam
# import numpy as np
import pandas as pd
import getStockData as gsd
import tensorflow as tf


def get_data(begin = "2017-01-01" , split ="2017-02-01" , end = "2017-10-01"):        
    train_data = gsd.get_101_data_test(start=begin, end = split)
    test_data  = gsd.get_101_data_test(start=split, end = end  )
    return train_data , test_data

# 自定义激活函数
def atan(x): 
    return tf.atan(x)*1
    return x

# 基础参数配置
class conf:
    start_date = '2017-08-01'
    split_date = '2017-09-05'
    end_date   = '2017-09-06'
    batch      = 200000
    FILE_PATH  = 'd:\model_1.h5'
    train_days = 10

def train(train_data ): 
    train_x        = train_data["data_101"]
    train_y        = train_data["CodeRetStd"] 
    train_return   = train_data["CodeReturn"]
#     train_shi_jian = train_data["shi_jian"]
#     train_code     = train_data["code"    ]
    
    train_y = train_return
    
    # print(train_x)
    # print(train_y)
    # print(train_return)
    # print(train_shi_jian)
    # print(train_code)
        
    input_         = Input(shape=(46,), name='input')
    Dense_output_1 = Dense(128,activation='linear')(input_)
    Dense_output_2 = Dense(64, activation='linear')(Dense_output_1)
    Dense_output_3 = Dense(32, activation='linear')(Dense_output_2)
    Dense_output_4 = Dense(16, activation='linear')(Dense_output_3)
    Dense_output_5 = Dense(8,  activation='linear')(Dense_output_4)
    Dense_output_6 = Dense(4,  activation='linear')(Dense_output_5)
    Dense_output_7 = Dense(2,  activation='linear')(Dense_output_6)
    predictions    = Dense(1,  activation='linear')(Dense_output_7)
    model          = Model(input=input_, output=predictions)
    model.compile(optimizer="adamax", loss='mae', metrics=['mse',"mape"])
    
    import os
    bExists = os.path.isfile(conf.FILE_PATH)
    if bExists :
        model = load_model(conf.FILE_PATH)
        print("loaded")
        
    model.fit(train_x, train_y, batch_size=conf.batch, epochs=1000, verbose=1)
    
    model.save(conf.FILE_PATH)
    print("saved")
    
    return model

def get_buy_list(today="" , buy_count = 20):
    start_date , split_date , end_date = gsd.get_101_data_3_times(today=today , train_days = conf.train_days)
    train_data , test_data = get_data(begin=start_date, split=split_date, end=end_date) 
        
    model = train(train_data = train_data)
    
    test_x        = test_data["data_101"]
#     test_y        = test_data["CodeRetStd"] 
#     test_return   = test_data["CodeReturn"]
#     test_shi_jian = test_data["shi_jian"]
    test_code     = test_data["code"    ]
        
    predictions = model.predict(test_x)
    predictions = predictions.reshape(-1)
#     print(predictions)
    data = pd.DataFrame()
    data["pre"] = predictions
    data["code"]= test_code
    data        = data.sort_values(by = "pre", ascending =False)
#     print(data)
    buy_list  = data["code"].values
    buy_list  = buy_list[:buy_count]
    buy_list_ = pd.DataFrame()
    
    buy_list_["code"] = buy_list
    
    return buy_list_
    




    