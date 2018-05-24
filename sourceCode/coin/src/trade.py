'''
Created on 2018年2月12日

@author: moonlit

python z:/StockAnalysis/sourceCode/coin/src/trade.py
'''
import pandas as pd
import numpy  as np
from sqlalchemy import create_engine
import time,cx_Oracle

import zb,huobipro,okex
import bitstampapi as bitstamp
import bitfinexapi as bitfinex
from maps import conn_coin

def get_act_id():
    engine = create_engine(conn_coin)
    sql = "select seq_act_id.nextval seq_act_id from dual"
    data = pd.read_sql_query(sql,con = engine)    
    return data["seq_act_id"].values[0]

def get_bids_asks():
    bids = []
    asks = []
    
    bid,ask=zb.get_bid_asks(coin="btcusdt")
    bids.append(["zb",bid[0],bid[1]])
    asks.append(["zb",ask[0],ask[1]])
    
    bid,ask=huobipro.get_bid_asks(coin="btcusdt")
    bids.append(["huobipro",bid[0],bid[1]])
    asks.append(["huobipro",ask[0],ask[1]])  
    
    bid,ask=okex.get_bid_asks(coin="btcusdt")
    bids.append(["okex",bid[0],bid[1]])
    asks.append(["okex",ask[0],ask[1]])      
    
    bid,ask=bitstamp.get_bid_asks(coin="btcusdt")
    bids.append(["bitstamp",float(bid[0]),float(bid[1])])
    asks.append(["bitstamp",float(ask[0]),float(ask[1])])  
    
    bid,ask=bitfinex.get_bid_asks(coin="btcusdt")
    bids.append(["bitfinex",float(bid[0]),float(bid[1])])
    asks.append(["bitfinex",float(ask[0]),float(ask[1])])      
    
    bids = pd.DataFrame(bids,columns=["market","price","vol"])  
    asks = pd.DataFrame(asks,columns=["market","price","vol"])
    
    return bids,asks

def get_match():
    bids,asks = get_bids_asks()
    bids = bids.sort_values(["price"],ascending = False)
    asks = asks.sort_values(["price"],ascending = True )
    
    bid_price = bids["price"].values[0]
    ask_price = asks["price"].values[0]
    
    res = "None"
    print("bid:",bid_price,bids["market"].values[0], "ask:",ask_price,asks["market"].values[0])
    if bid_price - ask_price >= 50.0 :
#         if asks["vol"].values[0]>=bids["vol"].values[0]:
#             vol = bids["vol"].values[0]
#         else :
#             vol = asks["vol"].values[0]
        
        res = {
               "act_id" : get_act_id() ,
               "buy" : 
                    {
                     "market" :asks["market"].values[0],
                     "price"  :ask_price               ,
                     "vol"    :asks["vol"].values[0]   ,
                    },
               "sell" :
                    {
                     "market" :bids["market"].values[0],
                     "price"  :bid_price               ,
                     "vol"    :bids["vol"].values[0]   ,
                    }        
               } 
    return res

def add_act_log(act_type,act_id,order , res,res_msg):
    sql = "insert into tb_act_log values "
    sql+= "( "
    sql+= "'"    + str(act_id         ) + "',"
    sql+= "'"    + str(act_type       ) + "',"
    sql+= "'"    + str(order["market"]) + "',"
    sql+= "'"    + str(order["price"] ) + "',"
    sql+= "'"    + str(order["vol"]   ) + "',"
    sql+= "'"    + str(res            ) + "',"
    sql+= "'"    + str(res_msg        ) + "',"
    sql+= "      sysdate "
    sql+= ") "
    db=cx_Oracle.connect('c##coin','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    cr.execute(sql)    
    db.commit()        
    cr.close ()  
    db.close ()  

def buy(act_id,order):
    if order["market"]   == "zb":
        res = zb.buy(act_id,order)
    elif order["market"] == "huobipro":
        res = huobipro.buy(act_id, order)
    elif order["market"] == "okex":
        res = okex.buy(act_id, order)     
    elif order["market"] == "bitstamp":
        res = bitstamp.buy(act_id, order)  
    elif order["market"] == "bitfinex":
        res = bitfinex.buy(act_id, order)                                
    
    add_act_log("buy",act_id,order,res["res"],res["res_msg"])
    
def sell(act_id,order):
    if order["market"]   == "zb":
        res = zb.sell(act_id,order)
    elif order["market"] == "huobipro":
        res = huobipro.sell(act_id, order)
    elif order["market"] == "okex":
        res = okex.sell(act_id, order)      
    elif order["market"] == "bitstamp":
        res = bitstamp.sell(act_id, order)  
    elif order["market"] == "bitfinex":
        res = bitfinex.sell(act_id, order)                  
    
    add_act_log("sell",act_id,order,res["res"],res["res_msg"])
    
def main():
    print("begin")
    res = "None"
    while True :
        try :
            res = get_match()            
        except Exception as e :
            print(e)
            
#         res = get_match()  
            
        if res != "None" :
            buy (res["act_id"],res["buy"] )
            sell(res["act_id"],res["sell"])
            print(res)
            time.sleep(5)
        time.sleep(0.0001)
    
        
main()