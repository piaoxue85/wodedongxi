import ta_lib_data as ta
import getStockData as gsd
import pandas as pd
import numpy as np
import cx_Oracle




#codes = gsd.get_code_list_by_classification(classification="上证50成份股") 
codes = gsd.get_code_list_not_in_sz50(daysago = 365*2)
codes = pd.DataFrame([])
codes['code']=["600105"]

cdls = [
        "CDL2CROWS"          ,
        "CDL3BLACKCROWS"     ,
        "CDL3INSIDE"         ,
        "CDL3LINESTRIKE"     ,
        "CDL3OUTSIDE"        ,
        "CDL3STARSINSOUTH"   ,
        "CDL3WHITESOLDIERS"  ,
        "CDLABANDONEDBABY"   ,
        "CDLADVANCEBLOCK"    ,
        "CDLBELTHOLD"        ,
        "CDLBREAKAWAY"       ,
        "CDLCLOSINGMARUBOZU" ,
        "CDLCONCEALBABYSWALL",
        "CDLCOUNTERATTACK"   ,
        "CDLDARKCLOUDCOVER"  ,
        "CDLDOJI"            ,
        "CDLDOJISTAR"        ,
        "CDLDRAGONFLYDOJI"   ,
        "CDLENGULFING"       ,
        "CDLEVENINGDOJISTAR" ,
        "CDLEVENINGSTAR"     ,
        "CDLGAPSIDESIDEWHITE",
        "CDLGRAVESTONEDOJI"  ,
        "CDLHAMMER"          ,
        "CDLHANGINGMAN"      ,
        "CDLHARAMI"          ,
        "CDLHARAMICROSS"     ,
        "CDLHIGHWAVE"        ,
        "CDLHIKKAKE"         ,
        "CDLHIKKAKEMOD"      ,
        "CDLHOMINGPIGEON"    ,
        "CDLIDENTICAL3CROWS" ,
        "CDLINNECK"          ,
        "CDLINVERTEDHAMMER"  ,
        "CDLKICKING"         ,
        "CDLKICKINGBYLENGTH" ,
        "CDLLADDERBOTTOM"    ,
        "CDLLONGLEGGEDDOJI"  ,
        "CDLLONGLINE"        ,
        "CDLMARUBOZU"        ,
        "CDLMATCHINGLOW"     ,
        "CDLMATHOLD"         ,
        "CDLMORNINGDOJISTAR" ,
        "CDLMORNINGSTAR"     ,
        "CDLONNECK"          ,
        "CDLPIERCING"        ,
        "CDLRICKSHAWMAN"     ,
        "CDLRISEFALL3METHODS",
        "CDLSEPARATINGLINES" ,
        "CDLSHOOTINGSTAR"    ,
        "CDLSHORTLINE"       ,
        "CDLSPINNINGTOP"     ,
        "CDLSTALLEDPATTERN"  ,
        "CDLSTICKSANDWICH"   ,
        "CDLTAKURI"          ,
        "CDLTASUKIGAP"       ,
        "CDLTHRUSTING"       ,
        "CDLTRISTAR"         ,
        "CDLUNIQUE3RIVER"    ,
        "CDLUPSIDEGAP2CROWS" ,
        "CDLXSIDEGAP3METHODS"              
       ]

# print(cdls[0])
# print(cdls[1])

db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
cr=db.cursor() 


for code in codes["code"] :
    df    = gsd.get_stock_data_daily_df(str(code)) 
    df    = df.astype(dtype='float64') 
    df1   = ta.appendAllTAData(df)
    dfcdl = pd.DataFrame()
    dfcdl['shi_jian'] = df.index
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

    for cdl in dfcdlarr :
        shi_jian = cdl[0]
        for i in range(len(cdl) ):
            if i == 0 :
                continue 
            
            if cdl[i] != 0 :
                sql = "insert into tb_stock_CDL values ('"+ code +"',to_date('" + shi_jian +" 15:00:00','yyyy-mm-dd hh24:mi:ss'),'" +cdls[i-1]+"',"+str(cdl[i])+")"  
                cr.execute(sql)
     
    print("%s 已导入"%code)           
    db.commit()  
