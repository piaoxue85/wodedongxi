'''
Created on 2017年1月23日

@author: moonlit
'''


#!/usr/bin/env python

import tensorflow as tf
import numpy as np


# Prepare train data
train_X = np.linspace(-1, 1, 100)
train_Y = 2 * train_X + np.random.randn(*train_X.shape) * 0.33 + 10

# print(train_X.shape)
# print(train_X)
# print(train_Y.shape)
# print(train_Y)
# 
# print(zip(train_X, train_Y))


# Define the model
X = tf.placeholder("float")
Y = tf.placeholder("float")
w = tf.Variable(0.0, name="weight")
b = tf.Variable(0.0, name="bias")
c = tf.Variable(0.0, name="test")

# y_ = tf.placeholder("float")
#loss = -tf.reduce_sum(y_*tf.log(Y))
loss = tf.square(Y - tf.multiply(X, w) - b)
train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

# Create session to run
with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())

    epoch = 1
    for i in range(10):
        for (x, y) in zip(train_X, train_Y):
            epoch += 1            
#             sess.run(train_op)
            sess.run([b, w,train_op], feed_dict={X: x,Y: y})
#             print(sess.run([b, w,train_op], feed_dict={X: x,Y: y}))
#             _, w_value, b_value = sess.run([train_op, w, b],
#                                            feed_dict={X: x,
#                                                       Y: y})             
#     print("Epoch: {}, w_value: {}, b_value: {}".format(epoch, w_value, b_value))
    print(sess.run(w))
    print(sess.run(b))   