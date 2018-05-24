'''
Created on 2017年9月25日

@author: moonlit

python Z:\StockAnalysis\sourceCode\TuShare\test\src\importAlpha101data_to_std.py
'''

# import numpy as np
import pandas as pd
import cx_Oracle
import getStockData as gsd
import math

unrealized = ["048","058","059","063","067","068","069","070","076","079","080","081","082","084","087","089","090","091","093","097","100",]

shi_jians = gsd.get_101_data_shi_jian()

db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
cr=db.cursor()

nan = 99999999.0

for shi_jian in shi_jians :
    
    data = gsd.get_101_data_for_std1(shi_jian=shi_jian )
    data = data.set_index("code")
    data = data.rank(axis=0, method="average", numeric_only=None, na_option="keep", ascending=False, pct=True)
    data = data.reset_index()
        
    for row in data.itertuples(): 
        code = getattr(row, "code")
        
        sql  = "update tb_stock_alpha101_1 set "
        
        for aid in range(1,102) :
            aid = ("000" + str(aid))[-3:]
            
            if aid in unrealized :
                continue
            
            alpha = "alpha_" + aid                       
                        
            if str( getattr(row, alpha) ) == "nan" :
                continue
            
            sql += alpha + "=" + str( getattr(row, alpha) )+ ","
            
        sql  = sql[:-1]    
        sql += " where "
        sql += "  code = '" + code +"'"
        sql += "    and "
        sql += "  shi_jian = to_date('" + shi_jian + " 15:00:00','yyyy-mm-dd hh24:mi:ss')"
            
        try :
            cr.execute(sql)
        except:
            pass
        
    db.commit()
    
    print("done:",shi_jian)

db.commit()
cr.close ()  
db.close ()        
         
print("all done")

# res = aa.factor_cal(data= data , factor_id = "001")
# print(res)
# res  = pd.DataFrame()
# res["code"] = code 
# print(data)
# res["101"]  = data[0]
# res = res.sort_values(by = "101", ascending =False)
# print(res[res["code"] == "600000"])

