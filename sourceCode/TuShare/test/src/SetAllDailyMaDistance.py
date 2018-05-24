'''
Created on 2017年7月26日

@author: moonlit
'''
import pandas as pd
import numpy  as np
from sklearn.preprocessing import normalize
import cx_Oracle
import getStockData as gsd

# python Z:\StockAnalysis\sourceCode\TuShare\test\src\SetAllDailyMaDistance.py

data = gsd.get_stock_data_daily_all_for_ma_process_df()

acode     = data["code"    ].values   
ashi_jian = data["shi_jian"].values    
ama = data[["ma6"  ,"ma12" ,"ma20" ,"ma30" ,"ma45" ,"ma60" ,"ma125","ma250"]].values
# ama = data[["ma6"  ,"ma12" ,"ma20" ,"ma30" ,"ma45" ,"ma60" ]].values
# ama = ama.reshape(-1,6)

count = 0
db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
cr=db.cursor()

for (code,shi_jian,ma) in zip(acode,ashi_jian,ama):
    ma      = normalize([ma])[0]*1000
    ma      = np.sort(ma)
    avg_dis_6 = (ma[-3] - ma[0])/(len(ma) - 1 - 2)
    avg_dis_7 = (ma[-2] - ma[0])/(len(ma) - 1 - 1)
    avg_dis_8 = (ma[-1] - ma[0])/(len(ma) - 1 - 0)
    if avg_dis_8 <0 :
        c = 1

    sql  = "update tb_stock_data_daily set MA_DISTANCE_AVG_6 = " + str(avg_dis_6) + ", " 
    sql += "                               MA_DISTANCE_AVG_7 = " + str(avg_dis_7) + ", " 
    sql += "                               MA_DISTANCE_AVG_8 = " + str(avg_dis_8) + "  " 
    sql += "where code ='" + code + "' and shi_jian = to_date('" + shi_jian +"','yyyymmddhh24miss')"

    cr.execute(sql)    
    
    if count>= 1000 :        
        db.commit() 
        print("commit") 
        count = 0      

    count += 1
#     print(avg_dis)
    
db.commit()  
cr.close ()  
db.close ()    
print("done")  
