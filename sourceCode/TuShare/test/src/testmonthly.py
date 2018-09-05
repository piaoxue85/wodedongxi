'''
Created on 2018年8月31日

@author: moonlit
'''

import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import cx_Oracle
from sqlalchemy import create_engine
from fbprophet import Prophet
import time

engine = create_engine('oracle://c##stock:didierg160@myoracle')
sql  = "select to_date(shi_jiana||'-01 00:00:00','yyyy-mm-dd hh24:mi:ss') shi_jian ,zhang/(zhang+die) y from                                                                                        "
sql += "(select to_char(shi_jian,'yyyy-mm') shi_jiana,count(*) zhang from tb_stock_data_monthly where zhang_die_rate >0 group by to_char(shi_jian,'yyyy-mm')) a "
sql += "inner join                                                                                                                                              "
sql += "(select to_char(shi_jian,'yyyy-mm') shi_jianb,count(*) die from tb_stock_data_monthly where zhang_die_rate <=0 group by to_char(shi_jian,'yyyy-mm')) b  "
sql += "on a.shi_jiana=b.shi_jianb                                                                                                                              "
sql += "order by shi_jiana asc   "
data       = pd.read_sql_query(sql,con = engine)
data["ds"] = data["shi_jian"]
# data["y"]  = np.log(data['y'])
data       = data.set_index('shi_jian')

m = Prophet()
m.fit(data)
future = m.make_future_dataframe(periods=200)
future.tail()
forecast = m.predict(future)
forecast[['ds','yhat','yhat_lower','yhat_upper']].tail()

print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail())

m.plot(forecast)
# m.plot_components(forecast);
print("end")
while True :
    time.sleep(0.1)
