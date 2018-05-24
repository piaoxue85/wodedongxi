'''
Created on 2017年4月11日

@author: moonlit
'''
import numpy as np
import pandas as pd
import cx_Oracle
from math import ceil
from   sqlalchemy import create_engine

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
    sql +=  "  shi_jian >= to_date('20140101000000','yyyymmddhh24miss')"
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

def dataProcess(df,num) :
    df = (df-np.sum(df)/len(df))/(np.std(df))
    df= df[:num]
    df1 = np.array(df)
    x = []
    for i in range(len(df1)):
        #temp = np.append(df2[i],df1[i])
        temp = df1[i]
        newresult = []
        for item in temp:
            newresult.append(item)
        x.append(newresult)

    return x

def getDataX(df,num):    
    #print(df.columns)
    #print(df.index)
    #print(df.shape)
    #print(df.shape)
    x = dataProcess(df,num)
    #print(df.shape)
    #print(df1.shape)
    #df2 = np.array(df.index)
        
    ##df = df.T
    x.pop()
    x.reverse()
    return x

def getDataY(df,num,days=-5):    
    df = (df-np.sum(df)/len(df))/(np.std(df))
    df = df[:num]
#     df1 = np.array(df)
#     #df2 = np.array(df.index)
#     
#     ##df = df.T
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
    templist=(P-P.shift(days))/P.shift(days)
    tempDATA = []
    #1  0.01  0
    ix=0
    for indextemp in templist:
        if(ix%days==0):
            if indextemp>0:
                tempDATA.append([1,0,0])
            elif(indextemp<=0):
                tempDATA.append([0,1,0])
            else:
                tempDATA.append([0,0,1])
         
        ix += 1

    tempDATA.pop()
    y=tempDATA
    y.reverse()
    return y

def getDataX_myself(df,num,days):    
    #print(df.columns)
    #print(df.index)
    #print(df.shape)
    #print(df.shape)
    x_ = dataProcess(df,num)
    #print(df.shape)
    #print(df1.shape)
    #df2 = np.array(df.index)

    x = []
    len_= len(x_)
    for i in range(len_) :
        if (len_-i-(-days)) < 0 :
            break
        x.append(x_[len_-i-(-days):len_-i])
        
    x.reverse()    
        
    ##df = df.T
    return x

def getDataY_myself(df,num,days=-5):    
#     df = (df-np.sum(df)/len(df))/(np.std(df))
#     df = df[:num]
    
    P=df['price']
    templist=(P-P.shift(days))/P.shift(days)
    tempDATA = []
    #1  0.01  0
    ix=0
#     print(len(templist))
#     print(len(df))
    templist = templist[:num]
#     print(len(templist))
    for indextemp in templist:
        if indextemp>0:
            tempDATA.append([1,0,0])
        elif(indextemp<=0):
            tempDATA.append([0,1,0])
        else:
            tempDATA.append([0,0,1])

        ix += 1
        if len(templist)-(-days)  < ix :
            break

#     tempDATA.pop()
    y=tempDATA
    y.reverse()
    return y

def getDataXY(df, num , days):

    x = getDataX_myself(df, num, days)
    y = getDataY_myself(df, num , days)


    return x,y
