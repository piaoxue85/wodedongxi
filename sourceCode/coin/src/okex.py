'''
Created on 2018年2月13日

@author: moonlit
https://www.okex.com/
13600069823
didierg160
apiKey: 93a80834-79df-47e2-9bdc-6f104153b3d4 
secretKey: 90051507E86A07D10276999E8A6D17E7 
'''
from okexapi.OkcoinSpotAPI   import OKCoinSpot
from okexapi.OkcoinFutureAPI import OKCoinFuture
from maps import coin_type

#初始化apikey，secretkey,url
apikey = '93a80834-79df-47e2-9bdc-6f104153b3d4'
secretkey = '90051507E86A07D10276999E8A6D17E7'
okcoinRESTURL = 'www.okex.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn   

#现货API
okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

#期货API
# okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)

def query_depth(market="",size=1):
    global okcoinSpot
    return okcoinSpot.depth(market,size=1)

def get_bid_asks(coin="btcusdt"):    
    res = query_depth(market=coin_type[coin]["okex"] ,size=1 )
    return res["bids"][0],res["asks"][-1]

def buy(act_id,order):    
    return {"res":0,"res_msg":"sim"}

def sell(act_id,order):    
    return {"res":0,"res_msg":"sim"}