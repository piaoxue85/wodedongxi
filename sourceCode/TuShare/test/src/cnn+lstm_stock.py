'''
Created on 2018年11月30日

@author: moonlit

深度学习模型 CNN+LSTM 预测收盘价

https://www.joinquant.com/research?target=research&url=/user/22199979333/notebooks/CNN%2BLSTM%E9%A2%84%E6%B5%8B%E6%94%B6%E7%9B%98%E4%BB%B7.ipynb
https://www.joinquant.com/community/post/detailMobile?postId=15443&page=&limit=20&replyId=&tag=&from=timeline&isappinstalled=0
'''
import pandas as pd
import time, datetime
import getStockData as gsd

import pandas as pd
import numpy as np
# import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from keras.layers import Input, Dense, LSTM
from keras.models import Model
from keras.layers import *
from keras.models import *
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

import cx_Oracle
from sqlalchemy import create_engine

def get_MSE_Test_loss(code="") :
    df_ = gsd.get_stock_data_daily_df_time(code, "2005-01-04","2018-11-30")
    df = pd.DataFrame()
    df_shi_jian = pd.DataFrame()
    
    df["close" ] = df_["price"           ].values
    df["open"  ] = df_["price_today_open"].values
    df["high"  ] = df_["max_price"       ].values
    df["low"   ] = df_["min_price"       ].values
    df["volume"] = df_["vol"             ].values
    df["money" ] = df_["amount"          ].values
    # df["shi_jian"] = df_["shi_jian"          ].values
    
    df_shi_jian["shi_jian"] = df_["shi_jian"].values
    
    # print(df)
    # print(df_shi_jian)
    
    data_train =df.iloc[:int(df.shape[0] * 0.85) , :]
    data_test = df.iloc[ int(df.shape[0] * 0.85):, :]
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(data_train)
    
    data_train = scaler.transform(data_train)
    data_test  = scaler.transform(data_test )

    batch_size = 256
    epochs = 120
    seq_len = 5

    TIME_STEPS = 5
    INPUT_DIM = 6
    
    lstm_units = 64
    
    X_train = np.array([data_train[i : i + seq_len    , :]     for i in range(data_train.shape[0] - seq_len*2 )])
    y_train = np.array([data_train[i     + seq_len*2  , 0]     for i in range(data_train.shape[0] - seq_len*2 )]) 
    X_test  = np.array([data_test[ i : i + seq_len    , :]     for i in range(data_test.shape[0]  - seq_len*2 )])
    y_test  = np.array([data_test[ i     + seq_len*2  , 0]     for i in range(data_test.shape[0]  - seq_len*2 )]) 
        
    inputs = Input(shape=(TIME_STEPS, INPUT_DIM))

    x = Conv1D(filters = 64, kernel_size = 1, activation = 'relu')(inputs)  #, padding = 'same'
    x = MaxPooling1D(pool_size = 5)(x)
    x = Dropout(0.2)(x)
    
    lstm_out = Bidirectional(LSTM(lstm_units, activation='relu'), name='bilstm')(x)
   
    output = Dense(1, activation='sigmoid')(lstm_out)
    
    model = Model(inputs=inputs, outputs=output)
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=5 , verbose= 0,mode="min")
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,verbose= 0,validation_data=(X_test, y_test), shuffle=False,callbacks=[early_stopping])    
#     y_pred = model.predict(X_test)
#     print('MSE Train loss:', model.evaluate(X_train, y_train, batch_size=batch_size))
#     print('MSE Test loss:' , model.evaluate(X_test, y_test  , batch_size=batch_size))
#     plt.plot(y_test, label='test')
#     plt.plot(y_pred, label='pred')
#     plt.legend()
#     plt.show()
    mse = model.evaluate(X_test, y_test  , batch_size=batch_size)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"done ", code ,'MSE Test loss:' , mse)
    return mse 
    
def get_code_list():
    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')    
    sql  = "select code from ("
    sql += "  select code,count(1) from tb_stock_data_daily where length(code)=6 and  shi_jian>= to_date('20050101150000','yyyymmddhh24miss') group by code having count(1) >= 3000 "
    sql += ")                               "
    sql += "where code not in               " 
    sql += "(                               "
    sql += "  select code from tb_stock_mse "
    sql += ")                               "
    data = pd.read_sql_query(sql,con = engine)
    return data["code"].values    
    
    
codes = get_code_list();
db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
cr=db.cursor()

for code in codes :
    mse = get_MSE_Test_loss(code)
    sql = "insert into tb_stock_mse values ('" + code + "'," + str(mse)+")"
    cr.execute(sql)
    db.commit()  
    
      
cr.close ()  
db.close ()    
print("all done")  