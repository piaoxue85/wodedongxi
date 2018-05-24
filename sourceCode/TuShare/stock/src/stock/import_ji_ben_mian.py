'''
Created on 2016年9月6日

@author: moonlit
python z:/StockAnalysis/sourceCode/TuShare/test/stock/src/stock/import_ji_ben_mian.py
'''
import importUtility as imp
# from WindPy import *
from datetime import datetime 
from datetime import timedelta 
import time
import pandas as pd
import talib as tb
# import Analysis as ana
import numpy as np

print('start')
now_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
now_year = now_date[0:4]
now_q    = now_date[5:7]

if int(now_q) >= 1  and int(now_q) <=3   : now_q = "1" 
if int(now_q) >= 4  and int(now_q) <=6   : now_q = "2"
if int(now_q) >= 7  and int(now_q) <=9   : now_q = "3"
if int(now_q) >= 10 and int(now_q) <=12  : now_q = "4"
 
for year in range(2017,2050) :
    for q in range(4,5) :
#         if year >= int(now_year) and q > int(now_q) :
        if int(str(year)+str(q))> int(now_year+now_q):
            break
    
        imp.fDeletePerformanceReport(year=year , quarter=q)
        imp.fImportPerformanceReport(year=year , quarter=q)
        print("\n",year,q ,"done")
    

print('end----------------------------------------------------------------------------------')