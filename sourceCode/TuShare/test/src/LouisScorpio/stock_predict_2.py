'''
Created on 2017年9月11日

@author: moonlit
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

#定义常量
rnn_unit=10       #hidden layer units
input_size=7
output_size=1
lr=0.0001         #学习率
#——————————————————导入数据——————————————————————
f=open('./data/dataset_2.csv') 
df=pd.read_csv(f)     #读入股票数据
data=df.iloc[:,2:10].values  #取第3-10列
train = False

def normalized(data = []):
    res   = []
    means = []
    stds  = []
    for d in data :
        mean = np.mean(d)
        std  = np.std(d)
        normalized = (d-mean)/std  #横向标准化
        normalized = normalized.tolist()
        res.append(normalized)
        means.append(mean)
        stds.append(std)
    return np.array(means) ,np.array(stds),np.array(res)

#获取训练集
def get_train_data(batch_size=60,time_step=20,train_begin=0,train_end=5800):
    batch_index=[]
    data_train=data[train_begin:train_end]
    _,_,normalized_train_data = normalized(data_train)
#     normalized_train_data=(data_train.reshape(8,-1)-np.mean(data_train,axis=1))/np.std(data_train,axis=1)  #标准化
#     normalized_train_data = normalized_train_data.reshape(-1,8)
    train_x,train_y=[],[]   #训练集 
    for i in range(len(normalized_train_data)-time_step):
        if i % batch_size==0:
            batch_index.append(i)
        x=normalized_train_data[i:i+time_step,:7]
#         y=normalized_train_data[i:i+time_step,7,np.newaxis]
        y=data_train[i:i+time_step,7,np.newaxis]        
        train_x.append(x.tolist())
        train_y.append(y.tolist())
    batch_index.append((len(normalized_train_data)-time_step))
    return batch_index,train_x,train_y



#获取测试集
def get_test_data(time_step=20,test_begin=5800):
    data_test=data[test_begin:]
#     mean=np.mean(data_test,axis=1)
#     std=np.std(data_test,axis=1)
#     data_test = data_test.reshape(8,-1)
#     normalized_test_data=(data_test-mean)
#     normalized_test_data = normalized_test_data/std  #标准化
#     normalized_test_data = normalized_test_data.reshape(-1,8)
#     print(normalized_test_data.shape)
    mean,std,normalized_test_data = normalized(data_test) 
    size=(len(normalized_test_data)+time_step-1)//time_step  #有size个sample 

    test_x,test_y=[],[]  
    for i in range(size-1):
        x=normalized_test_data[i*time_step:(i+1)*time_step,:7]
#         y=normalized_test_data[i*time_step:(i+1)*time_step,7]
        y=data_test[i*time_step:(i+1)*time_step,7]
        
        test_x.append(x.tolist())
        test_y.extend(y)
    test_x.append((normalized_test_data[(i+1)*time_step: , :7]).tolist())
    test_y.extend((normalized_test_data[(i+1)*time_step: ,  7]).tolist())
    return mean,std,test_x,test_y,data_test[0:,7]

#——————————————————定义神经网络变量——————————————————
#输入层、输出层权重、偏置

weights={
         'in':tf.Variable(tf.random_normal([input_size,rnn_unit])),
         'out':tf.Variable(tf.random_normal([rnn_unit,1]))
        }
biases={
        'in':tf.Variable(tf.constant(0.1,shape=[rnn_unit,])),
        'out':tf.Variable(tf.constant(0.1,shape=[1,]))
       }

#——————————————————定义神经网络变量——————————————————
def lstm(X):     
    batch_size=tf.shape(X)[0]
    time_step=tf.shape(X)[1]
    w_in=weights['in']
    b_in=biases['in']  
    input_=tf.reshape(X,[-1,input_size])  #需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
    input_rnn=tf.matmul(input_,w_in)+b_in
    input_rnn=tf.reshape(input_rnn,[-1,time_step,rnn_unit])  #将tensor转成3维，作为lstm cell的输入
    cell=tf.nn.rnn_cell.BasicLSTMCell(rnn_unit)
    init_state=cell.zero_state(batch_size,dtype=tf.float32)
    output_rnn,final_states=tf.nn.dynamic_rnn(cell, input_rnn,initial_state=init_state, dtype=tf.float32)  #output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
    output=tf.reshape(output_rnn,[-1,rnn_unit]) #作为输出层的输入
    w_out=weights['out']
    b_out=biases['out']
    pred=tf.matmul(output,w_out)+b_out
    return pred,final_states


#——————————————————训练模型——————————————————
def train_lstm(batch_size=5,time_step=15,train_begin=2000,train_end=5800):
    X=tf.placeholder(tf.float32, shape=[None,time_step,input_size])
    Y=tf.placeholder(tf.float32, shape=[None,time_step,output_size])
    batch_index,train_x,train_y=get_train_data(batch_size,time_step,train_begin,train_end)
    pred,_=lstm(X)
    #损失函数
    loss=tf.reduce_mean(tf.square(tf.reshape(pred,[-1])-tf.reshape(Y, [-1])))
    train_op=tf.train.AdamOptimizer(lr).minimize(loss)
    saver=tf.train.Saver(tf.global_variables(),max_to_keep=15)
   
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        #参数恢复
        try :
            #参数恢复            
            saver.restore(sess,"./stock2.model")
            print("已读取存档")
        except:
            pass
         
        #重复训练10000次
        for i in range(2000):
            for step in range(len(batch_index)-1):
                _,loss_=sess.run([train_op,loss],feed_dict={X:train_x[batch_index[step]:batch_index[step+1]],Y:train_y[batch_index[step]:batch_index[step+1]]})
            print(i,loss_)
            
#             if i % 200==0:
#                 print("保存模型：",saver.save(sess,'./stock2.model',global_step=i))
        print("保存模型：",saver.save(sess,'./stock2.model'))

#————————————————预测模型————————————————————
def prediction(time_step=20):
    X=tf.placeholder(tf.float32, shape=[None,time_step,input_size])
    #Y=tf.placeholder(tf.float32, shape=[None,time_step,output_size])
    mean,std,test_x,test_y,org_y=get_test_data(time_step)
    pred,_=lstm(X)     
    saver=tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        #参数恢复
        try :
            #参数恢复            
            saver.restore(sess,"./stock2.model")
            print("已读取存档")
        except:
            return 
        
        test_predict=[]
        
        for step in range(len(test_x)-1):
            prob=sess.run(pred,feed_dict={X:[test_x[step]]})   
            predict=prob.reshape((-1))
            test_predict.extend(predict)

        print(len(test_x),len(test_y),len(test_predict),len(std),len(mean))
         
#             y_       = []
#             predict_ = []
        
#             for y,pre,s,m in zip(test_y,test_predict,std,mean) :
#                 Y   = y * s + m 
#                 Pre = pre * s + m                 
#                 y_.append(Y)
#                 predict_.append(Pre) 
            
#             test_y = np.array(y_)
#             test_predict = np.array(predict_)
            
#             test_y=np.array(test_y)*std+mean                    
#             test_predict=np.array(test_predict)*std[:len(test_predict)]+mean[:len(test_predict)]
        test_predict = np.array(test_predict)
        acc=np.average(np.abs(test_predict-test_y[:len(test_predict)])/test_y[:len(test_predict)])  #偏差
        print(len(test_x),len(test_y),len(test_predict),len(std),len(mean))
        print("acc:" ,acc)
        #以折线图表示结果
        plt.figure()
        plt.plot(list(range(len(test_predict))), test_predict, color='b')
        plt.plot(list(range(len(test_y))), test_y,  color='r')
#             plt.plot(list(range(len(org_y))), org_y,  color='y')
        plt.show()
        
if train :    
    train_lstm()
else :
    prediction() 
    
print("end")