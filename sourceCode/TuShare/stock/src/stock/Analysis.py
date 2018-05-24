'''
Created on 2016年12月27日

@author: moonlit
'''
import pandas as pd
import talib as ta
import numpy as np
from telnetlib import theNULL

def test():
    from   sqlalchemy import create_engine
    engine = create_engine("oracle://c##stock:didierg160@myoracle")
    echo = True 
    data = pd.read_sql_query("select to_char(shi_jian,'yyyy-mm-dd') SHI_JIAN,PRICE_TODAY_OPEN,MAX_PRICE,MIN_PRICE,PRICE from tb_stock_data_daily where code='sh000001' ORDER BY SHI_JIAN ASC",con = engine)

    res = ta.CDL3INSIDE (data["price_today_open"].values ,
                            data["max_price"].values ,
                            data["min_price"].values ,
                            data["price"].values,
                            ) 
            
    data["res"] = res
    data = data.drop('price_today_open',axis=1)
    data = data.drop('max_price',axis=1)
    data = data.drop('min_price',axis=1)
    data = data.drop('price',axis=1)
    print(data)   
    
    res = data.as_matrix() 
    print(res)       
    np.savetxt("d:\B.txt", res ,fmt='%s    %s',delimiter=' ', newline='\n',header='')
    #np.savetxt(fname="d:\B.txt", X=res ) 
    
def testARTTrading():
    from   sqlalchemy import create_engine
    engine = create_engine("oracle://c##stock:didierg160@myoracle")
    dfCodes =   pd.read_sql_query("select code from tb_stock_list ",con = engine)
    arrCodes = dfCodes.as_matrix()
    
    for stock in arrCodes:
        # 获取股票的数据
        sql = "select to_char(shi_jian,'yyyy-mm-dd') SHI_JIAN,PRICE_TODAY_OPEN,MAX_PRICE,MIN_PRICE,PRICE from tb_stock_data_daily where code='"+stock[0]+"' and shi_jian >= sysdate-40 ORDER BY SHI_JIAN asc"
        xxx = pd.read_sql_query(sql,con = engine)
        if len(xxx['max_price'].values) <5 :
            continue
         
        h = xxx
        # 创建ATR买卖信号，包括最高价，最低价，收盘价和参数timeperiod
        # 注意：ATR函数使用的price必须是narray
        atr = ta.ATR(h['max_price'].values,h['min_price'].values,h['price'].values, timeperiod=14)[-1]
        # 获取当前股票的数据
#         current_position = context.portfolio.positions[stock].amount
        current_position=1000;
        # 获取当前股票价格
        current_price = prev_close = h['price'].values[-1]
        #获取四天前的收盘价
        prev_close = h['price'].values[-5]
        #如果当前价格比之前的价格高一个ATR的涨幅，买入股票
        upside_signal = current_price - (prev_close + atr)
        #如果之前的价格比当前价格高一个ATR的涨幅，卖出股票
        downside_signal = prev_close - (current_price + atr)
        # 当downside_signal大于0，且拥有的股票数量大于0时，卖出所有股票
        if downside_signal > 0 :
            print("sell,"+stock[0] + "," +str(h['shi_jian'].values[-1])+","+str(h['price'].values[-1]))
            
        # 当upside_signal大于0, 且拥有的股票数量为0时，则全仓买入
        if upside_signal > 0 :
            print("buy,"+stock[0] + "," +str(h['shi_jian'].values[-1])+","+str(h['price'].values[-1]))
    