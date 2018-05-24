# -*- coding:utf-8 -*-
 
'''
word embedding测试
在GTX960上，18s一轮
经过30轮迭代，训练集准确率为98.41%，测试集准确率为89.03%
Dropout不能用太多，否则信息损失太严重
'''
 
import numpy as np
import pandas as pd
import jieba
import os
 
pos = pd.read_excel('d:/pos.xls', header=None)
pos['label'] = 1
neg = pd.read_excel('d:/neg.xls', header=None)
neg['label'] = 0
all_ = pos.append(neg, ignore_index=True)
all_['words'] = all_[0].apply(lambda s: list(jieba.cut(s))) #调用结巴分词
 
maxlen = 100 #截断词数
min_count = 5 #出现次数少于该值的词扔掉。这是最简单的降维方法
 
content = []
for i in all_['words']:
    content.extend(i)
 
abc = pd.Series(content).value_counts()
abc = abc[abc >= min_count]
abc[:] = range(1, len(abc)+1)
abc[''] = 0 #添加空字符串用来补全
 
def doc2num(s, maxlen): 
    s = [i for i in s if i in abc.index]
    print(abc.index)
    s = s[:maxlen] + ['']*max(0, maxlen-len(s))
    return list(abc[s])
 
all_['doc2num'] = all_['words'].apply(lambda s: doc2num(s, maxlen))
temp = all_['doc2num'].values
 
#手动打乱数据
idx = np.arange(len(all_))
np.random.shuffle(idx)
all_ = all_.loc[idx]
 
#按keras的输入要求来生成数据
x = np.array(list(all_['doc2num']))
y = np.array(list(all_['label']))
y = y.reshape((-1,1)) #调整标签形状
 
 
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding
from keras.layers import LSTM
import keras
 
#建立模型
model = Sequential()
model.add(Embedding(len(abc), 256, input_length=maxlen))
model.add(LSTM(128)) 
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
 


batch_size = 128
train_num = 15000
isTrain = False
savedFile = "d:/wordembedding.h5"

def predict_one(s): #单个句子的预测函数
    s = np.array(doc2num(list(jieba.cut(s)), maxlen))
    s = s.reshape((1, s.shape[0]))
    return model.predict_classes(s, verbose=0)[0][0]

bExists = os.path.isfile(savedFile)

if not bExists : 
    model.fit(x[:train_num], y[:train_num], batch_size = batch_size, nb_epoch=30) 
    model.evaluate(x[train_num:], y[train_num:], batch_size = batch_size)
    model.save(savedFile)
    print("model saved")
else:
    model = keras.models.load_model(savedFile)
    print("model loaded")
    if isTrain :
        model.fit(x[:train_num], y[:train_num], batch_size = batch_size, nb_epoch=30) 
        model.evaluate(x[train_num:], y[train_num:], batch_size = batch_size)
        model.save(savedFile)
        print("model saved")
    else :
        s = "qnm的gou东，发二手的给我，吃屎吧，妈的就这样对待消费者是吧??"
        res = predict_one(s)
        print("res = " , str(res))