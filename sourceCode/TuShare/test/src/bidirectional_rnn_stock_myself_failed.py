
from __future__ import division
from __future__ import print_function  
import numpy as np
# import pandas as pd
# import matplotlib.pylab as plt
# import seaborn as sns
import tensorflow as tf
from tensorflow.contrib import rnn
import tushare as ts
import getStockData_bak20170412 as gsd
import math

days = 5
df_sh = ts.get_sz50s()['code']

#train dataset
fac = []
ret = []
#test dataset
facT = []
retT = []
for ishare in df_sh:    
    df = gsd.get_stock_data_daily_df(ishare)
    
    num = math.floor(len(df)/days)*days-days*2
    
    newfac,newret = gsd.getDataXY(df , num = num , days = -1 * days)
    
    #if len(newfac)/len(newret) != 5 :
    #    print(ishare)
    #    print(num)
    #    print(len(newfac))
    #    print(len(newret))
    #print(len(newfac))
    #print(len(newret))    
    #fac.append(newfac)
    for i in range(len(newfac)):
        fac.append(newfac[i])
    for i in range(len(newret)):
        ret.append(newret[i])
      
    #print(len(df))      
    #print(fac)
    #print(ret)
            
    newfacT ,newretT = gsd.getDataXY(df , num = num , days = -1 * days)
     
    #fac.append(newfac)
    for i in range(len(newfacT)):
        facT.append(newfacT[i])
    for i in range(len(newretT)):
        retT.append(newretT[i])


fac  = np.array(fac)
ret  = np.array(ret)
facT = np.array(facT)
retT = np.array(retT)

print(fac.shape)
print(ret.shape)
print(facT.shape)
print(retT.shape)

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

# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    step = 1
    print(len(fac))
    print(len(ret))
    for step in range(10):
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