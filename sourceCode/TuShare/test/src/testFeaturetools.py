'''
Created on 2018年9月10日

@author: moonlit
'''


import featuretools as ft 
import numpy as np 
import pandas as pd 
import getStockData as gsd


data = gsd.get_stock_data_daily_df_daysago(code="000001zs",daysago=30)
data["shi_jian"] = data.index

#创建实体
es = ft.EntitySet(id = 'code')

#添加日数据实体
es = es.entity_from_dataframe(entity_id = '上证', dataframe = data, 
                              index = 'shi_jian', time_index = 'shi_jian')

# es = es.add_relationship(ft.Relationship(es['上证']['shi_jian1']))
# print(es)
features, feature_names = ft.dfs(entityset = es, target_entity = '上证')
print(features.columns)
