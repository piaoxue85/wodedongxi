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
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import time

from keras.layers import Input, Dense, LSTM
from keras.models import Model
from keras.layers import *
from keras.models import *
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
# 000300zs

df_ = gsd.get_tb_temp_data()

print(df_.columns)

df = pd.DataFrame()
df_shi_jian = pd.DataFrame()

df["rate" ] = df_["rate"           ].values

df_shi_jian["shi_jian"] = df_["shi_jian"].values

# print(df)
# print(df_shi_jian)

data_train =df.iloc[:int(df.shape[0] * 0.9) , :]
data_test = df.iloc[ int(df.shape[0] * 0.9):, :]
print(data_train.shape, data_test.shape)

print(data_train)
print(data_test)

# scaler = MinMaxScaler(feature_range=(0, 1))
# scaler.fit(data_train)
# data_train = scaler.transform(data_train)
# data_test  = scaler.transform(data_test )

data_train = np.array(data_train)
data_test  = np.array(data_test )

print(data_train)

# output_dim = 1
batch_size = 2
epochs = 500
seq_len = 5
# hidden_size = 128


TIME_STEPS = seq_len
INPUT_DIM = len(df.columns)

lstm_units = 128

#预测多少天后的价格
pre_date = 1

X_train = np.array([data_train[i : i + seq_len           , :]     for i in range(data_train.shape[0] - seq_len-pre_date )])
y_train = np.array([data_train[i     + seq_len+pre_date  , 0]     for i in range(data_train.shape[0] - seq_len-pre_date )]) 
X_test  = np.array([data_test[ i : i + seq_len           , :]     for i in range(data_test.shape[0]  - seq_len-pre_date )])
y_test  = np.array([data_test[ i     + seq_len+pre_date  , 0]     for i in range(data_test.shape[0]  - seq_len-pre_date )]) 

print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

inputs = Input(shape=(TIME_STEPS, INPUT_DIM))
#drop1 = Dropout(0.3)(inputs)

x = Conv1D(filters = 128, kernel_size = 1, activation = 'relu')(inputs)  #, padding = 'same'
# x = Conv1D(filters = 64, kernel_size = 1, activation = 'relu')(inputs)  #, padding = 'same'
x = MaxPooling1D(pool_size = seq_len)(x)
x = Dropout(0.1)(x)

print(x.shape)

lstm_out = Bidirectional(LSTM(lstm_units, activation='relu'), name='bilstm')(x)
#lstm_out = LSTM(lstm_units,activation='relu')(x)
print(lstm_out.shape)

output = Dense(1, activation='sigmoid')(lstm_out)
#output = Dense(10, activation='sigmoid')(drop2)

model = Model(inputs=inputs, outputs=output)
print(model.summary())

model.compile(loss='mse', optimizer='adam')

# early_stopping = EarlyStopping(monitor='val_loss', patience=100 , verbose=2,mode="min")
# model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,validation_data=(X_test, y_test), shuffle=False,callbacks=[early_stopping])
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,shuffle=False)

y_pred = model.predict(X_test)
print('MSE Train loss:', model.evaluate(X_train, y_train, batch_size=batch_size))
print('MSE Test loss:' , model.evaluate(X_test, y_test  , batch_size=batch_size))
plt.plot(y_test, label='test')
plt.plot(y_pred, label='pred')
plt.legend()
plt.show()
print("end")