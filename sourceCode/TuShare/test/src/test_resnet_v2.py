import tensorflow as tf
from tensorflow.contrib.slim.nets import resnet_v2
from tensorflow.contrib.slim.python.slim.nets.resnet_utils import resnet_arg_scope
from alexnet_benchmark import time_tensorflow_run_

slim = tf.contrib.slim

batch_size = 32 
height , width = 1,1
inputs = tf.random_uniform((batch_size , height , width ,1))

with slim.arg_scope(resnet_arg_scope(is_training=False)) :
    net,enpoints = resnet_v2.resnet_v2_152(inputs, 3)
#     print(net)
    
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
num_batches = 1 
time_tensorflow_run_(sess , net , "Forward",num_batches = num_batches)
