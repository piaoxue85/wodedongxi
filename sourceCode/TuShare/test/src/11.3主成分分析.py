import numpy as np
import pandas as pd
import getStockData as gsd
from sklearn.decomposition import KernelPCA
from sklearn import preprocessing

codes = gsd.get_code_list_by_classification(classification="上证50成份股")
codes = list(codes["code"].values)
codes.append("000016zs")
noa = len(codes)
data = pd.DataFrame()

for code in codes :
    if code =="600485" :
        continue
    df = gsd.get_stock_data_daily_df_daysago(code=code,daysago=2000)["price"]
    if len(df)<400 :
        continue
    data[code] = df
print((len(data)))  
data = data.dropna()
print((len(data)))
dax = pd.DataFrame(data.pop("000016zs"))

# cols_ = data.columns 
# data_scale  = preprocessing.scale(data.as_matrix().astype(float) , axis =0 )
# data_scale  = pd.DataFrame(data_scale)
# data_scale.columns = cols_

# data = data.astype(float)
scale_function = lambda x: (x - x.mean()) / x.std()
data = data.apply(scale_function)

# print(data) 

pca = KernelPCA().fit(data.apply(scale_function)) 
print((len(pca.lambdas_)))
print((pca.lambdas_[:10].round()))

get_we = lambda x : x / x.sum()
print((get_we(pca.lambdas_)[:10]))
print((get_we(pca.lambdas_)[:5].sum()))

import matplotlib.pyplot as plt

pca = KernelPCA(n_components = 1).fit(data.apply(scale_function))
dax["PCA_1"] = pca.transform(data)
# cols_     = dax.columns 
# dax_scale = preprocessing.scale(dax.as_matrix().astype(float) , axis =0 )
# dax_scale = pd.DataFrame(dax_scale)
# dax_scale.columns = cols_
# dax_scale.plot(figsize=(8,4))
# plt.show()

pca = KernelPCA(n_components=5).fit(data.apply(scale_function))
pca_components = pca.transform(data)
weights = get_we(pca.lambdas_)
dax["PCA_5"] = np.dot(pca_components,weights)
# cols_     = dax.columns 
# dax_scale = preprocessing.scale(dax.as_matrix().astype(float) , axis =0 )
# dax_scale = pd.DataFrame(dax_scale)
# dax_scale.columns = cols_
# dax.apply(scale_function).plot(figsize=(8,4))
# plt.show()

import matplotlib as mpl
mpl_dates = [mpl.dates.date2num(t) for t in data.index]
# plt.figure(figsize=(8, 4))
# plt.scatter(dax['PCA_5'], dax['000016zs'], c=mpl_dates)
# lin_reg = np.polyval(np.polyfit(dax['PCA_5'],dax['000016zs'], 1),dax['PCA_5'])
# plt.plot(dax['PCA_5'], lin_reg, 'r', lw=3)
# plt.grid(True)
# plt.xlabel('PCA_5')
# plt.ylabel('000016zs')
# plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),format=mpl.dates.DateFormatter('%d %b %y'))
# plt.show()

cut_date = '2017/9/10'
early_pca = dax[dax.index < cut_date]['PCA_5']
early_reg = np.polyval(np.polyfit(early_pca,
dax['000016zs'][dax.index < cut_date], 1),early_pca)

late_pca = dax[dax.index >= cut_date]["PCA_5"]
late_reg = np.polyval(np.polyfit(late_pca,dax['000016zs'][dax.index >= cut_date], 1),late_pca)

plt.figure(figsize=(8, 4))
plt.scatter(dax["PCA_5"], dax['000016zs'], c=mpl_dates)
plt.plot(early_pca, early_reg, 'r', lw=3)
plt.plot(late_pca, late_reg, 'r', lw=3)
plt.grid(True)
plt.xlabel('PCA_5')
plt.ylabel('000016zs')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
format=mpl.dates.DateFormatter('%d %b %y'))
plt.show()

a = ""