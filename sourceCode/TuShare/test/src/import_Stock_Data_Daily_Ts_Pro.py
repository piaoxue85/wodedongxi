'''
Created on 2018年11月28日
python Z:\StockAnalysis\sourceCode\TuShare\test\src\import_Stock_Data_Daily_Ts_Pro.py
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
import time

#获取连接备用
print(ts.__version__)
ts.set_token("23bb6cd2f77e39ea16ca656f2fc1ec2aaaeb6d84aed8369030be7ee8")

cons = ts.pro_api()
  
def toTSCode(code=""):
    if code[0 ] == "6" :
        code += ".SH"
    else :
        code += ".SZ"
    return code

def importStockList():
    global cons
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
            time.sleep(1)
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
        
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
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

def my_Pro_bar(ts_code ,pro_api , start_date="", end_date="",adj="adj",asset=""):
        
    ts_code = toTSCode(ts_code)
    
    if start_date=="" :
        start_date="1990-12-19"   
                
    start_date = start_date.replace("-","")
    end_date   = end_date.replace("-","")
        
    dfAll,df1,df2,df3,df4,df5 = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    
    if start_date>="19901219" and  start_date<="19980101" :
        df1 = ts.pro_bar(ts_code, pro_api=pro_api, adj=adj,asset=asset, start_date=start_date, end_date="19980101",retry_count = 2)
            
        if str(df1) != "None" :
            if len(df1) > 0 :
                dfAll = dfAll.append(df1)
            
        start_date = "19980102"
    
    if start_date>="19980102" and  start_date<="20030101" :        
        df2 = ts.pro_bar(ts_code, pro_api=cons, adj=adj,asset=asset, start_date=start_date, end_date="20030101",retry_count = 2)
           
        if str(df2) != "None" :
            if len(df2) > 0 :
                dfAll = dfAll.append(df2)
                             
        start_date = "20030102"
        
    if start_date>="20030102" and  start_date<="20080101" :        
        df3 = ts.pro_bar(ts_code, pro_api=cons, adj=adj,asset=asset, start_date=start_date, end_date="20080101",retry_count = 2)


        if str(df3) != "None" :
            if len(df3) > 0 :
                dfAll = dfAll.append(df3)            
                       
        start_date = "20080102"     
        
    if start_date>="20080102" and  start_date<="20130101" :   
        df4 = ts.pro_bar(ts_code, pro_api=cons, adj=adj,asset=asset, start_date=start_date, end_date="20130101",retry_count = 2)

        if str(df4) != "None" :
            if len(df4) > 0 :
                dfAll = dfAll.append(df4)                   
        
        start_date = "20130102"  
        
    if start_date>="20130102" and  start_date<="20180101" :
        df5 = ts.pro_bar(ts_code, pro_api=cons, adj=adj,asset=asset, start_date=start_date, end_date="20180101",retry_count = 2) 
            
        if str(df5) != "None" :
            if len(df5) > 0 :
                dfAll = dfAll.append(df5)                   
        start_date = "20180102"                   
        
    df = ts.pro_bar(ts_code, pro_api=cons, adj=adj,asset=asset, start_date=start_date, end_date='',retry_count = 2)
    
    if str(df) != "None" :
        if len(df) > 0 :
            dfAll = dfAll.append(df)     
    
    return dfAll
    
def importStockDataDaily(codes= [],names=[],asset='E',adj='qfq'):
    global cons
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
            
            ####time.sleep(1)
        
        start_date = gsd.get_code_max_shi_jian(code=code + code_tail).replace("-","") 
               
        if start_date == "None" :
            start_date = ""
            
        tsFaile = 1
            
        while tsFaile !=0 :
            try:
                #if tsFaile >=2 :
                #    cons = ts.get_apis()                
                #df = ts.bar(code, conn=cons, adj=adj,asset=asset, start_date=start_date, end_date='',retry_count = 2)
                #df = ts.bar(code, conn=cons, adj=adj,asset=asset, start_date="", end_date="2018-06-13",retry_count = 2)
                df = my_Pro_bar(code, pro_api=cons, adj=adj,asset=asset, start_date=start_date, end_date='')
                tsFaile = 0
            except Exception as e:
#                 ts.close_apis(conn=cons)
                time.sleep(1)
                print(code,start_date ,"importStockDataDaily fail:",tsFaile,e)
                if tsFaile <=3  :
                    tsFaile += 1
                else:
                    continue
                
        if tsFaile > 0 :
            continue
        
        try :                                 
            df["datetime"] = df.index
        except Exception as e: 
            print("code:",code,e)
            continue
        
        df = df.reset_index(drop=True)
        df_shift = df.shift(-1)
                
        for row , row_s in zip(df.itertuples(),df_shift.itertuples()): 
            if round(float(getattr(row,"vol" )))<1 :
                continue                                
                                 
#             if len(getattr(row,"datetime")) <10 :
#                 continue
                    
            shi_jian = str(getattr(row,"datetime"))[0:10]
            
            if len(shi_jian)<8 :
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
            sql += " '" + str(getattr(row,"ts_code"    ))[:6] + code_tail+"',"
            sql += " '" + name +"',"
            sql += "  " + str(getattr(row,"open"    )) + ","
            sql += "  " + str(getattr(row,"close"   )) + ","
            sql += "  " + str(getattr(row,"high"    )) + ","
            sql += "  " + str(getattr(row,"low"     )) + ","
            sql += "  " + str(getattr(row,"vol"     )) + ","
            sql += "  " + str(getattr(row,"amount"  )) + ","
            sql += "  " + amount_last_day              + ","
            sql += "  to_date('" + shi_jian + " 15:00:00','yyyymmdd hh24:mi:ss'),"  
            sql += "  " + str(price_last_day         ) + ","
            sql += "  " + str(zhang_die              ) + ","
            sql += "  " + str(zhang_die_rate         ) + " "  
            sql += ")"
            
            try:
                cr.execute(sql)
            except Exception as e: 
                print(sql)
             
        ####time.sleep(1)
        db.commit()
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(now,code,"done")
    db.commit()        
    cr.close ()  
    db.close ()  
        
#是否除权
def isXR(code=""):
    global cons
    shi_jian = gsd.get_code_max_shi_jian(code)
    
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
                  
            data  = ts.pro_bar(toTSCode(code), pro_api=cons, adj='qfq', start_date=shi_jian.replace("-", ""), end_date=shi_jian.replace("-", ""),retry_count = 2)
#             data  = ts.bar(code, conn=cons, adj='qfq', start_date="1993-06-29", end_date="1995-06-30",retry_count = 2)
#             print("data",data)

            '''
            if len(data["close"].values)<1 :
                tsFaile += 1 
            else:
                tsFaile = 0
            '''                    
            if len(data)<1 :
                return False
            
            tsFaile = 0   
        except Exception as e:
            #获取连接备用
#             ts.close_apis(conn=cons)            
#             cons = ts.get_apis() 
            print(code,shi_jian ,"isXR fail:",tsFaile,e)
            time.sleep(1)
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
             
# 导入个股   
print("导入个股")      
codes,names = importStockList()
# codes = ["001872"]
# names = ["招商港口"]
importStockDataDaily(codes,names)

# #导入指数
# print("导入指数")
# df = ts.get_index()
# codes = df["code"].values
# names = df["name"].values
# importStockDataDailyZS(codes,names,asset='INDEX',adj='None')

print("导入完成")
# ts.close_apis(conn=cons)
