'''
Created on 2017年4月11日

@author: moonlit
'''
import numpy as np
import pandas as pd
import cx_Oracle
from math import ceil
from sqlalchemy import create_engine

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
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('"+start +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "
    sql +=  "    and "
    sql +=  "  shi_jian <= to_date('"+end   +" 15:00:00','yyyy-mm-dd hh24:mi:ss') "    
    sql +=  "order by shi_jian desc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
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
    sql +=  "order by shi_jian desc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
    return data

def get_stock_data_daily_df_daysago(code,daysago=365):
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
    sql +=  "  shi_jian >= sysdate-" + str(daysago) +" "
    sql +=  "order by shi_jian desc "    

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
    #sql +=  "from tb_stock_data_tf_test where "
    sql +=  "  code = '" + code + "'" 
    sql +=  "    and "
    sql +=  "  shi_jian >= to_date('20160601000000','yyyymmddhh24miss')"
    sql +=  "order by shi_jian desc "    

    data = pd.read_sql_query(sql,con = engine)
    data = data.set_index('shi_jian')
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
    sql +=  "  shi_jian >= to_date('20140101000000','yyyymmddhh24miss')"
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
    #df = (df-np.sum(df)/len(df))/(np.std(df))
    #print(df.shape)
    #df = df[:days]
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

def getDataX(df,days=5,pred_days=5):    
    #df = (df-np.sum(df)/len(df))/(np.std(df))
    df = df.sort_index(ascending=True)
    #print(df.shape)
    df1 = np.array(df)    
    
    x = []    
    for i in range(days  ,len(df1)):
        x_= df1[i-days   : i  , :]
        #x_= (x_-np.sum(x_)/len(x_))/(np.std(x_))
        x.append(x_)
     
    #print(np.array(x).shape)
    x = x[0 : len(x) - pred_days ]  
    #print(np.array(x).shape)         
    return np.array(x)

def getDataY(df,days=5, pred_days = 5):
    df = df.sort_index(ascending=True)        
    df1 = df["price"]
    
    y=[]
    for i in range(days , len(df1)) :
        if (i + pred_days ) >= len(df1) :
            break
                
        rate = (df1[i-1+pred_days]-df1[i-1])/df1[i-1] 
        '''
        if rate > 0.02 :
            one_hot = [df1[i-1],0,0]
        elif rate <= 0.02 :
            one_hot = [0,df1[i-1],0]
        else :
            one_hot = [0,0,df1[i-1]]
        '''
        if rate > 0.02 :
            one_hot = [1,0,0]
        elif rate <= 0.02 :
            one_hot = [0,1,0]
        else :
            one_hot = [0,0,1]        
        
        y.append(one_hot)

    return y
