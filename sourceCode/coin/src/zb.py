'''
Created on 2018年2月11日

@author: moonlit
钱包地址：1MEKhd1i7jcD3pUW1jB91rkhgDcWPqG2uA
access_key    = "a70a7d7f-9e9b-4805-b9cd-eb2d18d539df"
access_secret = "dcfe87c7-c20b-420c-ab98-18d4b5903edc"

https://www.zb.com/i/developer/restApi#market
13600069823
didierg160
'''

import json, hashlib,struct,time,sys
import urllib.request
from maps import coin_type

class zb_api:
    
    def __init__(self, mykey, mysecret):
        self.mykey    = mykey
        self.mysecret = mysecret
        self.jm = ''

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s.decode('utf-8'))
        for index in range(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb   = struct.pack("%ds" % len(aKey), aKey.encode('utf-8'))
        value  = struct.pack("%ds" % len(aValue), aValue.encode('utf-8'))
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad.encode('utf-8'))
        m.update(value)
        dg = m.digest()
        
        m = hashlib.md5()
        m.update(k_opad.encode('utf-8'))
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value  = struct.pack("%ds" % len(aValue), aValue.encode('utf-8'))
        print(value)
        h = hashlib.sha1()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params = ''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            self.jm = sign
            reqTime = (int)(time.time()*1000)
            params += '&sign=%s&reqTime=%d'%(sign, reqTime)
            url = 'https://trade.zb.com/api/' + path + '?' + params
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=2)
            doc = json.loads(res.read().decode(),encoding='utf-8')
            return doc
        except Exception as ex:
            print(sys.stderr, 'zb request ex: ', ex)
            return None
        
    def __data_api_call(self, path, params = ''):
        try:
            reqTime = (int)(time.time()*1000)
            url = 'http://api.zb.com/data/v1/' + path + '?' + params
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=2)
            doc = json.loads(res.read().decode(),encoding='utf-8')
            return doc
        except Exception as ex:
            print(sys.stderr, 'zb request ex: ', ex)
            return None        

    def query_account(self):
        try:
            params = "accesskey="+self.mykey+"&method=getAccountInfo"
            path = 'getAccountInfo'

            obj = self.__api_call(path, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb query_account exception,',ex)
            return None
        
    def query_depth(self,market="",size=0):
        try:
            params = "market="+market+"&size="+str(size)
            path = 'depth'

            obj = self.__data_api_call(path, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb query_account exception,',ex)
            return None    

        

access_key    = "a70a7d7f-9e9b-4805-b9cd-eb2d18d539df"
access_secret = "dcfe87c7-c20b-420c-ab98-18d4b5903edc"

def get_bid_asks(coin="btcusdt"): 
    api = zb_api(access_key, access_secret)
    res = api.query_depth(coin_type[coin]["zb"], 1)
    return res["bids"][0],res["asks"][0]

def buy(act_id,order):
    api = zb_api(access_key, access_secret)    
    return {"res":0,"res_msg":"sim"}

def sell(act_id,order):
    api = zb_api(access_key, access_secret)    
    return {"res":0,"res_msg":"sim"}
    
# print(get_bid_asks())
