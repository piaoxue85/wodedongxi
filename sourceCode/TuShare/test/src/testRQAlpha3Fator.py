from rqalpha.api import *
import os
import sys
import tushare
import talib as ta
import cx_Oracle   
import pandas as pd
import numpy as np

# import getStockData as gsd
  
# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -d D:\rqalpha\bundle -s 2017-01-01 -e 2017-07-28 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -d D:\rqalpha\bundle -s 2007-10-01 -e 2017-07-28 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha update_bundle -d D:\rqalpha\

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -d z:\rqalpha\bundle -s 2007-01-01 -e 2017-07-28 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -d z:\rqalpha\bundle -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 400000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle -d Z:\rqalpha\


# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -d z:\rqalpha\bundle -s 2017-01-01 -e 2017-09-22 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -d z:\rqalpha\bundle -s 2007-10-04 -e 2017-08-04 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -d z:\rqalpha\bundle -s 2007-10-04 -e 2007-11-04 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha3Fator.py -d z:\rqalpha\bundle -s 2008-11-01 -e 2017-09-01 -o result.pkl --plot --progress --account stock 400000 --benchmark 000016.XSHG



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
    

    # 每月的第一个交易日查询以下财务数据，以确保可以拿到最新更新的财务数据信息用来调整仓位
    scheduler.run_monthly(query_fundamental, tradingday=1)
    
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
    pass
    
def query_fundamental(context, bar_dict):
    print(str(context.now)[0:10])

# print("持仓",context.portfolio.positions)    
    


