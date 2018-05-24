
from __future__ import division
from __future__ import print_function  
import numpy as np
# import pandas as pd
# import matplotlib.pylab as plt
# import seaborn as sns
import tensorflow as tf
from tensorflow.contrib import rnn
# import tushare as ts
import getStockData as gsd
import math
import os
import cx_Oracle


# Network Parameters
#Factors
n_input = 32
#time steps
n_steps = 5
n_hidden = 1024
#types of results
n_classes = 3

days = 5

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

def testOneByOne(code=[],starttime='' , endtime='',datatype='sz50'):
    result = -1
    for ishare in code:    
        #train dataset
        fac = []
        #ret = []
        #test dataset
        #facT = []
        #retT = []    
        df = gsd.get_stock_data_daily_df_time(ishare,start=starttime , end=endtime)
        #df = gsd.get_stock_data_daily_df_daysago_(ishare,daysago=365*4 , endtime = endtime)
        #num = math.floor(len(df)/days)*days+1-days*2
        
        newfac = gsd.getDataXforTest(df , days = days )
        #newret = gsd.getDataY(df , num = num , days = days )
    #     if len(newfac)/len(newret) != 5 :
    #         print(ishare)
    #         print(num)
    #         print(len(newfac))
    #         print(len(newret))
        #fac.append(newfac)
        for i in range(len(newfac)):
            fac.append(newfac[i])
        #for i in range(len(newret)):
        #   ret.append(newret[i])
            
        #temp = np.array(fac)
        #print(temp.shape)
    
    #     newfacT = gsd.getDataX(df=df,num = math.floor(len(df)/days)*days+1                  )
    #     newretT = gsd.getDataY(df=df,num = math.floor(len(df)/days)*days+1,days = -1 * days )
#         newfacT = gsd.getDataX(df=df,num = num , days = days )
#         newretT = gsd.getDataY(df=df,num = num , days = days )
#         #fac.append(newfac)
#         for i in range(len(newfacT)):
#             facT.append(newfacT[i])
#         for i in range(len(newretT)):
#             retT.append(newretT[i])
    
    
    newf = []
    newfa = []
    for i in range(len(fac)):
        if((i+1)%days!=0):
            newf.append(fac[i])
        else:
            newf.append(fac[i])
            newfa.append(newf)
            newf = []
            
    fac = np.array(newfa)
    #ret = np.array(ret)
    
    fac = np.array(fac)
    #ret = np.array(ret)
   
    #learning_rate = 0.001
    #Number of images entered into the model
    batch_size = 1
    #training_iters = int(fac.shape[0]/batch_size)
    #display_step = 10    
    
    graph = tf.Graph()
    with graph.as_default() :
        # tf Graph input
        x = tf.placeholder('float',[None, n_steps, n_input])
        #y = tf.placeholder('float',[None, n_classes])
        
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
    
        pred = BiRNN(x, weights, biases)
        
        # Define loss and optimizer
        #cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
        #optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
        
        # Evaluate model
        #correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
        #accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        test_Y_pred = tf.nn.softmax(pred)
        test_Y_pred=tf.argmax( test_Y_pred , 1)
        
        # Initializing the variables
        init = tf.global_variables_initializer()
        
        saver = tf.train.Saver()
        # Launch the graph
        with tf.Session() as sess:
            sess.run(init)
            
            if datatype == 'sz50' :
                filename = "D:/stockcheckpoint/sz50/sz50.ckpt"
            else :
                filename = "D:/stockcheckpoint/others/"+code[0]+".ckpt"
                
            if os.path.exists(filename+".meta"):
                saver.restore(sess,filename)
                print(filename + "  restored")
            else :
                return -1
                        
            for step in range(1):
                for i in range(int(len(fac)/batch_size)):
                    #print(fac.shape)
                    #print(ret.shape)
                    batch_x = fac[i*batch_size:(i+1)*batch_size].reshape([batch_size,n_steps,n_input])
                    #batch_y = ret[i*batch_size:(i+1)*batch_size].reshape([batch_size,n_classes])
                    #print(batch_x.shape)
                    #print(batch_y.shape)
                    result = sess.run(test_Y_pred,feed_dict={x:batch_x})
                    #print("pre_y = " )
                    #print( result )         
      
            sess.close()
    return result 

def recordRediction(code='',pre=999,endtime=''): 
    sql  = "insert into tb_stock_predict " 
    sql += "(                            "
    sql += "  seq      ,                 "
    sql += "  code     ,                 "
    sql += "  end_time ,                 "
    sql += "  predict                    "
    sql += ")                            "
    sql += "values                       "
    sql += "(                            "
    sql += "   seq_stock_predict.nextval , "
    sql += "   '" + code + "' ,"
    sql += "   to_date( '" + endtime + " 15:00:00','yyyy-mm-dd hh24:mi:ss') , "
    sql += "   " + str(pre) + " "
    sql += ")"
    conn = cx_Oracle.connect('c##stock','didierg160','myoracle')    
    cursor = conn.cursor ()        
    cursor.execute (str(sql))   
    conn.commit()        
    cursor.close ()  
    conn.close ()   
    

# starttime = '2017-04-10'
# endtime   = '2017-04-14'

# starttime = '2015-10-19'
# endtime   = '2015-10-23'

starttime = '2016-12-19'
endtime   = '2016-12-23'

'''
df_sh = gsd.get_code_list_by_classification(classification="上证50成份股")['code']
df_sh = df_sh.reshape( -1 , 1 )
for c in df_sh :
    result = testOneByOne( c , starttime,endtime,datatype='sz50') 
    if result == -1 :
        continue
    recordRediction(code=c[0],pre=result[0],endtime=endtime)
    print((str(c[0]) + '   ' + str(result[0])))
'''  

df_sh = gsd.get_code_list_not_in_sz50(daysago=365*4 )['code']
#df_sh = np.array( ['002019','002017','002002','000619','000567'])
# df_sh = np.array( ['600021','600161','600186'])
df_sh = np.array( ['600000'])
df_sh = df_sh.reshape(-1 , 1)

weeks = gsd.get_week()
weeks = np.array(weeks)
#weeks = np.array([['2017-03-20','2017-03-24']])
#weeks = np.array([['2017-04-10','2017-04-14']])

for c in df_sh :
    for week in weeks :
        result = testOneByOne( c , week[0],week[1],datatype='sz50') 
        if result == -1 :
            continue    
        recordRediction(code=c[0],pre=result[0],endtime=week[1])
        print((str(c[0]) + '   ' + str(result[0])))

