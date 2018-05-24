'''
Created on 2018年2月12日

@author: moonlit
https://www.huobipro.com/zh-cn/login/?reg_success&id=11124530
13600069823
didierg160

access  0c39955f-050eb142-45c86e17-03147
secret  b3809ad0-d36a74ef-5c0553b5-a1f40

广信出口 219.137.167.250

'''
import huobiapi.HuobiServices as huobi
import json
from maps import coin_type

def query_depth(market="",size=0):
    return huobi.get_depth(symbol=market, type="step"+str(size))

def get_bid_asks(coin="btcusdt"):    
    res = query_depth(market=coin_type[coin]["huobipro"] , size=1)
    return res["tick"]["bids"][0],res["tick"]["asks"][0]

def buy(act_id,order):    
    return {"res":0,"res_msg":"sim"}

def sell(act_id,order):    
    return {"res":0,"res_msg":"sim"}

# print(get_bid_asks())