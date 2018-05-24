from rqalpha.api import *
import os
import sys
import tushare
import talib as ta
import cx_Oracle   
import pandas as pd
import numpy as np

# import getStockData as gsd

# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaMA8.py -d D:\rqalpha\bundle -s 2017-01-01 -e 2017-07-28 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaMA8.py -d D:\rqalpha\bundle -s 2007-10-01 -e 2017-07-28 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha update_bundle -d D:\rqalpha\

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMA8.py -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMA8.py -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMA8.py -d z:\rqalpha\bundle -s 2007-01-01 -e 2017-07-28 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMA8.py -d z:\rqalpha\bundle -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle -d Z:\rqalpha\


# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMA8.py -d z:\rqalpha\bundle -s 2017-01-01 -e 2017-03-10 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMA8.py -d z:\rqalpha\bundle -s 2007-12-04 -e 2017-08-02 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG



# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    
    context.alldate = pd.DataFrame([])
    strategy_file_path = context.config.base.strategy_file
    sys.path.append(os.path.realpath(os.path.dirname(strategy_file_path)))

#     context.s1 = "000725.XSHE"
#     context.s1 = "000016.XSHG"

    
    context.returns  = 0.0
    context.count    = 0
    context.fromtype = 0 
    context.buyPrice = 0.0
    context.buyTime  = "" 
    
#     import getStockData as gsd 
#     context.list = gsd.get_code_list()
#     context.list = list["code"].values   
    
    
def need_sell(codes =[],today="")  :
    import getStockData as gsd
    selector = []

    for code in codes :
        data  = gsd.get_stock_data_daily_rqalpha_ma8(code[:6],daysago=30,endtime=str(today))
        
        if len(data) <2 :        
            continue
        
        ma6   = data["ma6"  ].values
        ma12  = data["ma12" ].values
        ma20  = data["ma20" ].values
        ma30  = data["ma30" ].values
        ma45  = data["ma45" ].values
        ma60  = data["ma60" ].values
        ma125 = data["ma125"].values
        ma250 = data["ma250"].values
        
        count = 0        
        if ma6  [-1] < ma6  [-2] : count += 1
        if ma12 [-1] < ma12 [-2] : count += 1
        if ma20 [-1] < ma20 [-2] : count += 1
        if ma30 [-1] < ma30 [-2] : count += 1
        if ma45 [-1] < ma45 [-2] : count += 1
        if ma60 [-1] < ma60 [-2] : count += 1
        if ma125[-1] < ma125[-2] : count += 1
        if ma250[-1] < ma250[-2] : count += 1        
        if count >6 : 
            selector.append(code)     

    return selector
     
    
def getListToBuy( now="" ,buy_count = 20):
    import getStockData as gsd
#   import ta_lib_data as ta1

    df = gsd.get_stock_data_daily_rqalpha_ma8_all( endtime=str(now))
   
    codes = df["code"].values
    
    buy_list = []
        
    for code in codes :
#         if code[:6] == "601600" :
#             code = code 
        
#         df = gsd.get_stock_data_Quarterly_rqalpha(code= code , end=str(now))
#         df = df.astype(dtype='float64')
#         
#         kdj_k = df["kdj_k"].values
#         kdj_d = df["kdj_d"].values
#         kdj_j = df["kdj_j"].values
#         
#         if len(kdj_k) < 1 :
#             continue
#         
#         if kdj_k[-1] == 0.0 and kdj_d[-1] == 0.0 and kdj_j[-1] == 0.0 : 
#             continue
#         
#         if kdj_k[-1] > 20 or kdj_d[-1] > 20 or kdj_j[-1] > 20 :
#             continue  

        df = gsd.get_stock_data_daily_rqalpha_ma8(code, endtime=str(now),daysago=45)
        if len(df) <20:
            continue
                
        ma6   = df["ma6"  ].values
        ma12  = df["ma12" ].values
        ma20  = df["ma20" ].values
        ma30  = df["ma30" ].values
        ma45  = df["ma45" ].values
        ma60  = df["ma60" ].values
        ma125 = df["ma125"].values
        ma250 = df["ma250"].values
        
        if (ma250[-1]-ma250[-20])/ma250[-20] >= 0.01 :
#             print(str(ma250[-1]) ,
#                   str(ma250[-20]),
#                   str((ma250[-1]-ma250[-20])/ma250[-20])
#                   )
            continue         
        
        count = 0
        if ma6  [-1] > ma6  [-2] : count += 1
        if ma12 [-1] > ma12 [-2] : count += 1
        if ma20 [-1] > ma20 [-2] : count += 1
        if ma30 [-1] > ma30 [-2] : count += 1
        if ma45 [-1] > ma45 [-2] : count += 1
        if ma60 [-1] > ma60 [-2] : count += 1
        if ma125[-1] > ma125[-2] : count += 1
        if ma250[-1] > ma250[-2] : count += 1 

        if count < 5 : 
            continue
        
        buy_list.append(code)
        if len(buy_list) >= buy_count :
            break
         
#     print(buy_list)
    return buy_list
          
def getRQCode(code=""):
    rqcode = code
    if code[0] == "6" :
        rqcode += ".XSHG"
    else:
        rqcode += ".XSHE"
    
    return rqcode

def get_stock_data_daily_rqalpha_ma8_all_day():
    import getStockData as gsd
    return gsd.get_stock_data_daily_rqalpha_ma8_all_day()

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    if len(context.alldate) <1 :
        context.alldate = get_stock_data_daily_rqalpha_ma8_all_day()
        
    df = context.alldate
#     cur_position = 0.0                
    
    today     = str(context.now)[0:10]
    df = df[(df["shi_jian"]==today)]
    
    buy_count = 20
    print("持仓",context.portfolio.positions)
    if len(df) >0 :
    
        selllist= need_sell(codes = context.portfolio.positions,today = today)
        
        for code in selllist :
            res = order_target_value(code, 0)  
            print("卖出：",code)
            
    #         print(res)
       
        can_buy_num = buy_count - len(context.portfolio.positions)    
        if can_buy_num >0 :
            buylist = getListToBuy( now = today ,buy_count = buy_count)
            if len(buylist)>0 :
                buylist = buylist[:can_buy_num]
                print("positions",context.portfolio.positions)
                buylist = list(context.portfolio.positions) + buylist
                print("buylist",buylist)
                for code in buylist :
                    try :
                        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
                        code =getRQCode(code=code[:6])
                        res = order_target_percent(code, 1/len(buylist))
                        print("买入：",code)  
                    except:   
                        print("buy err " , code , today)
            
#     print(context.portfolio.positions)
    print("数量",len(context.portfolio.positions))
    print(context.portfolio.total_returns)     
    
    
# print("持仓",context.portfolio.positions)    
    


