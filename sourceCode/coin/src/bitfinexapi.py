'''
Created on 2018年2月11日

@author: moonlit
https://www.bitfinex.com/deposit
https://github.com/scottjbarr/bitfinex

moonlit77
Didierg160_
'''
import bitfinex
from maps import coin_type

parameters = {'limit_asks': 1, 'limit_bids': 1}
client = bitfinex.Client()

# symbol = coin_type["btcusdt"]["bitfinex"]
# orders = client.order_book(symbol, parameters)

def get_bid_asks(coin="btcusdt"): 
    global client,parameters

    res = client.order_book(symbol=coin_type[coin]["bitfinex"], parameters=parameters)
    return [res["bids"][0]["price"],res["bids"][0]["amount"]],[res["asks"][0]["price"],res["asks"][0]["amount"]]

def buy(act_id,order):  
    return {"res":0,"res_msg":"sim"}

def sell(act_id,order):
    return {"res":0,"res_msg":"sim"}

# print(orders)