'''
Created on 2017年9月30日
python D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\import_Stock_data_my_f_Auto_ML_wind.py
@author: moonlit
'''
 
import getStockData as gsd
import pandas as pd
import numpy as np
from auto_ml import Predictor
# from auto_ml.utils import get_boston_dataset
from auto_ml.utils_models import load_ml_model
from sklearn import preprocessing

def get_data(train_begin="",train_end="", test_begin="", test_end=""):
    train_data,_ = gsd.get_101_data_train_wind(start=train_begin, end = train_end)
    test_data,_  = gsd.get_101_data_test_wind (start=test_begin , end = test_end )
#     test_data  = gsd.get_101_data_test(start="2017-08-24" , end = "2017-08-25" )
    return train_data , test_data

# 基础参数配置
class conf:
#     today = '2017-07-17'    
#     today = '2017-06-02'
#     today = '2017-04-13'
#     today = '2017-09-22'
#     today = '2017-01-10'
#     today = '2017-01-04'
#     today = '2017-08-11'
    today = '2017-11-13'
    file = "d:/xgb.h"

# 035,

train_begin , train_end , test_begin,test_end  = gsd.get_101_data_4_times(today=conf.today )
train_data , test_data                         = get_data(train_begin , train_end , test_begin,test_end )  

# test_data = train_data

train_x        = train_data["data_101"]
train_y        = train_data["CodeReturn"]
train_return   = train_data["CodeReturn"]
train_shi_jian = train_data["shi_jian"]
train_code     = train_data["code"    ]

# train_y = train_return

# print(train_x)
# print(train_y)
# print(train_return)
# print(train_shi_jian)
# print(train_code)

test_x        = test_data["data_101"]
test_y        = test_data["CodeReturn"]
test_return   = test_data["CodeReturn"]
test_shi_jian = test_data["shi_jian"]
test_code     = test_data["code"    ]

cols = [
        "pb_mrq","history_low","history_high","breakout_ma","breakdown_ma","stage_low","stage_high","total_shares","holder_totalbyinst","holder_pctbyinst","pe_est_last","free_float_shares","down_days","up_days","bull_bear_ma","estpb","estpb_fy3","estpe_fy3","holder_avgnum","holder_num","pe_est","estpeg_fy1","close","estpe_fy2","estpeg_fy2","estpb_fy2","vwap","estpeg_ftm","pe_lyr","estpb_fy1","chg","high","estpe_fy1","low","pre_close","open","ev2","mf_amt","rel_ipo_pct_chg","ev1","mf_vol","mkt_cap_ashare2","pe_est_ftm","rel_ipo_chg","est_peg","pe_ttm","ps_lyr","pcf_ocflyr","val_pe_deducted_ttm","pb_lf","ev2_to_ebitda","mf_amt_ratio","pcf_nflyr","mkt_cap_ashare","pct_chg","mf_vol_ratio","pcf_ocf_ttm","volume","mf_amt_open","pcf_ncf_ttm","amt","swing","ps_ttm","dealnum","mf_amt_close"
        ]

clos_need = [
            "estpe_fy2","estpeg_fy2","estpb_fy2","vwap","estpeg_ftm","pe_lyr","estpb_fy1","chg","high","estpe_fy1","low","pre_close","open","ev2","mf_amt","rel_ipo_pct_chg","ev1","mf_vol","mkt_cap_ashare2","pe_est_ftm","rel_ipo_chg","est_peg","pe_ttm","ps_lyr","pcf_ocflyr","val_pe_deducted_ttm","pb_lf","ev2_to_ebitda","mf_amt_ratio","pcf_nflyr","mkt_cap_ashare","pct_chg","mf_vol_ratio","pcf_ocf_ttm","volume","mf_amt_open","pcf_ncf_ttm","amt","swing","ps_ttm","dealnum","mf_amt_close",                         
            ]

# clos_need = cols

def del_not_deed(df,cols = [] ,needed=[]):
    
    for col in cols:
        if col not in needed :
            df = df.drop(col,1)
    
    return df 

df_train = train_x.fillna(0)
# df_train.columns = cols
# df_train = del_not_deed(df_train, cols, clos_need)
df_train["y"] = train_y
cols_ = df_train.columns 
df_train = preprocessing.scale(df_train.as_matrix().astype(float) , axis =1 )
df_train = pd.DataFrame(df_train)
df_train.columns = cols_



df_test = test_x.fillna(0)
# df_test.columns =cols
# df_test = del_not_deed(df_test, cols, clos_need)
df_test["y"] = test_y
cols_ = df_test.columns 
df_test = preprocessing.scale(df_test.as_matrix().astype(float) , axis =1 )
df_test = pd.DataFrame(df_test)
df_test.columns = cols_

# print(df_train.corr())
# print(df_test.corr())


file_name = "d:/automl.saved"

if __name__ == '__main__':
    # Tell auto_ml which column is 'output'
    # Also note columns that aren't purely numerical
    # Examples include ['nlp', 'date', 'categorical', 'ignore']
    column_descriptions = {
      'y': 'output' ,
#       'CHAS': 'categorical'
    }
    
    ml_predictor = Predictor(type_of_estimator='regressor', column_descriptions=column_descriptions)
    
    model_names = ['LGBMRegressor',"AdaBoostRegressor","XGBRegressor","ExtraTreesRegressor","RANSACRegressor",]
    model_names = ['LGBMRegressor',"AdaBoostRegressor","XGBRegressor","ExtraTreesRegressor","RANSACRegressor","GradientBoostingRegressor","DeepLearningRegressor","RandomForestRegressor","SGDRegressor","PassiveAggressiveRegressor"]
#     ml_predictor.train(df_train , model_names = model_names )    
    ml_predictor.train(df_train)
    
    # Score the model on test data
    test_score = ml_predictor.score(df_test, df_test.y)
    
    # auto_ml is specifically tuned for running in production
    # It can get predictions on an individual row (passed in as a dictionary)
    # A single prediction like this takes ~1 millisecond
    # Here we will demonstrate saving the trained model, and loading it again
    file_name = ml_predictor.save(file_name="d:/automl.saved")  
    test_score = ml_predictor.score(df_test, df_test.y)
#     print(test_score)
      
    
    trained_model = load_ml_model(file_name)
    
    # .predict and .predict_proba take in either:
    # A pandas DataFrame
    # A list of dictionaries
    # A single dictionary (optimized for speed in production evironments)
    predictions = trained_model.predict(df_test)
#     print(df_test)
#     print(predictions)
    print("test:",len(df_test))
    print("train:",len(df_train))      
    
    
    f = open('d:/' + conf.today + '.csv','w')    
    #     for pre , test_y_ , test_code_ ,test_shi_jian_,test_return_ in zip(predictions , test_y , test_code ,test_shi_jian,test_return):
    for pre , test_y_ , test_code_ ,test_return_ in zip(predictions , test_y , test_code ,test_return):
    #         f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_ +","+test_shi_jian_ + "\n")
        f.writelines(str(test_return_) +"," + str(pre) +","+ str(test_y_) +","+test_code_  + "\n")
    #     print(pre[0] , test_y_ , test_code_ ,test_shi_jian_)    
    f.close()      
    print("finished")
    