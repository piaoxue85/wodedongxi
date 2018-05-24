'''
Created on 2017年6月3日

@author: moonlit

'''

from BigQuantTrade import TradeHLPrice
import numpy as np


Position_ratio = 46.37/100

Position       = [  # code    ,市值
                    ["002427", 18094.01],
                    ["002707", 51212.37],
                    ["002354", 27248.75],
                    ["002839", 21866.37],
                    #["", ],
                 ]    
buy_sell       = [   #            ，股数
                    ["002839","卖",2493],
                    ["002707","卖",4264],
                    ["002354","卖",1566],
                    ["000825","买",8413],
                    ["000055","买",4980],
                    ["300113","买",1421],
                ]


weights = []
    
print("#-------------------------------------------------------------------庄华-----------------------------------------------------------------------------------------------")        

buy_black  = []
sell_black = []
T = TradeHLPrice(user_name = "庄华",start_date = "2017-08-01" , op_date = "" ,Position_ratio = Position_ratio , Position = Position , buy_sell = buy_sell)     
T.can_buy_GEM = True  
# shi_jian  ="2017-08-02"
shi_jian  = T.get_op_date() 
T.op_date = shi_jian

# importR.importRank(prank = rank, shi_jian = shi_jian)
print(T.user)
sell_list = T.sell(sell_black)
print(sell_list)
buy = T.buy(blacklist = [])
print(buy)

print("#---------------------------------------------------------------龚雯-----------------------------------------------------------------------------------------------------")
sell_black = [
              "002307",
              "600419",
              ]

w = list(np.array(weights)/1) 

T = TradeHLPrice(user_name = "龚雯",start_date = "2017-08-01" , op_date = "" ,Position_ratio = Position_ratio , Position = Position , buy_sell = buy_sell)
T.can_buy_GEM = False   
T.op_date = shi_jian

# importR.importRank(prank = rank, shi_jian = shi_jian)
print(T.user)
sell_list = T.sell(sell_black)
print(sell_list)
buy = T.buy(buy_black)
print(buy)

