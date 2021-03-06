#复权数据  http://tushare.org/trading.html#id3
# 参数说明：
# 
#     code:string,股票代码 e.g. 600848
#     start:string,开始日期 format：YYYY-MM-DD 为空时取当前日期
#     end:string,结束日期 format：YYYY-MM-DD 为空时取去年今日
#     autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
#     index:Boolean，是否是大盘指数，默认为False
#     retry_count : int, 默认3,如遇网络等问题重复执行的次数
#     pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
# 
# 返回值说明：
# 
#     date : 交易日期 (index)
#     open : 开盘价
#     high : 最高价
#     close : 收盘价
#     low : 最低价
#     volume : 成交量
#     amount : 成交金额

from   sqlalchemy import create_engine
import tushare as ts
import pandas  as pd
import numpy as np
import cx_Oracle
import time
import math
import getStockData as gsd
# from WindPy import *

# def wsdToDF(WindData):
#     fm=pd.DataFrame(WindData.Data,index=WindData.Fields,columns=WindData.Times)
#     fm=fm.T
#     return fm
#股灾后反弹不多 股价5元以下 股东人数 社保持仓 盈利的稳定性

def ftest(pcode=""):
    df = ts.get_hist_data(code = pcode)
    df['shi_jian']=df.index
    df = df.reset_index(drop=True)
#     df = np.array(df)
    print(df)

def fImportAllTurnover():
    
    data = gsd.get_code_list() 
    codes = data["code"].values
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    
    for code in codes :
        data             = ts.get_hist_data(code = code)                 
        if len(data) < 1 :
            continue
        
        data['shi_jian'] = data.index
        data             = data.reset_index(drop=True)
        shi_jians = data["shi_jian"].values 
        turnovers = data["turnover"].values 
        for ( shi_jian ,turnover ) in zip(shi_jians,turnovers) :
            sql = "update tb_stock_data_daily set huan_sou_lv = "  + str(turnover) + " where code = '" + code + "' and shi_jian=to_date('" + shi_jian + " 15:00:00','yyyy-mm-dd hh24:mi:ss')"                   
            cr.execute(sql) 
    
    db.commit()        
    cr.close ()  
    db.close ()
    
def fImportReportData (year="" , quarter="") :
    df = ts.get_report_data     (year=year,quarter=quarter) 
    df['YEAR']    = year 
    df['QUARTER'] = quarter
    #print(df)
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_report_data',engine,if_exists='append') 
    
def fImportProfitData (year="" , quarter="") :
    df = ts.get_profit_data     (year=year,quarter=quarter) 
    df['YEAR']    = year 
    df['QUARTER'] = quarter
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_profit_data',engine,if_exists='append')     
    
def fImportOperationData (year="" , quarter="") :
    df = ts.get_operation_data(year=year,quarter=quarter) 
    df['YEAR']    = year 
    df['QUARTER'] = quarter
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_operation_data',engine,if_exists='append')      
    
def fImportGrowthData (year="" , quarter="") :
    df = ts.get_growth_data     (year=year,quarter=quarter)
    df['YEAR']    = year 
    df['QUARTER'] = quarter
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_growth_data',engine,if_exists='append')        
    
def fImportDebtpayingData (year="" , quarter="") :
    df = ts.get_debtpaying_data     (year=year,quarter=quarter)
    df['YEAR']    = year 
    df['QUARTER'] = quarter
    df = df.replace("--",np.nan)
    #print(df)
    df["currentratio"] =df["currentratio"].astype('float64')
    df["quickratio"  ] =df["quickratio"  ].astype('float64')
    df["cashratio"   ] =df["cashratio"   ].astype('float64')
    df["icratio"     ] =df["icratio"     ].astype('float64')
    df["sheqratio"   ] =df["sheqratio"   ].astype('float64')
    df["adratio"     ] =df["adratio"     ].astype('float64')     
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_debtpaying_data',engine,if_exists='append')     
       
def fImportReportData (year="" , quarter="") :
    df = ts.get_report_data     (year=year,quarter=quarter) 
    df['YEAR']    = year 
    df['QUARTER'] = quarter
    #print(df)
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_report_data',engine,if_exists='append')       

def fImportForecastData(year="" , quarter="") :
    df = ts.forecast_data   (year=year,quarter=quarter)
    df['YEAR']    = year 
    df['QUARTER'] = quarter
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_forecast_data',engine,if_exists='append')

def fDeletePerformanceReport(year="" , quarter="") :
    db=cx_Oracle.connect('c##tushare','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    sql = "delete tb_stock_report_data     where year = " + str(year) + " and quarter = " + str(quarter)
    cr.execute(sql)    
    sql = "delete tb_stock_profit_data     where year = " + str(year) + " and quarter = " + str(quarter)
    cr.execute(sql)    
    sql = "delete tb_stock_operation_data  where year = " + str(year) + " and quarter = " + str(quarter)
    cr.execute(sql)    
    sql = "delete tb_stock_growth_data     where year = " + str(year) + " and quarter = " + str(quarter)
    cr.execute(sql)    
    sql = "delete tb_stock_debtpaying_data where year = " + str(year) + " and quarter = " + str(quarter)
    cr.execute(sql)    
    sql = "delete tb_stock_cashflow_data   where year = " + str(year) + " and quarter = " + str(quarter)
    cr.execute(sql) 
    db.commit()        
    cr.close ()  
    db.close ()             

def fImportPerformanceReport(year="" , quarter="") : 
    try :  
        fDeletePerformanceReport (year=year,quarter=quarter)
    except Exception as err:  
        print("fDeletePerformanceReport %s" % str(err))  
    
    try : 
        fImportReportData        (year=year,quarter=quarter)
    except Exception as err:  
        print("fImportReportData %s" % str(err))   
            
    try : 
        fImportProfitData        (year=year,quarter=quarter)
    except Exception as err:  
        print("fImportProfitData %s" % str(err))       
    
    try : 
        fImportOperationData     (year=year,quarter=quarter)
    except Exception as err:  
        print("fImportOperationData %s" % str(err))    
                
    try : 
        fImportGrowthData        (year=year,quarter=quarter)
    except Exception as err:  
        print("fImportGrowthData %s" % str(err))    
            
    try : 
        fImportDebtpayingData    (year=year,quarter=quarter)
    except Exception as err:  
        print("fImportDebtpayingData %s" % str(err))      
    
    try : 
        fImportCashFlowFata      (year=year,quarter=quarter)
    except Exception as err:  
        print("fImportCashFlowFata %s" % str(err))         

def fImportPerformanceReportAll():
    startYear    = 2000
    startQuarter = 1
#     endYear      = int(time.strftime("%Y"))
#     endQuarter   = math.floor(float(time.strftime("%m"))/3)  #获取当前时间的上季度

    endYear      = 2000
    endQuarter   = 4  #获取当前时间的上季度
    
    if endQuarter == 0 :
        endYear -= endYear 
        endQuarter = 4

    for y in range(endYear - startYear) :
        y_ = endYear - y
        for q in range (startQuarter,4) :
            print(y_ ) 
            print(q )
            fImportPerformanceReport(year=y_,quarter=q)
            if y_ == endYear and q == endQuarter :
                break;

  

def fImportKData(   pname=''      ,
                    pcode=None    ,    #证券代码：  支持沪深A、B股，支持全部指数，支持ETF基金
                    pktype='D'    ,    #数据类型：  默认为D日线数据，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟
                    pautype='qfq' ,    #复权类型：  qfq-前复权 hfq-后复权 None-不复权，默认为qfq
                    pindex=False  ,    #是否为指数：默认为False 设定为True时认为code为指数代码
                    pstart=''     ,    #开始日期:   format：YYYY-MM-DD 为空时取当前日期
                    pend=''            #结束日期：  format：YYYY-MM-DD 
                ):
    df = ts.get_k_data( pcode  , 
                        pstart , 
                        pend   ,
                        pktype ,
                        pautype, 
                        pindex 
                        )
    
    print(df)
    
    
    df['name']=pname    
    df['shi_jian']= pd.to_datetime(df['date'])

    df = df.reset_index(drop=True)
    df = df.drop('date',axis=1)
    df.columns =[
                    'price_today_open',
                    'price'           ,
                    'max_price'       ,
                    'min_price'       ,
                    'vol'             ,
                    'code'            ,
                    'name'            ,
                    'shi_jian'
                ]
    df['price_today_open'] = df['price_today_open'].astype('float64')
    df['price'           ] = df['price'           ].astype('float64')
    df['max_price'       ] = df['max_price'       ].astype('float64')
    df['min_price'       ] = df['min_price'       ].astype('float64')
    df['vol'             ] = df['vol'             ].astype('float64')
    df['code'            ] = df['code'            ].astype(str      )
    df['name'            ] = df['name'            ].astype(str      )
    df = df.set_index('shi_jian')
#     print(df)
#     print(df.index)
#     print(df.columns)         
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_data_daily',engine,if_exists='append') 
  

def fImportHData(pCode,pName,pStart,pEnd) :  
    df = ts.get_h_data(pCode, start=pStart, end=pEnd)
    df['code']=pCode
    df['name']=pName    
    df['shi_jian']=df.index
    df = df.reset_index(drop=True)
    df.columns =[
                    'price_today_open',
                    'max_price'       ,
                    'price'           ,
                    'min_price'       ,
                    'vol'             ,
                    'amount'          ,
                    'code'            ,
                    'name'            ,
                    'shi_jian'
                ]
    df = df.set_index('shi_jian')
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_data_daily',engine,if_exists='append') 
    print(df)
    print(df.index)
    print(df.columns)
  
def fImportStockBasicsAll():
    df = ts.get_stock_basics()
    df.columns =["name","industry","area","pe","outstanding","totals","totalassets","liquidassets","fixedassets","reserved","reservedpershare","esp","bvps","pb","timetomarket","undp","perundp","rev","profit","gpr","npr","holders"]
    #print(df.columns)
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')
    df.to_sql('tb_stock_list',engine,if_exists='append')  

#导入股票分类数据
def fImportClass():
    db=cx_Oracle.connect('c##tushare','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    sql = "truncate table tb_stock_classified "
    cr.execute(sql)    
    db.commit()        
    cr.close ()  
    db.close ()       
    engine = create_engine('oracle://c##tushare:didierg160@myoracle')    
##-------------------------------地区分类
    print('地区分类\n')
    df = ts.get_area_classified()
    df = df.reset_index(drop=True)  
    df = df.dropna()       
    df.columns =[
                    'code'       ,
                    'name'       ,
                    'c_name'           
                ]    
    df = df.set_index('c_name')
    df.to_sql('tb_stock_classified',engine,if_exists='append')      
    
##----------------------------------行业分类    
    print('行业分类\n')
    df = ts.get_industry_classified()
    df = df.reset_index(drop=True)
    df = df.dropna() 
    df.columns =[
                    'code'       ,
                    'name'       ,
                    'c_name'           
                ]    
    df = df.set_index('c_name')   
    df.to_sql('tb_stock_classified',engine,if_exists='append')      
##--------------------------------概念分类
    print('概念分类\n')
    df = ts.get_concept_classified()
    df = df.reset_index(drop=True)
    df = df.dropna()
    df.columns =[
                    'code'       ,
                    'name'       ,
                    'c_name'           
                ]    
    df = df.set_index('c_name')
    df.to_sql('tb_stock_classified',engine,if_exists='append')  
 
###------------------------------中小板 
    
#     print('中小板\n')
#     df = ts.get_sme_classified()
#     df = df.reset_index(drop=True) 
#     df = df.dropna()
#     df['c_name'] = '中小板'   
#     df.columns =[
#                     'code'       ,
#                     'name'       ,
#                     'c_name'           
#                 ]    
#     df = df.set_index('c_name')
#     df.to_sql('tb_stock_classified',engine,if_exists='append') 
    
###----------------沪深300成份及权重    
    print('沪深300成份及权重\n')
    df = ts.get_hs300s()
    df = df.reset_index(drop=True) 
    df = df.dropna()
    df['c_name'] = '沪深300成份及权重'   
    df.columns =[
                    'code', 
                    'name', 
                    'shi_jian', 
                    'weight',
                    'c_name'           
                ]    
    df = df.set_index('c_name')
    df.to_sql('tb_stock_classified',engine,if_exists='append') 
###----------------上证50成份股
    print('上证50成份股\n')    
    df = ts.get_sz50s()
    df = df.reset_index(drop=True) 
    df = df.dropna()
    df = df.drop("date",1)
    df['c_name'] = '上证50成份股'   
    df.columns =[
                    'code', 
                    'name', 
                    'c_name'           
                ]    
    df = df.set_index('c_name')
    df.to_sql('tb_stock_classified',engine,if_exists='append')
###----------------中证500成份股  
    print('中证500成份股\n')     
    df = ts.get_sz50s()
    df = df.reset_index(drop=True) 
    df = df.dropna()
    df = df.drop("date",1)
    df['c_name'] = '中证500成份股'   
    df.columns =[
                    'code', 
                    'name', 
                    'c_name'           
                ]    
    df = df.set_index('c_name')
    df = df.dropna(axis=0)
    df.to_sql('tb_stock_classified',engine,if_exists='append')  
#     print(df)
#     print(df.columns)
#     print(df.index)

