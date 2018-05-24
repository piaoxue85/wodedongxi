'''
Created on 2017年4月6日
https://uqer.io/community/share/586dec2e89e3ba0048efdc22
@author: moonlit
结构 5层卷积 - 3层全连接 使用SVM 取代softmax进行预测； 计算量有点大，大家看看即可。 卷积网络结构可以参考AlexNet 话说我是先写完代码才看的AlexNet的论文和博客，这是恶习，要改！！
'''
# %%time
import numpy as np
import matplotlib.pylab as plt
# %matplotlib inline
import tensorflow as tf
from sklearn.cross_validation import train_test_split

fac = np.load('d:/fac16.npy').astype(np.float32)
ret = np.load('d:/ret16.npy').astype(np.float32)
print(fac.shape)
print(ret.shape)
train_X, test_X, train_Y, test_Y = train_test_split(fac, ret, test_size= 0.4)
print ('训练集/总数据集 %.3f'%(len(train_X)/len(fac)))

# Parameters
learning_rate = 0.001 # 学习速率，
training_iters = 20 # 训练次数
batch_size = 16 # 每次计算数量 批次大小
display_step = 10 # 显示步长
# Network Parameters
n_input = 40*17 # 40天×17多因子
n_classes = 7 # 根据涨跌幅度分成7类别
# 这里注意要使用 one-hot格式，也就是如果分类如3类 -1,0,1 则需要3列来表达这个分类结果，3类是-1 0 1 然后是哪类，哪类那一行为1 否则为0
dropout = 0.5# Dropout, probability to keep units
# tensorflow 图 Graph 输入 input，这里的占位符均为输入
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) #dropout (keep probability)

# 2 层 CNN 提取特征向量
def CNN_Net_two(x,weights,biases,dropout=0.8,m=1):
    # layer hidden 1
    x = tf.reshape(x, shape=[-1,40,17,1])
    x = tf.nn.conv2d(x, weights['wc1'], strides=[1,m,m,1],padding='SAME')
    x = tf.nn.bias_add(x,biases['bc1'])
    x = tf.nn.relu(x)
    x = tf.nn.local_response_normalization(x, depth_radius=5, bias=1.0, alpha=0.001/9.0)
    x = tf.nn.dropout(x,0.3)
    
    # layer hidden 2
    x = tf.nn.conv2d(x, weights['wc2'], strides=[1,m,m,1],padding='SAME')
    x = tf.nn.bias_add(x,biases['bc2'])
    x = tf.nn.relu(x)
    x = tf.nn.local_response_normalization(x, depth_radius=5, bias=1.0, alpha=0.001/9.0)
    x = tf.nn.dropout(x,0.3)
    
    # layer hidden 3
    x = tf.nn.conv2d(x, weights['wc3'], strides=[1,m,m,1],padding='SAME')
    x = tf.nn.bias_add(x,biases['bc3'])
    x = tf.nn.relu(x)
    x = tf.nn.local_response_normalization(x, depth_radius=5, bias=1.0, alpha=0.001/9.0)
    x = tf.nn.dropout(x,0.3)
    
    # layer hidden 4
    x = tf.nn.conv2d(x, weights['wc4'], strides=[1,m,m,1],padding='SAME')
    x = tf.nn.bias_add(x,biases['bc4'])
    x = tf.nn.relu(x)
    x = tf.nn.local_response_normalization(x, depth_radius=5, bias=1.0, alpha=0.001/9.0)
    x = tf.nn.dropout(x,0.3)
    
    # layer hidden 5
    x = tf.nn.conv2d(x, weights['wc5'], strides=[1,m,m,1],padding='SAME')
    x = tf.nn.bias_add(x,biases['bc5'])
    x = tf.nn.relu(x)
    x = tf.nn.local_response_normalization(x, depth_radius=5, bias=1.0, alpha=0.001/9.0)
    x = tf.nn.dropout(x,0.3)
    #print (x.get_shape().as_list())
    
    # 全连接层1
    x = tf.reshape(x,[-1,weights['wd1'].get_shape().as_list()[0]])
    x = tf.add(tf.matmul(x,weights['wd1']),biases['bd1'])
    x = tf.nn.relu(x)
    x = tf.nn.dropout(x,dropout)
    #print (x.get_shape().as_list())
    
    # 全连接层2
    x = tf.reshape(x,[-1,weights['wd2'].get_shape().as_list()[0]])
    x = tf.add(tf.matmul(x,weights['wd2']),biases['bd2'])
    x = tf.nn.relu(x)
    x = tf.nn.dropout(x,dropout)
    #print (x.get_shape().as_list())
    
    # 全连接层3
    x = tf.reshape(x,[-1,weights['wd3'].get_shape().as_list()[0]])
    x = tf.add(tf.matmul(x,weights['wd3']),biases['bd3'])
    x = tf.nn.relu(x)
    x = tf.nn.dropout(x,dropout)
    print (x.get_shape().as_list())
    
    
    t = tf.add(tf.matmul(x,weights['out']),biases['out'])
    print (t.get_shape().as_list())
    # 返回两个数值，t用于softmax分类，x用于提取CNN处理的数据，也就是经过卷积处理的特征向量。
    return t,x

# Store layers weight & bias
weights = {
    'wc1': tf.Variable(tf.random_normal([10, 5, 1, 64])),
    'wc2': tf.Variable(tf.random_normal([10, 5, 64, 128])),
    'wc3': tf.Variable(tf.random_normal([10, 5, 128, 256])),
    'wc4': tf.Variable(tf.random_normal([10, 5, 256, 512])),
    'wc5': tf.Variable(tf.random_normal([10, 5, 512, 1024])),
    'wd1': tf.Variable(tf.random_normal([40*17*1024, 1024])),
    'wd2': tf.Variable(tf.random_normal([1024, 256])),
    'wd3': tf.Variable(tf.random_normal([256, 32])),
    'out': tf.Variable(tf.random_normal([32, n_classes]))
}

biases = {
    'bc1': tf.Variable(tf.random_normal([64])),
    'bc2': tf.Variable(tf.random_normal([128])),
    'bc3': tf.Variable(tf.random_normal([256])),
    'bc4': tf.Variable(tf.random_normal([512])),
    'bc5': tf.Variable(tf.random_normal([1024])),
    'bd1': tf.Variable(tf.random_normal([1024])),
    'bd2': tf.Variable(tf.random_normal([256])),
    'bd3': tf.Variable(tf.random_normal([32])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}
# 模型优化
pred,tmp = CNN_Net_two(x,weights,biases,dropout=keep_prob)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred,labels=y))
print(cost)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
correct_pred = tf.equal(tf.argmax(pred,1),tf.arg_max(y,1))
# tf.argmax(input,axis=None) 由于标签的数据格式是 -1 0 1 3列，该语句是表示返回值最大也就是1的索引，两个索引相同则是预测正确。
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
# 更改数据格式，降低均值
init = tf.global_variables_initializer()

saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(init)
    # for step in range(300):
    for step in range(1):
        trl=int(len(train_X)/batch_size)
        for i in range(trl):
            print (i,'--',trl)
            batch_x = train_X[i*batch_size:(i+1)*batch_size]
            batch_y = train_Y[i*batch_size:(i+1)*batch_size]
            sess.run(optimizer,feed_dict={x:batch_x,y:batch_y,keep_prob:0.5})
        loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x,y: batch_y,keep_prob: 1.})
        print("Iter " + str(step*batch_size) + ", Minibatch Loss= " + \
                  "{:.6f}".format(loss) + ", Training Accuracy= " + \
                  "{:.5f}".format(acc))
    save_path = saver.save(sess,'F:/Quotes/test_var.ckpt')
    print ('保持变量')
    print("Optimization Finished!")   
    sess.close()
    
saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(init)
    saver.restore(sess,'F:/Quotes/test_var.ckpt')
    trainX_Convolution = sess.run(tmp, feed_dict={x:train_X, keep_prob:1.})
    # 经过卷积处理的特征向量
    nn_score = sess.run(accuracy,feed_dict={x:train_X, keep_prob:1.})
    nn_score1 = sess.run(accuracy,feed_dict={x:test_X, keep_prob:1.})
    print(nn_score,'---',nn_score1)
    sess.close()
    
        # train_Y 
ol_train_Y = []
for i in range(len(train_Y)):
    t = train_Y[i]
    arg = np.argmax(t)
    ol_train_Y.append(arg)
    
# softmax_pred 
ol_softmax_pred = []
for i in range(len(softmax_pred)):
    t = softmax_pred [i]
    arg = np.argmax(t)
    ol_softmax_pred.append(arg)
    
from sklearn.svm import SVC 

clf = SVC(C=0.9,gamma=1.0,decision_function_shape='ovo') 
clf.fit(trainX_Convolution, ol_train_Y) 
c = clf.predict(trainX_Convolution) 
print ('CNN预测',(np.corrcoef(a,c)[0][1]))    