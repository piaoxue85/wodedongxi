'''
Created on 2017年3月13日

@author: moonlit
'''
import numpy as np
import tensorflow as tf 

def xavier_init (fan_in , fan_out , constant = 1):
    low  = -constant * np.sqrt(6.0 / (fan_in + fan_out))
    high =  constant * np.sqrt(6.0 / (fan_in + fan_out))
    return tf.random_uniform((fan_in , fan_out ), 
                              minval = low, 
                              maxval = high, 
                              dtype  =tf.float32
                            )
    
class AdditiveGaussianNoiseAutoEncoder(object):
    def __init__(self,
                 n_input , 
                 n_hidden ,
                 transfer_function = tf.nn.softplus,
                 optimizer = tf.train.AdamOptimizer(),
                 scale=0.1                 
                ):    
        self.n_input  = n_input
        self.n_hidden = n_hidden
        self.transfer = transfer_function
        self.scale    = tf.placeholder(tf.float32)
        self.training_scale = scale
        network_weights     = self._initialize_weights()
        self.weights        = network_weights
        
        self.x = tf.placeholder(tf.float32 , [None , self.n_input])
        self.hidden = self.transfer(
                                    tf.add(
                                           tf.matmul(
                                                     self.x + scale * tf.random_normal((n_input,)),  #x 加上噪声 ，噪声= scale * tf.random_normal((n_input,))
                                                     self.weights['w1']                              #加了噪声的输入 与隐含成的权重 w1 相乘
                                                     ),
                                           self.weights['b1']                                                                                                          
                                           )
                                    )
        
        #经过隐藏层后需要对数据进行复原重建
        self.reconstruction = tf.add(
                                     tf.matmul(
                                               self.hidden , 
                                               self.weights['w2']
                                               ),
                                     self.weights['b2']
                                     )
        
        self.cost = 0.5 * tf.reduce_sum(
                                        tf.pow(
                                               tf.subtract(
                                                           self.reconstruction,
                                                           self.x
                                                           ),
                                               2.0
                                               )
                                        )
        self.optimizer = optimizer.minimize(self.cost)
        
        init = tf.global_variables_initializer()
        self.sess = tf.Session() 
        self.sess.run(init)
            
    def _initialize_weights(self):
        all_weights = dict()
        all_weights['w1'] = tf.Variable(xavier_init(self.n_input , self.n_hidden))
        all_weights['b1'] = tf.Variable(tf.zeros([self.n_hidden             ],dtype=tf.float32))
        all_weights['w2'] = tf.Variable(tf.zeros([self.n_hidden,self.n_input],dtype=tf.float32))
        all_weights['b2'] = tf.Variable(tf.zeros([self.n_input              ],dtype=tf.float32))
        
        return all_weights
    
    #定义计算损失cost及执行一步训练  实战 62页
    def partial_fit(self , X):
        cost , opt = self.sess.run(
                                   (self.cost , self.optimizer) ,
                                   feed_dict = {self.x : X , self.scale : self.training_scale}
                                   )
        return cost 
    
    #只求损失cost 的函数 实战 62页
    def calc_total_cost(self , X):
        return self.sess.run(
                             self.cost , 
                             feed_dict= {self.x : X , self.scale : self.training_scale}
                             )
        
    #返回自编码器隐含层的输出结果。实战 62页
    def transform(self , X):
        return self.sess.run(
                             self.hidden,
                             feed_dict={self.x : X , self.scale : self.training_scale }
                             )
        
    #将隐含层的输出结果作为输入，通过重建层提取高阶特征复原为原始数据  
    #实战 63页
    def generate(self , hidden = None):
        if hidden is None :
            hidden = np.random.normal(size = self.weights["b1"])
            
        return self.sess.run(
                             self.reconstruction ,
                             feed_dict={self.hidden:hidden} 
                             )
        
    #整体运行一遍复原过程，包括提取高阶特征和通过高阶特征复原数据，即包括transform 和generate。输入原数据，输出复原后数据
    #实战 63页
    def reconstruct(self , X):
        return self.sess.run(
                             self.reconstruction , 
                             feed_dict={self.x : X , self.scale:self.training_scale}
                             )
        
    def getWeights(self):
        return self.sess.run(self.weights['w1'])
    
    def getBiases(self):
        return self.sess.run(self.weights['b1'])
    
        

        

        