'''
Created on 2017年6月19日

@author: moonlit
'''
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import Convolution2D,MaxPooling2D , Flatten
model = Sequential()

#Convolution2D(25,3,3 的参数 25,3,3 是指 ： 25个filter ， 后面的“3,3”是指filter大小是3X3
#input_shape(28,28,1) 是指输入的图片大小是 28X28 解析度， 1表示只有一种颜色，即黑白的
model.add(Convolution2D(25,3,3 , input_shape=(28,28,1)))
model.add(MaxPooling2D((2,2)))
model.add(Convolution2D(50,3,3 ))
model.add(MaxPooling2D((2,2)))
model.add(Flatten())
model.add(Dense(output_dim = 100 ))
model.add(Activation('relu'))
model.add(Dense(output_dim = 10 ))
model.add(Activation('softmax'))

