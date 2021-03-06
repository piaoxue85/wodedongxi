import numpy as np
import random
import cx_Oracle
import math
        
class gameEnv():
    def __init__(self,code,eachstepdays,beginbalance):
        self.actions = 3
        self.code = code 
        self.eachstepdays = eachstepdays      #每次返回的state 包含过往多少天的数据
        self.daycount = 1                     #玩到第几天 
        self.stocknumber = 0                  #持仓股数
        self.beginbalance = beginbalance
        self.balanc = self.beginbalance                #资金余额
        self.buyPrice = 0  
        self.sellPrice= 0                            #买入时价格
        self.roundCount = 0
        self.costRate = 1.00
        db=cx_Oracle.connect('c##stock','didierg160','myoracle')  #创建连接  
        cr=db.cursor()      
        sql  = "select to_char(decode(price ,null,'0.0',price ),'fm999999999999990.099999999999999999999') price , "
        sql +=  "       to_char(decode(price_last_day  ,null,'0.0',price_last_day  ),'fm999999999999990.099999999999999999999') price_last_day   , "
        sql +=  "       to_char(decode(price_today_open,null,'0.0',price_today_open),'fm999999999999990.099999999999999999999') price_today_open , "
        sql +=  "       to_char(decode(zhang_die       ,null,'0.0',zhang_die       ),'fm999999999999990.099999999999999999999') zhang_die        , "
        sql +=  "       to_char(decode(zhang_die_rate  ,null,'0.0',zhang_die_rate  ),'fm999999999999990.099999999999999999999') zhang_die_rate   , "
        sql +=  "       to_char(decode(max_price       ,null,'0.0',max_price       ),'fm999999999999990.099999999999999999999') max_price        , "
        sql +=  "       to_char(decode(min_price       ,null,'0.0',min_price       ),'fm999999999999990.099999999999999999999') min_price        , "
        sql +=  "       to_char(decode(vol             ,null,'0.0',vol             ),'fm999999999999990.099999999999999999999') vol              , "
        sql +=  "       to_char(decode(amount          ,null,'0.0',amount          ),'fm999999999999990.099999999999999999999') amount           , "
        sql +=  "       to_char(decode(MA6             ,null,'0.0',MA6             ),'fm999999999999990.099999999999999999999') MA6              , "
        sql +=  "       to_char(decode(MA12            ,null,'0.0',MA12            ),'fm999999999999990.099999999999999999999') MA12             , "
        sql +=  "       to_char(decode(MA20            ,null,'0.0',MA20            ),'fm999999999999990.099999999999999999999') MA20             , "
        sql +=  "       to_char(decode(MA30            ,null,'0.0',MA30            ),'fm999999999999990.099999999999999999999') MA30             , "
        sql +=  "       to_char(decode(MA45            ,null,'0.0',MA45            ),'fm999999999999990.099999999999999999999') MA45             , "
        sql +=  "       to_char(decode(MA60            ,null,'0.0',MA60            ),'fm999999999999990.099999999999999999999') MA60             , "
        sql +=  "       to_char(decode(MA125           ,null,'0.0',MA125           ),'fm999999999999990.099999999999999999999') MA125            , "
        sql +=  "       to_char(decode(MA250           ,null,'0.0',MA250           ),'fm999999999999990.099999999999999999999') MA250            , "
        sql +=  "       to_char(decode(KDJ_K           ,null,'0.0',KDJ_K           ),'fm999999999999990.099999999999999999999') KDJ_K            , "
        sql +=  "       to_char(decode(KDJ_D           ,null,'0.0',KDJ_D           ),'fm999999999999990.099999999999999999999') KDJ_D            , "
        sql +=  "       to_char(decode(KDJ_J           ,null,'0.0',KDJ_J           ),'fm999999999999990.099999999999999999999') KDJ_J            , "
        sql +=  "       to_char(decode(xstd_SLONG      ,null,'0.0',xstd_SLONG      ),'fm999999999999990.099999999999999999999') xstd_SLONG       , "
        sql +=  "       to_char(decode(xstd_SSHORT     ,null,'0.0',xstd_SSHORT     ),'fm999999999999990.099999999999999999999') xstd_SSHORT      , "
        sql +=  "       to_char(decode(xstd_LLONG      ,null,'0.0',xstd_LLONG      ),'fm999999999999990.099999999999999999999') xstd_LLONG       , "
        sql +=  "       to_char(decode(xstd_LSHORT     ,null,'0.0',xstd_LSHORT     ),'fm999999999999990.099999999999999999999') xstd_LSHORT      , "
        sql +=  "       to_char(decode(BOLL_uBOLL      ,null,'0.0',BOLL_uBOLL      ),'fm999999999999990.099999999999999999999') BOLL_uBOLL       , "
        sql +=  "       to_char(decode(BOLL_dBOLL      ,null,'0.0',BOLL_dBOLL      ),'fm999999999999990.099999999999999999999') BOLL_dBOLL       , "
        sql +=  "       to_char(decode(BOLL_BOLL       ,null,'0.0',BOLL_BOLL       ),'fm999999999999990.099999999999999999999') BOLL_BOLL        , "
        sql +=  "       to_char(decode(MACD_DIF        ,null,'0.0',MACD_DIF        ),'fm999999999999990.099999999999999999999') MACD_DIF         , "
        sql +=  "       to_char(decode(MACD_MACD       ,null,'0.0',MACD_MACD       ),'fm999999999999990.099999999999999999999') MACD_MACD        , "
        sql +=  "       to_char(decode(MACD_DIF_MACD   ,null,'0.0',MACD_DIF_MACD   ),'fm999999999999990.099999999999999999999') MACD_DIF_MACD    , "
        sql +=  "       to_char(decode(DPO_DPO         ,null,'0.0',DPO_DPO         ),'fm999999999999990.099999999999999999999') DPO_DPO          , "
        sql +=  "       to_char(decode(DPO_6MA         ,null,'0.0',DPO_6MA         ),'fm999999999999990.099999999999999999999') DPO_6MA            "
        sql +=  "from tb_stock_data_daily where "
        sql +=  "  code = '" + code + "'" 
        sql +=  "order by shi_jian asc "
        
        cr.execute(sql)        
        alldaily=cr.fetchall()
        self.rs = np.array([alldaily],dtype=np.float)
        self.rs = self.rs.reshape(-1,32)  
          
        self.reset()

    def reset(self):
        self.daycount = 1                     #从eachstepdays  天 开始玩，每个step 增加1天
        self.stocknumber = 0                  #持仓股数
        self.balanc = self.beginbalance               #资金余额        
        state = self.getState(self.daycount+self.eachstepdays)
        #print(state.shape)
        self.state = state
        return state
    
    def getState(self , witchday):
        if witchday  >=128 :
            state = self.rs[(witchday - self.eachstepdays -1) : (witchday  - 1) , :]
            return state
        else :
            return []
    
    def getTotalStep(self):        
        return len(self.rs) - self.eachstepdays
    
    #action 0 卖出 1买入 3 不做买卖
    def step(self,action):
        todayis = self.daycount + self.eachstepdays
        price = float(self.rs[todayis-1][0])
        done = ((todayis ) >= len(self.rs) or (self.stocknumber<= 0 and (math.floor( self.balanc / (100.0*price ) ) * 100)<=0))         
        if action == 0 : 
            reward = 0.0
            if self.stocknumber > 0:
                reward = self.stocknumber*( price - self.buyPrice )
                self.balanc += self.stocknumber * price
                self.stocknumber = 0
                self.buyPrice = 0  
                self.sellPrice= price
        if action == 1 :
            reward = 0.0                        
            if  (math.floor( self.balanc / (100.0 * price * self.costRate ) ) * 100) >0 :
                self.stocknumber = math.floor( self.balanc / (100.0*price* self.costRate ) ) * 100
                self.buyPrice = price* self.costRate 
                self.sellPrice= 0
                self.balanc -= self.stocknumber * self.buyPrice            
        if action == 2 :
            reward = 0.0 
#             if self.stocknumber > 0 :
#                 reward = self.stocknumber*( price - self.buyPrice ) * 0.75
#             else :
#                 if self.sellPrice !=0 :
#                     reward = -self.balanc*(( price - self.sellPrice )/self.sellPrice) * 0.75

        state = self.getState(todayis)
#         if reward != 0 :
#             print("today : %d     reward : %f " % (todayis , reward))
        content = (
                  self.code + "," + 
                  str(self.roundCount) + "," + 
                  str(action)  + "," + 
                  str(self.balanc)  + "," + 
                  str(self.stocknumber ) + "," + 
                  str(self.balanc + self.stocknumber*price ) + "," +
                  str(self.daycount + self.eachstepdays) + "," +
                  str(price)
                  ) 
                  
        #self.writeLog('./stockgame_act_log.txt',content )
        if done :
            content = ("code:%s   roundCount:%d   balance :%f  stocknumber:%f   totalvalue:%f  daycount:%d "%(self.code, self.roundCount , self.balanc , self.stocknumber ,self.balanc + self.stocknumber*price , self.daycount )) 
            print(content)
            #self.writeLog('./stockgame_done_log.txt', content)
            self.roundCount += 1
        self.daycount +=1
        return state,reward/1000000,done
        
    def writeLog(self,filename,content):
        #f = open('./stockgame_log.txt','a')
        f = open('./' + filename ,'a')
        f.write('\n%s'%(content))
        f.close()

def testGame():
    game = gameEnv(code = "sh000001",
              eachstepdays = 128,
              beginbalance = 10000000.0
              )
    action = [0,1,2]
    aCur = -1
    for i in range(10000) :
        if i % 100 == 0 :
            aCur += 1
            if aCur >1 :
                aCur = 0            
            s1,r,d = game.step(action[aCur])
            actionval = action[aCur]
        else :
            s1,r,d = game.step(action[2])
            actionval = action[2]  
        
        print('step:%d action:%d reward:%f'%(i ,actionval , r))
        if d :
            game.reset()
 
# testGame() 