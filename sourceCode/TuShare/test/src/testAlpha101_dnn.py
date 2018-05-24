'''
Created on 2017年9月19日

@author: moonlit
'''
import numpy as np
import pandas as pd
import getStockData as gsd
import cx_Oracle
from sqlalchemy import create_engine
from keras.layers import Input, Dense, LSTM, merge,Dropout
from keras.models import Model
from keras.models import load_model
from keras.layers.advanced_activations import *
import tensorflow as tf

# from keras.datasets import cifar100
# 
# (X_train, y_train), (X_test, y_test) = cifar100.load_data(label_mode='fine')


def getXY():
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select * from tb_stock_alpha101 order by shi_jian asc"
    data = pd.read_sql_query(sql,con = engine)
    x = np.array(data)
    x = x[:,2:]
    shi_jians = data["shi_jian"]
    codes     = data["code"]
    
    y = []     
    for code, shi_jian in zip(codes,shi_jians) :
        sql  = "select * from ("
        sql += "select price from tb_stock_data_daily where code = '" + code + "' and shi_jian >= to_date( '" + shi_jian.strftime('%Y-%m-%d') + " 15:00:00' , 'yyyy-mm-dd hh24:mi:ss') order by shi_jian asc"
        sql += ") where rownum<=6 "
        
        data = pd.read_sql_query(sql,con = engine)
        data = np.array(data["price"])
        y_ = (data[-1] - data[0])/data[0]
        if y_*100 >0 :
            y_=[1,0]            #涨
        else :
            y_=[0,1]
        y.append(y_)
                
    return x,np.array(y)



class conf:
    batch = 50 #整数，指定进行梯度下降时每个batch包含的样本数,训练时一个batch的样本会被计算一次梯度下降，使目标函数优化一步
    FILE_PATH = 'd:\model.h5'


# 自定义激活函数
def atan(x): 
    return tf.atan(x)

# 构建神经网络层 1层LSTM层+3层Dense层
# 用于1个输入情况

In             = Input(shape=(101,), name='input')
Dense_output_1 = Dense(128  , activation="tanh")(In)
Dense_output_2 = Dense(64   , activation="tanh")(Dense_output_1)
Dense_output_3 = Dense(32   , activation="tanh")(Dense_output_2)
# drop_out_1     = Dropout(0.1)(Dense_output_3)
Dense_output_4 = Dense(16   , activation="tanh")(Dense_output_3)
Dense_output_5 = Dense(8    , activation="sigmoid")(Dense_output_4)
# drop_out_2     = Dropout(0.1)(Dense_output_5)
Dense_output_6 = Dense(4    , activation="sigmoid")(Dense_output_5)
Dense_output_7 = Dense(2    , activation="relu")(Dense_output_6)
predictions    = Dense(2    , activation="softmax")(Dense_output_7)

# In             = Input(shape=(101,), name='input')
# Dense_output_1 = Dense(128  , activation="tanh")(In)
# drop_out_1     = Dropout(0.2)(Dense_output_1)
# Dense_output_2 = Dense(64   , activation="tanh")(drop_out_1)
# drop_out_2     = Dropout(0.2)(Dense_output_2)
# Dense_output_3 = Dense(32   , activation="tanh")(drop_out_2)
# drop_out_3     = Dropout(0.2)(Dense_output_3)
# Dense_output_4 = Dense(16   , activation="sigmoid")(drop_out_3)
# drop_out_4     = Dropout(0.2)(Dense_output_4)
# Dense_output_5 = Dense(8    , activation="sigmoid")(drop_out_4)
# drop_out_5     = Dropout(0.2)(Dense_output_5)
# Dense_output_6 = Dense(4    , activation="relu")(drop_out_5)
# drop_out_6     = Dropout(0.2)(Dense_output_6)
# predictions    = Dense(2    , activation="softmax")(drop_out_6)

model = Model(input=In, output=predictions)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

x,y = getXY()
print(x.shape)
print(y.shape)
count = 2600
x_train = x[:count]
y_train = y[:count]
np.random.shuffle(x_train)
np.random.shuffle(y_train)
x_test  = x[count:]
y_test  = y[count:]
np.random.shuffle(x)
np.random.shuffle(y)

model.fit(x= x_train, y= y_train, batch_size=conf.batch, nb_epoch=2000,verbose=2)

res = model.evaluate(x=x_test, y=y_test,batch_size = 1,verbose=2) 
print("\n\r")
print("eva res :", res )

# predictions = model.predict(x=x_test)
# print(predictions)
# print(y_test)


