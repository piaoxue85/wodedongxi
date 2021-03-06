'''
Created on 2017年11月22日
python Z:\StockAnalysis\sourceCode\TuShare\test\src\import_Stock_Data_Daily.py
python D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\import_Stock_Data_Daily_wind.py
@author: moonlit
'''
import numpy as np
import pandas as pd
import cx_Oracle
# from math import ceil
from sqlalchemy import create_engine
# from sklearn.utils import shuffle  
import getStockData as gsd
import tushare as ts
from WindPy import *
import time


def process_nan_none(str=""):
    if str in ["nan","None"] :
        str = "null,"
    else :
        str = "'"+str+"',"
        
    if str == "'TRUE',"  : str = "'1'," 
    if str == "'FALSE'," : str = "'0',"
    
    return str 

def get_wind_data(code="",start_date="",end_date=""):
    
    if code[0]=="6" :
        code += ".SH"
    else :
        code += ".SZ"
        
    currentDay = time.strftime("%Y-%m-%d",time.localtime(time.time()))
#     currentDay = "1993-01-01"

    data_total = pd.DataFrame()

    req1 = "trade_code,sec_name,pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,rel_ipo_chg,rel_ipo_pct_chg,total_shares,free_float_shares,mf_amt,mf_vol,mf_amt_ratio,mf_vol_ratio,mf_amt_close,mf_amt_open,pe_ttm,val_pe_deducted_ttm,pe_lyr,pb_lf,pb_mrq,ps_ttm,ps_lyr,pcf_ocf_ttm,pcf_ncf_ttm,pcf_ocflyr,pcf_nflyr,pe_est,estpe_FY1,estpe_FY2,estpe_FY3,pe_est_last,pe_est_ftm,est_peg,estpeg_FY1,estpeg_FY2,estpeg_FTM"
    req2 = "estpb,estpb_FY1,estpb_FY2,estpb_FY3,ev1,ev2,ev2_to_ebitda,history_low,stage_high,history_high,stage_low,up_days,down_days,breakout_ma,breakdown_ma,bull_bear_ma,holder_num,holder_avgnum,holder_totalbyinst,holder_pctbyinst,mkt_cap_ashare2,mkt_cap_ashare"
     
    '''

    res = w.wsd(
                code, 
                req1 , 
                start_date, 
                end_date, 
                "year=2018;rptYear=2018;n=3;m=60;meanLine=60;N1=5;N2=10;N3=20;N4=30;upOrLow=1;shareType=1;Fill=Previous;PriceAdj=F"
                )
    
    print(code , "errcode:", res.ErrorCode)
    
    shi_jian = res.Times
    Fields   = res.Fields
    data     = res.Data
    
    Data = pd.DataFrame()
    
    for field , d in zip(Fields,data) :
        Data[field] = d
        
    res = w.wsd(
                code, 
                req2 , 
                start_date, 
                end_date, 
                "year=2018;rptYear=2018;n=3;m=60;meanLine=60;N1=5;N2=10;N3=20;N4=30;upOrLow=1;shareType=1;Fill=Previous;PriceAdj=F"
                )
    
    print(code , "errcode:", res.ErrorCode)
    
    Fields   = res.Fields
    data     = res.Data

    for field , d in zip(Fields,data) :
        Data[field] = d      
    '''  
    
    
     
    while end_date <= currentDay :
        need_retry = True ;
        while need_retry :
            end_date = gsd.get_next_date(start_date,int(365*0.1))
            
            scontent = "start_date:"+start_date+",end_date:"+end_date
            
    #         time.sleep(5)
            try :
                res = w.wsd(
                            code, 
                            req1 + "," +req2 , 
                            start_date, 
                            end_date, 
                            "year=2018;rptYear=2018;n=3;m=60;meanLine=60;N1=5;N2=10;N3=20;N4=30;upOrLow=1;shareType=1;Fill=Previous;PriceAdj=F"
                            )
            except Exception as e:
                #获取连接备用
    #             ts.close_apis(conn=cons)            
                print("get_wind_data ,ts soeket fail:",e,scontent)
                need_retry = True
                continue                 
            
    #         time.sleep(10)
            print(code , "errcode:", res.ErrorCode , scontent)
            
            if res.ErrorCode in [-40521008]:
                need_retry = True
            else :
                need_retry = False
                start_date = gsd.get_next_date(end_date,1)
            
            if res.ErrorCode == 0 :
                shi_jian = res.Times
                Fields   = res.Fields
                data     = res.Data
                
                Data = pd.DataFrame()
            
                for field , d in zip(Fields,data) :
                    Data[field] = d    
                    
                Data["shi_jian"] = shi_jian  
                
                data_total= pd.concat([data_total,Data],ignore_index=True)    
            else :
                break
#     w.stop()
    return data_total

def importStockList():
    df = ts.get_stock_basics()
    
    tsFaile = 1
        
    while tsFaile !=0 :
        try:
            #if tsFaile >=2 :
            #    cons = ts.get_apis()
            
            df = ts.get_stock_basics()
            tsFaile = 0
        except Exception as e:
            #获取连接备用
#             ts.close_apis(conn=cons)            
            print("get_stock_basics ,ts soeket fail:",tsFaile,e)
            time.sleep(5)
            if tsFaile <=5  :
                tsFaile += 1
            else:
                break      
    
    df["code"] = df.index
    df = df.reset_index(drop=True)
    
    db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
    cr=db.cursor()
    
    sql = "delete tb_stock_list_ts"
    cr.execute(sql) 
    
    sql = "delete tb_stock_list"
    cr.execute(sql)
    
#     sql = "delete tb_stock_list_tshis where shi_jian=to_char(sysdate,'yyyy-mm-dd')"
#     cr.execute(sql) 
    
    db.commit() 
    
    for row in df.itertuples(): 
        if getattr(row,"timeToMarket"    ) == 0 :
            continue
        
        sql = "insert into tb_stock_list_ts values (" 
        sql += "'" + str(getattr(row,"code"            )) + "',"            
        sql += "'" + str(getattr(row,"name"            )) + "',"        
        sql += "'" + str(getattr(row,"industry"        )) + "',"        
        sql += "'" + str(getattr(row,"area"            )) + "',"        
        sql += "'" + str(getattr(row,"pe"              )) + "',"        
        sql += "'" + str(getattr(row,"outstanding"     )) + "',"        
        sql += "'" + str(getattr(row,"totals"          )) + "',"        
        sql += "'" + str(getattr(row,"totalAssets"     )) + "',"        
        sql += "'" + str(getattr(row,"liquidAssets"    )) + "',"        
        sql += "'" + str(getattr(row,"fixedAssets"     )) + "',"        
        sql += "'" + str(getattr(row,"reserved"        )) + "',"        
        sql += "'" + str(getattr(row,"reservedPerShare")) + "',"        
        sql += "'" + str(getattr(row,"esp"             )) + "',"        
        sql += "'" + str(getattr(row,"bvps"            )) + "',"        
        sql += "'" + str(getattr(row,"pb"              )) + "',"        
        sql += "'" + str(getattr(row,"timeToMarket"    )) + "',"        
        sql += "'" + str(getattr(row,"undp"            )) + "',"        
        sql += "'" + str(getattr(row,"perundp"         )) + "',"        
        sql += "'" + str(getattr(row,"rev"             )) + "',"        
        sql += "'" + str(getattr(row,"profit"          )) + "',"        
        sql += "'" + str(getattr(row,"gpr"             )) + "',"        
        sql += "'" + str(getattr(row,"npr"             )) + "',"        
        sql += "'" + str(getattr(row,"holders"         )) + "',"
        sql += "sysdate"
        sql += ")"        
        cr.execute(sql)  
        
        sql = "insert into tb_stock_list values (" 
        sql += "'" + str(getattr(row,"code"            )) + "',"            
        sql += "'" + str(getattr(row,"name"            )) + "',"                
        sql += "'" + str(getattr(row,"pe"              )) + "',"  
        sql += "'" + str(getattr(row,"pb"              )) + "',"                
        sql += "'" + str(getattr(row,"liquidAssets"    )) + "'," 
        sql += "'" + str(getattr(row,"totalAssets"     )) + "',"               
        sql += "0,"        
        sql += "sysdate"
        sql += ")"        
        cr.execute(sql)          
                
    db.commit()        
    cr.close ()  
    db.close ()  
    return df["code"].values ,df["name"].values,df["timeToMarket"].values
    
def importStockDataDailyWind(codes= [],names=[],timeToMarket =[] ):
    
    code_tail = ""
    w.start()
    for code,name,ttm in zip(codes,names,timeToMarket) :      
        start_date = ""
                
        xred = True
        while xred :
    
            start_date_ = gsd.get_code_max_shi_jian_wind(code=code + code_tail) 
            
            if start_date_ == "None" :
                if int(ttm) < 19901219 :
                    continue
                ttm = str(ttm)
                start_date = ttm[0:4] + "-" + ttm[4:6] + "-" + ttm[6:8]
            else :
                start_date = start_date_
                
            try:               
                df = get_wind_data(code, start_date=start_date )
               
                if start_date_ == "None" : start_date = start_date_
            
            except Exception as e:
                print(code,start_date ,"importStockDataDaily fail:",e)
                continue
            
            if len(df) <1 :
                continue
            
            db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
            cr=db.cursor()                    
            xred = isXR(code=code , df=df , max_shi_jian=start_date_)
            if xred :
                sql = "delete tb_stock_data_daily_wind where code = '" + code + code_tail+ "'"
                cr.execute(sql)                
            db.commit()        
            cr.close ()  
            db.close ()              

        db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
        cr=db.cursor()        
        for row  in df.itertuples(): 
            if str(getattr(row,"VOLUME" ))=="None" :
                    continue
                
#             print(str(getattr(row,"VOLUME" )))
            if str(getattr(row,"VOLUME" ))=="nan" :
                    continue            
            
            if round(float(getattr(row,"VOLUME" )))<1 :
                continue                                
                                 
            shi_jian = getattr(row,"shi_jian").strftime('%Y-%m-%d')
            
            if len(shi_jian)<10:
                continue
            
            if shi_jian == start_date :
                continue      
            
            time_ = shi_jian+ " 17:00:00"
            time_ = time.mktime(time.strptime(time_, '%Y-%m-%d %H:%M:%S')) # 1482286976.0  
            
            if time.time() < time_ :
                continue 

            sql  = "insert into tb_stock_data_daily_wind values ("       
            sql += process_nan_none( str(getattr(row,"SEC_NAME"            )) )
            sql += process_nan_none( str(getattr(row,"TRADE_CODE"          )) )
            sql += process_nan_none( shi_jian                                 )
            sql += process_nan_none( str(getattr(row,"PRE_CLOSE"           )) )
            sql += process_nan_none( str(getattr(row,"OPEN"                )) )
            sql += process_nan_none( str(getattr(row,"HIGH"                )) )
            sql += process_nan_none( str(getattr(row,"LOW"                 )) )
            sql += process_nan_none( str(getattr(row,"CLOSE"               )) )
            sql += process_nan_none( str(getattr(row,"VOLUME"              )) )
            sql += process_nan_none( str(getattr(row,"AMT"                 )) )
            sql += process_nan_none( str(getattr(row,"DEALNUM"             )) )
            sql += process_nan_none( str(getattr(row,"CHG"                 )) )
            sql += process_nan_none( str(getattr(row,"PCT_CHG"             )) )
            sql += process_nan_none( str(getattr(row,"SWING"               )) )
            sql += process_nan_none( str(getattr(row,"VWAP"                )) )
#             sql += process_nan_none( str(getattr(row,"ADJFACTOR"           )) )
            sql += process_nan_none( str(getattr(row,"REL_IPO_CHG"         )) )
            sql += process_nan_none( str(getattr(row,"REL_IPO_PCT_CHG"     )) )
            sql += process_nan_none( str(getattr(row,"TOTAL_SHARES"        )) )
            sql += process_nan_none( str(getattr(row,"FREE_FLOAT_SHARES"   )) )
            sql += process_nan_none( str(getattr(row,"MF_AMT"              )) )
            sql += process_nan_none( str(getattr(row,"MF_VOL"              )) )
            sql += process_nan_none( str(getattr(row,"MF_AMT_RATIO"        )) )
            sql += process_nan_none( str(getattr(row,"MF_VOL_RATIO"        )) )
            sql += process_nan_none( str(getattr(row,"MF_AMT_CLOSE"        )) )
            sql += process_nan_none( str(getattr(row,"MF_AMT_OPEN"         )) )
            sql += process_nan_none( str(getattr(row,"PE_TTM"              )) )
            sql += process_nan_none( str(getattr(row,"VAL_PE_DEDUCTED_TTM" )) )
            sql += process_nan_none( str(getattr(row,"PE_LYR"              )) )
            sql += process_nan_none( str(getattr(row,"PB_LF"               )) )
            sql += process_nan_none( str(getattr(row,"PB_MRQ"              )) )
            sql += process_nan_none( str(getattr(row,"PS_TTM"              )) )
            sql += process_nan_none( str(getattr(row,"PS_LYR"              )) )
            sql += process_nan_none( str(getattr(row,"PCF_OCF_TTM"         )) )
            sql += process_nan_none( str(getattr(row,"PCF_NCF_TTM"         )) )
            sql += process_nan_none( str(getattr(row,"PCF_OCFLYR"          )) )
            sql += process_nan_none( str(getattr(row,"PCF_NFLYR"           )) )
            sql += process_nan_none( str(getattr(row,"PE_EST"              )) )
            sql += process_nan_none( str(getattr(row,"ESTPE_FY1"           )) )
            sql += process_nan_none( str(getattr(row,"ESTPE_FY2"           )) )
            sql += process_nan_none( str(getattr(row,"ESTPE_FY3"           )) )
            sql += process_nan_none( str(getattr(row,"PE_EST_LAST"         )) )
            sql += process_nan_none( str(getattr(row,"PE_EST_FTM"          )) )
            sql += process_nan_none( str(getattr(row,"EST_PEG"             )) )
            sql += process_nan_none( str(getattr(row,"ESTPEG_FY1"          )) )
            sql += process_nan_none( str(getattr(row,"ESTPEG_FY2"          )) )
            sql += process_nan_none( str(getattr(row,"ESTPEG_FTM"          )) )
            sql += process_nan_none( str(getattr(row,"ESTPB"               )) )
            sql += process_nan_none( str(getattr(row,"ESTPB_FY1"           )) )
            sql += process_nan_none( str(getattr(row,"ESTPB_FY2"           )) )
            sql += process_nan_none( str(getattr(row,"ESTPB_FY3"           )) )
            sql += process_nan_none( str(getattr(row,"EV1"                 )) )
            sql += process_nan_none( str(getattr(row,"EV2"                 )) )
            sql += process_nan_none( str(getattr(row,"EV2_TO_EBITDA"       )) )
            sql += process_nan_none( str(getattr(row,"HISTORY_LOW"         )) )
            sql += process_nan_none( str(getattr(row,"STAGE_HIGH"          )) )
            sql += process_nan_none( str(getattr(row,"HISTORY_HIGH"        )) )
            sql += process_nan_none( str(getattr(row,"STAGE_LOW"           )) )
            sql += process_nan_none( str(getattr(row,"UP_DAYS"             )) )
            sql += process_nan_none( str(getattr(row,"DOWN_DAYS"           )) )
            sql += process_nan_none( str(getattr(row,"BREAKOUT_MA"         )) )
            sql += process_nan_none( str(getattr(row,"BREAKDOWN_MA"        )) )
            sql += process_nan_none( str(getattr(row,"BULL_BEAR_MA"        )) )
            sql += process_nan_none( str(getattr(row,"HOLDER_NUM"          )) )
            sql += process_nan_none( str(getattr(row,"HOLDER_AVGNUM"       )) )
            sql += process_nan_none( str(getattr(row,"HOLDER_TOTALBYINST"  )) )
            sql += process_nan_none( str(getattr(row,"HOLDER_PCTBYINST"    )) )
            sql += process_nan_none( str(getattr(row,"MKT_CAP_ASHARE2"     )) )
            sql += process_nan_none( str(getattr(row,"MKT_CAP_ASHARE"      )) )            
            sql = sql[:-1]+")"
            
            try:
                cr.execute(sql)
            except Exception as e: 
                print(sql)
             
#         time.sleep(1)
        db.commit()
        cr.close ()  
        db.close ()           
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        print(now,code,"done")
#     db.commit()        
#     cr.close ()  
#     db.close ()  
    w.stop()
        
#是否除权
def isXR(code="" , df=None  , max_shi_jian="" ):
    if max_shi_jian =="None":
        return False
    
    data  = gsd.get_stock_data_daily_df_time_wind(code=code,start=max_shi_jian,end=max_shi_jian)    
    price = data["close"].values[0]    

    close = df["CLOSE"].values[0]
    
    if price == close :
        return False
    else :
        return True
    
def test(codes):
    for code in codes :
#         data = get_wind_data(code = code )
        data = get_wind_data(code = code ,start_date="1991-01-02",end_date="")
#         isXR(code)
#         print(code , "done")

def start():     
    #获取连接备用
    cons = ts.get_apis()
    # 导入个股   
    print("导入个股")      
    codes,names,timeToMarket = importStockList()
#     codes = ["600025"]
#     names = ["华能水电"]
#     timeToMarket = [20171215]
    #000002.SZ errcode: -40521008 start_date:1993-01-23,end_date:1993-01-26
#     codes = ["000002"]
#     names = ["万科A"]
#     timeToMarket = [19910102]
    print(len(codes) , len(names) , len(timeToMarket))
    importStockDataDailyWind(codes,names,timeToMarket)
    # test(codes)
    
    '''
    #导入指数
    print("导入指数")
    df = ts.get_index()
    codes = df["code"].values
    names = df["name"].values
    import import_Stock_Data_Daily
    import_Stock_Data_Daily.importStockDataDaily(codes,names,asset='INDEX',adj='None')
    '''    
    ts.close_apis(conn=cons)
    print("导入完成")

if __name__ == '__main__':
    start()
