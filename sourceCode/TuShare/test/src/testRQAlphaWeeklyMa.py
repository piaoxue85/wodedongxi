'''
Created on 2017年5月15日

@author: moonlit
'''

# 所有的股票代码，一个一个测试
# http://www.360doc.com/content/17/0525/07/34893884_657052875.shtml
from rqalpha.api import *
import os
import sys
import tushare
import talib as ta
import cx_Oracle   
import pandas as pd
import numpy as np

# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaWeeklyMa.py -d D:\rqalpha\bundle -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaWeeklyMa.py -d D:\rqalpha\bundle -s 2015-06-19 -e 2017-05-05 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha update_bundle -d D:\rqalpha\


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    
    strategy_file_path = context.config.base.strategy_file
    sys.path.append(os.path.realpath(os.path.dirname(strategy_file_path)))
        
    context.s1 = "600105.XSHG" 
    print(context.s1) 
    
    context.returns = 0.0
    context.count = 0
    context.fromtype = 0 
    context.buyPrice = 0.0
    context.buyTime = ""  


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    import getStockData as gsd
    
    df = gsd.get_stock_data_weekly_rqalpha(context.s1[0:6], end=str(context.now))
    df = df.astype(dtype='float64')
    print("get_stock_data_weekly_rqalpha")
    
    df['MA7' ] = ta.MA(df['price'].values, timeperiod=7 , matype=0)
    df['MA14'] = ta.MA(df['price'].values, timeperiod=14, matype=0)   
    df['MA5' ] = ta.MA(df['price'].values, timeperiod=5 , matype=0)
    df['MA13'] = ta.MA(df['price'].values, timeperiod=13, matype=0)
    df['MA34'] = ta.MA(df['price'].values, timeperiod=34, matype=0)     
    
    MA7 = df['MA7' ].values
    MA14 = df['MA14'].values
    MA5 = df['MA5' ].values
    MA13 = df['MA13'].values
    MA34 = df['MA34'].values
    amount = df['amount'].values
          
    kdj_k = df["kdj_k"].values
    kdj_d = df["kdj_d"].values
    kdj_j = df["kdj_j"].values          
          
    try :
        plot('MA7' , MA7   [-1])
        plot('MA14', MA14  [-1])
        plot('MA5' , MA5   [-1])
        plot('MA13', MA13  [-1])
        plot('MA34', MA34  [-1])
#         plot('amount', amount[-1]/1000000)         

        # 计算现在portfolio中股票的仓位
        cur_position = context.portfolio.positions[context.s1].quantity
        # 计算现在portfolio中的现金可以购买多少股票
        shares = context.portfolio.cash / bar_dict[context.s1].close
        max_price = 0.0
        drawdown = 0.0
        returnRate = 0.0
        price = [0.0]
        if cur_position > 0:
            returnRate = (bar_dict[context.s1].close - context.buyPrice) / context.buyPrice
            df1 = gsd.get_stock_data_daily_rqalpha(context.s1[0:6], end=str(context.now))
            price = df1["price"].values        
            max_price = gsd.get_stock_data_max_price_rqalpha(context.s1[0:6], start=str(context.buyTime) , end=str(context.now))
            drawdown = (max_price - price[-1]) / max_price 
            
        print("drawdown:%f   maxprice:%f    price:%f" % (drawdown , max_price , price[-1]))
        print(returnRate)
    
        if  (MA7[-1] < MA14[-1] or returnRate < -0.10) and cur_position > 0 :
            # 进行清仓
            selres = order_target_value(context.s1, 0)  
            cur_position = context.portfolio.positions[context.s1].quantity    
            if cur_position <= 0 :
                context.buyPrice = 0.0
                context.buyTime = ""
                print("已清仓 ")
         
            return 
        
        if (((MA7[-1] > MA14[-1] and kdj_k[-1] < 40)or amount[-1] >= amount[-2] * 4.0)  and cur_position <= 0):
            order_shares(context.s1, shares)
            print("已买入")         
            cur_position = context.portfolio.positions[context.s1].quantity 
            if cur_position > 0 :        
                context.buyPrice = bar_dict[context.s1].close
                context.buyTime = context.now         
    #     context.count = context.count + 1
        print("仓位 ：%f" % cur_position)

    except Exception as e :  
        print(e)
    
    finally: 
        print("total_returns" , str(context.portfolio.total_returns))
