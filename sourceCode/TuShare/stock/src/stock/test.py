'''
Created on 2016年9月6日

@author: moonlit
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
print(datetime.strptime("2017-07-14 15:00:00", "%Y-%m-%d %H:%M:%S")-timedelta(days=3) )

# ana.testARTTrading()
#----------------------wind --------------------------------
# w.start();
# data=w.wsd("600601.sh", "close", "19900101", "",showblank=0)
# data=w.wset("SectorConstituent","date=20161117;sectorId=a001010100000000")
# data=w.wsd("600601.SH","open,close,high,low,volume,amt,chg,pct_chg,swing", "2000-01-01", "2000-12-31", "Fill=Previous;PriceAdj=F")
# data=w.wset("SectorConstituent","date=20161118;sectorId=a001010100000000")
# data=w.wsd("600601.SH","open,close,high,low,volume,amt,chg,pct_chg,swing", "2000-01-01", "2000-12-31", "Fill=Previous")
# df=imp.wsdToDF(data)
# print(df)
print(round(1.1))
#------------------------------------tushare
# imp.fImportPerformanceReportAll()
# imp.fImportClass()
# imp.fImportStockBasicsAll()
# imp.fImportAllTurnover()
# imp.fImportForecastData(2017,4)

df = pd.DataFrame()
df.boxplot()

print('end----------------------------------------------------------------------------------')