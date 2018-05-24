'''
Created on 2017年9月30日

@author: moonlit
'''

import tensorflow as tf
import numpy as np
from docutils.nodes import target

def variable_with_weight_loss(shape , stddev , w1):
    var = tf.Variable(tf.truncated_normal(shape, stddev=stddev))
    
    if w1 is not None :
        #给weight 增加 L2_loss用于避免overfit，L2正则让特征权重不过大，L1是置为0 造成稀疏
        #实战86
        weight_loss = tf.multiply(tf.nn.l2_loss(var), w1, name='weight_loss')
        #add 到一个collection，计算总体loss 会用到
        tf.add_to_collection('losses' , weight_loss)
    
    return var

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def model(alphasOneDay , W , b ):
  
    rankpoint = tf.matmul(alphasOneDay,W) + b
    
    return rankpoint

def get_data(begin = "2017-01-01" , split ="2017-02-01" , end = "2017-10-01"):
    import getStockData as gsd
        
    train_data = gsd.get_101_data(start=begin, end = split)
    test_data  = gsd.get_101_data(start=split, end = end  )
    return train_data , test_data

alphasOneDay = tf.placeholder(tf.float32, [None,46] )
selected     = tf.placeholder(tf.float32, [None,None] )

W = variable_with_weight_loss(shape=[46,1], stddev = 5e-2 , w1 = 0.0)
b = bias_variable([1])

pre = model(alphasOneDay , W , b)

loss     = -tf.reduce_sum(selected*tf.log(pre))
train_op = train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)

train_data , test_data = get_data(begin="2017-01-01", split="2017-01-15", end="2017-02-01") 

train_X  = np.array(train_data["data_101"])
train_Y  = np.array(train_data["Selected"]) 
shi_jian = train_data["shi_jian"]

train_X = train_X.reshape(9,-1,46)

print(train_X.shape)
print(train_Y.shape)

    
batch_size   = 5
display_step = 5
    
with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    epoch = 1
    for i in range(10):
        for i in range(int(len(train_X)/batch_size)): 
            batch_x = train_X[i*batch_size:(i+1)*batch_size]
            batch_y = train_Y[i*batch_size:(i+1)*batch_size]
                  
            sess.run(train_op , feed_dict={alphasOneDay: batch_x,selected:batch_y})
            if i % display_step ==0:                
                print(i,'----',(int(len(train_X)/batch_size)))
    