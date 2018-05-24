
from __future__ import division
from __future__ import print_function  
import numpy as np
import pandas as pd
# import matplotlib.pylab as plt
# import seaborn as sns
import tensorflow as tf
from tensorflow.contrib import rnn
# import tushare as ts
import getStockData as gsd
# import math
import os
from tensorflow.contrib.session_bundle import exporter
import pickle

# 基础参数配置
class conf:
#     today = '2017-06-02'
    today = '2017-04-13'
#     today = '2017-09-22'
#     today = '2017-01-10'
#     today = '2017-01-04'
#     today = '2017-08-11'
#     file = "d:/xgb.h"
    days = 5
    total_days = 15
    train_file = "d:/train.h"
    test_file  = "d:/test.h"
    
def get_data(time=[],days=5):
    x        = []
    y        = []
    code     = []
    shi_jian = []  
    ret      = []
    ret_std  = []
    ret_hot  = []       
    
    for i in range(0,len(time)) :
        if i+days > len(time) :
            break
        
        end   = time[i]
        begin = time[i+days-1]
        _,data = gsd.get_101_data_train1_my_f_lstm(start = begin , end = end)
        x,y,code,ret,ret_std,ret_hot =genLstmData (data,x,y,code,days,ret,ret_std , ret_hot)
        shi_jian.append(end)
        
        data = { "x"       :  x        ,
                 "y"       :  y        ,
                 "code"    :  code     ,
                 "return"  :  ret      ,
                 "ret_std" :  ret_std  ,
                 "shi_jian":  shi_jian ,
                 "ret_hot" :  ret_hot         
                }

    return data
   
def genLstmData( df,x,y,pcode,days,ret = [] , ret_std = [] , ret_hot = [] ):
    codes = pd.DataFrame()
    codes["code"] = df["code"]
    codes = codes.drop_duplicates() 
    
    print(len(codes))
    
    for code in codes["code"].values :
        c_data = df[df["code"] == code] 
        if len(c_data) != days :
            continue 
        
        pcode.append(code)
        
        y_  = c_data["ret_hot"].values[-1] 
        ret_hot.append(y_)
                     
        if y_ == 0 :
            y_= [0,1]
        else :
            y_= [1,0]            
        y.append(y_)
        
        ret.append(c_data["return"].values[-1])
        ret_std.append(c_data["ret_std"].values[-1] )
        
        c_data = c_data.drop('code', 1)
        c_data = c_data.drop('shi_jian', 1)
        c_data = c_data.drop('return', 1)
        c_data = c_data.drop('ret_std', 1)
        c_data = c_data.drop('ret_hot', 1) 
        c_data = np.array(c_data).tolist()

        x.append(c_data)      
    
    return x,y,pcode,ret,ret_std,ret_hot

train_time , test_time  = gsd.get_my_f_lstm_times( today=conf.today ,lenth=conf.total_days,days = conf.days)

if os.path.isfile(conf.train_file) == False :    
    train_data  = get_data(train_time , conf.days)    
    ftrain = open(conf.train_file, "wb")
    pickle.dump(train_data, ftrain)
    ftrain.close()
    print("train data saved")
else :
    ftrain = open(conf.train_file, "rb")
    train_data = pickle.load(ftrain)
    ftrain.close()    
    print("train data loaded")    
    
if os.path.isfile(conf.test_file) == False :  
    test_data   = get_data(test_time , conf.days)   
    ftest  = open(conf.test_file , "wb")    
    pickle.dump(test_data, ftest)
    ftest.close()    
    print("test data saved")    
else :
    ftest = open(conf.test_file, "rb")
    test_data  = pickle.load(ftest)
    ftest.close()    
    print("test data loaded")


train_x        = np.array( train_data["x"]       )
train_y        = np.array( train_data["y"]       ) 
train_return   = np.array( train_data["return"]  )
train_ret_std  = np.array( train_data["ret_std"] )
train_shi_jian = np.array( train_data["shi_jian"])
train_code     = np.array( train_data["code"    ])

test_x        = np.array( test_data["x"]       )
test_y        = np.array( test_data["y"]       )
test_return   = np.array(test_data["return"]   )
test_ret_std  = np.array(test_data["ret_std"]  )
test_shi_jian = np.array(test_data["shi_jian"] )
test_code     = np.array(test_data["code"    ] )


learning_rate = 0.001
#Number of images entered into the model
batch_size = 1000
training_iters = int(len(train_y)/batch_size)
display_step = 10

# Network Parameters
#Factors
n_input = 6
#time steps
n_steps = conf.days
n_hidden = 1024
#types of results
n_classes = 2

# tf Graph input
x = tf.placeholder('float',[None, n_steps, n_input])
y = tf.placeholder('float',[None, n_classes])

# # tf Graph input
# x = tf.placeholder("float", [None, n_steps, n_input])
# y = tf.placeholder("float", [None, n_classes])

# Define weights
weights = {
    # Hidden layer weights => 2*n_hidden because of forward + backward cells
    'out': tf.Variable(tf.random_normal([2*n_hidden, n_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([n_classes]))
}

def BiRNN(x, weights, biases):

    # Prepare data shape to match `bidirectional_rnn` function requirements
    # Current data input shape: (batch_size, n_steps, n_input)
    # Required shape: 'n_steps' tensors list of shape (batch_size, n_input)

    # Permuting batch_size and n_steps
    x = tf.transpose(x, [1, 0, 2])
    # Reshape to (n_steps*batch_size, n_input)
    x = tf.reshape(x, [-1, n_input])
    # Split to get a list of 'n_steps' tensors of shape (batch_size, n_input)
    x = tf.split( value = x , num_or_size_splits = n_steps )

    # Define lstm cells with tensorflow
    # Forward direction cell
    lstm_fw_cell = rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    # Backward direction cell
    lstm_bw_cell = rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)

    # Get lstm cell output
    try:
        outputs, _, _ = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x,
                                              dtype=tf.float32)
    except Exception: # Old TensorFlow version only returns outputs not states
        outputs = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x,
                                        dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

pred = BiRNN(x, weights, biases)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

pred_res = tf.argmax(pred,1)

# Initializing the variables
init = tf.global_variables_initializer()

saver = tf.train.Saver()
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    
    filename = "d://bidirectional_rnn_stock_dis.ckpt"
    if os.path.exists(filename+".meta"):
        saver.restore(sess,filename)
        print("restored")
        
    step = 1
    for step in range(50):
        for i in range(training_iters):
            #print(fac.shape)
            #print(ret.shape)
            batch_x = train_x[i*batch_size:(i+1)*batch_size].reshape([batch_size,n_steps,n_input])
            batch_y = train_y[i*batch_size:(i+1)*batch_size].reshape([batch_size,n_classes])
            #print(batch_x.shape)
            #print(batch_y.shape)
            sess.run(optimizer,feed_dict={x:batch_x,y:batch_y})           
            if i % display_step ==0:                
                print(i,'----',training_iters)
                
        loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x,y: batch_y})
        print("Iter " + str(step*batch_size) + ", Minibatch Loss= " +    "{:.6f}".format(loss) + ", Training Accuracy= " +  "{:.5f}".format(acc))
       
#         save_path = saver.save(sess,filename)
#         print("%s saved" %save_path )
    print("Optimization Finished!")   
    # Calculate accuracy for 128 mnist test images
    #test_len = 1280
    
    print("Accuracy in data set")
    test_data  = train_x[:batch_size].reshape([batch_size,n_steps,n_input])
    test_label = train_y[:batch_size].reshape([batch_size,n_classes])
    print("training Accuracy:", sess.run(accuracy, feed_dict={x: test_data, y: test_label}))
    
    print("Accuracy out of data set")
#     test_dataT  = test_x[:batch_size].reshape([batch_size,n_steps,n_input])
#     test_labelT = test_y[:batch_size].reshape([batch_size,n_classes])

    test_dataT  = test_x.reshape([-1,n_steps,n_input])
    test_labelT = test_y.reshape([-1,n_classes])    
    
    predictions ,acc = sess.run([pred_res,accuracy], feed_dict={x: test_dataT, y: test_labelT})
    
    print("Testing Accuracy:",acc )  
    
    f = open('d:/test.csv','w')    
#     for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , test_y , test_code ,test_shi_jian,test_return):
    for pre , test_y_ , test_code_ ,test_return_ in zip(predictions , test_y , test_code ,test_return):
#         f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_ +","+test_shi_jian_ + "\n")
        f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_  + "\n")
    #     print(pre[0] , test_y_ , test_code_ ,test_shi_jian_)    
    f.close()      
    
    
    sess.close()
    
def export_model(sess, saver, signature, model_path, model_version):
    print("Export the model to {}".format(model_path))
    model_exporter = exporter.Exporter(saver)
    model_exporter.init(sess.graph.as_graph_def(),
                        med_graph_signatures=signature)
    model_exporter.export(model_path, tf.constant(model_version), sess)    