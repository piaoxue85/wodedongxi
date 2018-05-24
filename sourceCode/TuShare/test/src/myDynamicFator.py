'''
Created on 2018年1月22日

@author: moonlit
python z:/StockAnalysis/sourceCode/TuShare/test/src/myDynamicFator.py
'''
import getStockData as gsd
import pandas as pd
import numpy as np
import cx_Oracle
from sqlalchemy import create_engine

tb_stock_report_data=[
        "EPS"                  , #每股收益          
        "EPS_YOY"              , #每股收益同比(%)   
        "BVPS"                 , #每股净资产        
        "ROE"                  , #净资产收益率(%)   
        "EPCF"                 , #每股现金流量(元)  
        "NET_PROFITS"          , #净利润(万元)      
        "PROFITS_YOY"          , #净利润同比(%) 
       ]
tb_stock_profit_data=[    
        "ROE"                  , #净资产收益率(%)                 
        "NET_PROFIT_RATIO"     , #净利率(%)                      
        "GROSS_PROFIT_RATE"    , #毛利率(%)                      
        "NET_PROFITS"          , #净利润(万元)                   
        "EPS"                  , #每股收益                       
        "BUSINESS_INCOME"      , #营业收入(百万元)               
        "BIPS"                 , #每股主营业务收入(元)
        ]
tb_stock_operation_data=[   
        "ARTURNOVER"           , #应收账款周转率(次)  
        "ARTURNDAYS"           , #应收账款周转天数(天)
        "INVENTORY_TURNOVER"   , #存货周转率(次)      
        "INVENTORY_DAYS"       , #存货周转天数(天)    
        "CURRENTASSET_TURNOVER", #流动资产周转率(次)  
        "CURRENTASSET_DAYS"    , #流动资产周转天数(天)
        ]
tb_stock_growth_data=[            
        "MBRG"                 , #主营业务收入增长率(%)
        "NPRG"                 , #净利润增长率(%)      
        "NAV"                  , #净资产增长率         
        "TARG"                 , #总资产增长率         
        "EPSG"                 , #每股收益增长率       
        "SEG"                  , #股东权益增长率    
        ]
tb_stock_debtpaying_data=[            
         "CURRENTRATIO"         , #流动比率                                               
         "QUICKRATIO"           , #速动比率                                               
         "CASHRATIO"            , #现金比率                                               
         "ICRATIO"              , #利息支付倍数                                           
         "SHEQRATIO"            , #股东权益比率                                           
         "ADRATIO"              , #股东权益增长率   
         ]
tb_stock_cashflow_data=[                   
         "CF_SALES"             , #经营现金净流量对销售收入比率     
         "RATEOFRETURN"         , #资产的经营现金流量回报率       
         "CF_NM"                , #经营现金净流量与净利润的比率   
         "CF_LIABILITIES"       , #经营现金净流量对负债比率       
         "CASHFLOWRATIO"        , #现金流量比率   
     ]
tb_stock_data_market_cap = ["MARKET_CAP"]

def del_duplicate():
    db=cx_Oracle.connect('c##tushare','didierg160','myoracle')  #创建连接 
    cr=db.cursor()
    sql  ="DELETE from tb_stock_report_data WHERE "                                                             
    sql +=" (code||YEAR||QUARTER) IN              "
    sql +=" (                                     "
    sql +="    SELECT code||YEAR||QUARTER FROM tb_stock_report_data GROUP BY code||YEAR||QUARTER HAVING COUNT(code||YEAR||QUARTER) > 1 "
    sql +=" )                "
    sql +="   AND            "
    sql +=" （ROWID） NOT IN "
    sql +=" (                "
    sql +="   SELECT MIN(ROWID) FROM tb_stock_report_data GROUP BY code||YEAR||QUARTER HAVING COUNT(*) > 1 "
    sql +=" ) "
    cr.execute(sql) 
    
    sql  ="DELETE from tb_stock_profit_data WHERE "                                                             
    sql +=" (code||YEAR||QUARTER) IN              "
    sql +=" (                                     "
    sql +="    SELECT code||YEAR||QUARTER FROM tb_stock_profit_data GROUP BY code||YEAR||QUARTER HAVING COUNT(code||YEAR||QUARTER) > 1 "
    sql +=" )                "
    sql +="   AND            "
    sql +=" （ROWID） NOT IN "
    sql +=" (                "
    sql +="   SELECT MIN(ROWID) FROM tb_stock_profit_data GROUP BY code||YEAR||QUARTER HAVING COUNT(*) > 1 "
    sql +=" ) "
    cr.execute(sql) 
    
    sql  ="DELETE from tb_stock_operation_data WHERE "                                                             
    sql +=" (code||YEAR||QUARTER) IN              "
    sql +=" (                                     "
    sql +="    SELECT code||YEAR||QUARTER FROM tb_stock_operation_data GROUP BY code||YEAR||QUARTER HAVING COUNT(code||YEAR||QUARTER) > 1 "
    sql +=" )                "
    sql +="   AND            "
    sql +=" （ROWID） NOT IN "
    sql +=" (                "
    sql +="   SELECT MIN(ROWID) FROM tb_stock_operation_data GROUP BY code||YEAR||QUARTER HAVING COUNT(*) > 1 "
    sql +=" ) "
    cr.execute(sql) 
    
    sql  ="DELETE from tb_stock_growth_data WHERE "                                                             
    sql +=" (code||YEAR||QUARTER) IN              "
    sql +=" (                                     "
    sql +="    SELECT code||YEAR||QUARTER FROM tb_stock_growth_data GROUP BY code||YEAR||QUARTER HAVING COUNT(code||YEAR||QUARTER) > 1 "
    sql +=" )                "
    sql +="   AND            "
    sql +=" （ROWID） NOT IN "
    sql +=" (                "
    sql +="   SELECT MIN(ROWID) FROM tb_stock_growth_data GROUP BY code||YEAR||QUARTER HAVING COUNT(*) > 1 "
    sql +=" ) "
    cr.execute(sql) 
    
    sql  ="DELETE from tb_stock_debtpaying_data WHERE "                                                             
    sql +=" (code||YEAR||QUARTER) IN              "
    sql +=" (                                     "
    sql +="    SELECT code||YEAR||QUARTER FROM tb_stock_debtpaying_data GROUP BY code||YEAR||QUARTER HAVING COUNT(code||YEAR||QUARTER) > 1 "
    sql +=" )                "
    sql +="   AND            "
    sql +=" （ROWID） NOT IN "
    sql +=" (                "
    sql +="   SELECT MIN(ROWID) FROM tb_stock_debtpaying_data GROUP BY code||YEAR||QUARTER HAVING COUNT(*) > 1 "
    sql +=" ) "
    cr.execute(sql) 
    
    sql  ="DELETE from tb_stock_cashflow_data WHERE "                                                             
    sql +=" (code||YEAR||QUARTER) IN              "
    sql +=" (                                     "
    sql +="    SELECT code||YEAR||QUARTER FROM tb_stock_cashflow_data GROUP BY code||YEAR||QUARTER HAVING COUNT(code||YEAR||QUARTER) > 1 "
    sql +=" )                "
    sql +="   AND            "
    sql +=" （ROWID） NOT IN "
    sql +=" (                "
    sql +="   SELECT MIN(ROWID) FROM tb_stock_cashflow_data GROUP BY code||YEAR||QUARTER HAVING COUNT(*) > 1 "
    sql +=" ) "   
    cr.execute(sql) 
    
    db.commit()        
    cr.close ()  
    db.close ()      
    print("del_duplicate done")
    
def get_buy_list(today="" , buy_count = 20):    
    data=test_my_factor(today=today,buy_count=buy_count)
    return data

def test_my_factor(today="",buy_count=20):
    begin_y,begin_q,end_y,end_q = get_begin_end_q (today=today)

    fators=[
#             "EPS"                  , #每股收益          
#             "EPS_YOY"              , #每股收益同比(%)   
#             "BVPS"                 , #每股净资产        
#             "ROE"                  , #净资产收益率(%)   
#             "EPCF"                 , #每股现金流量(元)  
#             "NET_PROFITS"          , #净利润(万元)      
#             "PROFITS_YOY"          , #净利润同比(%)   
            "ROE"                  , #净资产收益率(%)                 
            "NET_PROFIT_RATIO"     , #净利率(%)                      
            "GROSS_PROFIT_RATE"    , #毛利率(%)                      
            "NET_PROFITS"          , #净利润(万元)                   
            "EPS"                  , #每股收益                       
            "BUSINESS_INCOME"      , #营业收入(百万元)               
            "BIPS"                 , #每股主营业务收入(元)    
            "ARTURNOVER"           , #应收账款周转率(次)  
            "ARTURNDAYS"           , #应收账款周转天数(天)
            "INVENTORY_TURNOVER"   , #存货周转率(次)      
            "INVENTORY_DAYS"       , #存货周转天数(天)    
            "CURRENTASSET_TURNOVER", #流动资产周转率(次)  
            "CURRENTASSET_DAYS"    , #流动资产周转天数(天)
            "MBRG"                 , #主营业务收入增长率(%)
            "NPRG"                 , #净利润增长率(%)      
            "NAV"                  , #净资产增长率         
            "TARG"                 , #总资产增长率         
            "EPSG"                 , #每股收益增长率       
            "SEG"                  , #股东权益增长率    
            "CURRENTRATIO"         , #流动比率                                               
            "QUICKRATIO"           , #速动比率                                               
            "CASHRATIO"            , #现金比率                                               
            "ICRATIO"              , #利息支付倍数                                           
            "SHEQRATIO"            , #股东权益比率                                           
            "ADRATIO"              , #股东权益增长率          
            "CF_SALES"             , #经营现金净流量对销售收入比率     
            "RATEOFRETURN"         , #资产的经营现金流量回报率       
            "CF_NM"                , #经营现金净流量与净利润的比率   
            "CF_LIABILITIES"       , #经营现金净流量对负债比率       
            "CASHFLOWRATIO"        , #现金流量比率   
            "MARKET_CAP"           , #市值
        ]
    
    res = []
#     fators = ["MARKET_CAP"]
    for fator in fators :
        codes_asc,return_asc,codes_desc,return_desc = get_fator_data(fator ,begin_y,begin_q,end_y,end_q,today,buy_count =buy_count) 
        res.append([fator+"_asc" ,codes_asc,return_asc]  )
        res.append([fator+"_desc",codes_desc,return_desc])
        print(fator,"done")
        
    res = pd.DataFrame(res,columns=['因子类型', '代码列表', '平均收益'])
    res = res.sort_values(by = "平均收益", ascending =False)    
    return res 
    
def get_fator_data(fator = "EPS" ,begin_y="" ,begin_q="",end_y="",end_q="",today="",buy_count=20):
    #if fator in tb_stock_report_data     : table = "tb_stock_report_data"        
    if fator in tb_stock_profit_data     : table = "tb_stock_profit_data"    
    if fator in tb_stock_operation_data  : table = "tb_stock_operation_data" 
    if fator in tb_stock_growth_data     : table = "tb_stock_growth_data"    
    if fator in tb_stock_debtpaying_data : table = "tb_stock_debtpaying_data"
    if fator in tb_stock_cashflow_data   : table = "tb_stock_cashflow_data"  
    if fator in tb_stock_data_market_cap : table = "c##stock.tb_stock_data_market_cap"  

    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
# #     sql  = "select code,avg(nvl("+fator+",0)) f from " + table + " where to_number(YEAR||QUARTER)>="+ begin_y +begin_q
#     sql  = "select code,max("+fator+") f from " + table + " where "
#     sql += " to_number(YEAR||QUARTER)>="+ begin_y +begin_q    
#     sql += " and " 
#     sql += " to_number(YEAR||QUARTER)<="+ end_y + end_q 
#     sql += " and "
#     sql += " code not in (select code from c##stock.tb_stock_data_daily where shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)<=250)"
# #     sql += "group by code order by avg(nvl("+fator+",0)) asc"
#     sql += "group by code order by max("+fator+") asc"
    
    if table == "c##stock.tb_stock_data_market_cap" :
        sql  = "select code,"+fator+" f from " + table + " where "
        sql += " shi_jian =(select max(shi_jian) from " + table + " where shi_jian<='" + today + "')"
        sql += " and "
        sql += " code in (select code from c##stock.tb_stock_data_daily where shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)>=250)"
        sql += "  and "
        sql += " code in (select code from c##stock.tb_stock_data_daily where shi_jian >=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss')-10 and shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)>0)"
        sql += " order by "+fator+" asc"        
        codes_asc = pd.read_sql_query(sql,con = engine)
        codes_asc = codes_asc["code"].values[:buy_count]
         
        sql  = "select code,"+fator+" f from " + table + " where "
        sql += " shi_jian =(select max(shi_jian) from " + table + " where shi_jian<='" + today + "')"
        sql += " and "
        sql += " code in (select code from c##stock.tb_stock_data_daily where shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)>=250)"
        sql += "  and "
        sql += " code in (select code from c##stock.tb_stock_data_daily where shi_jian >=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss')-10 and shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)>0)"
        sql += " order by "+fator+" desc"       
        codes_desc = pd.read_sql_query(sql,con = engine) 
        codes_desc = codes_desc["code"].values[:buy_count]        
    else:    
        sql  = "select code,"+fator+" f from " + table + " where "
        sql += " to_number(YEAR||QUARTER) ="+ end_y + end_q 
        sql += " and "
        sql += " code in (select code from c##stock.tb_stock_data_daily where shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)>=250)"
        sql += "  and "
        sql += " code in (select code from c##stock.tb_stock_data_daily where shi_jian >=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss')-10 and shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)>0)"        
        sql += " order by "+fator+" asc"        
        codes_asc = pd.read_sql_query(sql,con = engine)
        codes_asc = codes_asc["code"].values[:buy_count]
         
        sql  = "select code,"+fator+" f from " + table + " where "
        sql += " to_number(YEAR||QUARTER) ="+ end_y + end_q 
        sql += " and "
        sql += " code in (select code from c##stock.tb_stock_data_daily where shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)>=250)"
        sql += "  and "
        sql += " code in (select code from c##stock.tb_stock_data_daily where shi_jian >=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss')-10 and shi_jian <=to_date('"+today+" 15:00:00','yyyy-mm-dd hh24:mi:ss') group by code having count(*)>0)"        
        sql += " order by "+fator+" desc"      
        codes_desc = pd.read_sql_query(sql,con = engine) 
        codes_desc = codes_desc["code"].values[:buy_count]
        
    return_asc = []
    for code in codes_asc :
        ret = gsd.get_stock_data_daily_df_monthsafter(code=code,monthsafter=3,begintime=today)
        if len(ret)< 1 :
            continue
        ret = ret["price"].values[-1]/ret["price"].values[0] - 1
        return_asc.append(ret)
        
    return_desc = []
    for code in codes_desc :
        ret = gsd.get_stock_data_daily_df_monthsafter(code=code,monthsafter=3,begintime=today)
        if len(ret)< 1 :
            continue        
        ret = ret["price"].values[-1]/ret["price"].values[0] - 1
        return_desc.append(ret) 
        
    if len(return_asc )<1 :
        return_asc = 0
    else :
        return_asc  = sum(return_asc )/len(return_asc )
    
    if len(return_desc )<1 :
        return_desc = 0
    else :
        return_desc = sum(return_desc)/len(return_desc)    
        
    return codes_asc,return_asc,codes_desc,return_desc
  
def get_begin_end_q (today="yyyy-mm-dd"):
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    
    sql = "select to_char(add_months(trunc(to_date('"+today+"','yyyy-mm-dd'),'q')-1,-3-9),'yyyy') year , to_char(add_months(trunc(to_date('"+today+"','yyyy-mm-dd'),'q')-1,-3-9),'q') q from dual"    
    data = pd.read_sql_query(sql,con = engine) 
    begin_y = data["year"].values[0]
    begin_q = data["q"].values[0]
    
    sql = "select to_char(add_months(trunc(to_date('"+today+"','yyyy-mm-dd'),'q')-1,-3),'yyyy')   year , to_char(add_months(trunc(to_date('"+today+"','yyyy-mm-dd'),'q')-1,  -3),'q') q from dual"
    data = pd.read_sql_query(sql,con = engine) 
    end_y = data["year"].values[0]
    end_q = data["q"].values[0]        
    
    return begin_y,begin_q,end_y,end_q


del_duplicate()

db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接 
cr=db.cursor()
for year in range(2007,2019) :
    for month in ("01","04","07","10") :
        today = str(year) + "-" + month + "-01"
         
        if today == "2018-04-01":
            break ;
         
        data = get_buy_list(today=today , buy_count = 10)
          
        for fator,codes,avg_ret in zip(data["因子类型"].values,data["代码列表"].values,data["平均收益"].values):                        
            sql  = "insert into tb_stock_fator_test values ("
            sql += "'" + today + "','" + fator + "','" + str(codes).replace("'", "") + "','" + str(avg_ret)+"'"
            sql += ")"
            cr.execute(sql) 
        db.commit()
         
        print(today,"done")
         
db.commit()        
cr.close ()  
db.close ()        

'''
data = get_buy_list(today="2016-01-01" , buy_count = 10)
data = get_buy_list(today="2015-04-01" , buy_count = 10)
data = get_buy_list(today="2015-07-01" , buy_count = 10)
data = get_buy_list(today="2015-10-01" , buy_count = 10)
f       = data["因子类型"].values[0]
codes   = data["代码列表"].values[0]
avg_ret = data["平均收益"].values[0]

d_tmp = pd.DataFrame()
d_tmp["因子类型"] = data["因子类型"].values
d_tmp["平均收益"] = data["平均收益"].values
print(d_tmp)
print(data["因子类型"].values[0])
print(codes)
print(avg_ret)
# print(data)
'''