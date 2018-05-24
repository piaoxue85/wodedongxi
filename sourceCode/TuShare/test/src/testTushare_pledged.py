'''
Created on 2018年2月8日

@author: moonlit
'''

import tushare as ts

if __name__ == '__main__':
    df = ts.stock_pledged()
    print(df.columns)
    print(len(df))
    df = ts.pledged_detail()
    print(df.columns)
    print(len(df))    