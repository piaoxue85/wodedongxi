'''
Created on 2017年9月30日

@author: moonlit
'''


from keras.layers import Input, Dense
from keras.models import Model
from keras.models import load_model
# from keras.optimizers import SGD,Adam
# import numpy as np
# import pandas as pd
# import getStockData as gsd
import tensorflow as tf


def get_data(begin = "2017-01-01" , split ="2017-02-01" , end = "2017-10-01"):
    import getStockData as gsd
        
    train_data = gsd.get_101_data_test(start=begin, end = split)
    test_data  = gsd.get_101_data_test(start=split, end = end  )
    return train_data , test_data

# 自定义激活函数
def atan(x): 
    return tf.atan(x)*1
    return x

# 基础参数配置
class conf:

    start_date = '2017-01-01'
    split_date = '2017-09-22'
    end_date   = '2017-09-23'
    batch      = 200000 
    FILE_PATH  = 'd:\model_1.h5'

train_data , test_data = get_data(begin=conf.start_date, split=conf.split_date, end=conf.end_date) 

train_x        = train_data["data_101"]
train_y        = train_data["CodeRetStd"] 
train_return   = train_data["CodeReturn"]
train_shi_jian = train_data["shi_jian"]
train_code     = train_data["code"    ]

train_y = train_return*10

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

input_         = Input(shape=(46,), name='input')
Dense_output_1 = Dense(1024,activation='linear')(input_)
Dense_output_2 = Dense(512, activation='linear')(Dense_output_1)
Dense_output_3 = Dense(256, activation='linear')(Dense_output_2)
Dense_output_4 = Dense(128, activation='linear')(Dense_output_3)
Dense_output_5 = Dense(64,  activation='linear')(Dense_output_4)
Dense_output_6 = Dense(32,  activation='linear')(Dense_output_5)
Dense_output_7 = Dense(16,  activation='linear')(Dense_output_6)
Dense_output_8 = Dense(8,   activation='linear')(Dense_output_7)
Dense_output_9 = Dense(4,   activation='linear')(Dense_output_8)
Dense_output_0 = Dense(2,   activation='linear')(Dense_output_9)
predictions    = Dense(1,   activation='linear')(Dense_output_0)
model          = Model(input=input_, output=predictions)
model.compile(optimizer="adamax", loss='mae', metrics=['mse',"mape"])

import os
bExists = os.path.isfile(conf.FILE_PATH)
if bExists :
    model = load_model(conf.FILE_PATH)
    print("loaded")
    
model.fit(train_x, train_y, batch_size=conf.batch, epochs=1500, verbose=2)
model.save(conf.FILE_PATH)
print("saved")

predictions = model.predict(test_x)

# import matplotlib.pyplot as plt
# # 预测值和真实值的关系
# data1 = test_y
# data2 = predictions
# fig, ax = plt.subplots(figsize=(8, 6))
# ax.plot(data2,data1, 'o', label="data")
# #ax.legend(loc='best')    

f = open('d:/test.csv','w')
for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , test_y , test_code ,test_shi_jian,test_return):
    f.writelines(str(test_return_) +"," + str(pre[0]) +","+ str(test_y_) +","+test_code_ +","+test_shi_jian_ + "\n")
#     print(pre[0] , test_y_ , test_code_ ,test_shi_jian_)
    
f.close()    



    