'''
Created on 2017年3月15日

@author: moonlit
'''
# git clone https://github.com/tensorflow/models.git
import cifar10
import cifar10_input
import tensorflow as tf
import numpy as np
import time


max_steps  = 3000 
batch_size = 128
data_dir   = 'D:/tmp/cifar10_data/cifar-10-batches-bin/'

def variable_with_weight_loss(shape , stddev , w1):
    var = tf.Variable(tf.truncated_normal(shape, stddev=stddev))
    
    if w1 is not None :
        #给weight 增加 L2_loss用于避免overfit，L2正则让特征权重不过大，L1是置为0 造成稀疏
        #实战86
        weight_loss = tf.multiply(tf.nn.l2_loss(var), w1, name='weight_loss')
        #add 到一个collection，计算总体loss 会用到
        tf.add_to_collection('losses' , weight_loss)
    
    return var

cifar10.maybe_download_and_extract() 
images_train,labels_train = cifar10_input.distorted_inputs( data_dir = data_dir , batch_size = batch_size )
images_test , labels_test = cifar10_input.inputs(
                                                    eval_data = True ,
                                                    data_dir = data_dir ,
                                                    batch_size=batch_size 
                                                )

image_holder = tf.placeholder(tf.float32, [batch_size , 24,24,3])
label_holder = tf.placeholder(tf.int32 , [batch_size])

#卷积1 ， maxpool 步长不一致，可以增加数据丰富性。并使用lrn，配合relu减少错误率
#不对这层的weight进行L2正则，所以w1=0
#实战88
weight1 = variable_with_weight_loss(shape=[5,5,3,64], stddev = 5e-2 , w1 = 0.0 )
kernel1 = tf.nn.conv2d(image_holder, weight1 , [1,1,1,1 ], padding='SAME')
bias1   = tf.Variable(tf.constant(0.0 , shape = [64]))
conv1   = tf.nn.relu(tf.nn.bias_add(kernel1,bias1))
pool1   = tf.nn.max_pool(conv1 , ksize=[1,3,3,1] , strides = [1,2,2,1] ,padding ='SAME')
norm1   = tf.nn.lrn(pool1,4,bias = 1.0 , alpha = 0.001/9.0 , beta = 0.75)

#卷积2 bias 初始化为0.1。
#先进行LRN层处理，在使用maxpool
weight2 = variable_with_weight_loss(shape=[5,5,64,64], stddev=5e-2, w1=0.0)
kernel2 = tf.nn.conv2d(norm1,weight2,[1,1,1,1],padding='SAME')
bias2   = tf.Variable(tf.constant(0.1 , shape=[64]))
conv2   = tf.nn.relu(tf.nn.bias_add(kernel2,bias2))
norm2   = tf.nn.lrn(conv2,4,bias=1.0 , alpha=0.001/9.0 , beta=0.75)
pool2   = tf.nn.max_pool(norm2,ksize=[1,3,3,1],strides=[1,2,2,1] , padding='SAME')

#全连接层
#希望这层不要过拟合，所以设置了weight loss 为 0.04,让这层的所有参数都被L2正则约束。最后用ReLU激活函数进行非线性化
reshape = tf.reshape(pool2, [batch_size,-1])
dim     = reshape.get_shape()[1].value
weight3 = variable_with_weight_loss(shape=[dim , 384], stddev=0.04, w1=0.004)
bias3   = tf.Variable(tf.constant(0.1 , shape=[384]))
local3  = tf.nn.relu(tf.matmul(reshape , weight3) + bias3)

#又一个全连接层，隐含节点数量减少一半
weight4 = variable_with_weight_loss(shape=[384,192], stddev=0.04, w1=0.004)
bias4   = tf.Variable(tf.constant(0.1,shape=[192]))
local4  = tf.nn.relu(tf.matmul(local3 ,weight4) + bias4)

#最后一层,不计入L2正则
#注意，这里没有像往常使用了softmax ， 是因为把softmax 放在了计算loss部分，所以不需要对inference 输出进行softmax 就可以获得最终分类
#（直接比较输出各类数值大小即可），计算softmax主要是为了计算loss，因此softmax整合到后面是合适的
weight5 = variable_with_weight_loss(shape = [192,10], stddev=1/192.0, w1=0.0)
bias5   = tf.Variable(tf.constant(0.0 , shape=[10]))
logits  = tf.add(tf.matmul(local4,weight5), bias5)             #模型输出结果

#计算cnn的loss，把softmax 和 cross entropy loss 计算合并
#使用tf.reduce_mean 对cross entropy 计算均值
#最后使用tf.add_n 将整体的losses 的collection中的全部loss求和得到最终loss，包括cross entropy loss,还包括了后两个全连接层中的weight的L2 loss
def loss(logits , labels):
    labels = tf.cast(labels, tf.int64)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
                                                                    logits = logits ,
                                                                    labels = labels ,
                                                                    name   = 'cross_entropy_per_example'
                                                                   )
    print(logits)
    print(labels)
    corss_entropy_mean = tf.reduce_mean(cross_entropy, name='cross_entropy')
    tf.add_to_collection('losses' , corss_entropy_mean)
    return tf.add_n(tf.get_collection('losses'), name = 'total_loss')

#接着将logits节点和label_holder传入获得最终loss
loss = loss(logits , label_holder)

train_op = tf.train.AdamOptimizer(1e-3).minimize(loss)

#使用in top k 输出结果中top k 准确率
#实战91
top_k_op = tf.nn.in_top_k(logits, label_holder , 1 )

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

#启动图片数据增强线程队列  ， 使用16线程
tf.train.start_queue_runners()

#正式开始训练
for step in range(max_steps) :
    start_time = time.time()
    image_batch , label_batch = sess.run([images_train , labels_train])
    _, loss_value = sess.run(
                             [train_op,loss],
                             feed_dict={
                                        image_holder : image_batch ,
                                        label_holder : label_batch                                         
                                        }
                            )
    duration = time.time() - start_time
    
    if step %10 == 0 :
        example_per_sec = batch_size / duration
        sec_per_batch   = float(duration)
        
        format_str = ('step%d , loss=%.2f (%.1f examples/sec; %.3f sec/batch)')
        print(format_str %(step , loss_value , example_per_sec , sec_per_batch))
        
import math        
num_examples = 10000
num_iter     = int(math.ceil(num_examples / batch_size))
true_count   = 0 
total_sample_count = num_iter * batch_size
step = 0 

while step < num_iter:
    image_batch , label_batch = sess.run ( [images_test , labels_test])
    
#     top_k_op.run([top_k_op] , feed_dict={
#                                                    image_holder : image_batch , 
#                                                    label_holder : label_batch
#                                                    }
#                  )
    
    predictions = sess.run([top_k_op] , feed_dict={
                                                   image_holder : image_batch , 
                                                   label_holder : label_batch
                                                   }
                           )
    
    true_count += np.sum(predictions)
    step +=1
    
precision = true_count / total_sample_count
print('precision @ 1 = %.3f' % precision)
    