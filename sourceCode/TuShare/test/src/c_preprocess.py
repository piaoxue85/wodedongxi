'''
Created on 2017年7月26日

@author: moonlit
'''
import logging 
import os.path 
import sys 
import re 
import jieba 
import json
import pandas as pd
import numpy  as np
from dask.dataframe.core import DataFrame
from nose.util import tolist
from gensim.models.word2vec import Word2Vec
from sklearn.utils import shuffle  

#---------------------------------------------Announcements 测试集合--------------------------------------------------------------------
answer = open("D:/Competition/src/data/test/初赛第二次提交测试集答案.json"        ,'r', encoding='utf_8_sig')
rt     = open("D:/Competition/src/data/test/AnnouncementsTrainSample_jieba.json" ,'r', encoding='utf_8_sig')
       
foutput  = open("D:/Competition/src/data/test/CodeAndAnnouncements_wordVec.json",'w', encoding='utf-8') 
   
program = os.path.basename(sys.argv[0]) 
logger = logging.getLogger(program) 
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s' )
logging.root.setLevel(level=logging.INFO) 
logger.info("running %s" % ' '.join(sys.argv)) 
       
df_answer     = json.load(answer)
# df_answer= pd.DataFrame(data)
data     = json.load(rt)
df_rt    = pd.DataFrame(data)
  
i = 0
       
for info in df_answer :
#     try :
    df = df_rt[(df_rt["uuid"]==info["uuid"]) ]
    if len(df)>0 :  
                                            
        info["Announcements"] = str(df.to_json(orient='records',force_ascii = False)) 
                          
        line_write = str(info)
        line_write = str(json.dumps(line_write, ensure_ascii = False))
        foutput.write(line_write+",")        
#     except:
#         pass
            
    i = i + 1 
    if (i % 1000 == 0) :
        logger.info("Saved " + str(i) + " articles_seg") 

#---------------------------------------------research 测试集合--------------------------------------------------------------------
# answer = open("D:/Competition/src/data/test/初赛第二次提交测试集答案.json"        ,'r', encoding='utf_8_sig')
# rt     = open("D:/Competition/src/data/test/ResearchTrainSample_jieba.json" ,'r', encoding='utf_8_sig')
#       
# foutput  = open("D:/Competition/src/data/test/CodeAndResearch_wordVec.json",'w', encoding='utf-8') 
#   
# program = os.path.basename(sys.argv[0]) 
# logger = logging.getLogger(program) 
# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s' )
# logging.root.setLevel(level=logging.INFO) 
# logger.info("running %s" % ' '.join(sys.argv)) 
#       
# df_answer     = json.load(answer)
# # df_answer= pd.DataFrame(data)
# data     = json.load(rt)
# df_rt    = pd.DataFrame(data)
#  
# i = 0
#       
# for info in df_answer :
# #     try :
#     df = df_rt[(df_rt["uuid"]==info["uuid"]) ]
#     if len(df)>0 :  
#                                            
#         info["Announcements"] = str(df.to_json(orient='records',force_ascii = False)) 
#                          
#         line_write = str(info)
#         line_write = str(json.dumps(line_write, ensure_ascii = False))
#         foutput.write(line_write+",")        
# #     except:
# #         pass
#            
#     i = i + 1 
#     if (i % 1000 == 0) :
#         logger.info("Saved " + str(i) + " articles_seg") 



#-----------------------------------------------------------------------------------------------------------------
      
# rr  = open("D:/Competition/src/data/test/AnnouncementsRelations.json",'r', encoding='utf_8_sig')
# rt  = open("D:/Competition/src/data/test/AnnouncementsTrainSample_jieba.json",'r', encoding='utf_8_sig')
# rpd = open("D:/Competition/src/data/test/pricedetail.json",'r', encoding='utf_8_sig')
#              
# foutput  = open("D:/Competition/src/data/test/CodeAndAnnouncements_wordVec.json",'w', encoding='utf-8') 
#              
# program = os.path.basename(sys.argv[0]) 
# logger = logging.getLogger(program) 
# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s' )
# logging.root.setLevel(level=logging.INFO) 
# logger.info("running %s" % ' '.join(sys.argv)) 
#              
# data = json.load(rr)
# df_rr= pd.DataFrame(data)
# data = json.load(rt)
# df_rt= pd.DataFrame(data)
#              
# data = pd.DataFrame(json.load(rpd))
# data = shuffle(data) 
# data = data.to_dict(orient='records ')
#  
# i = 0
#              
# for info in data :
#     try :
#         df = df_rr[(df_rr["security_id"]==info["security_id"])&(df_rr["publish_date"]==info["data_date"]) ]
#     #     df = pd.DataFrame(df , columns=["news_id","security_id","publish_date"])
# #         print(df)
#         if len(df)>0 :  
#             news_id = tolist(df["news_id"])
#                         
#             df = df_rt[(df_rt["news_id"].isin(news_id))]  
#                            
#             info["Announcements"] = str(df.to_json(orient='records',force_ascii = False))             
# #             line_write = str(info)            
# #             foutput.write(line_write)
#             line_write = str(info)
#             line_write = str(json.dumps(line_write, ensure_ascii = False))
#             foutput.write(line_write+",")              
#     except:
#         pass
#                   
#     i = i + 1 
#     if (i % 1000 == 0) :
#         logger.info("Saved " + str(i) + " articles_seg") 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# rr  = open("D:/Competition/src/data/test/ResearchRelation.json",'r', encoding='utf_8_sig')
# rt  = open("D:/Competition/src/data/test/ResearchTrainSample_jieba.json",'r', encoding='utf_8_sig')
# rpd = open("D:/Competition/src/data/test/pricedetail.json",'r', encoding='utf_8_sig')
#      
# foutput  = open("D:/Competition/src/data/test/CodeAndResearch_wordVec.json",'w', encoding='utf-8') 
#  
# program = os.path.basename(sys.argv[0]) 
# logger = logging.getLogger(program) 
# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s' )
# logging.root.setLevel(level=logging.INFO) 
# logger.info("running %s" % ' '.join(sys.argv)) 
#      
# data = json.load(rr)
# df_rr= pd.DataFrame(data)
# data = json.load(rt)
# df_rt= pd.DataFrame(data)
#      
# data = pd.DataFrame(json.load(rpd))
# data = shuffle(data) 
# data = data.to_dict(orient='records ')
# 
# i = 0
#      
# for info in data :
# #     try :
#     df = df_rr[(df_rr["security_code"]==info["security_id"])&(df_rr["publish_date"]==info["data_date"]) ]
#     if len(df)>0 :  
#          
#         news_id = tolist(df["news_id"])                      
#         df = df_rt[(df_rt["news_id"].isin(news_id))]           
#                            
#         info["Announcements"] = str(df.to_json(orient='records',force_ascii = False)) 
#                         
#         line_write = str(info)
#         line_write = str(json.dumps(line_write, ensure_ascii = False))
#         foutput.write(line_write+",")        
# #     except:
# #         pass
#           
#     i = i + 1 
#     if (i % 1000 == 0) :
#         logger.info("Saved " + str(i) + " articles_seg") 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
# # #载入保存的文件
# model = Word2Vec.load("D:\Competition\src\data\SogouCA\corpus.model")  
# #获得权重
# weights = model.wv.syn0  
# #获得词库
# vocab = dict([(k, v.index) for k,v in model.wv.vocab.items()])  
#    
# def to_ids(words):  
#     def word_to_id(word):
#         word_id = vocab.get(word)
#         if word_id is None:
#             word_id = 0
#         return word_id
#     x = words
#     x = list(map(word_to_id, x))
#     return np.array(x)
#    
# f        = open('D:/Competition/src/data/test/AnnouncementsTrainSample.json','r',encoding="utf_8_sig")
# foutput  = open("D:/Competition/src/data/test/AnnouncementsTrainSample_jieba.json",'w', encoding='utf-8') 
# data = json.load(f) 
# # space = " "    
# i = 0
# trased = []
#          
# program = os.path.basename(sys.argv[0]) 
# logger = logging.getLogger(program) 
# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s' )
# logging.root.setLevel(level=logging.INFO) 
# logger.info("running %s" % ' '.join(sys.argv)) 
#          
# errCount = 0
# for info in data :
#     try :
#         line_seg        = jieba.cut(info["content"])
#         info["content"] = list(to_ids(line_seg))
#              
#         line_seg        = jieba.cut(info["title"])
#         info["title"]   = list(to_ids(line_seg)) 
#                  
#         line_seg             = jieba.cut(info["annonce_type"])
#         info["annonce_type"] = list(to_ids(line_seg))
#           
#         line_write = str(info)
#         line_write = str(json.dumps(line_write, ensure_ascii = False))
#         foutput.write(line_write+",") 
#     except:
#         errCount +=1
#         print("err count :" + str(errCount))
#               
#     i = i + 1 
#     if (i % 1000 == 0) :
#         logger.info("Saved " + str(i) + " articles_seg")                     
# #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
# #载入保存的文件
# model = Word2Vec.load("D:\Competition\src\data\SogouCA\corpus.model")  
# #获得权重
# weights = model.wv.syn0  
# #获得词库
# vocab = dict([(k, v.index) for k,v in model.wv.vocab.items()])  
#    
# def to_ids(words):  
#     def word_to_id(word):
#         word_id = vocab.get(word)
#         if word_id is None:
#             word_id = 0
#         return word_id
#     x = words
#     x = list(map(word_to_id, x))
#     return np.array(x)
#   
# f        = open('D:/Competition/src/data/test/ResearchTrainSample.json','r',encoding="utf_8_sig")
# foutput  = open("D:/Competition/src/data/test/ResearchTrainSample_jieba.json",'w', encoding='utf-8') 
# data = json.load(f)   
# i = 0
# trased = []
#      
# program = os.path.basename(sys.argv[0]) 
# logger = logging.getLogger(program) 
# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s' )
# logging.root.setLevel(level=logging.INFO) 
# logger.info("running %s" % ' '.join(sys.argv)) 
#      
# errCount = 0
# for info in data :
#     try :
#         line_seg        = jieba.cut(info["content"])
#         info["content"] = list(to_ids(line_seg))
#          
#         line_seg        = jieba.cut(info["title"])
#         info["title"]   = list(to_ids(line_seg)) 
#              
#         line_seg            = jieba.cut(info["column_type"])
#         info["column_type"] = list(to_ids(line_seg))            
#            
#         line_write = str(info)
#         line_write = str(json.dumps(line_write, ensure_ascii = False))
#         foutput.write(line_write+",")        
#     except:
#         errCount +=1
#          
#     i = i + 1 
#     if (i % 1000 == 0) :
#         logger.info("Saved " + str(i) + " articles_seg")    
#            
# print("err count :" + str(errCount))        