'''
Created on 2017年3月13日

@author: moonlit
'''

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf 


mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)

in_units = 784
h1_units = 300 

#定义权重和偏置
#w1 b1 隐含层的权重和偏置，权重初始化为截断的正态分布，标准差为0.1，
#实战70页
W1 = tf.Variable(tf.truncated_normal([in_units,h1_units],
                                     stddev=0.1
                                     )
                 )
sess = tf.InteractiveSession()

#b1全部赋值为0
b1 = tf.Variable(tf.zeros([h1_units]))
W2 = tf.Variable(tf.zeros([h1_units,10]))
b2 = tf.Variable(tf.zeros([10]))

#定义输入
x = tf.placeholder(tf.float32, [None , in_units])
keep_prob = tf.placeholder(tf.float32)

hidden1 = tf.nn.relu(tf.matmul(x,W1) + b1)
hiddend1_drop = tf.nn.dropout(hidden1,keep_prob)
y = tf.nn.softmax(tf.matmul( hiddend1_drop , W2 )+b2)

#计算损失，优化损失
y_= tf.placeholder(tf.float32 , [None , 10])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(
                                                y_*tf.log(y) ,
                                                reduction_indices = [1]
                                              )
                               )
train_step = tf.train.AdagradOptimizer(0.3).minimize(cross_entropy)

tf.global_variables_initializer().run()
for i in range(3000):
    batch_xs , batch_ys = mnist.train.next_batch(100)
    train_step.run( {x:batch_xs , y_:batch_ys , keep_prob:0.75} )
    
correct_prediction = tf.equal(
                                tf.argmax( y , 1 ),
                                tf.argmax( y_, 1 )
                              )
accuracy = tf.reduce_mean(
                            tf.cast(
                                    correct_prediction , 
                                    tf.float32
                                    )
                          )
print(
        accuracy.eval(
                        {x:mnist.test.images ,y_:mnist.test.labels , keep_prob : 1.0}
                      )
      )
