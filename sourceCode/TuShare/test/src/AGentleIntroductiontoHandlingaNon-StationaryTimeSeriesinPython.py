'''
Created on 2018年11月19日

@author: moonlit
'''
#loading important libraries
import pandas as pd
import matplotlib.pyplot as plt
import getStockData as gsd


#reading the dataset
# train = pd.read_csv('AirPassengers.csv')
train = gsd.get_stock_data_daily_df_time("399001zs","2017-01-01","2018-11-16")

#preprocessing
# train.timestamp = pd.to_datetime(train.Month , format = '%Y-%m')
# train.index = train.timestamp
# train.drop('Month',axis = 1, inplace = True)

#looking at the first few rows
#train.head()

# train['price'].plot()
# plt.show()

#define function for ADF test
from statsmodels.tsa.stattools import adfuller
def adf_test(timeseries):
    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
       dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)

#apply adf test on the series
adf_test(train['price'])

#define function for kpss test
from statsmodels.tsa.stattools import kpss
#define KPSS
def kpss_test(timeseries):
    print ('Results of KPSS Test:')
    kpsstest = kpss(timeseries, regression='c')
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value    
        
    print(kpss_output)
    
kpss_test(train['price'])

train['price_diff'] = train['price'] - train['price'].shift(1)
train['price_diff'].dropna().plot()

n=7
train['price_diff'] = train['price'] - train['price'].shift(n)

import numpy as np

train['price_log'] = np.log(train['price'])
train['price_log_diff'] = train['price_log'] - train['price_log'].shift(1)
(train['price_log_diff'].dropna()).plot()
plt.show()