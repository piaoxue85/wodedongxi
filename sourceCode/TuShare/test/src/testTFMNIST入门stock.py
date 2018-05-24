'''
Created on 2017年1月20日

@author: moonlit
'''
import input_data
import tensorflow as tf
import numpy as np
from Cython.Plex.Actions import Begin
from numpy import int


def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
                                       serialized_example,
                                       features={
                                                 "label": tf.FixedLenFeature([], tf.float32),
                                                 "features": tf.FixedLenFeature([4096], tf.float32),
                                                 }
                                       )
    label = features["label"]
    features = features["features"]
    return label,features

# mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(dtype="float",shape= [None, 4095] ,name="x" )
W = tf.Variable(tf.zeros([4095,3]))
b = tf.Variable(tf.zeros([3]))
y = tf.nn.softmax(tf.matmul(x,W) + b)             #计算答案
y_ = tf.placeholder("float", [None,3])           #标准答案          
cross_entropy = -tf.reduce_sum(y_*tf.log(y))

train_step = tf.train.AdagradOptimizer(0.01).minimize(cross_entropy)

filename_queue = tf.train.string_input_producer(
                                                ["./StockTrain.csv.tfrecords"]
                                                #num_epochs=100
                                                )
label, features = read_and_decode(filename_queue)
print(label)
batch_labels, batch_features = tf.train.shuffle_batch(
                                                      [label, features],
                                                      batch_size=100,
                                                      num_threads=1,
                                                      capacity=150,
                                                      min_after_dequeue=100
                                                      )  

init = tf.global_variables_initializer()
sess = tf.Session()
# sess.run(init)
# coord = tf.train.Coordinator()
# threads = tf.train.start_queue_runners(coord=coord, sess=sess)

sess.run(init)
# threads = tf.train.start_queue_runners(sess=sess)


inference_data = np.genfromtxt("./StockTrain.csv", delimiter=",")

begin = 0 
end =50
irange = 100000

for i in range(irange):
    batch_features = inference_data[begin:end, 0:4095]
    batch_labels = inference_data[begin:end, 4096]
    batch_y = np.zeros([len(batch_labels),3],int)
    
    for ii in range(len(batch_labels)) :
        batch_y[ ii ][ np.int( batch_labels[ii]) ] = 1    
           
    sess.run(train_step, feed_dict={x: batch_features, y_: batch_y})
    begin = int(begin + 50)
    end = int(end + 50)
    if end > len(inference_data) :
        begin = 0 
        end =50  

# Read TFRecords files for training   

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

test_data = np.genfromtxt("./StockTest.csv", delimiter=",")
batch_features = inference_data[:, 0:4095]
batch_labels = inference_data[:, 4096]

batch_y = np.zeros([len(batch_labels),3],int)
for ii in range(len(batch_labels)) :
    batch_y[ ii ][ np.int( batch_labels[ii]) ] = 1
 
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(sess.run(accuracy, feed_dict={x: batch_features, y_: batch_y}))  