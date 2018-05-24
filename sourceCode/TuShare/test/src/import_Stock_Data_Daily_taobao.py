'''
Created on 2017年11月22日
python Z:\StockAnalysis\sourceCode\TuShare\test\src\import_Stock_Data_Daily_taobao.py
python D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\import_Stock_Data_Daily_taobao.py
@author: moonlit
'''
import numpy as np
import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine  
import getStockData as gsd
import time
import os  
import os.path 

# path  ="D:/data_from_taobao"
path  ="Z:/bt/data_from_taobao"
count = 0

def get_file_list(path = ""):
    all = []
    for _, _, files in os.walk(path):  
        all += files
    return all    
    
def insertdb(file = ""):
    global count
    try :
#         finput = open(file ,'rb') 
#         s = finput.read()
#         s = s.decode("gb2312",errors='ignore')
#         foutput = open(file+"_temp",'w', encoding="gb2312") 
#         foutput.write(s)
#         finput.close() 
#         foutput.close()         

        df = pd.read_csv(file, encoding = "gb2312" )
    except Exception as e:            
        print(file,e)
        return  
        
    df = df.fillna("null")
    df = df.replace([np.inf, -np.inf],"null")
    
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接 
    cr=db.cursor()
    
    for row in df.itertuples():
        sql = "insert into tb_stock_data_daily_taobao values ("     
        sql += "'" + str(getattr(row,"股票代码"      ))[2:] + "',"      
        sql += "'" + str(getattr(row,"股票名称"      )) + "',"      
        sql += "'" + str(getattr(row,"交易日期"      )) + "',"      
        sql += "'" + str(getattr(row,"新浪行业"      )) + "',"      
        sql += "'" + str(getattr(row,"新浪概念"      )) + "',"      
        sql += "'" + str(getattr(row,"新浪地域"      )) + "',"      
        sql += " " + str(getattr(row,"开盘价"        )) + " ,"      
        sql += " " + str(getattr(row,"最高价"        )) + " ,"      
        sql += " " + str(getattr(row,"最低价"        )) + " ,"      
        sql += " " + str(getattr(row,"收盘价"        )) + " ,"      
        sql += " " + str(getattr(row,"后复权价"      )) + " ,"      
        sql += " " + str(getattr(row,"前复权价"      )) + " ,"      
        sql += " " + str(getattr(row,"涨跌幅"        )) + " ,"      
        sql += " " + str(getattr(row,"成交量"        )) + " ,"      
        sql += " " + str(getattr(row,"成交额"        )) + " ,"      
        sql += " " + str(getattr(row,"换手率"        )) + " ,"      
        sql += " " + str(getattr(row,"流通市值"      )) + " ,"      
        sql += " " + str(getattr(row,"总市值"        )) + " ,"      
        sql += " " + str(getattr(row,"是否涨停"      )) + " ,"      
        sql += " " + str(getattr(row,"是否跌停"      )) + " ,"      
        sql += " " + str(getattr(row,"市盈率TTM"     )) + " ,"      
        sql += " " + str(getattr(row,"市销率TTM"     )) + " ,"      
        sql += " " + str(getattr(row,"市现率TTM"     )) + " ,"      
        sql += " " + str(getattr(row,"市净率"        )) + " ,"      
        sql += " " + str(getattr(row,"MA_5"          )) + " ,"      
        sql += " " + str(getattr(row,"MA_10"         )) + " ,"      
        sql += " " + str(getattr(row,"MA_20"         )) + " ,"      
        sql += " " + str(getattr(row,"MA_30"         )) + " ,"      
        sql += " " + str(getattr(row,"MA_60"         )) + " ,"      
        sql += "'" + str(getattr(row,"MA金叉死叉"    )) + "',"      
        sql += " " + str(getattr(row,"MACD_DIF"      )) + " ,"      
        sql += " " + str(getattr(row,"MACD_DEA"      )) + " ,"      
        sql += " " + str(getattr(row,"MACD_MACD"     )) + " ,"      
        sql += "'" + str(getattr(row,"MACD_金叉死叉" )) + "',"      
        sql += " " + str(getattr(row,"KDJ_K"         )) + " ,"      
        sql += " " + str(getattr(row,"KDJ_D"         )) + " ,"      
        sql += " " + str(getattr(row,"KDJ_J"         )) + " ,"      
        sql += "'" + str(getattr(row,"KDJ_金叉死叉"  )) + "',"      
        sql += " " + str(getattr(row,"布林线中轨"    )) + " ,"      
        sql += " " + str(getattr(row,"布林线上轨"    )) + " ,"      
        sql += " " + str(getattr(row,"布林线下轨"    )) + " ,"      
        sql += " " + str(getattr(row,"psy"           )) + " ,"      
        sql += " " + str(getattr(row,"psyma"         )) + " ,"      
        sql += " " + str(getattr(row,"rsi1"          )) + " ,"      
        sql += " " + str(getattr(row,"rsi2"          )) + " ,"      
        sql += " " + str(getattr(row,"rsi3"          )) + " ,"      
        sql += " " + str(getattr(row,"振幅"          )) + " ,"      
        sql += " " + str(getattr(row,"量比"          )) + "  "      
        sql += ")"  
        
        try :
            cr.execute(sql)
        except Exception as e:            
            print(e)
            print(sql)
            
             
    count += 1     
    print(count , file , "done") 
    
    db.commit()        
    cr.close ()  
    db.close () 

files= get_file_list(path ) 

for file in files :
    insertdb(path+"/"+file)
    
print("all done")  
