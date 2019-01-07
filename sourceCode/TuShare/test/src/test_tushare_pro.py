# 23bb6cd2f77e39ea16ca656f2fc1ec2aaaeb6d84aed8369030be7ee8

# from torch import randperm
# import autokeras as ak
# clf = ak.ImageClassifier()

import tushare as ts
import numpy as np
print(ts.__version__)
ts.set_token("23bb6cd2f77e39ea16ca656f2fc1ec2aaaeb6d84aed8369030be7ee8")

pro = ts.pro_api()
 
# df = pro.adj_factor(ts_code='002230.SZ', trade_date='')
# print(df)
# 
# df = pro.daily(ts_code='002230.SZ', start_date='', end_date='')
# print(df)


# df = pro.pledge_detail(ts_code='603520.SH')
df = ts.pro_bar(pro_api=pro, ts_code='001872.SZ', adj='qfq', start_date='', end_date='')
print(df.columns)
print(np.array(df))
print(df)