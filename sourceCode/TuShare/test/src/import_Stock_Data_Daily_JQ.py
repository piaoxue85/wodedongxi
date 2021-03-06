'''
Created on 2017年11月22日
python Z:\StockAnalysis\sourceCode\TuShare\test\src\import_Stock_Data_Daily_JQ.py
@author: moonlit
'''
# import numpy as np
import pandas as pd
import cx_Oracle
# from math import ceil
from sqlalchemy import create_engine
# from sklearn.utils import shuffle  
import getStockData as gsd
import tushare as ts
import jqdatasdk as jq
import time

#获取连接备用
cons = ts.get_apis()
jq.auth('13600069823','didierg160')

def importStockList():
    df = ts.get_stock_basics()
    
    tsFaile = 1
        
    while tsFaile !=0 :
        try:
            #if tsFaile >=2 :
            #    cons = ts.get_apis()
            
            df = ts.get_stock_basics()
            tsFaile = 0
        except Exception as e:
            #获取连接备用
#             ts.close_apis(conn=cons)            
            print("get_stock_basics ,ts soeket fail:",tsFaile,e)
            time.sleep(5)
            if tsFaile <=5  :
                tsFaile += 1
            else:
                break      
    
    df["code"] = df.index
    df = df.reset_index(drop=True)
    
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    
    sql = "delete tb_stock_list_ts"
    cr.execute(sql) 
    
    sql = "delete tb_stock_list"
    cr.execute(sql)
    
    sql = "delete tb_stock_list_tshis where shi_jian=to_char(sysdate,'yyyy-mm-dd')"
    cr.execute(sql) 
    
    db.commit() 
    
    for row in df.itertuples(): 
        if getattr(row,"timeToMarket"    ) == 0 :
            continue
        
        sql = "insert into tb_stock_list_ts values (" 
        sql += "'" + str(getattr(row,"code"            )) + "',"            
        sql += "'" + str(getattr(row,"name"            )) + "',"        
        sql += "'" + str(getattr(row,"industry"        )) + "',"        
        sql += "'" + str(getattr(row,"area"            )) + "',"        
        sql += "'" + str(getattr(row,"pe"              )) + "',"        
        sql += "'" + str(getattr(row,"outstanding"     )) + "',"        
        sql += "'" + str(getattr(row,"totals"          )) + "',"        
        sql += "'" + str(getattr(row,"totalAssets"     )) + "',"        
        sql += "'" + str(getattr(row,"liquidAssets"    )) + "',"        
        sql += "'" + str(getattr(row,"fixedAssets"     )) + "',"        
        sql += "'" + str(getattr(row,"reserved"        )) + "',"        
        sql += "'" + str(getattr(row,"reservedPerShare")) + "',"        
        sql += "'" + str(getattr(row,"esp"             )) + "',"        
        sql += "'" + str(getattr(row,"bvps"            )) + "',"        
        sql += "'" + str(getattr(row,"pb"              )) + "',"        
        sql += "'" + str(getattr(row,"timeToMarket"    )) + "',"        
        sql += "'" + str(getattr(row,"undp"            )) + "',"        
        sql += "'" + str(getattr(row,"perundp"         )) + "',"        
        sql += "'" + str(getattr(row,"rev"             )) + "',"        
        sql += "'" + str(getattr(row,"profit"          )) + "',"        
        sql += "'" + str(getattr(row,"gpr"             )) + "',"        
        sql += "'" + str(getattr(row,"npr"             )) + "',"        
        sql += "'" + str(getattr(row,"holders"         )) + "',"
        sql += "sysdate"
        sql += ")"        
        cr.execute(sql)  
        
        sql = "insert into tb_stock_list values (" 
        sql += "'" + str(getattr(row,"code"            )) + "',"            
        sql += "'" + str(getattr(row,"name"            )) + "',"                
        sql += "'" + str(getattr(row,"pe"              )) + "',"  
        sql += "'" + str(getattr(row,"pb"              )) + "',"                
        sql += "'" + str(getattr(row,"liquidAssets"    )) + "'," 
        sql += "'" + str(getattr(row,"totalAssets"     )) + "',"               
        sql += "0,"        
        sql += "sysdate"
        sql += ")"        
        cr.execute(sql)          
        
        engine = create_engine('oracle://c##stock:didierg160@myoracle')
        sql  = "select count(*) count from tb_stock_list_tshis where "
        sql += " CODE            = '" + str(getattr(row,"code"            )) + "' and"    
        sql += " NAME            = '" + str(getattr(row,"name"            )) + "' and"
        sql += " INDUSTRY        = '" + str(getattr(row,"industry"        )) + "' and"
        sql += " AREA            = '" + str(getattr(row,"area"            )) + "' and"
        sql += " PE              = '" + str(getattr(row,"pe"              )) + "' and"
        sql += " OUTSTANDING     = '" + str(getattr(row,"outstanding"     )) + "' and"
        sql += " TOTALS          = '" + str(getattr(row,"totals"          )) + "' and"
        sql += " totalAssets     = '" + str(getattr(row,"totalAssets"     )) + "' and"
        sql += " liquidAssets    = '" + str(getattr(row,"liquidAssets"    )) + "' and"
        sql += " fixedAssets     = '" + str(getattr(row,"fixedAssets"     )) + "' and"
        sql += " RESERVED        = '" + str(getattr(row,"reserved"        )) + "' and"
        sql += " reservedPerShare= '" + str(getattr(row,"reservedPerShare")) + "' and"
        sql += " ESP             = '" + str(getattr(row,"esp"             )) + "' and"
        sql += " BVPS            = '" + str(getattr(row,"bvps"            )) + "' and"
        sql += " PB              = '" + str(getattr(row,"pb"              )) + "' and"
        sql += " timeToMarket    = '" + str(getattr(row,"timeToMarket"    )) + "' and"
        sql += " UNDP            = '" + str(getattr(row,"undp"            )) + "' and"
        sql += " PERUNDP         = '" + str(getattr(row,"perundp"         )) + "' and"
        sql += " REV             = '" + str(getattr(row,"rev"             )) + "' and"
        sql += " PROFIT          = '" + str(getattr(row,"profit"          )) + "' and"
        sql += " GPR             = '" + str(getattr(row,"gpr"             )) + "' and"
        sql += " NPR             = '" + str(getattr(row,"npr"             )) + "' and"
        sql += " HOLDERS         = '" + str(getattr(row,"holders"         )) + "' "        
        data = pd.read_sql_query(sql,con = engine)
        count = data["count"].values[0]
        
        if count >0 :
            continue
        
        sql = "insert into tb_stock_list_tshis values (" 
        sql += "'" + str(getattr(row,"code"            )) + "',"            
        sql += "'" + str(getattr(row,"name"            )) + "',"        
        sql += "'" + str(getattr(row,"industry"        )) + "',"        
        sql += "'" + str(getattr(row,"area"            )) + "',"        
        sql += "'" + str(getattr(row,"pe"              )) + "',"        
        sql += "'" + str(getattr(row,"outstanding"     )) + "',"        
        sql += "'" + str(getattr(row,"totals"          )) + "',"        
        sql += "'" + str(getattr(row,"totalAssets"     )) + "',"        
        sql += "'" + str(getattr(row,"liquidAssets"    )) + "',"        
        sql += "'" + str(getattr(row,"fixedAssets"     )) + "',"        
        sql += "'" + str(getattr(row,"reserved"        )) + "',"        
        sql += "'" + str(getattr(row,"reservedPerShare")) + "',"        
        sql += "'" + str(getattr(row,"esp"             )) + "',"        
        sql += "'" + str(getattr(row,"bvps"            )) + "',"        
        sql += "'" + str(getattr(row,"pb"              )) + "',"        
        sql += "'" + str(getattr(row,"timeToMarket"    )) + "',"        
        sql += "'" + str(getattr(row,"undp"            )) + "',"        
        sql += "'" + str(getattr(row,"perundp"         )) + "',"        
        sql += "'" + str(getattr(row,"rev"             )) + "',"        
        sql += "'" + str(getattr(row,"profit"          )) + "',"        
        sql += "'" + str(getattr(row,"gpr"             )) + "',"        
        sql += "'" + str(getattr(row,"npr"             )) + "',"        
        sql += "'" + str(getattr(row,"holders"         )) + "',"
        sql += "sysdate ,"
        sql += "to_char(sysdate,'yyyy-mm-dd')"
        sql += ")"        
        cr.execute(sql)             
        
    db.commit()        
    cr.close ()  
    db.close ()  
    return df["code"].values ,df["name"].values
    
def importStockDataDailyJQ(codes= [],names=[],asset='E',adj='qfq'):
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    
    code_tail = ""
    if asset == "INDEX":
        code_tail = "zs"

    for code,name in zip(codes,names) :      
        start_date = ""
        
        if adj == "qfq" :
            if isXR(code=code) :
                sql = "delete tb_stock_data_daily where code = '" + code + code_tail+ "'"
                cr.execute(sql)
            
            #time.sleep(1)
        
        start_date = gsd.get_code_max_shi_jian(code=code + code_tail) 
               
        if start_date == "None" :
            start_date = ""
            
        tsFaile = 1
            
        while tsFaile !=0 :
            try:
                #if tsFaile >=2 :
                #    cons = ts.get_apis()                
                
                #df = ts.bar(code, conn=cons, adj=adj,asset=asset, start_date=start_date, end_date='',retry_count = 2)
                #print(df)
                
                import datetime
                df = jq.get_price(jq.normalize_code(code),start_date=start_date, end_date=datetime.datetime.now().strftime("%Y-%m-%d"),skip_paused=True)
                df = df.dropna()
                df = df.sort_index(ascending=False)  
                #print(df)
                
                tsFaile = 0
            except Exception as e:
#                 ts.close_apis(conn=cons)
                if "找不到" in str(e) :
                    tsFaile = 4
                else :
                    time.sleep(5)
                print(code,start_date ,"importStockDataDaily fail:",tsFaile,e)
                if tsFaile <=3  :
                    tsFaile += 1
                else:
                    break
                
        if tsFaile > 0 :
            continue
                                         
        df["datetime"] = df.index
        df = df.reset_index(drop=True)
        df_shift = df.shift(-1)
                
        for row , row_s in zip(df.itertuples(),df_shift.itertuples()): 
            if round(float(getattr(row,"volume" )))<1 :
                continue                                
                                 
#             if len(getattr(row,"datetime")) <10 :
#                 continue
                    
            shi_jian = str(getattr(row,"datetime"))[0:10]
            
            if len(shi_jian)<10 :
                continue
            
            if shi_jian == start_date :
                continue        
            
            if str(getattr(row_s,"close" ))=="nan" : 
                price_last_day  = "null"
                amount_last_day = "null"
                zhang_die       = "null"
                zhang_die_rate  = "null"
            else:
                price_last_day = getattr(row_s,"close" )
                amount_last_day= str(getattr(row_s,"money"))
                zhang_die      = getattr(row,"close" ) - getattr(row_s,"close" )
                zhang_die_rate = getattr(row,"close" )/getattr(row_s,"close" )-1
                            
            sql  = "insert into tb_stock_data_daily "
            sql += "(                   " 
            sql += "  code            , "
            sql += "  name            , "
            sql += "  price_today_open, "
            sql += "  price           , "
            sql += "  max_price       , "
            sql += "  min_price       , "
            sql += "  vol             , "
            sql += "  amount          , "
            sql += "  amount_last_day , "            
            sql += "  shi_jian        , "
            sql += "  price_last_day  , "
            sql += "  zhang_die       , "
            sql += "  zhang_die_rate    "
            sql += ")                   "
            sql += "values              "
            sql += "(                   "
            sql += " '" + code + code_tail+"',"
            sql += " '" + name +"',"
            sql += "  " + str(getattr(row,"open"    )) + ","
            sql += "  " + str(getattr(row,"close"   )) + ","
            sql += "  " + str(getattr(row,"high"    )) + ","
            sql += "  " + str(getattr(row,"low"     )) + ","
            sql += "  " + str(getattr(row,"volume"  )) + ","
            sql += "  " + str(getattr(row,"money"   )) + ","
            sql += "  " + amount_last_day              + ","
            sql += "  to_date('" + shi_jian + " 15:00:00','yyyy-mm-dd hh24:mi:ss'),"  
            sql += "  " + str(price_last_day         ) + ","
            sql += "  " + str(zhang_die              ) + ","
            sql += "  " + str(zhang_die_rate         ) + " "  
            sql += ")"
            
            try:
                cr.execute(sql)
            except Exception as e: 
                print(sql)
             
        #time.sleep(1)
        db.commit()
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(now,code,"done")
    db.commit()        
    cr.close ()  
    db.close ()  
        
#是否除权
def isXR(code=""):
    global cons 
    shi_jian = gsd.get_code_min_shi_jian(code)
    
    if shi_jian =="None":
        return False
    
    data  = gsd.get_stock_data_daily_df_time(code=code,start=shi_jian,end=shi_jian)    
    price = data["price"].values[0]    

    tsFaile = 1
        
    while tsFaile !=0 :
        try:
            
#             print(code,shi_jian)
            
#             if tsFaile >=2 :
#                 cons = ts.get_apis()          
                  
            data  = ts.bar(code, conn=cons, adj='qfq', start_date=shi_jian, end_date=shi_jian,retry_count = 2)
#             print("data",data)

            '''
            if len(data["close"].values)<1 :
                tsFaile += 1 
            else:
                tsFaile = 0
            '''
            tsFaile = 0             
            if len(data["close"].values)<1 :
                return False
        except Exception as e:
            #获取连接备用
            ts.close_apis(conn=cons)            
            cons = ts.get_apis() 
            print(code,shi_jian ,"isXR fail:",tsFaile,e)
            time.sleep(5)
            if tsFaile <=3  :
                tsFaile += 1
            else:
                return False    
#     print(code,shi_jian)
#     data  = ts.bar(code, conn=cons, adj='qfq', start_date=shi_jian, end_date=shi_jian,retry_count = 20)
#     print("data",data)
    close = data["close"].values[0]
    
    if price == close :
        return False
    else :
        return True
    
def importStockDataDaily(codes= [],names=[],asset='E',adj='qfq'):
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    
    code_tail = ""
    if asset == "INDEX":
        code_tail = "zs"

    for code,name in zip(codes,names) :      
        start_date = ""
        
        if adj == "qfq" :
            if isXR(code=code) :
                sql = "delete tb_stock_data_daily where code = '" + code + code_tail+ "'"
                cr.execute(sql)
            
            time.sleep(1)
        
        start_date = gsd.get_code_max_shi_jian(code=code + code_tail) 
               
        if start_date == "None" :
            start_date = ""
            
        tsFaile = 1
            
        while tsFaile !=0 :
            try:
                #if tsFaile >=2 :
                #    cons = ts.get_apis()                
                df = ts.bar(code, conn=cons, adj=adj,asset=asset, start_date=start_date, end_date='',retry_count = 2)
                tsFaile = 0
            except Exception as e:
#                 ts.close_apis(conn=cons)
                time.sleep(5)
                print(code,start_date ,"importStockDataDaily fail:",tsFaile,e)
                if tsFaile <=3  :
                    tsFaile += 1
                else:
                    break
                
        if tsFaile > 0 :
            continue
                                         
        df["datetime"] = df.index
        df = df.reset_index(drop=True)
        df_shift = df.shift(-1)
                
        for row , row_s in zip(df.itertuples(),df_shift.itertuples()): 
            if round(float(getattr(row,"vol" )))<1 :
                continue                                
                                 
#             if len(getattr(row,"datetime")) <10 :
#                 continue
                    
            shi_jian = str(getattr(row,"datetime"))[0:10]
            
            if len(shi_jian)<10 :
                continue
            
            if shi_jian == start_date :
                continue        
            
            if str(getattr(row_s,"close" ))=="nan" : 
                price_last_day  = "null"
                amount_last_day = "null"
                zhang_die       = "null"
                zhang_die_rate  = "null"
            else:
                price_last_day = getattr(row_s,"close" )
                amount_last_day= str(getattr(row_s,"amount"))
                zhang_die      = getattr(row,"close" ) - getattr(row_s,"close" )
                zhang_die_rate = getattr(row,"close" )/getattr(row_s,"close" )-1
                            
            sql  = "insert into tb_stock_data_daily "
            sql += "(                   " 
            sql += "  code            , "
            sql += "  name            , "
            sql += "  price_today_open, "
            sql += "  price           , "
            sql += "  max_price       , "
            sql += "  min_price       , "
            sql += "  vol             , "
            sql += "  amount          , "
            sql += "  amount_last_day , "            
            sql += "  shi_jian        , "
            sql += "  price_last_day  , "
            sql += "  zhang_die       , "
            sql += "  zhang_die_rate    "
            sql += ")                   "
            sql += "values              "
            sql += "(                   "
            sql += " '" + str(getattr(row,"code"    )) + code_tail+"',"
            sql += " '" + name +"',"
            sql += "  " + str(getattr(row,"open"    )) + ","
            sql += "  " + str(getattr(row,"close"   )) + ","
            sql += "  " + str(getattr(row,"high"    )) + ","
            sql += "  " + str(getattr(row,"low"     )) + ","
            sql += "  " + str(getattr(row,"vol"     )) + ","
            sql += "  " + str(getattr(row,"amount"  )) + ","
            sql += "  " + amount_last_day              + ","
            sql += "  to_date('" + shi_jian + " 15:00:00','yyyy-mm-dd hh24:mi:ss'),"  
            sql += "  " + str(price_last_day         ) + ","
            sql += "  " + str(zhang_die              ) + ","
            sql += "  " + str(zhang_die_rate         ) + " "  
            sql += ")"
            
            try:
                cr.execute(sql)
            except Exception as e: 
                print(sql)
             
        time.sleep(1)
        db.commit()
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(now,code,"done")
    db.commit()        
    cr.close ()  
    db.close ()      
         
         
# 导入个股   
print("导入个股")      
codes,names = importStockList()
# codes = ["000002"]
# names = ["万科A"]
importStockDataDailyJQ(codes,names)

#导入指数
print("导入指数")
df = ts.get_index()
codes = df["code"].values
names = df["name"].values
importStockDataDaily(codes,names,asset='INDEX',adj='None')

print("导入完成")
ts.close_apis(conn=cons)
