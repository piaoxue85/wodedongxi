'''
Created on 2018年2月12日

@author: moonlit
'''

coin_type = {
             "btcusdt" :{
                            "zb"       : "btc_usdt"  ,
                            "huobipro" : "btcusdt"   ,
                            "okex"     : "btc_usdt"  ,
                            "bitstamp" : "btcusd"    ,
                            "bitfinex" : "btcusd"    ,
                        },
             }

conn_coin = "oracle://c##coin:didierg160@myoracle"