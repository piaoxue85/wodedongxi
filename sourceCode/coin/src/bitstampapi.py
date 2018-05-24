'''
Created on 2018年2月11日

@author: moonlit
https://www.bitstamp.net/
https://github.com/kmadac/bitstamp-python-client

Client ID: loit3250
Password: CK8?4XpQ15uK
'''

import bitstamp.client
from maps import coin_type

client = bitstamp.client.Public()

def get_bid_asks(coin="btcusdt"): 
    global client
    res = client.order_book(group=False,base=coin_type[coin]["bitstamp"], quote="")
    return res["bids"][0],res["asks"][0]

def buy(act_id,order):  
    return {"res":0,"res_msg":"sim"}

def sell(act_id,order):
    return {"res":0,"res_msg":"sim"}

# print(get_bid_asks(coin="btcusdt"))