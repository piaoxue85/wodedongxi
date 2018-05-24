'''
Created on 2017年5月16日

@author: moonlit
'''
import numpy as np
import pandas as pd
import getStockData as gsd 
import time

print("start")
gsd.del_found_before_rqalpha()
codes , stop_count = gsd.get_stock_code_list_after_kdj_test_rqalpha()

#搜索符合买入条件的股票
for code,stop in zip(codes ,stop_count ):
    try : 
        
#         if code == "600577" :
#             code = "600577"
        if (stop == 0) :
            df = gsd.get_stock_data_weekly_rqalpha(code=code, end =time.strftime('%Y-%m-%d',time.localtime(time.time())) )
            kdj_k = df["kdj_k"].values
            kdj_d = df["kdj_d"].values
            kdj_j = df["kdj_j"].values
            shi_jian = df.index    
        
        
            if (kdj_k[-3] <= 14 ):        
                content = "符合周线  kdj_k[-3] <= 14"
                print(code , content)
                gsd.add_found_rqalpha(code=code, content=content, shi_jian = shi_jian[-1])
                       
            if( kdj_k[-3] <= 14 and kdj_k[-1] >= kdj_k[-2] and kdj_k[-2] >= kdj_k[-3]): 
                content = "符合周线  kdj_k[-3] <= 14 and kdj_k[-1] >= kdj_k[-2] and kdj_k[-2] >= kdj_k[-3]"
                print(code , content)
                gsd.add_found_rqalpha(code=code, content=content, shi_jian = shi_jian[-1])
          
        if ( stop == 1 ) :      
            df = gsd.get_stock_data_monthly_rqalpha(code=code, end =time.strftime('%Y-%m-%d',time.localtime(time.time())) )
            kdj_k = df["kdj_k"].values
            kdj_d = df["kdj_d"].values
            kdj_j = df["kdj_j"].values  
            shi_jian = df.index 
            if( kdj_k[-3] <= 14 and kdj_k[-1] >= kdj_k[-2] and kdj_k[-2] >= kdj_k[-3]): 
                content = "符合月线  kdj_k[-3] <= 14 and kdj_k[-1] >= kdj_k[-2] and kdj_k[-2] >= kdj_k[-3]"
                print(code , content)
                gsd.add_found_rqalpha(code=code, content=content, shi_jian = shi_jian[-1]) 
                               
        if ( stop == 2 ) :   
            df = gsd.get_stock_data_Quarterly_rqalpha(code=code, end =time.strftime('%Y-%m-%d',time.localtime(time.time())) )
            kdj_k = df["kdj_k"].values
            kdj_d = df["kdj_d"].values
            kdj_j = df["kdj_j"].values    
            shi_jian = df["shi_jian"].values                  
            if( kdj_k[-3] <= 14 and kdj_k[-1] >= kdj_k[-2] and kdj_k[-2] >= kdj_k[-3]):
                print(code , "符合季度线  kdj_k[-3] <= 14 and kdj_k[-1] >= kdj_k[-2] and kdj_k[-2] >= kdj_k[-3]") 
        
    except Exception as e :  
        print( code, e )   
        
gsd.add_done_mark_rqalpha(WHAT_DONE = "RQAlphaKdjWM")           

print("end")