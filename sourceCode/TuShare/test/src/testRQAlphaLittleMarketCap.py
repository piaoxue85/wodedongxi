from rqalpha.api import *
import os
import sys
import tushare
import talib as ta
import cx_Oracle   
import pandas as pd
import numpy as np

# import getStockData as gsd

# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -d D:\rqalpha\bundle -s 2017-01-01 -e 2017-07-28 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -d D:\rqalpha\bundle -s 2007-10-01 -e 2017-07-28 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha update_bundle -d D:\rqalpha\

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -d z:\rqalpha\bundle -s 2007-01-01 -e 2017-07-28 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -d z:\rqalpha\bundle -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle -d Z:\rqalpha\


# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -d z:\rqalpha\bundle -s 2017-01-01 -e 2017-09-22 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -d z:\rqalpha\bundle -s 2007-10-04 -e 2017-08-04 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -d z:\rqalpha\bundle -s 2007-10-04 -e 2007-11-04 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaLittleMarketCap.py -d z:\rqalpha\bundle -s 2008-11-01 -e 2017-09-01 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG



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
    
    
def need_sell(codes ,codelist,today = ""):
    selector = []
    
    for code in codes :
        df = codelist[(codelist["code"]== code[:6])]
        if len(df) < 1 :
            selector.append(code)
    return selector
     
    
def getListToBuy(positions ,codelist ):

    buy_list = []
    for code in codelist["code"].values :
        if len(positions) > 0 :
            for poscode in positions :
                if code[:6] != poscode[:6] :
                    buy_list.append(code)
                    break 
        else :
            buy_list.append(code)  
    return buy_list
          
def getRQCode(code=""):
    rqcode = code
    if code[0] == "6" :
        rqcode += ".XSHG"
    else:
        rqcode += ".XSHE"
    
    return rqcode

def get_stock_data_daily_rqalpha_lmc_all_day():
    import getStockData as gsd
    return gsd.get_stock_data_daily_rqalpha_lmc_all_day()

def get_stock_data_daily_rqalpha_lmc_all(date=""):
    import getStockData as gsd
    return gsd.get_stock_data_daily_rqalpha_lmc_all(date)

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    if len(context.alldate) <1 :        
        context.alldate = get_stock_data_daily_rqalpha_lmc_all_day()
               
    df = context.alldate          
#     print("context.alldate",context.alldate)  
    today     = str(context.now)[0:10]
     
    df1 = df[(df["shi_jian"]==today)]
    buy_count = 20
    
    print("持仓",context.portfolio.positions)

    if len(df1) >0 : 
        
        codelist = get_stock_data_daily_rqalpha_lmc_all(date=today)
        codelist = codelist[:buy_count]
        selllist= need_sell(codes = context.portfolio.positions,codelist=codelist,today = today)
        
        for code in selllist :
            res = order_target_value(code, 0)  
            print("卖出：",code)
            
    #         print(res)
         
        buylist = getListToBuy(positions = context.portfolio.positions,codelist = codelist)
        if len(buylist)>0 :
#             print("positions",context.portfolio.positions)
            print("buylist",buylist)
            for code in buylist :
                try :
                    # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
                    code =getRQCode(code=code[:6])
                    res = order_target_percent(code, 1/buy_count)
                    print("买入：",code)  
                except:   
                    print("buy err " , code , today)
            
#     print(context.portfolio.positions)
    print("数量",len(context.portfolio.positions))
    print(context.portfolio.total_returns)     
    
    
# print("持仓",context.portfolio.positions)    
    


