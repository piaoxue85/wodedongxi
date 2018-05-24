
import pandas as pd
import numpy as np
from fbprophet import Prophet
import time

df = pd.read_csv('Z:/StockAnalysis/sourceCode/TuShare/test/stock/src/stock/fbprophet/sh.txt')
df['date'] = pd.to_datetime(df['date'])
df.tail()
# df['price']=np.log(df['price'])
df.set_index ('date').plot()
# plot.show()
df.columns=["ds","y"]
df['y'] = np.log(df['y'])
# df['cap'] = 0.1
print(df)
df.head() 

# m = Prophet(growth='logistic')
# m = Prophet()
# m = Prophet(changepoint_prior_scale=1.0)
m = Prophet(changepoints=[
                            '1994-07-27',
                            '2001-06-21',
                            '2005-07-18',
                            '2007-10-16',
                            '2008-11-01',
                            '2015-06-12',
                            '2016-01-27',                            
                         ])
m.fit(df)

future = m.make_future_dataframe(periods=3000)
# future['cap'] = 0.1
future.tail()
forecast = m.predict(future)
forecast[['ds','yhat','yhat_lower','yhat_upper']].tail()

m.plot(forecast)
# m.plot_components(forecast);
print("end")
while True :
    time.sleep(0.1)