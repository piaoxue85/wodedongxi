'''
Created on 2017年6月3日
@author: moonlit
'''

from BigQuantTrade import TradeSmallMarketValue
import BigQuantImportRank as importR
import numpy as np

def getRank(rank , buy_black):
    rank_new = []
    for r in rank:
        if r in buy_black :
            continue
        rank_new.append(r)
    
    return rank_new

def getweights(rank):
    if len(rank) == 0 :
        return []
    
    stockCount = len(rank)
    weights = []
    
    for i_ in range(stockCount):
        weights.append(1/stockCount)
    
    return weights
    
buy_black   = []      

print("#-------------------------------------------------------------------庄华-----------------------------------------------------------------------------------------------")        
rank = ['603788.SHA' ,'300251.SZA' ,'600332.SHA']
rank = getRank(rank = rank , buy_black=buy_black)
sell_black = []
T = TradeSmallMarketValue(user_name = "庄华",start_date = "2017-08-01" , op_date = "" ,weights = getweights(rank))     
T.can_buy_GEM = True  
# shi_jian  ="2017-08-02"
shi_jian  = T.get_op_date() 
T.op_date = shi_jian

importR.importRank(prank = rank, shi_jian = shi_jian)
print(T.user,"总市值", T.portfolio_value())
sell_list = T.sell(sell_black)
print(sell_list)
buy = T.buy(buy_black)
print(buy)

print("#---------------------------------------------------------------龚雯-----------------------------------------------------------------------------------------------------")
rank = ['603788.SHA', '600332.SHA']
rank = getRank(rank = rank , buy_black=buy_black)
sell_black = [
              "002307",
              "600419",
              ]

T = TradeSmallMarketValue(user_name = "龚雯",start_date = "2017-08-01" , op_date = shi_jian ,weights = getweights(rank)) 
T.can_buy_GEM = False   
T.op_date = shi_jian
importR.importRank(prank = rank, shi_jian = shi_jian)
print(T.user,"总市值", T.portfolio_value())
sell_list = T.sell(sell_black)
print(sell_list)
buy = T.buy(buy_black)
print(buy)

