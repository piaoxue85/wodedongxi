'''
Created on 2017&#x5E74;3&#x6708;30&#x65E5;

@author: moonlit
'''
import numpy as np 
import tensorflow as tf
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import  pyplot as plt
import cx_Oracle

learn = tf.contrib.learn 

HIDDEN_SIZE       = 30         #lstm中隐藏节点个数
NUM_LAYERS        = 2          #lstm层数
TIMESTEPS         = 120        #循环神经网络的截断长度
TRAINING_STEPS    = 100000     #训练轮数
BATCH_SIZE        = 32         #batch 大小
TRAINING_EXAMPLES = 5000       #训练数据个数
TESTING_EXAMPLES  = 1000       #测试数据个数
SAMPLE_GAP        = 0.01       #采样间隔

def get_stock_data_daily(code):
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()  
    sql = "select price from tb_stock_data_daily where code ='" + code + "' order by shi_jian asc"  
    cr.execute(sql)        
    alldaily =cr.fetchall()
    alldaily = np.array([alldaily],dtype=np.float)
    return alldaily.reshape(-1)
              

def generate_data(seq):
    x = []
    y = []

    #序列的第i项和后面的timesteps -1项合在一起作为输入
    #第i + timesteps项作为输出
    #就是用sin函数前面的timesteps个点信息，预测第i + timesteps个点的函数值
    for i in range(len(seq) - TIMESTEPS - 1) :
        x.append([seq[i:i + TIMESTEPS]] )
        y.append([seq[i + TIMESTEPS]] )
    return np.array(x , dtype= np.float32) , np.array(y,dtype=np.float32)

def lstm_model(X ,y) :

        #使用多层lstm
#         lstm_cell = tf.contrib.rnn.BasicLSTMCell(HIDDEN_SIZE)
#         cell      = tf.contrib.rnn.MultiRNNCell ([lstm_cell] * NUM_LAYERS)
        cell      = tf.contrib.rnn.MultiRNNCell ([tf.contrib.rnn.BasicLSTMCell(HIDDEN_SIZE) for _ in range(NUM_LAYERS)])
        x_        = tf.unstack(X , axis=1)
        
        #使用tensorflow接口将多层的lstm结构连接成rnn网络并计算期向前传播结果。
        output,_ = tf.contrib.rnn.static_rnn(cell , x_ ,dtype=tf.float32)
        
        #本问题只关注最后一个时刻的输出结果，改结果为下一时刻的预测值
        output   = output[-1]
        
        #对lstm网络的输出再做一层全链接并计算损失。
        #这里默认的损失为平均平方差 损失函数
        prediction , loss  = learn.models.linear_regression(output,y)
        
        train_op = tf.contrib.layers.optimize_loss(
                                                    loss, 
                                                    tf.contrib.framework.get_global_step() ,
                                                    optimizer="Adagrad" ,
                                                    learning_rate = 0.1
                                                   )
    
        return prediction , loss , train_op

#建立深层循环网络模型
regressor= learn.Estimator(model_fn = lstm_model)

#用正弦函数生成训练和测试数据集合。

# test_start = TRAINING_EXAMPLES * SAMPLE_GAP
# test_end   = (TRAINING_EXAMPLES + TESTING_EXAMPLES) * SAMPLE_GAP
# train_X, train_y = generate_data(
#                                     np.sin(np.linspace(0         , test_start , TRAINING_EXAMPLES, dtype = np.float32))
#                                 )
# test_X, test_y = generate_data(
#                                     np.sin(np.linspace(test_start, test_end   , TESTING_EXAMPLES, dtype = np.float32))
#                                 )

seq = get_stock_data_daily("sh000001")
train_X, train_y = generate_data( seq[-4800:-240] )
test_X , test_y  = generate_data( seq[-240:] )

# train_X, train_y = generate_data( seq[len(seq)-TRAINING_EXAMPLES -TESTING_EXAMPLES : len(seq)-TESTING_EXAMPLES ] )
# test_X , test_y  = generate_data( seq[len(seq)-TESTING_EXAMPLES +1                 : len(seq)                  ] )



#调用fit函数训练模型
regressor.fit(
                train_X , 
                train_y , 
                batch_size = BATCH_SIZE , 
                steps      = TRAINING_STEPS
             )

#使用训练好的模型对测试数据进行预测
predicted = [[pred] for pred in regressor.predict(test_X)]

print(predicted)

#计算rmse作为评价指标
rmse= np.sqrt(((predicted - test_y)**2).mean(axis=0))
print("Mean Square Err is: %f"%rmse[0])


fig = plt.figure()
plot_predicted = plt.plot(predicted, label= 'predicted')
plot_test = plt.plot(test_y , label='real_sin')
plt.legend([plot_predicted , plot_test] , ['predicted' , 'redal_sin'])
fig.savefig('sin.png')


    
