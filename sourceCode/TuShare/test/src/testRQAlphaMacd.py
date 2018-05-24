from rqalpha.api import *
import os
import sys
import tushare
import talib as ta
import cx_Oracle   
import pandas as pd
import numpy as np



# import getStockData as gsd

# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaMacd.py -d D:\rqalpha\bundle -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaMacd.py -d D:\rqalpha\bundle -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle -d D:\rqalpha\

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMacd.py -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMacd.py -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMacd.py -d z:\rqalpha\bundle -s 2007-10-19 -e 2017-07-19 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaMacd.py -d z:\rqalpha\bundle -s 2015-06-01 -e 2017-07-21 --stock-starting-cash 100000 --benchmark 000016.XSHG --plot
# rqalpha update_bundle -d Z:\rqalpha\

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
 
    strategy_file_path = context.config.base.strategy_file
    sys.path.append(os.path.realpath(os.path.dirname(strategy_file_path)))

#     context.s1 = "000725.XSHE"
    context.s1 = "000016.XSHG"

    # 设置这个策略当中会用到的参数，在策略中可以随时调用，这个策略使用长短均线，我们在这里设定长线和短线的区间，在调试寻找最佳区间的时候只需要在这里进行数值改动
    context.SHORTPERIOD = 20
    context.LONGPERIOD = 120
    
    context.returns  = 0.0
    context.count    = 0
    context.fromtype = 0 
    context.buyPrice = 0.0
    context.buyTime  = ""  


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    import getStockData as gsd
#     import ta_lib_data as ta1

    list = gsd.get_code_list()
    list = list["code"].values
    
    cur_position = 0.0
    
    for code in list :
        if code[0] == "6" :
            context.s1 = code+".XSHG"
        else:
            context.s1 = code+".XSHE"
        
        df = gsd.get_stock_data_daily_rqalpha(context.s1[0:6], end=str(context.now))
#         print("get_stock_data_daily_rqalpha")        
                
        df= df.astype(dtype='float64')
        
        if len(df) <100:
            continue 
        
        kdj_k = df["kdj_k"].values
        kdj_d = df["kdj_d"].values
        kdj_j = df["kdj_j"].values
        
        MACD = df["macd_macd"].values
        MA12 = df["ma12"].values
        MA20 = df["ma20"].values
        amount = df["amount"].values
#         print(df)
#         print(code,MACD)
        plot("MACD", MACD[-1])
        plot("MA12", MA12[-1])
        plot("MA20", MA20[-1])
          
    
        # 计算现在portfolio中股票的仓位
        cur_position =context.portfolio.positions[context.s1].quantity    
        # 计算现在portfolio中的现金可以购买多少股票
        shares = context.portfolio.cash / bar_dict[context.s1].close
#         max_price  = 0.0
#         drawdown   = 0.0
#         returnRate = 0.0
#         price      = [0.0]
#         if cur_position > 0:
#             returnRate = (bar_dict[context.s1].close - context.buyPrice)/context.buyPrice
#             df1        = gsd.get_stock_data_daily_rqalpha(context.s1[0:6], end=str(context.now))
#             price      = df1["price"].values        
#             max_price  = gsd.get_stock_data_max_price_rqalpha(context.s1[0:6],start= str( context.buyTime ) ,end= str( context.now ))
#             drawdown   = ( max_price - price[-1])/max_price 
#         print("drawdown:%f   maxprice:%f    price:%f"% ( drawdown , max_price , price[-1]))
#         print(returnRate)

        if MA12[-2] < MA20[-2] and cur_position > 0 :
            # 进行清仓
            selres = order_target_value(context.s1, 0)  
            cur_position = context.portfolio.positions[context.s1].quantity    
            if cur_position <= 0 :
                context.buyPrice = 0.0
                context.buyTime  = ""
                print("已清仓 ")  
                   
            return 
        
        if (MA12[-2] > MA20[-2] and MA12[-3] > MA20[-3] and MA12[-4] > MA20[-4] and cur_position <=0  ):
            if (MACD[-4] >0 and MACD[-3]>MACD[-4] and MACD[-2]>MACD[-3] ) :
                if (amount[-5]*1.5 <amount[-4] and abs((amount[-3] - amount[-4])/amount[-4]) <= 0.3 and  abs((amount[-2] - amount[-3])/amount[-3]) <= 0.3):
                # 满仓入股
                    order_shares(context.s1, shares)    
                    print("已买入")     
                       
            cur_position = context.portfolio.positions[context.s1].quantity 
            
            if cur_position >0 :        
                context.buyPrice = bar_dict[context.s1].close
                context.buyTime  = context.now         
                
    print("仓位 ：%f"%cur_position)
#     if str(context.now)[0:10] == "2017-07-21" :
#         print(type(context.portfolio))
#         print(str(context.portfolio.total_returns))

