'''
Created on 2017年9月25日

@author: moonlit

python Z:\StockAnalysis\sourceCode\TuShare\test\src\importAlpha101data2.py
'''


# import numpy as np
import pandas as pd
# from Alpha101 import WQ_Alphas_Analysis as aa
from Alpha101 import WQ_Alphas_Analysis as waa
import cx_Oracle
import getStockData as gsd
import math

def formatData(data):   
    
    test = pd.DataFrame()
    test["shi_jian"] = pd.to_datetime(data["shi_jian"])
    test["code"] = data["code"]
    test["max_price"] = data["max_price"]
    test = test.set_index(['code','shi_jian'])
    max_price=test.unstack(level=0)
    max_price=max_price["max_price"]
    
    test = pd.DataFrame()
    test["shi_jian"] = pd.to_datetime(data["shi_jian"])
    test["code"] = data["code"]
    test["min_price"] = data["min_price"]
    test = test.set_index(['code','shi_jian'])
    min_price=test.unstack(level=0)    
    min_price=min_price["min_price"]
    
    test = pd.DataFrame()
    test["shi_jian"] = pd.to_datetime(data["shi_jian"])
    test["code"] = data["code"]
    test["price"] = data["price"]
    test = test.set_index(['code','shi_jian'])
    price=test.unstack(level=0)       
    price=price["price"] 
    
    test = pd.DataFrame()
    test["shi_jian"] = pd.to_datetime(data["shi_jian"])
    test["code"] = data["code"]
    test["return"] = data["return"]
    test = test.set_index(['code','shi_jian'])
    return_=test.unstack(level=0)    
    return_=return_["return"]
    
    test = pd.DataFrame()
    test["shi_jian"] = pd.to_datetime(data["shi_jian"])
    test["code"] = data["code"]
    test["open"] = data["price_today_open"]
    test = test.set_index(['code','shi_jian'])
    open_=test.unstack(level=0)  
    open_=open_["open"]
#     print(open_)
    
    test = pd.DataFrame()
    test["shi_jian"] = pd.to_datetime(data["shi_jian"])
    test["code"] = data["code"]
    test["value"] = data["amount"]
    test = test.set_index(['code','shi_jian'])
    amount=test.unstack(level=0)  
    amount=amount["value"]
    
    test = pd.DataFrame()
    test["shi_jian"] = pd.to_datetime(data["shi_jian"])
    test["code"] = data["code"]
    test["volume"] = data["vol"] 
    test = test.set_index(['code','shi_jian'])
    vol=test.unstack(level=0)
    vol = vol["volume"]
 
    
    test = pd.DataFrame()
    test["shi_jian"] = pd.to_datetime(data["shi_jian"])
    test["code"] = data["code"]
    test["cap"] = data["market_cap"]
    test = test.set_index(['code','shi_jian'])
    market_cap=test.unstack(level=0)  
    market_cap=market_cap["cap"]

    data = {'high'  : max_price       ,     
            'low'   : min_price       , 
            'close' : price           ,
            'return': return_         ,
            'open'  : open_,
            'value' : amount,
            'volume': vol,
            'cap'   : market_cap,
            "stop"  : pd.DataFrame([]),
            } 
    return data

pd.DataFrame



# data,tray_dates = gsd.get_stock_data_daily_101(begin_time="2006-01-04" , end_time="2017-09-22")
data,tray_dates = gsd.get_stock_data_daily_101(begin_time="2015-06-01" , end_time="2017-09-22")
data            = formatData(data= data)
tray_dates      = tray_dates["shi_jian"].values

all_fieldName = []
all_alpha = []
for aid in range(1,102) :
# for aid in range(68,102) :
    aid = ("000" + str(aid))[-3:]
    Alphas=waa.factor_cal(data,aid)  
    try :
#         print(Alphas)
        if Alphas == "id not found":
            continue
    except:
        pass
        
    fieldName = "ALPHA_" + aid
    
    all_fieldName.append(fieldName)       
    all_alpha.append(Alphas)
    print(fieldName , " done")
     

codes = gsd.get_code_list()
codes = codes["code"].values
# codes = ['600668','600009']
    
db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
cr=db.cursor()
for code in codes :
    
#     if code not in not_done :
#         print("code:",code , "skip")
#         continue

#     if code in done :
#         print("code:",code , "skip")
#         continue
    
    for tray_date in tray_dates :
        count = 0
        sql  = "update tb_stock_alpha101 set " 
        for fieldName,alpha in zip(all_fieldName,all_alpha) : 

            try :
                code_data = alpha[code]
            except:
                continue;
#             
#             temp = alpha[alpha.index == tray_date]
#             print(temp)
            
            shi_jian = str(tray_date)[:10]
            value = code_data[code_data.index == tray_date].values
            
            if math.isinf(value) or math.isnan(value) :
                continue            
            
            sql += fieldName +"=" + str(value[0]) + "," 
            count += 1

        if count <1 :
            continue
        
        sql = sql[:-1]
        sql += " where code = '" + code + "' and shi_jian = to_date('" + shi_jian + " 15:00:00','yyyy-mm-dd hh24:mi:ss')"                   
#         print(sql)    
        try : 
            cr.execute(sql)
        except:
            f = open('z:/sqlErr.txt','a')
            f.writelines(sql +"\n")
            print("err:" + sql)     
        
    print("code:",code , "done")
    db.commit()
    
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

