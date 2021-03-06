'''
Created on 2017年6月2日

@author: moonlit  
'''
import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine
import tushare as ts
import numpy as np
from nose.util import tolist
import getStockData as gsd
from  math import floor
# from math import round



class Trade(object):
    
    def update_position_last_price(self):
        sql = "select code from tb_stock_bigquant_position "
        codes = pd.read_sql_query(sql,con = self.engine) 
        codes = codes["code"].values  
        for code in codes :
            price = self.get_last_price(code = code)
            sql = "update tb_stock_bigquant_position set last_price = "  + str(price) + " where code = '" + code + "'"    

    def __init__(self , user_name = "庄华" , start_date = '2007-06-05' , op_date = '2007-06-05',weights = []):
        self.db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
        self.cr=self.db.cursor()
        self.engine = create_engine('oracle://c##stock:didierg160@myoracle')
        
        self.user              = user_name
        self.start_date        = start_date
        self.op_date           = op_date
        self.max_cash_per_code = 0.2            # 设置每只股票占用的最大资金比例
        self.hold_days         = 30
        self.weights           = weights    
        self.can_buy_GEM       = True           #是否开通了创业板
        self.update_position_last_price()   
        
    
#     def get_op_date (self):
#         sql = "select to_char(sysdate,'yyyy-mm-dd') today ,to_char(sysdate - 1,'yyyy-mm-dd') yesterday , to_char(sysdate,'hh24miss') time from dual"
#         data = pd.read_sql_query(sql,con = self.engine)   
#         today     = data["today"].values    
#         yesterday = data["yesterday"].values
#         time      = data["time"].values
# 
#         today     = str(today[0])
#         yesterday = str(yesterday[0])
#         time      = int(time[0])       
#        
#         if time > 220000 :
#             res = today
#         else:
#             res = yesterday        
#         return res     

    def get_op_date (self):
        sql = "select to_char(max(shi_jian),'yyyy-mm-dd') op_date from tb_stock_data_daily where code = '000001zs'"
        data = pd.read_sql_query(sql,con = self.engine)   
        op_date   = data["op_date"].values    
        
        return op_date[0]      
    
    #总市值/配置的持仓时间   平均明天买入的金额
    def cash_avg (self):
        return self.portfolio_value()/self.hold_days
    
    #获取剩余现金
    def cash_balance(self):
        sql = "select value from tb_stock_bigquant_dict where key = '"+self.user+"cash_balance'"
        cash_balance = pd.read_sql_query(sql,con = self.engine)   
        cash_balance = cash_balance["value"].values     
        return float( cash_balance[0] )  
    
    def get_last_price(self,code = ""):
        df = ts.get_realtime_quotes(code) #Single stock symbol
        price_now = float(df["price"].values[0])

        if price_now <= 0.0 :
            shi_jian  = gsd.get_code_max_shi_jian(code=code)
            df        = gsd.get_stock_data_daily_df_time(code=code,start=shi_jian,end=shi_jian)
            price_now = df["price"].values[0] 
                
        return float(price_now)
    
    #持仓的单个股票市值
    def position_price(self,code = ""):        
        sql = "select sum(Volume*last_price) total_price from tb_stock_bigquant_position where user_name ='"+self.user+"' and code = '" + code + "'"
        total_price = pd.read_sql_query(sql,con = self.engine)   
        total_price = total_price["total_price"].values   
        if total_price == [None]:
            total_price = [0]
        return float( total_price[0] )        
    
    #持仓股票的总价值
    def position_total_price(self):       
        sql = "select sum(Volume*last_price) total_price from tb_stock_bigquant_position where user_name ='"+self.user+"'"
        total_price = pd.read_sql_query(sql,con = self.engine)   
        total_price = total_price["total_price"].values 
        if total_price == [None] :
            total_price = [0]
        return float( total_price[0] )  

    #获取总市值
    def portfolio_value(self):
        return self.cash_balance() + self.position_total_price()   
    
    #是否在建仓期 
    def is_staging(self):
        sql   = "select count(1) count  from tb_stock_data_daily where code = '000001zs' and shi_jian >=to_date('" + self.start_date + " 15:00:00','yyyy-mm-dd hh24:mi:ss')"
        count = pd.read_sql_query(sql,con = self.engine)   
        count = count["count"].values    
        count = count[0]
        return  int(count) < self.hold_days        
    
    #用来买每一只股票的现金 = 剩余现金 和 （最初30天 1 * cash_avg ，30天后 1.5 * cash_avg ）2者的小的那个
    def cash_for_buy(self):
        return min(self.cash_balance(), (1 if self.is_staging() else 1.5) * self.cash_avg())
    
    #当天卖出套现资金配额
    def cash_for_sell(self):
        return  self.cash_avg() - (self.cash_balance() - self.cash_for_buy())
    
    
    def get_position_ranked(self , order_type = ""):
        sql  = "select b.code ,                                                                      "
        sql += "       b.Volume                                                                      "
        sql += "from tb_stock_bigquant_rank     a ,                                                  "
        sql += "     (                                                                               "
        sql += "        select code,sum(volume) volume from tb_stock_bigquant_position where user_name ='"+self.user+"' group by code "
        sql += "     )                                                                               "
        sql += "      b                                                                              "
        sql += "where                                                                                "
        sql += "  a.shi_jian = to_date('" + self.op_date +" 15:00:00','yyyy-mm-dd hh24:mi:ss')       "
        sql += "    and                                                                              "
        sql += "  a.code = b.code                                                                    "
        sql += "order by a.rank " + order_type                                                 

        code_ranked = pd.read_sql_query(sql,con = self.engine)
        code   = code_ranked["code"].values    
        volume = code_ranked["volume"].values 
        return code,volume   
    
    #获取所有持仓股票及股数
    def get_all_position(self , order_type = ""):
        sql  = "select code ,                                                                      "
        sql += "       sum(Volume) volume                                                          "
        sql += "from tb_stock_bigquant_position where  user_name ='"+self.user+"' group by code    "                                             

        code_ranked = pd.read_sql_query(sql,con = self.engine)
        code   = code_ranked["code"].values    
        volume = code_ranked["volume"].values 
        return code,volume     
      
    #获取持仓股票及股数
    def get_position(self ,  code=""):
        sql  = "select code ,                                                                      "
        sql += "       sum(Volume) volume                                                          "
        sql += "from tb_stock_bigquant_position where  user_name ='"+self.user+"' "
        sql += " and code = '" + code[:6] + "' " 
        sql += " group by code    "                                             

        code_ranked = pd.read_sql_query(sql,con = self.engine)   
        volume = code_ranked["volume"].values 
        return volume         
    
    def get_code_list_to_buy_ranked(self , list_length = 5):
        sql  = "select code ,rank                                                                "
        sql += "from tb_stock_bigquant_rank where                                                "
        sql += "  shi_jian = to_date('" + self.op_date +" 15:00:00','yyyy-mm-dd hh24:mi:ss')     "
        sql += "    and                                                                          "
#         sql += "  code in                                                   "
#         sql += "  (                                                         "
#         sql += "    select code from                                        "
#         sql += "    (                                                       "
#         sql += "      select code,min(shi_jian) shi_jian from tb_stock_data_daily "  
#         sql += "      group by code   "        
#         sql += "    )   "
#         sql += "    where shi_jian <= to_date('" + self.op_date +" 15:00:00','yyyy-mm-dd hh24:mi:ss') - 365 "
#         sql += "  )     "
#         sql += "    and "     
        sql += "  code not in                                                                    "
        sql += "  (                                                                              "
        sql += "    select code from tb_stock_list where                                         "
        sql += "      upper(name) like '%ST%'                                                    "
        sql += "        or                                                                       "
        sql += "      upper(name) like '%退%'                                                    "
        if self.can_buy_GEM == False:
            sql += " or substr(code,1,1) = '3'"        
        sql += "  )                                                                              "
        sql += "order by rank asc                                                                "                                               
#         print(sql)
        code_ranked = pd.read_sql_query(sql,con = self.engine)   
        code   = code_ranked["code"].values           
        return code[:list_length]           
              
    #收盘卖出
    def sell(self ):
        sell_list = []
        self.update_position_last_price() 
        #print( self.is_staging())
        #print(self.cash_for_sell())
        
        if  not self.is_staging() and self.cash_for_sell() > 0:
        #if True :
            cash_for_sell = self.cash_for_sell()
            #res = self.get_position_ranked(order_type="desc")  
            codes,volumes = self.get_position_ranked(order_type="desc")  
            for (code,volume) in zip(codes,volumes) :
                price_now = self.get_last_price(code = code)
                cash_for_sell -= price_now * volume
                sell_list.append( code ) 
                if cash_for_sell <= 0:
                    break 
        if len(sell_list) >0 :
            sell_list = pd.DataFrame(sell_list)
            sell_list.columns = ["股票代码"]               
        return sell_list              
    
    #开盘买入
    def buy(self ):
        buy_list = []
#         buy_xls = []
        self.update_position_last_price()        
        buy_instruments         = self.get_code_list_to_buy_ranked(list_length = len(self.weights))
#         buy_instruments = [
#                             '300029',
#                             '300321',
#                             '000004',
#                             '600561',
#                             '600689',
#                             ]      
                
        max_cash_per_instrument = self.portfolio_value() * self.max_cash_per_code
        for code ,weight in zip(buy_instruments,self.weights):
            cash = self.cash_for_buy() * weight
            if cash > max_cash_per_instrument - self.position_price(code=code) : 
                cash = max_cash_per_instrument - self.position_price(code=code)
            
            if cash > 0:
                market = ""
                if (code[0:1] == "6") :
                    market = "上海"
                else :
                    market = "深圳"
                    
                last_price = self.get_last_price(code=code)
                buy_vol = floor((float(cash)/last_price)/100)*100
                buy_list.append([market ,code , buy_vol , last_price , cash])
#                 buy_xls.append(object)
        if len(buy_list) < 1 :
            buy_list = [['','','','','']]
#             buy_list.append(['','','','',''])
        buy_list = pd.DataFrame(buy_list)
        buy_list.columns =[
                        "市场" ,
                        '股票代码 ',
                        '买入股数',
                        "价格" ,
                        '理论买入金额'       
                    ]        
        return buy_list

class TradeSmallMarketValue(Trade):
    #开盘买入
    def buy(self,blacklist = []):
        buy_list = []
        self.update_position_last_price()        
        buy_instruments         = self.get_code_list_to_buy_ranked(list_length = len(self.weights))      
        #print(buy_instruments)   
        #print(self.weights)      
        #print(len(self.weights)) 
        #print(self.portfolio_value())
        max_cash_per_instrument = self.portfolio_value()*self.weights[0]
        cash_balance = self.cash_balance()
        #print(cash_balance) 
        for code  in buy_instruments:     
            if code in blacklist :
                continue
             
            cash_to_buy = max_cash_per_instrument - self.position_price(code=code )
            if cash_to_buy <= 0.0 :
                continue
            
            if cash_balance < cash_to_buy  :
                cash_to_buy   = cash_balance
                
            last_price = round(self.get_last_price(code=code)*100*1.01)/100
                                         
            if cash_balance >= cash_to_buy : 
                #cash_balance -= cash_to_buy
                #last_price = round(self.get_last_price(code=code)*100*1.01)/100
                buy_vol    = floor((float(cash_to_buy)/last_price)/100)*100
                cash_balance -= last_price * buy_vol 
            
            if cash_to_buy > 0.0 :
                market = ""
                if (code[0:1] == "6") :
                    market = "上海"
                else :
                    market = "深圳"
                                    
                #last_price = round(self.get_last_price(code=code)*100*1.01)/100
                if last_price == 0 :
                    print(code,"price:",last_price)
                    continue                
                
                buy_vol = floor((float(cash_to_buy)/last_price)/100)*100
                buy_list.append([market ,code , buy_vol , last_price , cash_to_buy])

                #buy_xls.append(object)
        if len(buy_list) < 1 :
            buy_list = [['','','','','']]
        buy_list = pd.DataFrame(buy_list)
        buy_list.columns =[
                        "市场" ,
                        '股票代码 ',
                        '买入股数',
                        "价格" ,
                        '理论买入金额'       
                    ]        
        return buy_list
    
    #收盘卖出
    def sell(self ,sell_black_list = []):
        sell_list = []
        self.update_position_last_price() 
        #print( self.is_staging())
        #print(self.cash_for_sell())
        
        buy_instruments         = self.get_code_list_to_buy_ranked(list_length = len(self.weights)) 
        max_cash_per_instrument = self.portfolio_value()*self.weights[0]
        #res = self.get_position_ranked(order_type="desc")  
        codes,volumes = self.get_all_position(order_type="desc")  
        for (code,volume) in zip(codes,volumes) :
            if code in sell_black_list :
                continue 
                        
            if code in buy_instruments :
                last_price = round(self.get_last_price(code=code) * 0.99*100)/100 
                buy_vol = floor((float(max_cash_per_instrument)/last_price)/100)*100
                sell_vol= volume - buy_vol
                
                if sell_vol >= 100 :
                    volume = sell_vol
                else :
                    continue
                              
            if (code[0:1] == "6") :
                market = "上海"
            else :
                market = "深圳"
                    
            last_price = round(self.get_last_price(code=code) * 0.99*100)/100 
                
            sell_list.append([market ,code , volume , last_price, volume*last_price]) 


        if len(sell_list) < 1 :
            sell_list = [['','','','','']]
#             buy_list.append(['','','','',''])
        sell_list = pd.DataFrame(sell_list)
        sell_list.columns =[
                        "市场" ,
                        '股票代码 ',
                        '卖出股数',
                        "价格" ,
                        '理论卖出金额'       
                    ]        
        return sell_list          
    
class TradeHLPrice(Trade):
    def val_ratio(self,Position_ratio,Position):
        Position_ = pd.DataFrame(Position,columns=["code","amount"])
        
        his_amount = sum(tolist(Position_["amount"].values))/Position_ratio
        my_amount  = self.portfolio_value()
        print("我的总市值：",my_amount)
        print("他的总市值：",his_amount)
        print("我的总市值/他的总市值:",my_amount/his_amount)
        return my_amount/his_amount
            
    def __init__(self, user_name = "庄华" , start_date = '2007-06-05' , op_date = '2007-06-05',Position_ratio = 0.1 , Position = [] , buy_sell = []):         
        Trade.__init__(self , user_name = user_name , start_date = start_date , op_date = op_date , weights = [])
        
        self.Position_ratio = Position_ratio
        self.Position       = Position
        self.buy_sell       = pd.DataFrame(buy_sell , columns = ["code","act","vol"])
        self.val_ratio_     = self.val_ratio(Position_ratio,Position)        
    
    #开盘买入
    def buy(self,blacklist = []):
        buy_list = []
        buy_info=self.buy_sell[self.buy_sell["act"]=="买"]
        self.update_position_last_price()        
        buy_instruments = buy_info["code"].values  
        vols            = buy_info["vol"].values
        cash_balance = self.cash_balance()
        #print(buy_instruments)   
        #print(self.weights)      
        #print(len(self.weights)) 
        #print(self.portfolio_value())

        #print(cash_balance) 
        for code,buy_vol in zip(buy_instruments,vols):  
               
            if code in blacklist :
                continue
             
            cash_to_buy = self.get_last_price(code=code)*buy_vol*self.val_ratio_
            if cash_to_buy <= 0.0 :
                continue
            
            if cash_balance < cash_to_buy  :
                cash_to_buy   = cash_balance
                                         
            if cash_balance >= cash_to_buy : 
                cash_balance -= cash_to_buy
            
            if cash_to_buy > 0.0 :
                market = ""
                if (code[0:1] == "6") :
                    market = "上海"
                else :
                    market = "深圳"

                last_price = round(self.get_last_price(code=code)*100)/100
                if last_price == 0 :
                    print(code,"price:",last_price)
                    continue                
                
                buy_vol = floor((float(cash_to_buy)/last_price)/100)*100
                buy_list.append([market ,code , buy_vol , last_price*1.0 , cash_to_buy])

                #buy_xls.append(object)
        if len(buy_list) < 1 :
            buy_list = [['','','','','']]
        buy_list = pd.DataFrame(buy_list)
        buy_list.columns =[
                        "市场" ,
                        '股票代码 ',
                        '买入股数',
                        "价格" ,
                        '理论买入金额'       
                    ]        
        return buy_list
    
    #收盘卖出
    def sell(self ,sell_black_list = []):
        sell_list = []
        self.update_position_last_price() 
        #print( self.is_staging())
        #print(self.cash_for_sell())
        sell_info=self.buy_sell[self.buy_sell["act"]=="卖"]
        sell_instruments = sell_info["code"].values  
        sell_vols        = sell_info["vol"].values 
        #res = self.get_position_ranked(order_type="desc")   
        for (code,volume) in zip(sell_instruments,sell_vols) :
            if code in sell_black_list :
                continue 
             
            volume = floor(volume * self.val_ratio_ /100)*100
            vol    = self.get_position(code = code)
            
            if volume > vol :
                volume = vol
            
            if (code[0:1] == "6") :
                market = "上海"
            else :
                market = "深圳"
                    
            last_price = round(self.get_last_price(code=code) * 0.96*100)/100
                
            sell_list.append([market ,code , volume , last_price, volume*last_price]) 


        if len(sell_list) < 1 :
            sell_list = [['','','','','']]
#             buy_list.append(['','','','',''])
        sell_list = pd.DataFrame(sell_list)
        sell_list.columns =[
                        "市场" ,
                        '股票代码 ',
                        '卖出股数',
                        "价格" ,
                        '理论卖出金额'       
                    ]        
        return sell_list                       
    
    
    
    
        