'''
Created on 2018年1月22日

@author: moonlit
python z:/StockAnalysis/sourceCode/TuShare/test/src/myDynamicFator.py
'''
import getStockData as gsd
import pandas as pd
import numpy as np
import cx_Oracle
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

def get_stock_fator_test(fator=""):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
#     sql = "select shi_jian,avg_ret from tb_stock_fator_test where fator = '"+fator+"'  order by shi_jian asc"
    sql = "select shi_jian,avg_ret from tb_stock_fator_test where fator = '"+fator+"' and shi_jian >= '2017-01-01' order by shi_jian asc"
    data = pd.read_sql_query(sql,con = engine)
#     data = data.set_index('shi_jian')

    return data  

def get_stock_fators():
    engine = create_engine('oracle://c##stock:didierg160@myoracle')    
    sql = "select distinct(fator) fator from tb_stock_fator_test order by fator asc"
    fators = pd.read_sql_query(sql,con = engine)
    fators = fators["fator"].values
    
    return fators     
    
data  = pd.DataFrame()
fators = get_stock_fators()
# fators=[
# "MARKET_CAP_asc",
# "MARKET_CAP_desc",
# "ROE_asc",
# "ROE_desc",
# "EPS_asc",
# "EPS_desc",
# "EPSG_asc",
# "EPSG_desc",
# ]

# for fator in fators :
#     df = get_stock_fator_test(fator)       
#     data[fator] = df["avg_ret"].values
#     data["shi_jian"]=df["shi_jian"].values

# db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接 
# cr=db.cursor()

for fator in fators :
    if fator == "MARKET_CAP_asc" :
        continue
    df = get_stock_fator_test(fator)
    total = []
    y = 1
    for ret,shi_jian in zip(df["avg_ret"].values ,df["shi_jian"].values):
        y = y * (1+ret)
        total.append(y)
#         sql = "insert into tb_temp values ('"+shi_jian+"','"+fator+"',"+str(y) + ")"
#         cr.execute(sql)
    if total[-1]> 1 :
        data[fator] = total
    data["shi_jian"]=df["shi_jian"].values

# db.commit()        
# cr.close ()  
# db.close () 

# data = data.set_index("shi_jian")
data.plot()
plt.grid(True)
plt.show()
 
data = data.corr()
data.to_csv('d:/b.csv', encoding = "utf-8")  
    