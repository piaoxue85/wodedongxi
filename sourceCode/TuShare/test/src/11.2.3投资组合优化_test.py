# import time
# import getStockData as gsd
# import matplotlib as mpl 
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from mpl_toolkits.mplot3d import Axes3D
# import statsmodels.api as sm
# import scipy.optimize as spo
# from math import  sqrt
# 
# '''
# python D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\import_Stock_Data_Daily_wind.py
# '''
# def eu(xxx_todo_changeme):
# 
#     (s,b) = xxx_todo_changeme
#     return -(0.5* sqrt(s*15+b*5)+0.5*sqrt(s*5+b*12))
#     
# def f(x):
#     return np.sin(x) + 0.5*x
# 
# def fm(x,y):
# #     return np.sin(x) + 0.25*x + np.sqrt(y) + 0.05*y**2
#     return np.sin(x) + 0.05*x**2 + np.sin(y) + 0.05*y**2
# output = True
# 
# def fo(xy):
#     x,y = xy
#     z = np.sin(x) + 0.05*x**2 + np.sin(y) + 0.05*y**2
#     if output :
#         print(("%8.4f %8.4f %8.4f"%(x,y,z)))
#     return z
# 
# cons = ({"type":"ineq","fun":lambda s_b:100-s_b[0]*10-s_b[1]*10}) 
# bnds = ((0,100),(0,100))
# 
# res = spo.minimize(eu , [5,5] , method = "SLSQP" , bounds = bnds , constraints=cons)
# print(res)
# '''
# opt1 = spo.brute(fo,(slice(-10,10.1,0.1),slice(-10,10.1,0.1)),finish=None)
# opt2 = spo.fmin(fo,opt1,xtol=.001,ftol=0.001,maxiter=15,maxfun=20)
# print(opt1)
# print(fm(opt1[0],opt1[1]))
# print(opt2)
# print(fm(opt2[0],opt2[1]))
# 
# # x = np.linspace(0,10,20)
# # y = np.linspace(0,10,20)
# x = np.linspace(-10,10,50)
# y = np.linspace(-10,10,50)
# X,Y = np.meshgrid(x,y)
# Z = fm(X,Y)
# 
# 
# fig  = plt.figure(figsize=(9,6))
# ax   = fig.gca(projection="3d")
# surf1 = ax.plot_surface(X,Y,Z,rstride=2,cstride=2,cmap=mpl.cm.coolwarm,linewidth=0.5,antialiased=True)
# # surf2 = ax.plot_wireframe(X,Y,RZ , rstride=2,cstride=2,label="regression")
# ax.set_xlabel("x")
# ax.set_ylabel("y")
# ax.set_zlabel("f(x,y)")
# # ax.legend()
# fig.colorbar(surf1,shrink=0.5,aspect=5)
# plt.show()
# '''
#    
# 
# '''
# mpl.use('qt4agg')  
# #指定默认字体  
# mpl.rcParams['font.sans-serif'] = ['SimHei']   
# mpl.rcParams['font.family']='sans-serif'  
# #解决负号'-'显示为方块的问题  
# mpl.rcParams['axes.unicode_minus'] = False 
# 
# # plt.plot(df["shi_jian"].values,df["close"].values)
# # plt.plot(df["mf_amt"].rolling(120).mean()*1e-7+7)
# # plt.plot(df["holder_num"]/10000)
# plt.plot( xn, yn , "b^" , label="f(x)")
# plt.plot( xn ,ry , "ro" , label = "regression")
# plt.legend(loc=0)
# plt.grid(True)
# plt.axis("tight")
# plt.xlabel(u"日期")
# plt.ylabel(u"前复权")
# plt.title(u"测试")
# plt.show()
# '''
# a = ""

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt 
# import datetime
# import time
import getStockData as gsd

# codes = gsd.get_code_list()
# codes = codes["code"].values[:5]
# noa = len(codes)
# data = pd.DataFrame()
# for code in codes :
#     data[code] = gsd.get_stock_data_daily_df_daysago(code=code,daysago=1000)["price"]

codes = ['300401', '300298', '300410' ,'603306']
noa = len(codes)
data = pd.DataFrame()
for code in codes :
    print(gsd.get_stock_data_daily_df_time(code=code,start="2018-01-02",end="2018-02-01"))
    data[code] = gsd.get_stock_data_daily_df_time(code=code,start="2018-01-02",end="2018-02-01")["price"]
    
print(data)
# (data/data.ix[0]*100).plot(figsize=(8,5))
# plt.show()
rets = np.log(data/data.shift(1))
len = len(data)
print(rets.mean()*len)
print(rets.cov()*len)
weights = np.random.random(noa)
weights /= np.sum(weights)

fret = np.sum(rets.mean()*weights)*len
print(fret)
fret=np.sqrt(np.dot(weights.T,np.dot(rets.cov()*len,weights)))
print(fret)

prets = []
pvols = []
for p in range (2500) :
    weights = np.random.random(noa)
    weights /= np.sum(weights)
    prets.append(np.sum(rets.mean()*weights)*len)
    pvols.append(np.sqrt(np.dot(weights.T,np.dot(rets.cov()*len,weights))))
    
prets = np.array(prets)
pvols = np.array(pvols)    
    
def statistics(weights):
    '''return portfolio statistics'''
    weights = np.array(weights)
    pret = np.sum(rets.mean()*weights)*len
    pvol = np.sqrt(np.dot(weights,np.dot(rets.cov()*len,weights))) #夏普比率
    return np.array([pret,pvol,pret/pvol])

import scipy.optimize as sco
def min_func_sharpe(weights):
    return -statistics(weights)[2]

''' 最小化夏普指数的负值'''
cons = ({'type':'eq','fun':lambda x:np.sum(x)-1})
bnds = tuple((0,1) for x in range(noa))
fret = noa * [1. /noa, ] #初始状态使用平均分布
print(fret)
opts= sco.minimize(min_func_sharpe,noa*[1./noa,],method='SLSQP',bounds=bnds,constraints=cons)
print(opts)
print(opts['x'].round(3))    
statistics(opts['x'].round(3)) #预期收益率，预期波动率，夏普比率

def min_func_variance(weights):
    return statistics(weights)[1]**2

optv = sco.minimize(min_func_variance,noa*[1./noa,],method='SLSQP',bounds=bnds,constraints=cons)
print(optv)
print(optv["x"].round(3))

fret = statistics(optv['x']).round(3)
print(fret)

plt.figure(figsize=(8,4))
plt.scatter(pvols,prets,c=prets/pvols,marker='o')
plt.grid(True)
plt.xlabel("expected volatility")
plt.ylabel("expected return")
plt.colorbar(label="Sharpe ratio")
plt.show()
a= ""