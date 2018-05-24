'''
Created on 2017年11月22日
python Z:\StockAnalysis\sourceCode\TuShare\test\src\import_Stock_Data_Daily_pledged.py
@author: moonlit
导入股权质押数据
'''
# import numpy as np
import pandas as pd
import cx_Oracle
# from math import ceil
from sqlalchemy import create_engine
# from sklearn.utils import shuffle  
import getStockData as gsd
import tushare as ts
import time

def import_stock_pledged() :
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()   
    
    sql = "delete tb_stock_pledged"
    cr.execute(sql)
    
    df = ts.stock_pledged()
    
    for row in df.itertuples():
        sql = "insert into tb_stock_pledged values (" 
        sql += "'" + str(getattr(row,"code"           )) + "',"            
        sql += "'" + str(getattr(row,"name"           )) + "',"        
        sql += "'" + str(getattr(row,"deals"          )) + "',"        
        sql += "'" + str(getattr(row,"unrest_pledged" )) + "',"        
        sql += "'" + str(getattr(row,"rest_pledged"   )) + "',"        
        sql += "'" + str(getattr(row,"totals"         )) + "',"        
        sql += "'" + str(getattr(row,"p_ratio"        )) + "',"        
        sql += "sysdate"
        sql += ")"        
        cr.execute(sql)         
    
    db.commit()        
    cr.close ()  
    db.close ()     
    print("stock_pledged done")
    

def import_pledged_detail():
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()   
    
    sql = "delete tb_stock_pledged_detail"
    cr.execute(sql)
    
    df = ts.pledged_detail()
    
    for row in df.itertuples():
        sql = "insert into tb_stock_pledged_detail values (" 
        sql += "'" + str(getattr(row,"code"      )) + "',"            
        sql += "'" + str(getattr(row,"name"      )) + "',"        
        sql += "'" + str(getattr(row,"ann_date"  )) + "',"        
        sql += "'" + str(getattr(row,"pledgor"   )) + "',"        
        sql += "'" + str(getattr(row,"pledgee"   )) + "',"        
        sql += "'" + str(getattr(row,"volume"    )) + "',"        
        sql += "'" + str(getattr(row,"from_date" )) + "',"
        sql += "'" + str(getattr(row,"end_date"  )) + "',"          
        sql += "sysdate"
        sql += ")"        
        cr.execute(sql)         
    
    db.commit()        
    cr.close ()  
    db.close ()     
    print("pledged_detail done")
    
import_stock_pledged()
import_pledged_detail()

