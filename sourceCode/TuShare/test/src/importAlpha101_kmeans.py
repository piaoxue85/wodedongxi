import numpy as np
import kmeans 
import sys
import numpy as np
import pandas as pd
import getStockData as gsd


def get_data(begin = "2017-01-01" , split ="2017-02-01" , end = "2017-10-01"):
    train_data = gsd.get_101_data_test(start=begin, end = split)
    test_data  = gsd.get_101_data_test(start=split, end = end  )
    return train_data , test_data

# 基础参数配置
class conf:

    start_date = '2017-09-21'
    split_date = '2017-09-22'
    end_date   = '2017-09-23'
    batch      = 200000 
    FILE_PATH  = 'd:\model_1.h5'

train_data , test_data = get_data(begin=conf.start_date, split=conf.split_date, end=conf.end_date) 

train_x        = train_data["data_101"]
train_y        = train_data["CodeRetStd"] 
train_return   = train_data["CodeReturn"]
train_shi_jian = train_data["shi_jian"]
train_code     = train_data["code"    ]

print(len(train_x))

test_x        = test_data["data_101"]
test_y        = test_data["CodeRetStd"] 
test_return   = test_data["CodeReturn"]
test_shi_jian = test_data["shi_jian"]
test_code     = test_data["code"    ]

centroids , assignments = kmeans.TFKMeansCluster(vectors=train_x , noofclusters= 10)
print(centroids)
np.savetxt("D:/centroids.txt",np.array(centroids))
print(assignments)  
np.savetxt("D:/assignments.txt",np.array(assignments))

data = pd.DataFrame()
data["code"]        = train_code
data["assignments"] = assignments
data["return"]      = train_return
data.to_csv('D:/b.csv',index=False)