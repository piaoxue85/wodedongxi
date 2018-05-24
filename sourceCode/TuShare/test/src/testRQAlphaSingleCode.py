'''
Created on 2017年5月15日

@author: moonlit
'''

#所有的股票代码，一个一个测试
from rqalpha.api import *
import os
import sys
import tushare
import talib as ta
import cx_Oracle   
import pandas as pd
import numpy as np



# import getStockData as gsd

# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaSingleCode.py -d D:\rqalpha\bundle -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlphaSingleCode.py -d D:\rqalpha\bundle -s 2015-06-01 -e 2017-05-05 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha update_bundle -d D:\rqalpha\

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaSingleCode.py -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 000002.XSHE --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaSingleCode.py -s 2015-06-01 -e 2017-05-05 --stock-starting-cash 100000 --benchmark 000002.XSHE --plot
# rqalpha update_bundle

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaSingleCode.py -d z:\rqalpha\bundle -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlphaSingleCode.py -d z:\rqalpha\bundle -s 2015-06-01 -e 2017-05-05 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha update_bundle -d Z:\rqalpha\



# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    
    strategy_file_path = context.config.base.strategy_file
    sys.path.append(os.path.realpath(os.path.dirname(strategy_file_path)))
    
    import getStockData as gsd
    
    context.s1, context.max_id , context.cur = gsd.get_stock_code_rqalpha()   
    print(context.s1) 

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
    
    print("context.fromtype %d"%context.fromtype)
    if context.fromtype == 0 :  #周线数据
        df = gsd.get_stock_data_weekly_rqalpha(context.s1[0:6], end=str(context.now))
        print("get_stock_data_weekly_rqalpha")
    
    if context.fromtype == 1 :  #月线数据
        df = gsd.get_stock_data_monthly_rqalpha(context.s1[0:6], end=str(context.now))
        print("get_stock_data_monthly_rqalpha")
        
    if context.fromtype == 2 :  #季线数据
        df = gsd.get_stock_data_Quarterly_rqalpha(context.s1[0:6], end=str(context.now))
        print("get_stock_data_Quarterly_rqalpha")
            
    df= df.astype(dtype='float64')

    kdj_k = df["kdj_k"].values
    kdj_d = df["kdj_d"].values
    kdj_j = df["kdj_j"].values

    try :
        plot("k", kdj_k[-1])
        plot("d", kdj_d[-1])
        plot("j", kdj_j[-1])

        # 计算现在portfolio中股票的仓位
        cur_position = context.portfolio.positions[context.s1].quantity
        # 计算现在portfolio中的现金可以购买多少股票
        shares = context.portfolio.cash / bar_dict[context.s1].close
        max_price  = 0.0
        drawdown   = 0.0
        returnRate = 0.0
        price      = [0.0]
        if cur_position > 0:
            returnRate = (bar_dict[context.s1].close - context.buyPrice)/context.buyPrice
            df1        = gsd.get_stock_data_daily_rqalpha(context.s1[0:6], end=str(context.now))
            price      = df1["price"].values        
            max_price  = gsd.get_stock_data_max_price_rqalpha(context.s1[0:6],start= str( context.buyTime ) ,end= str( context.now ))
            drawdown   = ( max_price - price[-1])/max_price 
        print("drawdown:%f   maxprice:%f    price:%f"% ( drawdown , max_price , price[-1]))
        print(returnRate)
    
        if  ( ( drawdown >= 0.2 and kdj_j[-1] < kdj_k[-1] and kdj_k[-1] < kdj_d[-1] ) or returnRate<=-0.10) and cur_position > 0 :
            # 进行清仓
            selres = order_target_value(context.s1, 0)  
            cur_position = context.portfolio.positions[context.s1].quantity    
            if cur_position <= 0 :
                context.buyPrice = 0.0
                context.buyTime  = ""
                print("已清仓 ")
    
                if returnRate<=-0.10 and context.fromtype < 2:
                #if  context.fromtype < 2:
                    context.fromtype = context.fromtype + 1
    #                 if context.fromtype > 2 :
    #                     context.fromtype = 0          
            return 
        
        if (kdj_k[-3] <= 14 and cur_position <=0  ):
            if context.fromtype == 0 :        
                # 满仓入股
                order_shares(context.s1, shares)
                print("已买入")
            elif kdj_k[-1] >= kdj_k[-2] and kdj_k[-2] >= kdj_k[-3]:
            #elif kdj_j[-1] >= kdj_k[-1] and kdj_k[-1] >= kdj_d[-1]:
                # 满仓入股
                order_shares(context.s1, shares)    
                print("已买入")            
            cur_position = context.portfolio.positions[context.s1].quantity 
            if cur_position >0 :        
                context.buyPrice = bar_dict[context.s1].close
                context.buyTime  = context.now         
    #     context.count = context.count + 1
        print("仓位 ：%f"%cur_position)

    except Exception as e :  
        print( e )
    
    finally: 
        if str(context.now)[0:10] == "2014-06-23" :
            set_ = gsd.set_test_res_rqalpha(code=context.s1 , 
                                            total_returns = context.portfolio.total_returns , 
                                            last_fromtype=context.fromtype , 
                                            start_time= "2007-10-19", 
                                            end_time  = "2014-06-23"
                                            )
            set_ = gsd.move_to_next_cur_rqalpha(max_id = context.max_id , cur = context.cur)
            print(str(context.portfolio.total_returns) , set_ , context.max_id , context.cur )
