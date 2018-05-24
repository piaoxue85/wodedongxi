'''
Created on 2017年9月25日

@author: moonlit

python Z:\StockAnalysis\sourceCode\TuShare\test\src\importAlpha101data.py

'''


# import numpy as np
import pandas as pd
# from Alpha101 import WQ_Alphas_Analysis as aa
from Alpha101 import Alpha101_from_ricequant as ar
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
#     print(vol) 
#     print(vol.index)
#     print(vol.columns)  
    
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

unrealized = [
               '048',
               '058',
               '059',
               '063',
               '067',
               '069',
               '070',
               '076',
               '079',
               '080',
               '081',
               '082',
               '087',
               '089',
               '090',
               '091',
               '093',
               '097',
               '100',
             ]

# t = pd.DataFrame([1,2,0,3,np.nan , 4,5])
# t = t.rank(axis = 0,pct=True )

data = gsd.get_stock_data_daily_101(begin_time="2006-01-04" , end_time="2017-09-22")
code = data["code"]
returns = data["return"]

data = formatData(data= data)

alpha=ar.Alphas(data)  

db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
cr=db.cursor()

for aid in range(41,60) :
    Alphas=alpha.alpha(aid)
    try :
        if Alphas == "id not found":
            continue
    except:
        pass
    
    fieldName = "ALPHA_" + ("000" + str(aid))[-3:]
    codes = gsd.get_code_list()
    codes = codes["code"].values
    
    for code in codes :
        try :
            code_data = Alphas[code]
        except:
            continue;

        shi_jians=code_data.index.values
        values    = code_data.values
        for shi_jian , value in zip(shi_jians , values ):
            if math.isinf(value) or math.isnan(value) :
                continue
             
            shi_jian = str(shi_jian)[:10]
            sql  = "update TB_STOCK_ALPHA101 set " +fieldName +" =  " + str(value) 
            sql += " where code = '" + code + "' and shi_jian = to_date('" + shi_jian + " 15:00:00','yyyy-mm-dd hh24:mi:ss')"                        
            cr.execute(sql)        
        
        print("code:",code , "  alpha:" , aid , "done")
        db.commit()
    print("alpha",aid,"done")
    
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

