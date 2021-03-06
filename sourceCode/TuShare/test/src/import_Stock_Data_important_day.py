'''
Created on 2017年11月22日
python Z:\StockAnalysis\sourceCode\TuShare\test\src\import_Stock_Data_Daily.py
@author: moonlit
'''
# import numpy as np
import pandas as pd
import cx_Oracle
# from math import ceil
from sqlalchemy import create_engine
# from sklearn.utils import shuffle  
import getStockData as gsd

def import_holiday():
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    
    sql = "delete tb_stock_important_day" 
    cr.execute(sql) 
    
    for i in list(range(1990,2100)) :
        res_code,res_msg,data = gsd.get_holiday_yearly(year=str(i))
        
        if res_code != 0 :
            continue
        
        names     = data["name"    ].values
        startdays = data["startday"].values
        
        for day , name in zip(startdays,names) :
            sql = "insert into tb_stock_important_day values ('" + day + "','" + name + "')" 
            cr.execute(sql) 
            
    db.commit() 

import_holiday()
