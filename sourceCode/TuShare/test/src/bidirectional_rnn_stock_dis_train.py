
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
from tensorflow.contrib.session_bundle import exporter


days = 5
# df_sh = ts.get_sz50s()['code']
df_sh = gsd.get_code_list_by_classification(classification="上证50成份股")['code']

# print(len(df_sh))
#train dataset
fac = []
ret = []
#test dataset
facT = []
retT = []
for ishare in df_sh:    
    df = gsd.get_stock_data_daily_df(ishare)
    
    num = math.floor(len(df)/days)*days+1-days*2
    
    newfac = gsd.getDataX(df , num = num , days = days )
    newret = gsd.getDataY(df , num = num , days = days )
#     if len(newfac)/len(newret) != 5 :
#         print(ishare)
#         print(num)
#         print(len(newfac))
#         print(len(newret))
    #fac.append(newfac)
    for i in range(len(newfac)):
        fac.append(newfac[i])
    for i in range(len(newret)):
        ret.append(newret[i])

#     newfacT = gsd.getDataX(df=df,num = math.floor(len(df)/days)*days+1                  )
#     newretT = gsd.getDataY(df=df,num = math.floor(len(df)/days)*days+1,days = -1 * days )
    newfacT = gsd.getDataX(df=df,num = num, days = days )
    newretT = gsd.getDataY(df=df,num = num, days = days )
    #fac.append(newfac)
    for i in range(len(newfacT)):
        facT.append(newfacT[i])
    for i in range(len(newretT)):
        retT.append(newretT[i])


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
ret = np.array(ret)

newfT = []
newfaT = []
for i in range(len(facT)):
    if((i+1)%5!=0):
        newfT.append(facT[i])
    else:
        newfT.append(facT[i])
        newfaT.append(newfT)
        newfT = []
facT = np.array(newfaT)
retT = np.array(retT)

print("**")
print(len(facT))
print(len(retT))
print("**")

fac = np.array(fac)
ret = np.array(ret)

learning_rate = 0.001
#Number of images entered into the model
batch_size = 10
training_iters = int(fac.shape[0]/batch_size)
display_step = 10

# Network Parameters
#Factors
n_input = 32
#time steps
n_steps = 5
n_hidden = 1024
#types of results
n_classes = 3

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

# Initializing the variables
init = tf.global_variables_initializer()

saver = tf.train.Saver()
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    
    filename = "d:/bidirectional_rnn_stock_dis.ckpt"
    if os.path.exists(filename+".meta"):
        saver.restore(sess,filename)
        print("restored")
        
    step = 1
    for step in range(60):
        for i in range(int(len(fac)/batch_size)):
            #print(fac.shape)
            #print(ret.shape)
            batch_x = fac[i*batch_size:(i+1)*batch_size].reshape([batch_size,n_steps,n_input])
            batch_y = ret[i*batch_size:(i+1)*batch_size].reshape([batch_size,n_classes])
            #print(batch_x.shape)
            #print(batch_y.shape)
            sess.run(optimizer,feed_dict={x:batch_x,y:batch_y})           
            if i % display_step ==0:                
                print(i,'----',(int(len(fac)/batch_size)))
                
        loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x,y: batch_y})
        print("Iter " + str(step*batch_size) + ", Minibatch Loss= " +    "{:.6f}".format(loss) + ", Training Accuracy= " +  "{:.5f}".format(acc))
       
        save_path = saver.save(sess,filename)
        print("%s saved" %save_path )
    print("Optimization Finished!")   
    # Calculate accuracy for 128 mnist test images
    #test_len = 1280
    
    print("Accuracy in data set")
    test_data = fac[:batch_size].reshape([batch_size,n_steps,n_input])
    test_label = ret[:batch_size].reshape([batch_size,n_classes])
    print("Testing Accuracy:",         sess.run(accuracy, feed_dict={x: test_data, y: test_label}))
    
    print("Accuracy out of data set")
    test_dataT = facT[:batch_size].reshape([batch_size,n_steps,n_input])
    test_labelT = retT[:batch_size].reshape([batch_size,n_classes])
    print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: test_dataT, y: test_labelT}))
    
    sess.close()
    
def export_model(sess, saver, signature, model_path, model_version):
    print("Export the model to {}".format(model_path))
    model_exporter = exporter.Exporter(saver)
    model_exporter.init(sess.graph.as_graph_def(),
                        med_graph_signatures=signature)
    model_exporter.export(model_path, tf.constant(model_version), sess)    