'''
Created on 2017年11月29日
python Z:\StockAnalysis\sourceCode\TuShare\test\src\import_my_f.py
@author: moonlit
'''
# import numpy as np
import pandas as pd
import numpy as np
import cx_Oracle
# from math import ceil
from sqlalchemy import create_engine
# from sklearn.utils import shuffle  
import getStockData as gsd

def import_f():
    shi_jians = gsd.get_shi_jian_my_f()
#     shi_jians = ["2017-09-22"]
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()    
    
    for shi_jian in shi_jians :
        df= gsd.get_stock_data_daily_my_f(begin_time=shi_jian,end_time=shi_jian)
        f1 = df["price"].values
        f2 = 1e15*((df["price_today_open"].values - df["price"].values) / (df["max_price"].values-df["min_price"].values))/df["amount"].values
        f3 = 1e15*df["zhang_die_rate"].values/df["market_cap"].values  
        f4 = 1e15*df["zhang_die_rate"].values/df["amount"].values
        f5 = df["amount"].values / df["amount_last_day"].values - 1
        f6 = df["price_today_open"].values / df["price_last_day"].values - 1
        
        df_std = pd.DataFrame()
        df_std["code"] = df["code"].values
#         df_std["shi_jian"] = df["shi_jian"].values
        df_std["f1"] = f1
        df_std["f2"] = f2
        df_std["f3"] = f3
        df_std["f4"] = f4
        df_std["f5"] = f5
        df_std["f6"] = f6
        
        # 去掉极值
        def normalizeData(fdf,factors = []):
            
            for factor in factors:
                std = np.std(fdf[factor])
                MA = np.mean(fdf[factor])
#                 print ("(MA + 3*std) %s"%(MA + 3*std))
#                 print ("(MA - 3*std) %s"%(MA - 3*std))
#                 print ("去极值前：%s" % fdf)
                fdf = fdf[fdf[factor]<= (MA + 3*std)] 
                fdf = fdf[fdf[factor]>= (MA - 3*std)] 
#                 print ("去极值后：%s" % fdf)
            return fdf 
        
        factors = ["f1","f2","f3","f4","f5","f6",] 
        
#         print(len(df_std))
        df_std = normalizeData(df_std,factors)      
#         print(len(df_std))
        
        
        df_std = df_std.set_index("code")
        df_std = df_std.rank(axis=0, method="average", numeric_only=None, na_option="keep", ascending=False, pct=True)
        df_std = df_std.reset_index()
        
#         print(df_std)

        for row in df_std.itertuples():
            code = getattr(row, "code")
            
            sql  = "update tb_stock_my_f set "
        
            for aid in range(1,7) :
                
                alpha = "f" + str(aid)                       
                            
                if str( getattr(row, alpha) ) == "nan" :
                    continue
                
                sql += alpha + "=" + str( getattr(row, alpha) )+ ","
                
            sql  = sql[:-1]    
            sql += " where "
            sql += "  code = '" + code +"'"
            sql += "    and "
            sql += "  shi_jian = '" + shi_jian + "'"
                
            try :
                cr.execute(sql)
#                 print(sql)
            except:
                print(sql)
        print(shi_jian,"done")
    db.commit()            
    print("all done")

        
import_f()
        
        