'''
Created on 2017年7月18日

@author: moonlit

python D:\Competition\src\train.py
'''

import json
import pandas as pd
import numpy  as np
import jieba

import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn.utils import shuffle  
from keras.layers import Input, Dense, LSTM, merge,Flatten
from keras.layers.convolutional import Conv1D,Conv2D
from keras.models import Model
from keras.layers import Embedding 
import keras
from sklearn.utils import shuffle  

from gensim.models.word2vec import Word2Vec
# 基础参数配置
class conf:
    seq_len = 2000 #每个input的长度
    batch = 200 #整数，指定进行梯度下降时每个batch包含的样本数,训练时一个batch的样本会被计算一次梯度下降，使目标函数优化一步               
    
    savedFile = "D:/Competition/src/saved.h5"
    atcType = "predict"      # train , evaluate , predict

# 自定义激活函数
import tensorflow as tf
def atan(x): 
    return tf.atan(x)

def getModel(weights):
    # 构建神经网络层 1层LSTM层+3层Dense层
    # 用于1个输入情况
    lstm_input = Input(shape=(2000,), name='lstm_input')
    embedding_layer = Embedding(input_dim=weights.shape[0], output_dim=weights.shape[1], weights=[weights],trainable=False)(lstm_input)    
    lstm_output = LSTM(128, activation=atan, dropout_W=0.2, dropout_U=0.1,return_sequences=True)(embedding_layer)
    lstm_output1 = LSTM(64, activation=atan, dropout_W=0.2, dropout_U=0.1,return_sequences=True)(lstm_output)
    lstm_output2 = LSTM(32, activation=atan, dropout_W=0.2, dropout_U=0.1,return_sequences=True)(lstm_output1)
    cnn_output =Conv1D(8,3)(lstm_output2)
    flatten = Flatten()(cnn_output)
    Dense_output_1 = Dense(8, activation='linear')(flatten)
    Dense_output_2 = Dense(4, activation='linear')(Dense_output_1)
    predictions = Dense(3, activation=atan)(Dense_output_2)    
    model = Model(input=lstm_input, output=predictions)
    return model

#     lstm_input = Input(shape=(2000,), name='lstm_input')
#     embedding_layer = Embedding(input_dim=weights.shape[0], output_dim=weights.shape[1], weights=[weights],trainable=False)(lstm_input)    
#     lstm_output = LSTM(64, activation="sigmoid", dropout_W=0.2, dropout_U=0.1,return_sequences=True)(embedding_layer)
#     cnn_output =Conv1D(8,3)(lstm_output)
#     flatten = Flatten()(cnn_output)
#     Dense_output_1 = Dense(8, activation='linear')(flatten)
#     Dense_output_2 = Dense(4, activation='linear')(Dense_output_1)
#     predictions = Dense(3, activation="sigmoid")(Dense_output_2)    
#     model = Model(input=lstm_input, output=predictions)
#     return model

#     lstm_input = Input(shape=(2000,), name='lstm_input')
#     embedding_layer = Embedding(input_dim=weights.shape[0], output_dim=weights.shape[1], weights=[weights],trainable=False)(lstm_input)    
#     lstm_output = LSTM(32, activation=atan, dropout_W=0.2, dropout_U=0.1,return_sequences=True)(embedding_layer)
#     cnn_output =Conv1D(8,3)(lstm_output)
#     flatten = Flatten()(cnn_output)
#     Dense_output_1 = Dense(4, activation='linear')(flatten)
#     predictions = Dense(3, activation=atan)(Dense_output_1)    
#     model = Model(input=lstm_input, output=predictions)
#     return model

def generate(data):  
        x = []
        y = []      
        count = 0  
        while  True:
            for info in data:
                y1 = (info["d1_open"]-info["d0_open"])/info["d0_open"]
                y2 = (info["d2_open"]-info["d1_open"])/info["d1_open"]
                y3 = (info["d3_open"]-info["d2_open"])/info["d2_open"]
                
                newses = eval(info["Announcements"] )
                
                title        = []
                annonce_type = []
                content      = []
                x_           = []
                
                for news in newses :
                    title        = news["title"]
                    #公告
                    annonce_type = news["annonce_type"]
                    #研报
#                     annonce_type = news["column_type"]                    
                    content      = news["content"]
                    
                    x_ = content+annonce_type+title
                    
                    if len(x_ ) > 200 :
                        #768479
                        if len(x_ ) < 20 :
                            print(x_)
                        
                        if len(x_)<conf.seq_len :
                            padding = np.zeros((conf.seq_len-len(x_)), dtype=np.int)
                            x_ += list(padding)    
                        else:
                            x_ = x_[:conf.seq_len]
                    else :
                        continue
                                
        
                    x.append(x_)
                    y.append([y1,y2,y3])
#                     x = [x_]
#                     y = [[y1,y2,y3]]
                    count += 1
                    
                    if count % conf.batch == 0 :
                        x = np.array(x)
                        y = np.array(y)
    
                        yield x,y*100
                        x = []
                        y = []
                
def getEvaData(data):
    x = []
    y = []      

    for info in data:
        y1 = info["value1"]
        y2 = info["value2"]
        y3 = info["value3"]
        
        newses = eval(info["Announcements"] )
    
        x_           = []
        
        for news in newses :
            title        = news["title"]
            #公告
            annonce_type = news["annonce_type"]
            #研报
#             annonce_type = news["column_type"]                    
            content      = news["content"]
            
            x_ = content+annonce_type+title
            
            if len(x_ ) > 200 :
                #768479
                if len(x_ ) < 20 :
                    print(x_)
                
                if len(x_)<conf.seq_len :
                    padding = np.zeros((conf.seq_len-len(x_)), dtype=np.int)
                    x_ += list(padding)    
                else:
                    x_ = x_[:conf.seq_len]
            else :
                continue
                        

            x.append(x_)
            y.append([y1,y2,y3])
                      
    return x, y*1000
    
def getPredictData(data) :   
    x = []
    y = []      
    code     = []
    shi_jian = []
    for info in data:
        y1 = info["value1"]
        y2 = info["value2"]
        y3 = info["value3"]
        
        newses = eval(info["Announcements"] )
        
        x_           = []
        
        for news in newses :
            title        = news["title"]
            #公告
            annonce_type = news["annonce_type"]
            #研报
#             annonce_type = news["column_type"]                    
            content      = news["content"]
            
            x_ = content+annonce_type+title
            
            if len(x_ ) > 200 :
                #768479
                if len(x_ ) < 20 :
                    print(x_)
                
                if len(x_)<conf.seq_len :
                    padding = np.zeros((conf.seq_len-len(x_)), dtype=np.int)
                    x_ += list(padding)    
                else:
                    x_ = x_[:conf.seq_len]
            else :
                continue
                        
            code.append(info["security_id"])
            shi_jian.append(info["data_date"])
            x.append(x_)
            y.append([y1,y2,y3])
            
#         if len(x)>=10 :
#             break
                      
    return code,shi_jian ,x, y     


#载入保存的文件
modelWord2Vec = Word2Vec.load("D:\Competition\src\data\SogouCA\corpus.model")    
#获得权重
weights = modelWord2Vec.wv.syn0  


model = getModel(weights)
model.compile(optimizer='adam', loss='mse', metrics=['mse','accuracy'])
try :
    model.load_weights(conf.savedFile)
    print("model loaded")
except :    
    print("load model err")
    
if conf.atcType == "train" :  # train , evaluate , predict
    #公告
    file = open("D:/Competition/src/data/train/CodeAndAnnouncements_wordVec.json",'r', encoding='utf_8_sig')
    #研报
#     file = open("D:/Competition/src/data/train/CodeAndResearch_wordVec.json",'r', encoding='utf_8_sig')
    data = json.load(file)    
#     early_stopping = EarlyStopping(monitor='loss', patience=2)
    model.fit_generator(generate(data), steps_per_epoch=100,epochs=1)
    model.save_weights(conf.savedFile)
    print("model saved")
elif conf.atcType == "evaluate":
#     file = open("D:/Competition/src/data/test/CodeAndResearch_wordVec.json",'r', encoding='utf_8_sig')
    file = open("D:/Competition/src/data/test/CodeAndAnnouncements_wordVec.json",'r', encoding='utf_8_sig')  
    data = json.load(file)      
    x,y =  getEvaData(data) 
    score = model.evaluate(x, y, batch_size = conf.batch)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))
    #research : mean_squared_error: 0.10%
    #Announcements ：mean_squared_error: 0.13%
elif conf.atcType == "predict" :
    file = open("D:/Competition/src/data/test/CodeAndAnnouncements_wordVec.json",'r', encoding='utf_8_sig')  
    data = json.load(file)      
    code,shi_jian ,x, y   =  getPredictData(data)
#     print(y)
    predictions = model.predict(x)/100
    df = pd.DataFrame()
    df["code"]    = code 
    df["shi_jian"]= shi_jian
    df["y"] = y
    df["prediction"] = predictions.tolist()
    df.to_csv('D:/Competition/src/data/predict.csv')
    
    



        
         


 
