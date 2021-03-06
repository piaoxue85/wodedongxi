from rqalpha.api import *
import os
import sys
import tushare
import talib as ta
import cx_Oracle   
import pandas as pd
import numpy as np



# import getStockData as gsd

# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlpha.py -d D:\rqalpha\bundle -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha run -f D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\src\testRQAlpha.py -d D:\rqalpha\bundle -s 2015-06-01 -e 2017-05-05 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha update_bundle -d D:\rqalpha\

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha.py -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha.py -s 2015-06-01 -e 2017-05-05 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha update_bundle

# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha.py -d z:\rqalpha\bundle -s 2007-10-19 -e 2014-06-23 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha run -f Z:\StockAnalysis\sourceCode\TuShare\test\src\testRQAlpha.py -d z:\rqalpha\bundle -s 2015-06-01 -e 2017-05-05 --stock-starting-cash 100000 --benchmark 600105.XSHG --plot
# rqalpha update_bundle -d Z:\rqalpha\

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
 
    strategy_file_path = context.config.base.strategy_file
    sys.path.append(os.path.realpath(os.path.dirname(strategy_file_path)))

#     context.s1 = "000725.XSHE"
    context.s1 = "600105.XSHG"

    # 设置这个策略当中会用到的参数，在策略中可以随时调用，这个策略使用长短均线，我们在这里设定长线和短线的区间，在调试寻找最佳区间的时候只需要在这里进行数值改动
    context.SHORTPERIOD = 20
    context.LONGPERIOD = 120
    
    context.returns  = 0.0
    context.count    = 0
    context.fromtype = 0 
    context.buyPrice = 0.0
    context.buyTime  = ""  


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    import getStockData as gsd
    import ta_lib_data as ta1
    #import getStockData as gsd
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！

    # 因为策略需要用到均线，所以需要读取历史数据
    #prices = history_bars(context.s1, context.LONGPERIOD+1, '1d', 'close')
#     print(context.now)
    print("context.fromtype %d"%context.fromtype)
    if context.fromtype == 0 :  #周线数据
        df = gsd.get_stock_data_weekly_rqalpha(context.s1[0:6], end=str(context.now))
        print("get_stock_data_weekly_rqalpha")
    
    if context.fromtype == 1 :  #月线数据
        df = gsd.get_stock_data_monthly_rqalpha(context.s1[0:6], end=str(context.now))
        print("get_stock_data_monthly_rqalpha")
        
    if context.fromtype == 2 :  #季线数据
        df = gsd.get_stock_data_Quarterly_rqalpha(context.s1[0:6], end=str(context.now))
        print("get_stock_data_Quarterly_rqalpha")
            
    df= df.astype(dtype='float64')
    '''
    df1 = ta1.appendAllTAData(df)
    dfcdl = pd.DataFrame()
    dfcdl['shi_jian']            = df.index
    dfcdl["CDL2CROWS"          ] = df1["CDL2CROWS"          ]
    dfcdl["CDL3BLACKCROWS"     ] = df1["CDL3BLACKCROWS"     ]
    dfcdl["CDL3INSIDE"         ] = df1["CDL3INSIDE"         ]
    dfcdl["CDL3LINESTRIKE"     ] = df1["CDL3LINESTRIKE"     ]
    dfcdl["CDL3OUTSIDE"        ] = df1["CDL3OUTSIDE"        ]
    dfcdl["CDL3STARSINSOUTH"   ] = df1["CDL3STARSINSOUTH"   ]
    dfcdl["CDL3WHITESOLDIERS"  ] = df1["CDL3WHITESOLDIERS"  ]
    dfcdl["CDLABANDONEDBABY"   ] = df1["CDLABANDONEDBABY"   ]
    dfcdl["CDLADVANCEBLOCK"    ] = df1["CDLADVANCEBLOCK"    ]
    dfcdl["CDLBELTHOLD"        ] = df1["CDLBELTHOLD"        ]
    dfcdl["CDLBREAKAWAY"       ] = df1["CDLBREAKAWAY"       ]
    dfcdl["CDLCLOSINGMARUBOZU" ] = df1["CDLCLOSINGMARUBOZU" ]
    dfcdl["CDLCONCEALBABYSWALL"] = df1["CDLCONCEALBABYSWALL"]
    dfcdl["CDLCOUNTERATTACK"   ] = df1["CDLCOUNTERATTACK"   ]
    dfcdl["CDLDARKCLOUDCOVER"  ] = df1["CDLDARKCLOUDCOVER"  ]
    dfcdl["CDLDOJI"            ] = df1["CDLDOJI"            ]
    dfcdl["CDLDOJISTAR"        ] = df1["CDLDOJISTAR"        ]
    dfcdl["CDLDRAGONFLYDOJI"   ] = df1["CDLDRAGONFLYDOJI"   ]
    dfcdl["CDLENGULFING"       ] = df1["CDLENGULFING"       ]
    dfcdl["CDLEVENINGDOJISTAR" ] = df1["CDLEVENINGDOJISTAR" ]
    dfcdl["CDLEVENINGSTAR"     ] = df1["CDLEVENINGSTAR"     ]
    dfcdl["CDLGAPSIDESIDEWHITE"] = df1["CDLGAPSIDESIDEWHITE"]
    dfcdl["CDLGRAVESTONEDOJI"  ] = df1["CDLGRAVESTONEDOJI"  ]
    dfcdl["CDLHAMMER"          ] = df1["CDLHAMMER"          ]
    dfcdl["CDLHANGINGMAN"      ] = df1["CDLHANGINGMAN"      ]
    dfcdl["CDLHARAMI"          ] = df1["CDLHARAMI"          ]
    dfcdl["CDLHARAMICROSS"     ] = df1["CDLHARAMICROSS"     ]
    dfcdl["CDLHIGHWAVE"        ] = df1["CDLHIGHWAVE"        ]
    dfcdl["CDLHIKKAKE"         ] = df1["CDLHIKKAKE"         ]
    dfcdl["CDLHIKKAKEMOD"      ] = df1["CDLHIKKAKEMOD"      ]
    dfcdl["CDLHOMINGPIGEON"    ] = df1["CDLHOMINGPIGEON"    ]
    dfcdl["CDLIDENTICAL3CROWS" ] = df1["CDLIDENTICAL3CROWS" ]
    dfcdl["CDLINNECK"          ] = df1["CDLINNECK"          ]
    dfcdl["CDLINVERTEDHAMMER"  ] = df1["CDLINVERTEDHAMMER"  ]
    dfcdl["CDLKICKING"         ] = df1["CDLKICKING"         ]
    dfcdl["CDLKICKINGBYLENGTH" ] = df1["CDLKICKINGBYLENGTH" ]
    dfcdl["CDLLADDERBOTTOM"    ] = df1["CDLLADDERBOTTOM"    ]
    dfcdl["CDLLONGLEGGEDDOJI"  ] = df1["CDLLONGLEGGEDDOJI"  ]
    dfcdl["CDLLONGLINE"        ] = df1["CDLLONGLINE"        ]
    dfcdl["CDLMARUBOZU"        ] = df1["CDLMARUBOZU"        ]
    dfcdl["CDLMATCHINGLOW"     ] = df1["CDLMATCHINGLOW"     ]
    dfcdl["CDLMATHOLD"         ] = df1["CDLMATHOLD"         ]
    dfcdl["CDLMORNINGDOJISTAR" ] = df1["CDLMORNINGDOJISTAR" ]
    dfcdl["CDLMORNINGSTAR"     ] = df1["CDLMORNINGSTAR"     ]
    dfcdl["CDLONNECK"          ] = df1["CDLONNECK"          ]
    dfcdl["CDLPIERCING"        ] = df1["CDLPIERCING"        ]
    dfcdl["CDLRICKSHAWMAN"     ] = df1["CDLRICKSHAWMAN"     ]
    dfcdl["CDLRISEFALL3METHODS"] = df1["CDLRISEFALL3METHODS"]
    dfcdl["CDLSEPARATINGLINES" ] = df1["CDLSEPARATINGLINES" ]
    dfcdl["CDLSHOOTINGSTAR"    ] = df1["CDLSHOOTINGSTAR"    ]
    dfcdl["CDLSHORTLINE"       ] = df1["CDLSHORTLINE"       ]
    dfcdl["CDLSPINNINGTOP"     ] = df1["CDLSPINNINGTOP"     ]
    dfcdl["CDLSTALLEDPATTERN"  ] = df1["CDLSTALLEDPATTERN"  ]
    dfcdl["CDLSTICKSANDWICH"   ] = df1["CDLSTICKSANDWICH"   ]
    dfcdl["CDLTAKURI"          ] = df1["CDLTAKURI"          ]
    dfcdl["CDLTASUKIGAP"       ] = df1["CDLTASUKIGAP"       ]
    dfcdl["CDLTHRUSTING"       ] = df1["CDLTHRUSTING"       ]
    dfcdl["CDLTRISTAR"         ] = df1["CDLTRISTAR"         ]
    dfcdl["CDLUNIQUE3RIVER"    ] = df1["CDLUNIQUE3RIVER"    ]
    dfcdl["CDLUPSIDEGAP2CROWS" ] = df1["CDLUPSIDEGAP2CROWS" ]
    dfcdl["CDLXSIDEGAP3METHODS"] = df1["CDLXSIDEGAP3METHODS"]    
    
    dfcdlarr = np.array(dfcdl)
    doji = False
    cdl = dfcdlarr[-1]
    #print(cdl)
    for i in range(len(cdl) ):            
        if i == 0 :
            continue 
           
        if cdl[i] != 0.0 :
            print(cdl[i])
            doji = True
            break
    '''
    kdj_k = df["kdj_k"].values
    kdj_d = df["kdj_d"].values
    kdj_j = df["kdj_j"].values
    

   
#     kdj_k =kdj_k[-1]
#     kdj_d =kdj_d[-1]
#     kdj_j =kdj_j[-1] 

    '''
    # 使用talib计算长短两根均线，均线以array的格式表达
    short_avg = ta.SMA(prices, context.SHORTPERIOD)
    long_avg  = ta.SMA(prices, context.LONGPERIOD )

    plot("short avg", short_avg[-1])
    plot("long avg", long_avg[-1])
    '''
    plot("k", kdj_k[-1])
    plot("d", kdj_d[-1])
    plot("j", kdj_j[-1])

    # 计算现在portfolio中股票的仓位
    cur_position = context.portfolio.positions[context.s1].quantity
    # 计算现在portfolio中的现金可以购买多少股票
    shares = context.portfolio.cash / bar_dict[context.s1].close
    max_price  = 0.0
    drawdown   = 0.0
    returnRate = 0.0
    price      = [0.0]
    if cur_position > 0:
        returnRate = (bar_dict[context.s1].close - context.buyPrice)/context.buyPrice
        df1        = gsd.get_stock_data_daily_rqalpha(context.s1[0:6], end=str(context.now))
        price      = df1["price"].values        
        max_price  = gsd.get_stock_data_max_price_rqalpha(context.s1[0:6],start= str( context.buyTime ) ,end= str( context.now ))
        drawdown   = ( max_price - price[-1])/max_price 
    print("drawdown:%f   maxprice:%f    price:%f"% ( drawdown , max_price , price[-1]))
    print(returnRate)
    # 如果短均线从上往下跌破长均线，也就是在目前的bar短线平均值低于长线平均值，而上一个bar的短线平均值高于长线平均值
    #if (short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0) or (kdj_j < kdj_k and kdj_k < kdj_d) and cur_position > 0:
    #if short_avg[-1] - long_avg[-1] < 0 and short_avg[-2] - long_avg[-2] > 0  and cur_position > 0:
    #if  (kdj_k[-1]>=80 or kdj_j[-1]>110 or returnRate<=-0.10) and cur_position > 0 :
    
     
    #if  (drawdown >= 0.2 or returnRate<=-0.10) and cur_position > 0 :
    if  ( ( drawdown >= 0.2 and kdj_j[-1] < kdj_k[-1] and kdj_k[-1] < kdj_d[-1] ) or returnRate<=-0.10) and cur_position > 0 :
        # 进行清仓
        selres = order_target_value(context.s1, 0)  
        cur_position = context.portfolio.positions[context.s1].quantity    
        if cur_position <= 0 :
            context.buyPrice = 0.0
            context.buyTime  = ""
            print("已清仓 ")

            if returnRate<=-0.10 and context.fromtype < 2:
            #if  context.fromtype < 2:
                context.fromtype = context.fromtype + 1
#                 if context.fromtype > 2 :
#                     context.fromtype = 0          
        return 
    
    if (kdj_k[-3] <= 14 and cur_position <=0  ):
        if context.fromtype == 0 :        
            # 满仓入股
            order_shares(context.s1, shares)
            print("已买入")
        elif kdj_k[-1] >= kdj_k[-2] and kdj_k[-2] >= kdj_k[-3]:
        #elif kdj_j[-1] >= kdj_k[-1] and kdj_k[-1] >= kdj_d[-1]:
            # 满仓入股
            order_shares(context.s1, shares)    
            print("已买入")            
        cur_position = context.portfolio.positions[context.s1].quantity 
        if cur_position >0 :        
            context.buyPrice = bar_dict[context.s1].close
            context.buyTime  = context.now         
#     context.count = context.count + 1
    print("仓位 ：%f"%cur_position)
    if str(context.now)[0:10] == "2017-05-05" :
        print(type(context.portfolio))
        print(str(context.portfolio.total_returns))

