'''
Created on 2017年4月11日

@author: moonlit
'''
import numpy as np
import pandas as pd
import cx_Oracle
from math import ceil
from sqlalchemy import create_engine
from sklearn.utils import shuffle  

import json, urllib.request, urllib.parse, urllib.error
from urllib.parse import urlencode
import pandas as pd

def get_tb_temp_data():
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select * from tb_temp order by shi_jian asc"
    data = pd.read_sql_query(sql,con = engine)
    return data  

def get_report_data(year="" , quarter=""):
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    sql = "select * from tb_stock_report_data     where year = " + str(year) + " and quarter = " + str(quarter)
    data = pd.read_sql_query(sql,con = engine)
    return data  

def get_profit_data(year="" , quarter=""):
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    sql = "select * from tb_stock_profit_data     where year = " + str(year) + " and quarter = " + str(quarter)
    data = pd.read_sql_query(sql,con = engine)
    return data  

def get_operation_data(year="" , quarter=""):
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    sql = "select * from tb_stock_operation_data  where year = " + str(year) + " and quarter = " + str(quarter)
    data = pd.read_sql_query(sql,con = engine)
    return data  

def get_growth_data(year="" , quarter=""):
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    sql = "select * from tb_stock_growth_data      where year = " + str(year) + " and quarter = " + str(quarter)
    data = pd.read_sql_query(sql,con = engine)
    return data  

def get_debtpaying_data(year="" , quarter=""):
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    sql = "select * from tb_stock_debtpaying_data   where year = " + str(year) + " and quarter = " + str(quarter)
    data = pd.read_sql_query(sql,con = engine)
    return data  

def get_cashflow_data(year="" , quarter=""):
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    sql = "select * from tb_stock_cashflow_data     where year = " + str(year) + " and quarter = " + str(quarter)
    data = pd.read_sql_query(sql,con = engine)
    return data  



def get_next_date(date="" , add_days = 0):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select to_char(to_date('" + date + "','yyyy-mm-dd') + " + str(add_days) +" , 'yyyy-mm-dd') shi_jian from dual"
    data = pd.read_sql_query(sql,con = engine)
    res  = str(data["shi_jian"].values[0]) 
    return res

def get_important_day():
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select shi_jian,name from tb_stock_important_day order by shi_jian asc"
    data = pd.read_sql_query(sql,con = engine)
    return data   

#按年获取的假期列表
#get_holiday_yearly(year="2017") 
def get_holiday_yearly(appkey="419925bb58e7879c11e597d23a7f958d",year="2017", m="GET"):
    df = None
    url = "http://v.juhe.cn/calendar/year"
    params = {
        "key"  : appkey, #您申请的appKey
        "year" : year  , #指定年份,格式为YYYY,如:2015
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    print(res)    
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            df = pd.DataFrame( eval(res["result"]["data"]["holidaylist"]) )
#             print(df)            
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")

    return error_code,res["reason"],df
    


def get_code_list():
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select code from tb_stock_list order by code asc"
    data = pd.read_sql_query(sql,con = engine)
    return data    

def get_code_max_shi_jian(code=""):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select to_char(max(shi_jian),'yyyy-mm-dd') shi_jian from tb_stock_data_daily where code = '" + code + "'" 
    data = pd.read_sql_query(sql,con = engine)
    res  = str(data["shi_jian"].values[0]) 
    return res

def get_code_max_shi_jian_wind(code=""):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select max(shi_jian) shi_jian from tb_stock_data_daily_wind where code = '" + code + "'" 
    data = pd.read_sql_query(sql,con = engine)
    if len(data["shi_jian"].values) >0 :
        res  = str(data["shi_jian"].values[0])
    else :
        res = "None" 
    return res

def get_code_min_shi_jian(code=""):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql  = "select to_char(min(shi_jian),'yyyy-mm-dd') shi_jian from tb_stock_data_daily where code = '" + code + "'" 
    data = pd.read_sql_query(sql,con = engine)
    res  = str(data["shi_jian"].values[0]) 
    return res

def get_code_min_shi_jian_wind(code=""):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql  = "select min(shi_jian) shi_jian from tb_stock_data_daily_wind where code = '" + code + "'" 
    data = pd.read_sql_query(sql,con = engine)
    if len(data["shi_jian"].values) >0 :
        res  = str(data["shi_jian"].values[0])
    else :
        res = "None"
    return res

def get_week():
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select to_char(Monday,'yyyy-mm-dd') Monday , to_char(Friday,'yyyy-mm-dd') Friday from tb_stock_week_time order by Monday asc"
    data = pd.read_sql_query(sql,con = engine)
    return data    

def get_code_list_by_classification(classification="上证50成份股"):
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    sql = "select code from tb_stock_classified where c_name='"+classification+"'"
    data = pd.read_sql_query(sql,con = engine)
    return data
    
def get_code_list_not_in_sz50(daysago = 365) :
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  ="select code,count(1) count from tb_stock_data_daily where "
    sql +="  shi_jian >= sysdate - "+str(daysago)+" "
    sql +="    and                                  "
    sql +="  code not in                            "
    sql +="  (                                      "
    sql +="    select distinct(code) from c##tushare.tb_stock_classified where c_name='上证50成份股' "
    sql +="  )           "
    sql +="    and       "
    sql +="  code not in "
    sql +="  (           "
    sql +="    select distinct(code) from tb_stock_data_daily where "
    sql +="      shi_jian >= sysdate - "+str(daysago)+"             "
    sql +="        and          "
    sql +="      price = 0      "
    sql +="  )                  "
    sql +="group by code        "
    sql +="having count(1)>=300 "
    
    data = pd.read_sql_query(sql,con = engine)
    return data    

def del_found_before_rqalpha():
    sql = "delete tb_stock_found_rqalpha" 
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    cr.execute(sql)    
    db.commit()        
    cr.close ()  
    db.close ()                 
    return True 

def add_found_rqalpha(code = "" , content = "" , shi_jian = ""):
    sql = "insert into tb_stock_found_rqalpha(code,content,shi_jian) values ('"+code + "','" + content + "',to_date('" + shi_jian + " 15:00:00' ,'yyyy-mm-dd hh24:mi:ss'))" 
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    cr.execute(sql)    
    db.commit()        
    cr.close ()  
    db.close ()                 
    return True 

def add_done_mark_rqalpha(WHAT_DONE = ""):
    sql = "insert into tb_stock_job_done values ('"+WHAT_DONE + "',sysdate)" 
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    cr.execute(sql)    
    db.commit()        
    cr.close ()  
    db.close ()                 
    return True 

def get_stock_code_list_after_kdj_test_rqalpha():
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
#     sql = "select substr(code , 1 , 6 ) code from tb_stock_test_res_rqalpha where total_returns>= 0.7 and start_time='2015-06-01' order by code asc"
    sql  = "select substr(a.code , 1 , 6 ) code ,"   
    sql += "       b.stop_count stop_count       " 
    sql += "from tb_stock_test_res_rqalpha  a ,  " 
    sql += "     tb_stock_stop_loss_rqalpha b    " 
    sql += "where                                " 
    sql += "  a.total_returns>= 0.7              " 
    sql += "    and                              " 
    sql += "  a.start_time='2015-06-01'          " 
    sql += "    and                              " 
    sql += "  a.code = b.code                    " 
    sql += "order by a.code asc                  " 
    
    data       = pd.read_sql_query(sql,con = engine)
    codes      = data['code'].values   
    stop_count = data["stop_count"].values       
    return codes , stop_count      

def get_stock_code_rqalpha():
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = "select cur from tb_stock_cursor_rqalpha where rownum<2"  
    cur = pd.read_sql_query(sql,con = engine)
    cur = cur['cur'].values
    cur = cur[0]      
    sql = "select code from tb_stock_list_rqalpha where id = " + str(cur)  
    code = pd.read_sql_query(sql,con = engine)
    code = code['code'].values
    code = code[0]   
    
    sql = "select max(id) max_id from tb_stock_list_rqalpha  "
    data = pd.read_sql_query(sql,con = engine)
    data = data['max_id'].values
    max_id = data[0]   
    
    if code[0:1] == "6" :
        code += ".XSHG" 
    else :
        code += ".XSHE"
      
    return str(code) , str( max_id ) , str( cur )  

def move_to_next_cur_rqalpha(max_id = 0 , cur = 0):
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    if int(cur) < int(max_id) :
        sql = "update tb_stock_cursor_rqalpha set cur = cur + 1"
    else :
        sql = "update tb_stock_cursor_rqalpha set cur = 1"
    cr.execute(sql)    
    db.commit()        
    cr.close ()  
    db.close ()                 
    return True

def set_test_res_rqalpha(code="" , total_returns = 0.0 , last_fromtype=0 , start_time= "", end_time = ""):
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    sql  = " insert into tb_stock_test_res_rqalpha values "
    sql += "     (                              "
    sql += "     '" + str(code         ) + "'," 
    sql += "     '" + str(total_returns) + "',"
    sql += "     '" + str(last_fromtype) + "',"
    sql += "     '" + str(start_time   ) + "',"
    sql += "     '" + str(end_time     ) + "' "
    sql += "    )"
    cr.execute(sql)    
    db.commit()        
    cr.close ()  
    db.close ()                 
    return True    


def get_stock_data_daily_rqalpha(code='',end=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
    sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
    sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
    sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
    sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
    sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
    sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
    sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
    sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
    sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
    sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
    sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
    sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
    sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
    sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
    sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
    sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
    sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
    sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
    sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
    sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
    sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD      "
    sql +=  "from tb_stock_data_daily where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+end[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') - 365"
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+end[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
    return data  
 
def get_stock_data_weekly_rqalpha(code='',end=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
    sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
    sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
    sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
    sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
    sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
    sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
    sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
    sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
    sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
    sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
    sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
    sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
    sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
    sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
    sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
    sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
    sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
    sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
    sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
    sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
    sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD      "
    sql +=  "from tb_stock_data_weekly where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+end[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') - 365 "
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+end[0:10]   +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
    return data       

def get_stock_data_monthly_rqalpha(code='',end=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
    sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
    sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
    sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
    sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
    sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
    sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
    sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
    sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
    sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
    sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
    sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
    sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
    sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
    sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
    sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
    sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
    sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
    sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
    sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
    sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
    sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD      "
    sql +=  "from tb_stock_data_monthly where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+end[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') - 365 "
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+end[0:10]   +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
#     print(sql)
    data = data.set_index('shi_jian')
    return data      

def get_stock_data_monthly(code='',begin="",end=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
    sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
    sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
    sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
    sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
    sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
    sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
    sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
    sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
    sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
    sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
    sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
    sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
    sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
    sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
    sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
    sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
    sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
    sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
    sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
    sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
    sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD      "
    sql +=  "from tb_stock_data_monthly where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+begin[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+end[0:10]   +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
#     print(sql)
#     data = data.set_index('shi_jian')
    return data      
    
    
def get_stock_data_Quarterly_rqalpha(code='',end=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
    sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
    sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
    sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
    sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
    sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
    sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
    sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
    sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
    sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
    sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
    sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
    sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
    sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
    sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
    sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
    sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
    sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
    sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
    sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
    sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
    sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD      "
    sql +=  "from tb_stock_data_Quarterly where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+end[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') - 365*2 "
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+end[0:10]   +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
    return data       
    
def get_stock_data_max_price_rqalpha(code='',start='',end=''): # "yyyy-mm-dd"
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select max(max_price) max_price from tb_stock_data_daily where " 
    sql +=  "  code = '" + code + "'" 
    
    if start != '' :
        sql +=  "    and "
        sql +=  "  shi_jian >= to_date('"+start[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "

    if end != '' :
        sql +=  "    and "
        sql +=  "  shi_jian <= to_date('"+end[0:10]   +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    

    #print(sql)
    data = pd.read_sql_query(sql,con = engine)
    max_price = data['max_price'].values
    return float( max_price[0] )   
    
def get_stock_data_daily_df_time(code='',start='',end=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
    sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
    sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
    sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
    sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
    sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
    sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
    sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
    sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
    sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
    sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
    sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
    sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
    sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
    sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
    sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
    sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
    sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
    sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
    sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
    sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
    sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD    , "
    sql +=  "       decode(DPO_DPO         ,null,0,DPO_DPO         ) DPO_DPO          , "
    sql +=  "       decode(DPO_6MA         ,null,0,DPO_6MA         ) DPO_6MA            "
    sql +=  "from tb_stock_data_daily where "
    sql +=  "  code = '" + code[0:8] + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+start[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+end[0:10]   +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
#     print(sql)
#     data = data.set_index('shi_jian')
    return data    

def get_stock_data_weekly_df_time(code='',start='',end=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount             "
    sql +=  "from tb_stock_data_weekly where "
    sql +=  "  code = '" + code[0:8] + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+start[0:10] +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+end[0:10]   +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
#     print(sql)
#     data = data.set_index('shi_jian')
    return data    

def get_stock_data_daily_df_time_wind(code='',start='',end=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select * "
    sql +=  "from tb_stock_data_daily_wind where "
    sql +=  "  code = '" + code[0:8] + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= '"+start[0:10] +"'"
    sql +=  "    and "
    sql +=  "  shi_jian <= '"+  end[0:10] +"'"    
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)

    return data  

def get_stock_data_daily_df_daysago_(code,daysago=365,endtime=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
    sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
    sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
    sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
    sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
    sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
    sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
    sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
    sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
    sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
    sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
    sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
    sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
    sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
    sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
    sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
    sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
    sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
    sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
    sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
    sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
    sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD    , "
    sql +=  "       decode(DPO_DPO         ,null,0,DPO_DPO         ) DPO_DPO          , "
    sql +=  "       decode(DPO_6MA         ,null,0,DPO_6MA         ) DPO_6MA            "
    sql +=  "from tb_stock_data_daily where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+endtime+" 15:00:00','yyyy-mm-dd hh24:mi:ss') - " + str(daysago) 
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+endtime+" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
    return data

def get_stock_data_daily_df_monthsafter(code,monthsafter=3,begintime=''):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price              "
#     sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
#     sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
#     sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
#     sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
#     sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
#     sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
#     sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
#     sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
#     sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
#     sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
#     sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
#     sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
#     sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
#     sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
#     sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
#     sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
#     sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
#     sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
#     sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
#     sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
#     sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
#     sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
#     sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
#     sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
#     sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
#     sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
#     sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
#     sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
#     sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD    , "
#     sql +=  "       decode(DPO_DPO         ,null,0,DPO_DPO         ) DPO_DPO          , "
#     sql +=  "       decode(DPO_6MA         ,null,0,DPO_6MA         ) DPO_6MA            "
    sql +=  "from tb_stock_data_daily where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+begintime+" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "    and "
    sql +=  "  shi_jian < add_months(to_date('"+begintime+" 15:00:00','yyyy-mm-dd hh24:mi:ss')," + str(monthsafter) + ") "
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
    return data

def get_stock_data_daily_df_daysago(code,daysago=365):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select shi_jian , "
#     sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount            "
#     sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
#     sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
#     sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
#     sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
#     sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
#     sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
#     sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
#     sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
#     sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
#     sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
#     sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
#     sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
#     sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
#     sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
#     sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
#     sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
#     sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
#     sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
#     sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
#     sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
#     sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD    , "
#     sql +=  "       decode(DPO_DPO         ,null,0,DPO_DPO         ) DPO_DPO          , "
#     sql +=  "       decode(DPO_6MA         ,null,0,DPO_6MA         ) DPO_6MA            "
    sql +=  "from tb_stock_data_daily where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= sysdate-" + str(daysago) +" "
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
    return data



def get_stock_data_daily_df(code):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select to_char(shi_jian,'yyyy-mm-dd')                   shi_jian         , "
    sql +=  "       decode(price           ,null,0,price )           price            , "
    sql +=  "       decode(price_last_day  ,null,0,price_last_day  ) price_last_day   , "
    sql +=  "       decode(price_today_open,null,0,price_today_open) price_today_open , "
    sql +=  "       decode(zhang_die       ,null,0,zhang_die       ) zhang_die        , "
    sql +=  "       decode(zhang_die_rate  ,null,0,zhang_die_rate  ) zhang_die_rate   , "
    sql +=  "       decode(max_price       ,null,0,max_price       ) max_price        , "
    sql +=  "       decode(min_price       ,null,0,min_price       ) min_price        , "
    sql +=  "       decode(vol             ,null,0,vol             ) vol              , "
    sql +=  "       decode(amount          ,null,0,amount          ) amount           , "
    sql +=  "       decode(MA6             ,null,0,MA6             ) MA6              , "
    sql +=  "       decode(MA12            ,null,0,MA12            ) MA12             , "
    sql +=  "       decode(MA20            ,null,0,MA20            ) MA20             , "
    sql +=  "       decode(MA30            ,null,0,MA30            ) MA30             , "
    sql +=  "       decode(MA45            ,null,0,MA45            ) MA45             , "
    sql +=  "       decode(MA60            ,null,0,MA60            ) MA60             , "
    sql +=  "       decode(MA125           ,null,0,MA125           ) MA125            , "
    sql +=  "       decode(MA250           ,null,0,MA250           ) MA250            , "
    sql +=  "       decode(KDJ_K           ,null,0,KDJ_K           ) KDJ_K            , "
    sql +=  "       decode(KDJ_D           ,null,0,KDJ_D           ) KDJ_D            , "
    sql +=  "       decode(KDJ_J           ,null,0,KDJ_J           ) KDJ_J            , "
    sql +=  "       decode(xstd_SLONG      ,null,0,xstd_SLONG      ) xstd_SLONG       , "
    sql +=  "       decode(xstd_SSHORT     ,null,0,xstd_SSHORT     ) xstd_SSHORT      , "
    sql +=  "       decode(xstd_LLONG      ,null,0,xstd_LLONG      ) xstd_LLONG       , "
    sql +=  "       decode(xstd_LSHORT     ,null,0,xstd_LSHORT     ) xstd_LSHORT      , "
    sql +=  "       decode(BOLL_uBOLL      ,null,0,BOLL_uBOLL      ) BOLL_uBOLL       , "
    sql +=  "       decode(BOLL_dBOLL      ,null,0,BOLL_dBOLL      ) BOLL_dBOLL       , "
    sql +=  "       decode(BOLL_BOLL       ,null,0,BOLL_BOLL       ) BOLL_BOLL        , "
    sql +=  "       decode(MACD_DIF        ,null,0,MACD_DIF        ) MACD_DIF         , "
    sql +=  "       decode(MACD_MACD       ,null,0,MACD_MACD       ) MACD_MACD        , "
    sql +=  "       decode(MACD_DIF_MACD   ,null,0,MACD_DIF_MACD   ) MACD_DIF_MACD    , "
    sql +=  "       decode(DPO_DPO         ,null,0,DPO_DPO         ) DPO_DPO          , "
    sql +=  "       decode(DPO_6MA         ,null,0,DPO_6MA         ) DPO_6MA            "
    sql +=  "from tb_stock_data_daily where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('20120101000000','yyyymmddhh24miss')"
    sql +=  "order by shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
    return data

def get_stock_data_daily_101(begin_time="",end_time=""):
    print(begin_time,end_time)
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select a.code , "
    sql +=  "       to_char(a.shi_jian,'yyyy-mm-dd') shi_jian , "
    sql +=  "       a.price            , "
    sql +=  "       a.zhang_die  return, "
    sql +=  "       a.zhang_die_rate   , "
    sql +=  "       a.price_today_open , "
    sql +=  "       a.price_last_day   , "
    sql +=  "       a.max_price        , "
    sql +=  "       a.min_price        , "
    sql +=  "       a.vol              , "
    sql +=  "       a.amount           , "
    sql +=  "       b.market_cap "
    sql +=  "from tb_stock_data_daily a ,tb_stock_data_market_cap b where "
#     sql +=  "  a.code in ('600668','600009') and"
#     sql +=  "  a.code in ('600009') and"
    sql +=  "  a.code = b.code "
    sql +=  "    and           "
    sql +=  "  to_char(a.shi_jian,'yyyy-mm-dd') = b.shi_jian "
    sql +=  "    and "
    sql +=  "  a.shi_jian <= to_date('" + end_time   + " 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +=  "    and "
    sql +=  "  a.shi_jian >= to_date('" + begin_time + " 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "order by a.shi_jian asc "    

    data = pd.read_sql_query(sql,con = engine)
    
    sql   = "select distinct( to_date(shi_jian||' 00:00:00','yyyy-mm-dd hh24:mi:ss')) shi_jian from tb_stock_data_market_cap where "
#     sql +=  " code in ('600668','600009') and"
    sql +=  " to_date(shi_jian||' 15:00:00','yyyy-mm-dd hh24:mi:ss') <= to_date('" + end_time   + " 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +=  "   and "
    sql +=  " to_date(shi_jian||' 15:00:00','yyyy-mm-dd hh24:mi:ss') >= to_date('" + begin_time + " 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "order by shi_jian asc"    
    tray_date = pd.read_sql_query(sql,con = engine)

    return data , tray_date

def get_stock_data_daily_my_f(begin_time="",end_time=""):
#     print(begin_time,end_time)
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  =  "select a.code , "
    sql +=  "       to_char(a.shi_jian,'yyyy-mm-dd') shi_jian , "
    sql +=  "       a.price            , "
    sql +=  "       a.zhang_die  return, "
    sql +=  "       a.zhang_die_rate   , "
    sql +=  "       a.price_today_open , "
    sql +=  "       a.price_last_day   , "
    sql +=  "       a.max_price        , "
    sql +=  "       a.min_price        , "
    sql +=  "       a.vol              , "
    sql +=  "       a.amount           , "
    sql +=  "       a.amount_last_day  , "
    sql +=  "       b.market_cap "
    sql +=  "from tb_stock_data_daily a ,tb_stock_data_market_cap b where "
#     sql +=  "  a.code in ('600668','600009') and"
#     sql +=  "  a.code in ('600009') and"
    sql +=  "  a.code = b.code "
    sql +=  "    and           "
    sql +=  "  to_char(a.shi_jian,'yyyy-mm-dd') = b.shi_jian "
    sql +=  "    and "
    sql +=  "  a.shi_jian <= to_date('" + end_time   + " 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "    and "
    sql +=  "  a.shi_jian >= to_date('" + begin_time + " 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "order by a.shi_jian desc "    

    data = pd.read_sql_query(sql,con = engine)

    return data 

def get_stock_data_daily_101_price(code):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select price,to_char(shi_jian,'yyyy-mm-dd') shi_jian from tb_stock_data_daily where "             
    sql += "  code = '" + code + "'"                                  
    sql += "    and                                                   "           
    sql += "  shi_jian >= (                                           "           
    sql += "                 select min(shi_jian) from tb_stock_data_daily where "
    sql += "                   code = '" + code + "'"                                           
    sql += "                     and "
    sql += "                   shi_jian > (select min(shi_jian) from tb_stock_data_daily where code = '" + code + "')"
    sql += "                     and "
    sql += "                   max_price <> min_price                            "
    sql += "                     and                                             "
    sql += "                   amount >0                                         "
    sql += "              )  order by shi_jian asc                               "    
    data = pd.read_sql_query(sql , con = engine)
    return data

def get_stock_data_daily_wind_price(code):
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select close price,shi_jian from tb_stock_data_daily_wind where "             
    sql += "  code = '" + code + "'"                                  
    sql += "    and                                                   "           
    sql += "  shi_jian >= (                                           "           
    sql += "                 select min(shi_jian) from tb_stock_data_daily_wind where "
    sql += "                   code = '" + code + "'"                                           
    sql += "                     and "
    sql += "                   shi_jian > (select min(shi_jian) from tb_stock_data_daily_wind where code = '" + code + "')"
    sql += "                     and "
    sql += "                   high <> low          "
    sql += "                     and                "
    sql += "                   amt >0               "
    sql += "              )  order by shi_jian asc  "    
    data = pd.read_sql_query(sql , con = engine)
    return data

def get_101_data(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  = "select distinct(to_char(shi_jian,'yyyy-mm-dd')) shi_jian from TB_STOCK_ALPHA101 where "
    sql += "  shi_jian >= to_date('" + start + " 15:00:00','yyyy-mm-dd hh24:mi:ss')"
    sql += "    and "
    sql += "  shi_jian <  to_date('" + end   + " 15:00:00','yyyy-mm-dd hh24:mi:ss')"
    sql += "order by shi_jian asc"
    data = pd.read_sql_query(sql,con = engine)       
    
    shi_jians = data["shi_jian"].values     
            
    data_101   = []
    CodeReturn = []
    TotalReturn= []
    Selected   = []
    code       = []
    
    for shi_jian in shi_jians :        
        sql  ="select code,"
        sql +="decode(alpha_001,null,0,0,1E-5,alpha_001) alpha_001,"
        sql +="decode(alpha_002,null,0,0,1E-5,alpha_002) alpha_002,"
        sql +="decode(alpha_003,null,0,0,1E-5,alpha_003) alpha_003,"
        sql +="decode(alpha_004,null,0,0,1E-5,alpha_004) alpha_004,"
        sql +="decode(alpha_006,null,0,0,1E-5,alpha_006) alpha_006,"
        sql +="decode(alpha_007,null,0,0,1E-5,alpha_007) alpha_007,"
        sql +="decode(alpha_008,null,0,0,1E-5,alpha_008) alpha_008,"
        sql +="decode(alpha_009,null,0,0,1E-5,alpha_009) alpha_009,"
        sql +="decode(alpha_010,null,0,0,1E-5,alpha_010) alpha_010,"
        sql +="decode(alpha_012,null,0,0,1E-5,alpha_012) alpha_012,"
        sql +="decode(alpha_013,null,0,0,1E-5,alpha_013) alpha_013,"
        sql +="decode(alpha_014,null,0,0,1E-5,alpha_014) alpha_014,"
        sql +="decode(alpha_015,null,0,0,1E-5,alpha_015) alpha_015,"
        sql +="decode(alpha_016,null,0,0,1E-5,alpha_016) alpha_016,"
        sql +="decode(alpha_017,null,0,0,1E-5,alpha_017) alpha_017,"
        sql +="decode(alpha_018,null,0,0,1E-5,alpha_018) alpha_018,"
        sql +="decode(alpha_019,null,0,0,1E-5,alpha_019) alpha_019,"
        sql +="decode(alpha_020,null,0,0,1E-5,alpha_020) alpha_020,"
        sql +="decode(alpha_021,null,0,0,1E-5,alpha_021) alpha_021,"
        sql +="decode(alpha_022,null,0,0,1E-5,alpha_022) alpha_022,"
        sql +="decode(alpha_023,null,0,0,1E-5,alpha_023) alpha_023,"
        sql +="decode(alpha_024,null,0,0,1E-5,alpha_024) alpha_024,"
        sql +="decode(alpha_026,null,0,0,1E-5,alpha_026) alpha_026,"
        sql +="decode(alpha_028,null,0,0,1E-5,alpha_028) alpha_028,"
        sql +="decode(alpha_029,null,0,0,1E-5,alpha_029) alpha_029,"
        sql +="decode(alpha_030,null,0,0,1E-5,alpha_030) alpha_030,"
        sql +="decode(alpha_031,null,0,0,1E-5,alpha_031) alpha_031,"
        sql +="decode(alpha_033,null,0,0,1E-5,alpha_033) alpha_033,"
        sql +="decode(alpha_034,null,0,0,1E-5,alpha_034) alpha_034,"
        sql +="decode(alpha_035,null,0,0,1E-5,alpha_035) alpha_035,"
        sql +="decode(alpha_037,null,0,0,1E-5,alpha_037) alpha_037,"
        sql +="decode(alpha_038,null,0,0,1E-5,alpha_038) alpha_038,"
        sql +="decode(alpha_039,null,0,0,1E-5,alpha_039) alpha_039,"
        sql +="decode(alpha_040,null,0,0,1E-5,alpha_040) alpha_040,"
        sql +="decode(alpha_043,null,0,0,1E-5,alpha_043) alpha_043,"
        sql +="decode(alpha_044,null,0,0,1E-5,alpha_044) alpha_044,"
        sql +="decode(alpha_045,null,0,0,1E-5,alpha_045) alpha_045,"
        sql +="decode(alpha_046,null,0,0,1E-5,alpha_046) alpha_046,"
        sql +="decode(alpha_049,null,0,0,1E-5,alpha_049) alpha_049,"
        sql +="decode(alpha_051,null,0,0,1E-5,alpha_051) alpha_051,"
        sql +="decode(alpha_052,null,0,0,1E-5,alpha_052) alpha_052,"
        sql +="decode(alpha_053,null,0,0,1E-5,alpha_053) alpha_053,"
        sql +="decode(alpha_054,null,0,0,1E-5,alpha_054) alpha_054,"
        sql +="decode(alpha_055,null,0,0,1E-5,alpha_055) alpha_055,"
        sql +="decode(alpha_056,null,0,0,1E-5,alpha_056) alpha_056,"
        sql +="decode(alpha_060,null,0,0,1E-5,alpha_060) alpha_060 "
        sql +="from TB_STOCK_ALPHA101 where shi_jian = to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
        sql +="order by code asc"        
        data = pd.read_sql_query(sql,con = engine)
         
        d    = data["code"].values
        data = data.drop('code', 1)
        
        code.append(d.tolist())
        data_101.append(data)
        

        sql  = "select code, return , ret_std from tb_stock_101_return where "
        sql += "shi_jian='" + shi_jian +"' and "
        sql += "code in (select code from TB_STOCK_ALPHA101 where shi_jian = to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss')) "
        sql += "order by code asc"
        data = pd.read_sql_query(sql,con = engine) 
        CodeReturn.append(data)
         
#         sql = "select return from tb_stock_101_total_return where shi_jian='" + shi_jian +"'"
#         data = pd.read_sql_query(sql,con = engine) 
#         TotalReturn.append(data["return"].values)    

#         sql  = "select selected from tb_stock_101_selected where "
#         sql += "shi_jian='" + shi_jian +"' and "
#         sql += "code in (select code from TB_STOCK_ALPHA101 where shi_jian = to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss')) "
#         sql += "order by code asc"
#         data = pd.read_sql_query(sql,con = engine) 
#         Selected.append(np.array(data))            
                           
    data = {
                "data_101"    :data_101    ,
                "CodeReturn"  :CodeReturn  ,
                "TotalReturn" :TotalReturn ,
                "Selected"    :Selected    ,  
                "shi_jian"    :shi_jians   ,
                "code"        :code        ,       
           }
    
    return data


def get_101_data_test(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
               
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    sql +="decode(a.alpha_001,null,0,0,1E-5,a.alpha_001) alpha_001,"
    sql +="decode(a.alpha_002,null,0,0,1E-5,a.alpha_002) alpha_002,"
    sql +="decode(a.alpha_003,null,0,0,1E-5,a.alpha_003) alpha_003,"
    sql +="decode(a.alpha_004,null,0,0,1E-5,a.alpha_004) alpha_004,"
    sql +="decode(a.alpha_006,null,0,0,1E-5,a.alpha_006) alpha_006,"
    sql +="decode(a.alpha_007,null,0,0,1E-5,a.alpha_007) alpha_007,"
    sql +="decode(a.alpha_008,null,0,0,1E-5,a.alpha_008) alpha_008,"
    sql +="decode(a.alpha_009,null,0,0,1E-5,a.alpha_009) alpha_009,"
    sql +="decode(a.alpha_010,null,0,0,1E-5,a.alpha_010) alpha_010,"
    sql +="decode(a.alpha_012,null,0,0,1E-5,a.alpha_012) alpha_012,"
    sql +="decode(a.alpha_013,null,0,0,1E-5,a.alpha_013) alpha_013,"
    sql +="decode(a.alpha_014,null,0,0,1E-5,a.alpha_014) alpha_014,"
    sql +="decode(a.alpha_015,null,0,0,1E-5,a.alpha_015) alpha_015,"
    sql +="decode(a.alpha_016,null,0,0,1E-5,a.alpha_016) alpha_016,"
    sql +="decode(a.alpha_017,null,0,0,1E-5,a.alpha_017) alpha_017,"
    sql +="decode(a.alpha_018,null,0,0,1E-5,a.alpha_018) alpha_018,"
    sql +="decode(a.alpha_019,null,0,0,1E-5,a.alpha_019) alpha_019,"
    sql +="decode(a.alpha_020,null,0,0,1E-5,a.alpha_020) alpha_020,"
    sql +="decode(a.alpha_021,null,0,0,1E-5,a.alpha_021) alpha_021,"
    sql +="decode(a.alpha_022,null,0,0,1E-5,a.alpha_022) alpha_022,"
    sql +="decode(a.alpha_023,null,0,0,1E-5,a.alpha_023) alpha_023,"
    sql +="decode(a.alpha_024,null,0,0,1E-5,a.alpha_024) alpha_024,"
    sql +="decode(a.alpha_026,null,0,0,1E-5,a.alpha_026) alpha_026,"
    sql +="decode(a.alpha_028,null,0,0,1E-5,a.alpha_028) alpha_028,"
    sql +="decode(a.alpha_029,null,0,0,1E-5,a.alpha_029) alpha_029,"
    sql +="decode(a.alpha_030,null,0,0,1E-5,a.alpha_030) alpha_030,"
    sql +="decode(a.alpha_031,null,0,0,1E-5,a.alpha_031) alpha_031,"
    sql +="decode(a.alpha_033,null,0,0,1E-5,a.alpha_033) alpha_033,"
    sql +="decode(a.alpha_034,null,0,0,1E-5,a.alpha_034) alpha_034,"
    sql +="decode(a.alpha_035,null,0,0,1E-5,a.alpha_035) alpha_035,"
    sql +="decode(a.alpha_037,null,0,0,1E-5,a.alpha_037) alpha_037,"
    sql +="decode(a.alpha_038,null,0,0,1E-5,a.alpha_038) alpha_038,"
    sql +="decode(a.alpha_039,null,0,0,1E-5,a.alpha_039) alpha_039,"
    sql +="decode(a.alpha_040,null,0,0,1E-5,a.alpha_040) alpha_040,"
    sql +="decode(a.alpha_043,null,0,0,1E-5,a.alpha_043) alpha_043,"
    sql +="decode(a.alpha_044,null,0,0,1E-5,a.alpha_044) alpha_044,"
    sql +="decode(a.alpha_045,null,0,0,1E-5,a.alpha_045) alpha_045,"
    sql +="decode(a.alpha_046,null,0,0,1E-5,a.alpha_046) alpha_046,"
    sql +="decode(a.alpha_049,null,0,0,1E-5,a.alpha_049) alpha_049,"
    sql +="decode(a.alpha_051,null,0,0,1E-5,a.alpha_051) alpha_051,"
    sql +="decode(a.alpha_052,null,0,0,1E-5,a.alpha_052) alpha_052,"
    sql +="decode(a.alpha_053,null,0,0,1E-5,a.alpha_053) alpha_053,"
    sql +="decode(a.alpha_054,null,0,0,1E-5,a.alpha_054) alpha_054,"
    sql +="decode(a.alpha_055,null,0,0,1E-5,a.alpha_055) alpha_055,"
    sql +="decode(a.alpha_056,null,0,0,1E-5,a.alpha_056) alpha_056,"
    sql +="decode(a.alpha_060,null,0,0,1E-5,a.alpha_060) alpha_060 "
    sql +="from TB_STOCK_ALPHA101 a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= to_date('" + start +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian <  to_date('" + end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian  = to_date(b.shi_jian ||' 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "    
#     sql +="  rownum < 6"                    

    data = pd.read_sql_query(sql,con = engine)
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res

'''
def get_101_data_test1(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
                                           
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    #sql +="a.alpha_001  , "
    sql +="a.alpha_002  , "
    sql +="a.alpha_003  , "
    #sql +="a.alpha_004  , "
    sql +="a.alpha_006  , "
    #sql +="a.alpha_007  , "
    sql +="a.alpha_008  , "
    sql +="a.alpha_009  , "
    sql +="a.alpha_010  , "
    sql +="a.alpha_012  , "
    sql +="a.alpha_013  , "
    sql +="a.alpha_014  , "
    sql +="a.alpha_015  , "
    sql +="a.alpha_016  , "
    sql +="a.alpha_017  , "
    sql +="a.alpha_018  , "
    sql +="a.alpha_019  , "
    sql +="a.alpha_020  , "
    #sql +="a.alpha_021  , "
    sql +="a.alpha_022  , "
    #sql +="a.alpha_023  , "
    sql +="a.alpha_024  , "
    sql +="a.alpha_026  , "
    sql +="a.alpha_028  , "
    sql +="a.alpha_029  , "
    sql +="a.alpha_030  , "
    sql +="a.alpha_031  , "
    sql +="a.alpha_033  , "
    sql +="a.alpha_034  , "
    sql +="a.alpha_035  , "
    sql +="a.alpha_037  , "
    sql +="a.alpha_038  , "
    sql +="a.alpha_039  , "
    sql +="a.alpha_040  , "
    sql +="a.alpha_043  , "
    sql +="a.alpha_044  , "
    sql +="a.alpha_045  , "
    #sql +="a.alpha_046  , "
    #sql +="a.alpha_049  , "
    #sql +="a.alpha_051  , "
    #sql +="a.alpha_052  , "
    sql +="a.alpha_053  , "
    sql +="a.alpha_054  , "
    sql +="a.alpha_055  , "
    sql +="a.alpha_056  , "
    sql +="a.alpha_060    "
    sql +="from TB_STOCK_ALPHA101_1 a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= to_date('" + start +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian <  to_date('" + end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian  = to_date(b.shi_jian ||' 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "
#     sql +="  ( "  
#     sql +="    b.ret_std <=1/3 "  
#     sql +="       or "  
#     sql +="    b.ret_std >=2/3"
#     sql +="  )"                      
#     sql +="     and "    
#     sql +="  rownum < 6"                    

#     print(sql)
    data = pd.read_sql_query(sql,con = engine)
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res

def get_101_data_train1(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
               
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    #sql +="a.alpha_001  , "
    sql +="a.alpha_002  , "
    sql +="a.alpha_003  , "
    #sql +="a.alpha_004  , "
    sql +="a.alpha_006  , "
    #sql +="a.alpha_007  , "
    sql +="a.alpha_008  , "
    sql +="a.alpha_009  , "
    sql +="a.alpha_010  , "
    sql +="a.alpha_012  , "
    sql +="a.alpha_013  , "
    sql +="a.alpha_014  , "
    sql +="a.alpha_015  , "
    sql +="a.alpha_016  , "
    sql +="a.alpha_017  , "
    sql +="a.alpha_018  , "
    sql +="a.alpha_019  , "
    sql +="a.alpha_020  , "
    #sql +="a.alpha_021  , "
    sql +="a.alpha_022  , "
    #sql +="a.alpha_023  , "
    sql +="a.alpha_024  , "
    sql +="a.alpha_026  , "
    sql +="a.alpha_028  , "
    sql +="a.alpha_029  , "
    sql +="a.alpha_030  , "
    sql +="a.alpha_031  , "
    sql +="a.alpha_033  , "
    sql +="a.alpha_034  , "
    sql +="a.alpha_035  , "
    sql +="a.alpha_037  , "
    sql +="a.alpha_038  , "
    sql +="a.alpha_039  , "
    sql +="a.alpha_040  , "
    sql +="a.alpha_043  , "
    sql +="a.alpha_044  , "
    sql +="a.alpha_045  , "
    #sql +="a.alpha_046  , "
    #sql +="a.alpha_049  , "
    #sql +="a.alpha_051  , "
    #sql +="a.alpha_052  , "
    sql +="a.alpha_053  , "
    sql +="a.alpha_054  , "
    sql +="a.alpha_055  , "
    sql +="a.alpha_056  , "
    sql +="a.alpha_060    "
    sql +="from TB_STOCK_ALPHA101_1 a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= to_date('" + start +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian <  to_date('" + end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian  = to_date(b.shi_jian ||' 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +="     and "    
    sql +="  a.code  = b.code "    
    sql +="     and "
    sql +="  ( "  
    sql +="    b.ret_std <=1/4 "  
    sql +="       or "  
    sql +="    b.ret_std >=3/4"
    sql +="  )"                      
#     sql +="     and "    
#     sql +="  rownum < 6"              
#     sql +="Order By dbms_random.value "      

    data = pd.read_sql_query(sql,con = engine)
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res
'''
def get_101_data_test1(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
                                           
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
#     sql +="b.ret_hot    , "
    sql +="a.alpha_001  , "
    sql +="a.alpha_002  , "
    sql +="a.alpha_003  , "
    sql +="a.alpha_004  , "
    sql +="a.alpha_005  , "
    sql +="a.alpha_006  , "
    sql +="a.alpha_007  , "
    sql +="a.alpha_008  , "
    sql +="a.alpha_009  , "
    sql +="a.alpha_010  , "
    sql +="a.alpha_011  , "
    sql +="a.alpha_012  , "
    sql +="a.alpha_013  , "
    sql +="a.alpha_014  , "
    sql +="a.alpha_015  , "
    sql +="a.alpha_016  , "
    sql +="a.alpha_017  , "
    sql +="a.alpha_018  , "
#     sql +="a.alpha_019  , "
    sql +="a.alpha_020  , "
    sql +="a.alpha_021  , "
    sql +="a.alpha_022  , "
    sql +="a.alpha_023  , "
    sql +="a.alpha_024  , "
    sql +="a.alpha_025  , "
    sql +="a.alpha_026  , "
    sql +="a.alpha_027  , "
    sql +="a.alpha_028  , "
    sql +="a.alpha_029  , "
    sql +="a.alpha_030  , "
    sql +="a.alpha_031  , "
#     sql +="a.alpha_032  , "
    sql +="a.alpha_033  , "
    sql +="a.alpha_034  , "
    sql +="a.alpha_035  , "
#     sql +="a.alpha_036  , "
#     sql +="a.alpha_037  , "
    sql +="a.alpha_038  , "
#     sql +="a.alpha_039  , "
    sql +="a.alpha_040  , "
    sql +="a.alpha_041  , "
    sql +="a.alpha_042  , "
    sql +="a.alpha_043  , "
    sql +="a.alpha_044  , "
    sql +="a.alpha_045  , "
    sql +="a.alpha_046  , "
    sql +="a.alpha_047  , "
    sql +="a.alpha_049  , "
    sql +="a.alpha_050  , "
    sql +="a.alpha_051  , "
#     sql +="a.alpha_052  , "
    sql +="a.alpha_053  , "
    sql +="a.alpha_054  , "
    sql +="a.alpha_055  , "
    sql +="a.alpha_056  , "
    sql +="a.alpha_057  , "
    sql +="a.alpha_060  , "
    sql +="a.alpha_061  , "
    sql +="a.alpha_062  , "
    sql +="a.alpha_064  , "
    sql +="a.alpha_065  , "
    sql +="a.alpha_066  , "
#     sql +="a.alpha_071  , "
    sql +="a.alpha_072  , "
    sql +="a.alpha_073  , "
    sql +="a.alpha_074  , "
    sql +="a.alpha_075  , "
    sql +="a.alpha_077  , "
    sql +="a.alpha_078  , "
    sql +="a.alpha_083  , "
    sql +="a.alpha_085  , "
    sql +="a.alpha_086  , "
    sql +="a.alpha_088  , "
    sql +="a.alpha_092  , "
    sql +="a.alpha_094  , "
    sql +="a.alpha_095  , "
    sql +="a.alpha_096  , "
    sql +="a.alpha_098  , "
    sql +="a.alpha_099  , "
    sql +="a.alpha_101    "
    sql +="from TB_STOCK_ALPHA101_1 a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= to_date('" + start +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian <  to_date('" + end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian  = to_date(b.shi_jian ||' 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "
#     sql +="  ( "  
#     sql +="    b.ret_std <=1/3 "  
#     sql +="       or "  
#     sql +="    b.ret_std >=2/3"
#     sql +="  )"                      
#     sql +="     and "    
#     sql +="  rownum < 6"                    

#     print(sql)
    data = pd.read_sql_query(sql,con = engine)
    data = data.dropna(axis=0, how='any')
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
#     CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
#     data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res

def get_101_data_test1_my_f(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
                                           
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    sql +="a.f1  , "
    sql +="a.f2  , "
    sql +="a.f3  , "
    sql +="a.f4  , "
    sql +="a.f5  , "
    sql +="a.f6  , " 
    sql +="a.f7  , "
    sql +="a.f8  , "
    sql +="a.f9  , "
    sql +="a.f10 , "
    sql +="a.f11 , "
    sql +="a.f12 , " 
    sql +="a.f13 , "
    sql +="a.f14 , "
    sql +="a.f15 , "    
    sql +="a.f16   "
    sql +="from tb_stock_my_f a , tb_stock_101_return b where" 
    sql +="  to_date(a.shi_jian||' 15:00:00','yyyy-mm-dd hh24:mi:ss') >= to_date('" + start +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  to_date(a.shi_jian||' 15:00:00','yyyy-mm-dd hh24:mi:ss') <  to_date('" + end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  to_date(a.shi_jian||' 15:00:00','yyyy-mm-dd hh24:mi:ss')  = to_date(b.shi_jian ||' 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "
#     sql +="  ( "  
#     sql +="    b.ret_std <=1/3 "  
#     sql +="       or "  
#     sql +="    b.ret_std >=2/3"
#     sql +="  )"                      
#     sql +="     and "    
#     sql +="  rownum < 6"                    

#     print(sql)
    data = pd.read_sql_query(sql,con = engine)
    data = data.dropna(axis=0, how='any')
    res_data = data
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res ,res_data

def get_101_data_test_wind(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
                                           
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    sql +="a.pre_close           ,"        
    sql +="a.open                ,"
    sql +="a.high                ,"
    sql +="a.low                 ,"
    sql +="a.close               ,"
    sql +="a.volume              ,"
    sql +="a.amt                 ,"
    sql +="a.dealnum             ,"
    sql +="a.chg                 ,"
    sql +="a.pct_chg             ,"
    sql +="a.swing               ,"
    sql +="a.vwap                ,"       
    sql +="a.rel_ipo_chg         ,"
    sql +="a.rel_ipo_pct_chg     ,"
    sql +="a.total_shares        ,"
    sql +="a.free_float_shares   ,"
    sql +="a.mf_amt              ,"
    sql +="a.mf_vol              ,"
    sql +="a.mf_amt_ratio        ,"
    sql +="a.mf_vol_ratio        ,"
    sql +="a.mf_amt_close        ,"
    sql +="a.mf_amt_open         ,"
    sql +="a.pe_ttm              ,"
    sql +="a.val_pe_deducted_ttm ,"
    sql +="a.pe_lyr              ,"
    sql +="a.pb_lf               ,"
    sql +="a.pb_mrq              ,"
    sql +="a.ps_ttm              ,"
    sql +="a.ps_lyr              ,"
    sql +="a.pcf_ocf_ttm         ,"
    sql +="a.pcf_ncf_ttm         ,"
    sql +="a.pcf_ocflyr          ,"
    sql +="a.pcf_nflyr           ,"
    sql +="a.pe_est              ,"
    sql +="a.estpe_FY1           ,"
    sql +="a.estpe_FY2           ,"
    sql +="a.estpe_FY3           ,"
    sql +="a.pe_est_last         ,"
    sql +="a.pe_est_ftm          ,"
    sql +="a.est_peg             ,"
    sql +="a.estpeg_FY1          ,"
    sql +="a.estpeg_FY2          ,"
    sql +="a.estpeg_FTM          ,"
    sql +="a.estpb               ,"
    sql +="a.estpb_FY1           ,"
    sql +="a.estpb_FY2           ,"
    sql +="a.estpb_FY3           ,"
    sql +="a.ev1                 ,"
    sql +="a.ev2                 ,"
    sql +="a.ev2_to_ebitda       ,"
    sql +="a.history_low         ,"
    sql +="a.stage_high          ,"
    sql +="a.history_high        ,"
    sql +="a.stage_low           ,"
    sql +="a.up_days             ,"
    sql +="a.down_days           ,"
    sql +="a.breakout_ma         ,"
    sql +="a.breakdown_ma        ,"
    sql +="a.bull_bear_ma        ,"
    sql +="a.holder_num          ,"
    sql +="a.holder_avgnum       ,"
    sql +="a.holder_totalbyinst  ,"
    sql +="a.holder_pctbyinst    ,"
    sql +="a.mkt_cap_ashare2     ,"
    sql +="a.mkt_cap_ashare      "
    sql +="from tb_stock_data_daily_wind a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= '" + start +"' "
    sql +="     and "
    sql +="  a.shi_jian <=  '" + end   +"' "
    sql +="     and "
    sql +="  a.shi_jian = b.shi_jian "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "
#     sql +="  ( "  
#     sql +="    b.ret_std <=1/5 "  
#     sql +="       or "  
#     sql +="    b.ret_std >=4/5"
#     sql +="  )"             
    sql +="Order By a.shi_jian asc "                  

#     print(sql)
    data = pd.read_sql_query(sql,con = engine)
#     data = data.dropna(axis=0, how='any')
    res_data = data
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :data_101   ,
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res ,res_data


def get_101_data_train1(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
#     sql +="b.ret_hot    , "
    sql +="a.alpha_001  , "
    sql +="a.alpha_002  , "
    sql +="a.alpha_003  , "
    sql +="a.alpha_004  , "
    sql +="a.alpha_005  , "
    sql +="a.alpha_006  , "
    sql +="a.alpha_007  , "
    sql +="a.alpha_008  , "
    sql +="a.alpha_009  , "
    sql +="a.alpha_010  , "
    sql +="a.alpha_011  , "
    sql +="a.alpha_012  , "
    sql +="a.alpha_013  , "
    sql +="a.alpha_014  , "
    sql +="a.alpha_015  , "
    sql +="a.alpha_016  , "
    sql +="a.alpha_017  , "
    sql +="a.alpha_018  , "
#     sql +="a.alpha_019  , "
    sql +="a.alpha_020  , "
    sql +="a.alpha_021  , "
    sql +="a.alpha_022  , "
    sql +="a.alpha_023  , "
    sql +="a.alpha_024  , "
    sql +="a.alpha_025  , "
    sql +="a.alpha_026  , "
    sql +="a.alpha_027  , "
    sql +="a.alpha_028  , "
    sql +="a.alpha_029  , "
    sql +="a.alpha_030  , "
    sql +="a.alpha_031  , "
#     sql +="a.alpha_032  , "
    sql +="a.alpha_033  , "
    sql +="a.alpha_034  , "
    sql +="a.alpha_035  , "
#     sql +="a.alpha_036  , "
#     sql +="a.alpha_037  , "
    sql +="a.alpha_038  , "
#     sql +="a.alpha_039  , "
    sql +="a.alpha_040  , "
    sql +="a.alpha_041  , "
    sql +="a.alpha_042  , "
    sql +="a.alpha_043  , "
    sql +="a.alpha_044  , "
    sql +="a.alpha_045  , "
    sql +="a.alpha_046  , "
    sql +="a.alpha_047  , "
    sql +="a.alpha_049  , "
    sql +="a.alpha_050  , "
    sql +="a.alpha_051  , "
#     sql +="a.alpha_052  , "
    sql +="a.alpha_053  , "
    sql +="a.alpha_054  , "
    sql +="a.alpha_055  , "
    sql +="a.alpha_056  , "
    sql +="a.alpha_057  , "
    sql +="a.alpha_060  , "
    sql +="a.alpha_061  , "
    sql +="a.alpha_062  , "
    sql +="a.alpha_064  , "
    sql +="a.alpha_065  , "
    sql +="a.alpha_066  , "
#     sql +="a.alpha_071  , "
    sql +="a.alpha_072  , "
    sql +="a.alpha_073  , "
    sql +="a.alpha_074  , "
    sql +="a.alpha_075  , "
    sql +="a.alpha_077  , "
    sql +="a.alpha_078  , "
    sql +="a.alpha_083  , "
    sql +="a.alpha_085  , "
    sql +="a.alpha_086  , "
    sql +="a.alpha_088  , "
    sql +="a.alpha_092  , "
    sql +="a.alpha_094  , "
    sql +="a.alpha_095  , "
    sql +="a.alpha_096  , "
    sql +="a.alpha_098  , "
    sql +="a.alpha_099  , "
    sql +="a.alpha_101    "
    sql +="from TB_STOCK_ALPHA101_1 a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= to_date('" + start +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian <  to_date('" + end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian  = to_date(b.shi_jian ||' 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "
#     sql +="  ( "  
#     sql +="    b.ret_std <=1/3 "  
#     sql +="       or "  
#     sql +="    b.ret_std >=2/3"
#     sql +="  )"             
    sql +="Order By dbms_random.value "          
    
    data = pd.read_sql_query(sql,con = engine)
#     data = data.dropna(axis=0, how='any')
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
#     CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
#     data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
#                 "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res


def get_101_data_train1_my_f(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    sql +="a.f1  , "
    sql +="a.f2  , "
    sql +="a.f3  , "
    sql +="a.f4  , "
    sql +="a.f5  , "
    sql +="a.f6  , " 
    sql +="a.f7  , "
    sql +="a.f8  , "
    sql +="a.f9  , "
    sql +="a.f10 , "
    sql +="a.f11 , "
    sql +="a.f12 , " 
    sql +="a.f13 , "
    sql +="a.f14 , "
    sql +="a.f15 , "    
    sql +="a.f16   "
    sql +="from tb_stock_my_f a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= '" + start +"' "
    sql +="     and "
    sql +="  a.shi_jian <  '" + end   +"' "
    sql +="     and "
    sql +="  a.shi_jian = b.shi_jian "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "
#     sql +="  ( "  
#     sql +="    b.ret_std <=1/5 "  
#     sql +="       or "  
#     sql +="    b.ret_std >=4/5"
#     sql +="  )"             
    sql +="Order By a.shi_jian asc "          
    
    data = pd.read_sql_query(sql,con = engine)
    data = data.dropna(axis=0, how='any')
    res_data = data 
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res,res_data

def get_101_data_train_wind(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    sql +="a.pre_close           ,"        
    sql +="a.open                ,"
    sql +="a.high                ,"
    sql +="a.low                 ,"
    sql +="a.close               ,"
    sql +="a.volume              ,"
    sql +="a.amt                 ,"
    sql +="a.dealnum             ,"
    sql +="a.chg                 ,"
    sql +="a.pct_chg             ,"
    sql +="a.swing               ,"
    sql +="a.vwap                ,"       
    sql +="a.rel_ipo_chg         ,"
    sql +="a.rel_ipo_pct_chg     ,"
    sql +="a.total_shares        ,"
    sql +="a.free_float_shares   ,"
    sql +="a.mf_amt              ,"
    sql +="a.mf_vol              ,"
    sql +="a.mf_amt_ratio        ,"
    sql +="a.mf_vol_ratio        ,"
    sql +="a.mf_amt_close        ,"
    sql +="a.mf_amt_open         ,"
    sql +="a.pe_ttm              ,"
    sql +="a.val_pe_deducted_ttm ,"
    sql +="a.pe_lyr              ,"
    sql +="a.pb_lf               ,"
    sql +="a.pb_mrq              ,"
    sql +="a.ps_ttm              ,"
    sql +="a.ps_lyr              ,"
    sql +="a.pcf_ocf_ttm         ,"
    sql +="a.pcf_ncf_ttm         ,"
    sql +="a.pcf_ocflyr          ,"
    sql +="a.pcf_nflyr           ,"
    sql +="a.pe_est              ,"
    sql +="a.estpe_FY1           ,"
    sql +="a.estpe_FY2           ,"
    sql +="a.estpe_FY3           ,"
    sql +="a.pe_est_last         ,"
    sql +="a.pe_est_ftm          ,"
    sql +="a.est_peg             ,"
    sql +="a.estpeg_FY1          ,"
    sql +="a.estpeg_FY2          ,"
    sql +="a.estpeg_FTM          ,"
    sql +="a.estpb               ,"
    sql +="a.estpb_FY1           ,"
    sql +="a.estpb_FY2           ,"
    sql +="a.estpb_FY3           ,"
    sql +="a.ev1                 ,"
    sql +="a.ev2                 ,"
    sql +="a.ev2_to_ebitda       ,"
    sql +="a.history_low         ,"
    sql +="a.stage_high          ,"
    sql +="a.history_high        ,"
    sql +="a.stage_low           ,"
    sql +="a.up_days             ,"
    sql +="a.down_days           ,"
    sql +="a.breakout_ma         ,"
    sql +="a.breakdown_ma        ,"
    sql +="a.bull_bear_ma        ,"
    sql +="a.holder_num          ,"
    sql +="a.holder_avgnum       ,"
    sql +="a.holder_totalbyinst  ,"
    sql +="a.holder_pctbyinst    ,"
    sql +="a.mkt_cap_ashare2     ,"
    sql +="a.mkt_cap_ashare      "
    sql +="from tb_stock_data_daily_wind a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= '" + start +"' "
    sql +="     and "
    sql +="  a.shi_jian <=  '" + end   +"' "
    sql +="     and "
    sql +="  a.shi_jian = b.shi_jian "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "
#     sql +="  ( "  
#     sql +="    b.ret_std <=1/5 "  
#     sql +="       or "  
#     sql +="    b.ret_std >=4/5"
#     sql +="  )"             
    sql +="Order By a.shi_jian asc "          
    
    data = pd.read_sql_query(sql,con = engine)
#     data = data.dropna(axis=0, how='any')
    res_data = data 
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :data_101   ,
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res,res_data

def get_101_data_train1_my_f_lstm(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    sql +="a.f1  , "
    sql +="a.f2  , "
    sql +="a.f3  , "
    sql +="a.f4  , "
    sql +="a.f5  , "
    sql +="a.f6    " 
    sql +="from tb_stock_my_f a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= '" + start +"' "
    sql +="     and "
    sql +="  a.shi_jian <=  '" + end   +"' "
    sql +="     and "
    sql +="  a.shi_jian = b.shi_jian "
    sql +="     and "    
    sql +="  a.code  = b.code "    
#     sql +="     and "
#     sql +="  ( "  
#     sql +="    b.ret_std <=1/5 "  
#     sql +="       or "  
#     sql +="    b.ret_std >=4/5"
#     sql +="  )"             
    sql +="Order By a.shi_jian asc "          
    
    data = pd.read_sql_query(sql,con = engine)
    data = data.dropna(axis=0, how='any')
    res_data = data 
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res,res_data



def get_101_data_for_std(shi_jian= "" ,alpha = "" ):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
               
    sql  ="select code, "
    sql += alpha + " "    
    sql +="from TB_STOCK_ALPHA101 where" 
    sql +="  shi_jian = to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "  
    sql +="    and "
    sql += alpha + " is not null "
    sql +=" order by " + alpha + " asc"
    
    
#     sql +="     and "    
#     sql +="  rownum < 6"                    

    data = pd.read_sql_query(sql,con = engine)
    
    sql  ="select count(distinct(" + alpha + " )) count "  
    sql +="from TB_STOCK_ALPHA101 where" 
    sql +="  shi_jian = to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "  
    sql +="    and "
    sql += alpha + " is not null "
    
#     sql +="     and "    
#     sql +="  rownum < 6"                    

    count = pd.read_sql_query(sql,con = engine)   
    count = count["count"].values
    count = count[0] 
           
    return data,count

def get_101_data_for_std1(shi_jian= "" ):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
               
    sql  ="select code, "
    sql +="       alpha_001 ,"
    sql +="       alpha_002 ,"
    sql +="       alpha_003 ,"
    sql +="       alpha_004 ,"
    sql +="       alpha_005 ,"
    sql +="       alpha_006 ,"
    sql +="       alpha_007 ,"
    sql +="       alpha_008 ,"
    sql +="       alpha_009 ,"
    sql +="       alpha_010 ,"
    sql +="       alpha_011 ,"
    sql +="       alpha_012 ,"
    sql +="       alpha_013 ,"
    sql +="       alpha_014 ,"
    sql +="       alpha_015 ,"
    sql +="       alpha_016 ,"
    sql +="       alpha_017 ,"
    sql +="       alpha_018 ,"
    sql +="       alpha_019 ,"
    sql +="       alpha_020 ,"
    sql +="       alpha_021 ,"
    sql +="       alpha_022 ,"
    sql +="       alpha_023 ,"
    sql +="       alpha_024 ,"
    sql +="       alpha_025 ,"
    sql +="       alpha_026 ,"
    sql +="       alpha_027 ,"
    sql +="       alpha_028 ,"
    sql +="       alpha_029 ,"
    sql +="       alpha_030 ,"
    sql +="       alpha_031 ,"
    sql +="       alpha_032 ,"
    sql +="       alpha_033 ,"
    sql +="       alpha_034 ,"
    sql +="       alpha_035 ,"
    sql +="       alpha_036 ,"
    sql +="       alpha_037 ,"
    sql +="       alpha_038 ,"
    sql +="       alpha_039 ,"
    sql +="       alpha_040 ,"
    sql +="       alpha_041 ,"
    sql +="       alpha_042 ,"
    sql +="       alpha_043 ,"
    sql +="       alpha_044 ,"
    sql +="       alpha_045 ,"
    sql +="       alpha_046 ,"
    sql +="       alpha_047 ,"
    sql +="       alpha_049 ,"
    sql +="       alpha_050 ,"
    sql +="       alpha_051 ,"
    sql +="       alpha_052 ,"
    sql +="       alpha_053 ,"
    sql +="       alpha_054 ,"
    sql +="       alpha_055 ,"
    sql +="       alpha_056 ,"
    sql +="       alpha_057 ,"
    sql +="       alpha_060 ,"
    sql +="       alpha_061 ,"
    sql +="       alpha_062 ,"
    sql +="       alpha_064 ,"
    sql +="       alpha_065 ,"
    sql +="       alpha_066 ,"
    sql +="       alpha_071 ,"
    sql +="       alpha_072 ,"
    sql +="       alpha_073 ,"
    sql +="       alpha_074 ,"
    sql +="       alpha_075 ,"
    sql +="       alpha_077 ,"
    sql +="       alpha_078 ,"
    sql +="       alpha_083 ,"
    sql +="       alpha_085 ,"
    sql +="       alpha_086 ,"
    sql +="       alpha_088 ,"
    sql +="       alpha_092 ,"
    sql +="       alpha_094 ,"
    sql +="       alpha_095 ,"
    sql +="       alpha_096 ,"
    sql +="       alpha_098 ,"
    sql +="       alpha_099 ,"
    sql +="       alpha_101 "
    sql +="from TB_STOCK_ALPHA101 where" 
    sql +="  shi_jian = to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "  

    data = pd.read_sql_query(sql,con = engine)
        
    return data


def get_101_data_train(start= "" , end =""):    
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
               
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    sql +="decode(a.alpha_001,null,0,0,1E-5,a.alpha_001) alpha_001,"
    sql +="decode(a.alpha_002,null,0,0,1E-5,a.alpha_002) alpha_002,"
    sql +="decode(a.alpha_003,null,0,0,1E-5,a.alpha_003) alpha_003,"
    sql +="decode(a.alpha_004,null,0,0,1E-5,a.alpha_004) alpha_004,"
    sql +="decode(a.alpha_006,null,0,0,1E-5,a.alpha_006) alpha_006,"
    sql +="decode(a.alpha_007,null,0,0,1E-5,a.alpha_007) alpha_007,"
    sql +="decode(a.alpha_008,null,0,0,1E-5,a.alpha_008) alpha_008,"
    sql +="decode(a.alpha_009,null,0,0,1E-5,a.alpha_009) alpha_009,"
    sql +="decode(a.alpha_010,null,0,0,1E-5,a.alpha_010) alpha_010,"
    sql +="decode(a.alpha_012,null,0,0,1E-5,a.alpha_012) alpha_012,"
    sql +="decode(a.alpha_013,null,0,0,1E-5,a.alpha_013) alpha_013,"
    sql +="decode(a.alpha_014,null,0,0,1E-5,a.alpha_014) alpha_014,"
    sql +="decode(a.alpha_015,null,0,0,1E-5,a.alpha_015) alpha_015,"
    sql +="decode(a.alpha_016,null,0,0,1E-5,a.alpha_016) alpha_016,"
    sql +="decode(a.alpha_017,null,0,0,1E-5,a.alpha_017) alpha_017,"
    sql +="decode(a.alpha_018,null,0,0,1E-5,a.alpha_018) alpha_018,"
    sql +="decode(a.alpha_019,null,0,0,1E-5,a.alpha_019) alpha_019,"
    sql +="decode(a.alpha_020,null,0,0,1E-5,a.alpha_020) alpha_020,"
    sql +="decode(a.alpha_021,null,0,0,1E-5,a.alpha_021) alpha_021,"
    sql +="decode(a.alpha_022,null,0,0,1E-5,a.alpha_022) alpha_022,"
    sql +="decode(a.alpha_023,null,0,0,1E-5,a.alpha_023) alpha_023,"
    sql +="decode(a.alpha_024,null,0,0,1E-5,a.alpha_024) alpha_024,"
    sql +="decode(a.alpha_026,null,0,0,1E-5,a.alpha_026) alpha_026,"
    sql +="decode(a.alpha_028,null,0,0,1E-5,a.alpha_028) alpha_028,"
    sql +="decode(a.alpha_029,null,0,0,1E-5,a.alpha_029) alpha_029,"
    sql +="decode(a.alpha_030,null,0,0,1E-5,a.alpha_030) alpha_030,"
    sql +="decode(a.alpha_031,null,0,0,1E-5,a.alpha_031) alpha_031,"
    sql +="decode(a.alpha_033,null,0,0,1E-5,a.alpha_033) alpha_033,"
    sql +="decode(a.alpha_034,null,0,0,1E-5,a.alpha_034) alpha_034,"
    sql +="decode(a.alpha_035,null,0,0,1E-5,a.alpha_035) alpha_035,"
    sql +="decode(a.alpha_037,null,0,0,1E-5,a.alpha_037) alpha_037,"
    sql +="decode(a.alpha_038,null,0,0,1E-5,a.alpha_038) alpha_038,"
    sql +="decode(a.alpha_039,null,0,0,1E-5,a.alpha_039) alpha_039,"
    sql +="decode(a.alpha_040,null,0,0,1E-5,a.alpha_040) alpha_040,"
    sql +="decode(a.alpha_043,null,0,0,1E-5,a.alpha_043) alpha_043,"
    sql +="decode(a.alpha_044,null,0,0,1E-5,a.alpha_044) alpha_044,"
    sql +="decode(a.alpha_045,null,0,0,1E-5,a.alpha_045) alpha_045,"
    sql +="decode(a.alpha_046,null,0,0,1E-5,a.alpha_046) alpha_046,"
    sql +="decode(a.alpha_049,null,0,0,1E-5,a.alpha_049) alpha_049,"
    sql +="decode(a.alpha_051,null,0,0,1E-5,a.alpha_051) alpha_051,"
    sql +="decode(a.alpha_052,null,0,0,1E-5,a.alpha_052) alpha_052,"
    sql +="decode(a.alpha_053,null,0,0,1E-5,a.alpha_053) alpha_053,"
    sql +="decode(a.alpha_054,null,0,0,1E-5,a.alpha_054) alpha_054,"
    sql +="decode(a.alpha_055,null,0,0,1E-5,a.alpha_055) alpha_055,"
    sql +="decode(a.alpha_056,null,0,0,1E-5,a.alpha_056) alpha_056,"
    sql +="decode(a.alpha_060,null,0,0,1E-5,a.alpha_060) alpha_060 "
    sql +="from TB_STOCK_ALPHA101 a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= to_date('" + start +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian <  to_date('" + end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian  = to_date(b.shi_jian ||' 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +="     and "    
    sql +="  a.code  = b.code "    
    sql +="     and "    
    sql +="  b.ret_hot  =  1"       
#     sql +="     and "    
#     sql +="  rownum < 6"                    

    data_1 = pd.read_sql_query(sql,con = engine)
    
    sql  ="select a.code, "
    sql +="b.shi_jian   , "
    sql +="b.return     , "
    sql +="b.ret_std    , "
    sql +="b.ret_hot    , "
    sql +="decode(a.alpha_001,null,0,0,1E-5,a.alpha_001) alpha_001,"
    sql +="decode(a.alpha_002,null,0,0,1E-5,a.alpha_002) alpha_002,"
    sql +="decode(a.alpha_003,null,0,0,1E-5,a.alpha_003) alpha_003,"
    sql +="decode(a.alpha_004,null,0,0,1E-5,a.alpha_004) alpha_004,"
    sql +="decode(a.alpha_006,null,0,0,1E-5,a.alpha_006) alpha_006,"
    sql +="decode(a.alpha_007,null,0,0,1E-5,a.alpha_007) alpha_007,"
    sql +="decode(a.alpha_008,null,0,0,1E-5,a.alpha_008) alpha_008,"
    sql +="decode(a.alpha_009,null,0,0,1E-5,a.alpha_009) alpha_009,"
    sql +="decode(a.alpha_010,null,0,0,1E-5,a.alpha_010) alpha_010,"
    sql +="decode(a.alpha_012,null,0,0,1E-5,a.alpha_012) alpha_012,"
    sql +="decode(a.alpha_013,null,0,0,1E-5,a.alpha_013) alpha_013,"
    sql +="decode(a.alpha_014,null,0,0,1E-5,a.alpha_014) alpha_014,"
    sql +="decode(a.alpha_015,null,0,0,1E-5,a.alpha_015) alpha_015,"
    sql +="decode(a.alpha_016,null,0,0,1E-5,a.alpha_016) alpha_016,"
    sql +="decode(a.alpha_017,null,0,0,1E-5,a.alpha_017) alpha_017,"
    sql +="decode(a.alpha_018,null,0,0,1E-5,a.alpha_018) alpha_018,"
    sql +="decode(a.alpha_019,null,0,0,1E-5,a.alpha_019) alpha_019,"
    sql +="decode(a.alpha_020,null,0,0,1E-5,a.alpha_020) alpha_020,"
    sql +="decode(a.alpha_021,null,0,0,1E-5,a.alpha_021) alpha_021,"
    sql +="decode(a.alpha_022,null,0,0,1E-5,a.alpha_022) alpha_022,"
    sql +="decode(a.alpha_023,null,0,0,1E-5,a.alpha_023) alpha_023,"
    sql +="decode(a.alpha_024,null,0,0,1E-5,a.alpha_024) alpha_024,"
    sql +="decode(a.alpha_026,null,0,0,1E-5,a.alpha_026) alpha_026,"
    sql +="decode(a.alpha_028,null,0,0,1E-5,a.alpha_028) alpha_028,"
    sql +="decode(a.alpha_029,null,0,0,1E-5,a.alpha_029) alpha_029,"
    sql +="decode(a.alpha_030,null,0,0,1E-5,a.alpha_030) alpha_030,"
    sql +="decode(a.alpha_031,null,0,0,1E-5,a.alpha_031) alpha_031,"
    sql +="decode(a.alpha_033,null,0,0,1E-5,a.alpha_033) alpha_033,"
    sql +="decode(a.alpha_034,null,0,0,1E-5,a.alpha_034) alpha_034,"
    sql +="decode(a.alpha_035,null,0,0,1E-5,a.alpha_035) alpha_035,"
    sql +="decode(a.alpha_037,null,0,0,1E-5,a.alpha_037) alpha_037,"
    sql +="decode(a.alpha_038,null,0,0,1E-5,a.alpha_038) alpha_038,"
    sql +="decode(a.alpha_039,null,0,0,1E-5,a.alpha_039) alpha_039,"
    sql +="decode(a.alpha_040,null,0,0,1E-5,a.alpha_040) alpha_040,"
    sql +="decode(a.alpha_043,null,0,0,1E-5,a.alpha_043) alpha_043,"
    sql +="decode(a.alpha_044,null,0,0,1E-5,a.alpha_044) alpha_044,"
    sql +="decode(a.alpha_045,null,0,0,1E-5,a.alpha_045) alpha_045,"
    sql +="decode(a.alpha_046,null,0,0,1E-5,a.alpha_046) alpha_046,"
    sql +="decode(a.alpha_049,null,0,0,1E-5,a.alpha_049) alpha_049,"
    sql +="decode(a.alpha_051,null,0,0,1E-5,a.alpha_051) alpha_051,"
    sql +="decode(a.alpha_052,null,0,0,1E-5,a.alpha_052) alpha_052,"
    sql +="decode(a.alpha_053,null,0,0,1E-5,a.alpha_053) alpha_053,"
    sql +="decode(a.alpha_054,null,0,0,1E-5,a.alpha_054) alpha_054,"
    sql +="decode(a.alpha_055,null,0,0,1E-5,a.alpha_055) alpha_055,"
    sql +="decode(a.alpha_056,null,0,0,1E-5,a.alpha_056) alpha_056,"
    sql +="decode(a.alpha_060,null,0,0,1E-5,a.alpha_060) alpha_060 "
    sql +="from TB_STOCK_ALPHA101 a , tb_stock_101_return b where" 
    sql +="  a.shi_jian >= to_date('" + start +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian <  to_date('" + end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss')  "
    sql +="     and "
    sql +="  a.shi_jian  = to_date(b.shi_jian ||' 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +="     and "    
    sql +="  a.code  = b.code "    
    sql +="     and "    
    sql +="  b.ret_hot = 0"
    sql +="     and "    
    sql +="  b.return < 0"           
    sql +="     and "    
    sql +="  rownum < =" + str(len(data_1)*1)                    

    data_0 = pd.read_sql_query(sql,con = engine)    
    
    data = pd.concat([data_1,data_0])
    data = shuffle(data)  
    
    code      = data["code"].values
    shi_jians = data["shi_jian"].values
    CodeReturn= data["return"].values
    CodeRetStd= data["ret_std"].values
    CodeRetHot= data["ret_hot"].values
    
    data = data.drop('code', 1)
    data = data.drop('shi_jian', 1)
    data = data.drop('return', 1)
    data = data.drop('ret_std', 1)
    data = data.drop('ret_hot', 1)
    
    data_101 = data
    
    res  = {
                "data_101"    :np.array(data_101   ),
                "CodeReturn"  :np.array(CodeReturn ),
                "CodeRetStd"  :np.array(CodeRetStd ),
                "CodeRetHot"  :np.array(CodeRetHot ),
                "shi_jian"    :np.array(shi_jians  ),
                "code"        :np.array(code       ),       
           }        
            
    return res

def get_101_data_3_times(today="", train_days = 10) :
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select distinct(shi_jian) shi_jian  from tb_stock_data_market_cap " 
    sql += "where "
    sql += "  shi_jian < '" + today + "'"
    sql += "    and "
    sql += "  shi_jian >= to_char(to_date('" + today + "' , 'yyyy-mm-dd') - " + str(train_days*6) + ",'yyyy-mm-dd')"
    sql += "order by shi_jian desc" 
    data = pd.read_sql_query(sql,con = engine)
    
    data = data["shi_jian"].values
#     print(data)
    
    start_date = data[train_days +1]
    split_date = data[1]
    end_date   = data[0]
    print(start_date , split_date , end_date)
    return start_date , split_date , end_date 

def get_my_f_lstm_times(today="",lenth=0,days= 30) :
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select distinct(shi_jian) shi_jian  from tb_stock_data_market_cap " 
    sql += "where "
    sql += "  shi_jian <= '" + today + "'"
    sql += "    and "
    sql += "  shi_jian >= to_char(to_date('" + today + "' , 'yyyy-mm-dd') - 400,'yyyy-mm-dd')"
    sql += "order by shi_jian desc" 
    data = pd.read_sql_query(sql,con = engine)
    
    data = data["shi_jian"].values

    train_time  = data[5:5+lenth]
    test_time   = data[0:days]   

    return train_time,test_time


def get_101_data_4_times(today="") :
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select distinct(shi_jian) shi_jian  from tb_stock_data_daily_wind " 
    sql += "where "
    sql += "  shi_jian <= '" + today + "'"
    sql += "    and "
    sql += "  shi_jian >= to_char(to_date('" + today + "' , 'yyyy-mm-dd') - 400,'yyyy-mm-dd')"
    sql += "order by shi_jian desc" 
    data = pd.read_sql_query(sql,con = engine)
    
    data = data["shi_jian"].values
#     print(data)
    
    train_begin  = data[3+60]
    train_end    = data[3]
#     train_begin  = data[0]
#     train_end    = today
    test_begin   = data[0]
    test_end     = today    
    
    print(train_begin , train_end , test_begin,test_end)
    return train_begin , train_end , test_begin,test_end 

def get_101_data_shi_jian() :
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select distinct(to_char(shi_jian,'yyyy-mm-dd')) shi_jian  from tb_stock_alpha101_1 order by shi_jian asc" 
    
    data = pd.read_sql_query(sql,con = engine)    
    data = data["shi_jian"].values
    
    return data

def get_shi_jian_my_f() :
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select distinct(shi_jian) shi_jian from tb_stock_my_f order by shi_jian asc" 
    
    data = pd.read_sql_query(sql,con = engine)    
    data = data["shi_jian"].values
    
    return data

def get_stock_data_daily_rqalpha_lmc_all_day():
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select distinct(shi_jian) shi_jian  from tb_stock_data_market_cap " 
#     sql += "where "
#     sql += " substr(code,1,1) = '3' "
#     sql += "   and "
#     sql += " code not in                            "
#     sql += " (                                      "
#     sql += "   select code from tb_stock_list where "
#     sql += "     upper(name) like '%ST%'            "
#     sql += "       or                               "
#     sql += "     upper(name) like '%退%'            "
#     sql += " )                                      " 
    sql += "order by shi_jian asc" 
    data = pd.read_sql_query(sql,con = engine)
    return data 

def get_stock_data_daily_rqalpha_lmc_all(date=''):
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    
#     sql = "select count(*) c from tb_stock_data_market_cap where shi_jian = '"+ date +"' and substr(code,1,1) = '3'"
#     data = pd.read_sql_query(sql,con = engine)
#     count = data["c"].values
#     count = count[0]
    
    sql  = "select code "                        
    sql += "from tb_stock_data_market_cap where "
    sql += " shi_jian = '"+ date +"'" 
#     if count > 0 : 
#         sql += "   and "
#         sql += " substr(code,1,1) = '3' "
#     sql += "   and "
#     sql += " code not in                            "
#     sql += " (                                      "
#     sql += "   select code from tb_stock_list where "
#     sql += "     upper(name) like '%ST%'            "
#     sql += "       or                               "
#     sql += "     upper(name) like '%退%'            "
#     sql += " )                                      "           
    sql += "order by market_cap asc"     
    data = pd.read_sql_query(sql,con = engine)
    return data    

def get_stock_data_daily_rqalpha_ma8_all_day():
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql = ""
    sql += "select distinct( to_char(shi_jian,'yyyy-mm-dd')) shi_jian     " 
    sql += "from tb_stock_data_daily where                                "
    sql += " shi_jian >= to_date('20041001000000','yyyymmddhh24miss') and "
    sql += " MA_DISTANCE_AVG_6 >0 and                                     "
    sql += " MA_DISTANCE_AVG_7 >0 and                                     "
    sql += " MA_DISTANCE_AVG_8 >0 and                                     "
    sql += " MA_DISTANCE_AVG > 0  and                                     "
    sql += " MA_DISTANCE_AVG < 5  and                                     "
    sql += " MA6   is not null and                                        "
    sql += " MA12  is not null and                                        "
    sql += " MA20  is not null and                                        "
    sql += " MA30  is not null and                                        "
    sql += " MA45  is not null and                                        "
    sql += " MA60  is not null and                                        "
    sql += " MA125 is not null and                                        "
    sql += " MA250 is not null                                            "
    sql += " order by shi_jian asc                                        "
    data = pd.read_sql_query(sql,con = engine)
    return data  

def get_stock_data_daily_rqalpha_ma8_all(endtime=''):
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql  =  "select code "          
    sql +=  "from tb_stock_data_daily where "
    sql +=  " shi_jian = to_date('"+endtime+" 15:00:00','yyyy-mm-dd hh24:mi:ss') and"
    sql +=  " MA_DISTANCE_AVG_6 >0 and "
    sql +=  " MA_DISTANCE_AVG_7 >0 and "
    sql +=  " MA_DISTANCE_AVG_8 >0 and "        
    sql +=  " MA_DISTANCE_AVG > 0  and "
    sql +=  " MA_DISTANCE_AVG < 5  and "  
    sql +=  " MA6   is not null and"
    sql +=  " MA12  is not null and"
    sql +=  " MA20  is not null and"
    sql +=  " MA30  is not null and"
    sql +=  " MA45  is not null and"
    sql +=  " MA60  is not null and"
    sql +=  " MA125 is not null and"
    sql +=  " MA250 is not null "
    sql +=  " order by MA_DISTANCE_AVG asc "
    data = pd.read_sql_query(sql,con = engine)
    return data    
        

def get_stock_data_daily_rqalpha_ma8(code,daysago=365,endtime=''):
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql  =  "select code , "
    sql +=  "       MA6              , "
    sql +=  "       MA12             , "
    sql +=  "       MA20             , "
    sql +=  "       MA30             , "
    sql +=  "       MA45             , "
    sql +=  "       MA60             , "
    sql +=  "       MA125            , "
    sql +=  "       MA250            , "
    sql +=  "       MA_DISTANCE_AVG_6, "
    sql +=  "       MA_DISTANCE_AVG_7, "
    sql +=  "       MA_DISTANCE_AVG_8, "           
    sql +=  "       to_char(shi_jian,'yyyy-mm-dd') shi_jian "
    sql +=  "from tb_stock_data_daily where "
    sql +=  "  code = '" + code + "' and "
    sql +=  "  shi_jian >= to_date('"+endtime+" 15:00:00','yyyy-mm-dd hh24:mi:ss') - " + str(daysago) 
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+endtime+" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "    and "
    sql +=  " MA6   is not null and"
    sql +=  " MA12  is not null and"
    sql +=  " MA20  is not null and"
    sql +=  " MA30  is not null and"
    sql +=  " MA45  is not null and"
    sql +=  " MA60  is not null and"
    sql +=  " MA125 is not null and"
    sql +=  " MA250 is not null order by shi_jian asc"

    data = pd.read_sql_query(sql,con = engine)
    return data    
    
    

def get_stock_data_daily_all_for_ma_process_df():
    #创建连接
    engine = create_engine('oracle://c##stock:didierg160@myoracle')
    sql  =  "select code , "
    sql +=  "       to_char(decode(MA6             ,null,'0.0',MA6             ),'fm999999999999990.099999999999999999999') MA6              , "
    sql +=  "       to_char(decode(MA12            ,null,'0.0',MA12            ),'fm999999999999990.099999999999999999999') MA12             , "
    sql +=  "       to_char(decode(MA20            ,null,'0.0',MA20            ),'fm999999999999990.099999999999999999999') MA20             , "
    sql +=  "       to_char(decode(MA30            ,null,'0.0',MA30            ),'fm999999999999990.099999999999999999999') MA30             , "
    sql +=  "       to_char(decode(MA45            ,null,'0.0',MA45            ),'fm999999999999990.099999999999999999999') MA45             , "
    sql +=  "       to_char(decode(MA60            ,null,'0.0',MA60            ),'fm999999999999990.099999999999999999999') MA60             , "
    sql +=  "       to_char(decode(MA125           ,null,'0.0',MA125           ),'fm999999999999990.099999999999999999999') MA125            , "
    sql +=  "       to_char(decode(MA250           ,null,'0.0',MA250           ),'fm999999999999990.099999999999999999999') MA250            , "
    sql +=  "       to_char(shi_jian,'yyyymmddhh24miss') shi_jian "
    sql +=  "from tb_stock_data_daily where "
    sql +=  " MA_DISTANCE_AVG_6 = 99999999 and"
    sql +=  " MA6   is not null and"
    sql +=  " MA12  is not null and"
    sql +=  " MA20  is not null and"
    sql +=  " MA30  is not null and"
    sql +=  " MA45  is not null and"
    sql +=  " MA60  is not null and"
    sql +=  " MA125 is not null and"
    sql +=  " MA250 is not null "

    data = pd.read_sql_query(sql,con = engine)
    return data

def get_stock_data_daily_np(code):
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()  
    sql  =  "select to_char(decode(price ,null,'0.0',price ),'fm999999999999990.099999999999999999999') price , "
    sql +=  "       to_char(decode(price_last_day  ,null,'0.0',price_last_day  ),'fm999999999999990.099999999999999999999') price_last_day   , "
    sql +=  "       to_char(decode(price_today_open,null,'0.0',price_today_open),'fm999999999999990.099999999999999999999') price_today_open , "
    sql +=  "       to_char(decode(zhang_die       ,null,'0.0',zhang_die       ),'fm999999999999990.099999999999999999999') zhang_die        , "
    sql +=  "       to_char(decode(zhang_die_rate  ,null,'0.0',zhang_die_rate  ),'fm999999999999990.099999999999999999999') zhang_die_rate   , "
    sql +=  "       to_char(decode(max_price       ,null,'0.0',max_price       ),'fm999999999999990.099999999999999999999') max_price        , "
    sql +=  "       to_char(decode(min_price       ,null,'0.0',min_price       ),'fm999999999999990.099999999999999999999') min_price        , "
    sql +=  "       to_char(decode(vol             ,null,'0.0',vol             ),'fm999999999999990.099999999999999999999') vol              , "
    sql +=  "       to_char(decode(amount          ,null,'0.0',amount          ),'fm999999999999990.099999999999999999999') amount           , "
    sql +=  "       to_char(decode(MA6             ,null,'0.0',MA6             ),'fm999999999999990.099999999999999999999') MA6              , "
    sql +=  "       to_char(decode(MA12            ,null,'0.0',MA12            ),'fm999999999999990.099999999999999999999') MA12             , "
    sql +=  "       to_char(decode(MA20            ,null,'0.0',MA20            ),'fm999999999999990.099999999999999999999') MA20             , "
    sql +=  "       to_char(decode(MA30            ,null,'0.0',MA30            ),'fm999999999999990.099999999999999999999') MA30             , "
    sql +=  "       to_char(decode(MA45            ,null,'0.0',MA45            ),'fm999999999999990.099999999999999999999') MA45             , "
    sql +=  "       to_char(decode(MA60            ,null,'0.0',MA60            ),'fm999999999999990.099999999999999999999') MA60             , "
    sql +=  "       to_char(decode(MA125           ,null,'0.0',MA125           ),'fm999999999999990.099999999999999999999') MA125            , "
    sql +=  "       to_char(decode(MA250           ,null,'0.0',MA250           ),'fm999999999999990.099999999999999999999') MA250            , "
    sql +=  "       to_char(decode(KDJ_K           ,null,'0.0',KDJ_K           ),'fm999999999999990.099999999999999999999') KDJ_K            , "
    sql +=  "       to_char(decode(KDJ_D           ,null,'0.0',KDJ_D           ),'fm999999999999990.099999999999999999999') KDJ_D            , "
    sql +=  "       to_char(decode(KDJ_J           ,null,'0.0',KDJ_J           ),'fm999999999999990.099999999999999999999') KDJ_J            , "
    sql +=  "       to_char(decode(xstd_SLONG      ,null,'0.0',xstd_SLONG      ),'fm999999999999990.099999999999999999999') xstd_SLONG       , "
    sql +=  "       to_char(decode(xstd_SSHORT     ,null,'0.0',xstd_SSHORT     ),'fm999999999999990.099999999999999999999') xstd_SSHORT      , "
    sql +=  "       to_char(decode(xstd_LLONG      ,null,'0.0',xstd_LLONG      ),'fm999999999999990.099999999999999999999') xstd_LLONG       , "
    sql +=  "       to_char(decode(xstd_LSHORT     ,null,'0.0',xstd_LSHORT     ),'fm999999999999990.099999999999999999999') xstd_LSHORT      , "
    sql +=  "       to_char(decode(BOLL_uBOLL      ,null,'0.0',BOLL_uBOLL      ),'fm999999999999990.099999999999999999999') BOLL_uBOLL       , "
    sql +=  "       to_char(decode(BOLL_dBOLL      ,null,'0.0',BOLL_dBOLL      ),'fm999999999999990.099999999999999999999') BOLL_dBOLL       , "
    sql +=  "       to_char(decode(BOLL_BOLL       ,null,'0.0',BOLL_BOLL       ),'fm999999999999990.099999999999999999999') BOLL_BOLL        , "
    sql +=  "       to_char(decode(MACD_DIF        ,null,'0.0',MACD_DIF        ),'fm999999999999990.099999999999999999999') MACD_DIF         , "
    sql +=  "       to_char(decode(MACD_MACD       ,null,'0.0',MACD_MACD       ),'fm999999999999990.099999999999999999999') MACD_MACD        , "
    sql +=  "       to_char(decode(MACD_DIF_MACD   ,null,'0.0',MACD_DIF_MACD   ),'fm999999999999990.099999999999999999999') MACD_DIF_MACD    , "
    sql +=  "       to_char(decode(DPO_DPO         ,null,'0.0',DPO_DPO         ),'fm999999999999990.099999999999999999999') DPO_DPO          , "
    sql +=  "       to_char(decode(DPO_6MA         ,null,'0.0',DPO_6MA         ),'fm999999999999990.099999999999999999999') DPO_6MA            "
    sql +=  "from tb_stock_data_daily where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('20150101000000','yyyymmddhh24miss')"
    sql +=  "order by shi_jian asc "    

    cr.execute(sql)        
    alldaily =cr.fetchall()
    alldaily = np.array([alldaily],dtype=np.float32)
    return alldaily.reshape(-1,32)

def generate_data(seq,days = 120 , fields = 32 , classes = 20):
    x = np.array([])
    y = np.array([])
    x_ = np.array([])
    for i in range(len(seq)-days) :
        if i + days+1 >= len(seq) :
            break
        
        y_one = [0 for i in range( classes )]        
        x_ = seq[i + days - days  : i + days]
        y_ = seq[i + days+1][4] 
        
        if y_>10.0:
            y_ = 10.0
        if y_<-10.0 :
            y_ = -10.0
        y_ = ceil(y_+10)
        y_one[y_] = 1
        #y_one = y_one[0:3]
        x = np.append(x,x_)        
        y = np.append(y,y_one)
        
    x = x.reshape(-1,fields*days)  
    y = y.reshape(-1,classes)
    
#     print(x.shape)
#     print(y.shape)
    
    train_x = x[0:-2]
    train_y = y[0:-2]
    test_x = x[-1].reshape(-1,fields*days)
    test_y = y[-1].reshape(-1,classes)
    return train_x,train_y,test_x,test_y

def getDataXforTest(df,days=5):    
    #print(df.columns)
    #print(df.index)
    #print(df.shape)
    #print(df.shape)
    df = (df-np.sum(df)/len(df))/(np.std(df))
    #print(df.shape)
    df = df[:days]
    #print(df.shape)
    df1 = np.array(df)
    
    #print(df1.shape)
    #df2 = np.array(df.index)
        
    ##df = df.T
    x = []
    for i in range(len(df1)):
        #temp = np.append(df2[i],df1[i])
        temp = df1[i]
        newresult = []
        for item in temp:
            newresult.append(item)
        x.append(newresult)
    
    x.reverse()
    return x

def getDataX_(df,num,days=5):
    #print(df.columns)
    #print(df.index)
    #print(df.shape)
    #print(df.shape)
    #df = (df-np.sum(df)/len(df))/(np.std(df))
    #print(df.shape)
    df['date'] = df.index
    df = df.reset_index(drop=True)
    df = df[:num]
    #print(df.shape)
    df1 = np.array(df)
    
    #print(df1.shape)
    #df2 = np.array(df.index)
        
    ##df = df.T
    x = []
    for i in range(len(df1)):
        #temp = np.append(df2[i],df1[i])
        temp = df1[i]
        newresult = []
        for item in temp:
            newresult.append(item)
        x.append(newresult)
    x.pop()  
    x.reverse()
    
    for i in range(5):
        x.pop()
#     print(df)
    print(x) 
    return x

def getDataY_(df,num,days=5):
#     df = (df-np.sum(df)/len(df))/(np.std(df))
    df['date'] = df.index
    df = df.reset_index(drop=True)
    df = df[:num]
#     df1 = np.array(df)
    #df2 = np.array(df.index)
    
    ##df = df.T
#     x = []
#     for i in range(len(df1)):
#         #temp = np.append(df2[i],df1[i])
#         temp = df1[i]
#         newresult = []
#         for item in temp:
#             newresult.append(item)
#         x.append(newresult)
#     x.pop()

    P=df['price']
    date = df['date']
    P1 = P.shift(days)
#     templist=(P-P.shift(-days))/P.shift(-days)
    templist=(P1-P)/P
    
#     print(templist)
    
    tempDATA = []
    tempRate = []
    #1  0.01  0
    ix=0
    for indextemp in templist:
        datetemp = date[ix]
        if(ix%days==0):
            tempRate.append(indextemp)
            if indextemp>0.02:
                tempDATA.append([1,0,0,indextemp,datetemp])
            elif(indextemp<=0.02):
                tempDATA.append([0,1,0,indextemp,datetemp])
            else:
                tempDATA.append([0,0,1,indextemp,datetemp])
        ix += 1
#     tempDATA.pop()
#     y=tempDATA
#     y.reverse()
    tempRate.pop()
    tempRate.reverse()
    tempRate.pop()
    
#     print(tempRate)
    
    tempDATA.pop()
    tempDATA.reverse()
    tempDATA.pop()
    
    y = tempDATA
    print(y)
    return y

def getDataX(df,num,days=5):    
    #print(df.columns)
    #print(df.index)
    #print(df.shape)
    #print(df.shape)
    df = (df-np.sum(df)/len(df))/(np.std(df))
    #print(df.shape)
    df = df[:num]
    #print(df.shape)
    df1 = np.array(df)
    
    #print(df1.shape)
    #df2 = np.array(df.index)
        
    ##df = df.T
    x = []
    for i in range(len(df1)):
        #temp = np.append(df2[i],df1[i])
        temp = df1[i]
        newresult = []
        for item in temp:
            newresult.append(item)
        x.append(newresult)
    x.pop() 
    x.reverse()
    
    for i in range(5):
        x.pop()
#     print(df)
#     print(x) 
    return x

def getDataY(df,num,days=5):    
#     df = (df-np.sum(df)/len(df))/(np.std(df))
    df = df[:num]
#     df1 = np.array(df)
    #df2 = np.array(df.index)
    
    ##df = df.T
#     x = []
#     for i in range(len(df1)):
#         #temp = np.append(df2[i],df1[i])
#         temp = df1[i]
#         newresult = []
#         for item in temp:
#             newresult.append(item)
#         x.append(newresult)
#     x.pop()

    P=df['price']
    P1 = P.shift(days)
#     templist=(P-P.shift(-days))/P.shift(-days)
    templist=(P1-P)/P
#     print(templist)
    
    tempDATA = []
    tempRate = []
    #1  0.01  0
    ix=0
    for indextemp in templist:
        if(ix%days==0):
            tempRate.append(indextemp)
            if indextemp>0.02:
                tempDATA.append([1,0,0])
            elif(indextemp<=0.02):
                tempDATA.append([0,1,0])
            else:
                tempDATA.append([0,0,1])
        ix += 1
#     tempDATA.pop()
#     y=tempDATA
#     y.reverse()
    tempRate.pop()
    tempRate.reverse()
    tempRate.pop()
    
#     print(tempRate)
    
    tempDATA.pop()
    tempDATA.reverse()
    tempDATA.pop()
    
    y = tempDATA
    return y
