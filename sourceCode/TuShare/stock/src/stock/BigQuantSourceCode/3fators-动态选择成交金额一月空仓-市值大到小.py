#上次你提到 回测结果显示中 显示最大回撤的时间段 
#m6.pyfolio_full_tear_sheet()   这个接口可以满足你的需求

import pandas as pd
import numpy as np
from sklearn import preprocessing

# 获取股票代码
instruments = D.instruments()
# # 确定起始时间
start_date = '2018-01-01' 
# start_date = '2016-01-01'
start_date = '2018-04-10'
# start_date = '2014-01-01'
# start_date = '2005-01-01'

# 确定结束时间
end_date = '2018-09-04'

# # 确定起始时间
# start_date = '2007-01-01' 
# # 确定结束时间
# end_date = '2018-01-17' 

# # 确定起始时间
# start_date = '2005-01-01 ' 
# # 确定结束时间
# end_date = '2007-11-01'  

# 起始日期
# start_date = '2006-01-01'
# # 结束日期
# end_date = '2007-01-08'

# def get_codes(date=""):
#     df = D.history_data(instruments,start_date = "1990-12-31",end_date =date,fields=['amount'])
#     df = df.groupby(by=['instrument']).size()
#     print(df.columns )

# 获取股票总市值数据，返回DataFrame数据格式
def get_data(date="",portfolio_value=0.0):
#     get_codes(date)
#     df = D.history_data(instruments, date, date, fields=['market_cap'  , 'fs_eps','amount',"st_status","pe_ttm","volatility_$i_0"])
    #,"beta_industry_5_0"
    fields = ["list_board_0","list_days_0",'market_cap_0',"amount_0","st_status_0","pe_ttm_0","fs_roe_0","fs_eps_0","west_eps_ftm_0"]
#     fields = ["list_board_0","list_days_0",'market_cap_0',"amount_0","st_status_0","pe_ttm_0","fs_roe_0","fs_eps_0"]
    df = D.features(    instruments, date, date, fields=fields, groupped_by_instrument=False, frequency='daily')
#     print(df)
#     剔除创业板
#     df = df[ (df['list_board_0'] != 3)]
    df = df[ (df['list_days_0'] >= 365*2)]
    #4 0.5 5674.42% 41.36%
    df = df[  df['fs_eps_0'] >= 0.5 ]
    df = df[  df['st_status_0'] == 0 ]
    daily_buy_stock = df[df['amount_0'] >= ((portfolio_value/4)/0.025) ]
#     daily_buy_stock = df[df['amount_0'] >= ((portfolio_value/4)/0.05) ]
    daily_buy_stock = daily_buy_stock.dropna()
#     print(daily_buy_stock)
    return daily_buy_stock

def get_buy_list(date="",portfolio_value=0.0):
    data = get_data(date,portfolio_value)
    code = data["instrument"].values
#     beta = data["beta_industry_5_0"].values
    mc   = data["market_cap_0"].values
    eps  = data["fs_eps_0"].values
    fx   = data["west_eps_ftm_0"].values
    
#     beta  = preprocessing.scale(abs(beta-1))
#     beta  = preprocessing.scale(beta*-1)
    if len(mc)<1 :
        return []
    
    mc    = preprocessing.scale(mc*1)
    eps   = preprocessing.scale(eps*-1)
    fx    = preprocessing.scale(fx*-1)
    
    data = pd.DataFrame()
    data["code"]  = code     
    data["factor"]= mc
    
    #6 3806.69% 36.74%
    #5 3334.79% 35.24%
    #4 3948.35% 37.15%
    #3 2118.67% 30.29%    
    data = data.sort_values('factor',ascending =True)[:4]
    data = data.sort_values('factor',ascending =False)
#     print(data)
    return data["code"].values

    

# 回测参数设置，initialize函数只运行一次
def initialize(context):
    # 手续费设置
    context.set_commission(PerOrder(buy_cost=0.002, sell_cost=0.002, min_cost=5)) 
    # 调仓规则（每月的第一天调仓）
    context.schedule_function(rebalance, date_rule=date_rules.month_start(days_offset=0)) 
#     context.schedule_function(rebalance, date_rule=date_rules.month_end()) 
    # 传入 整理好的调仓股票数据
#     context.daily_buy_stock = daily_buy_stock
    set_long_only()
#     set_max_leverage(1)  

#     print(context.daily_buy_stock)

# handle_data函数会每天运行一次
def handle_data(context,data):
    if data.current_dt.strftime('%Y-%m-%d') == end_date :
        rebalance(context,data)
        # 打印持仓的股票
        positions = context.portfolio.positions
        for equity in positions:
            position = positions[equity]
            print(position.sid)
            
#     if data.current_dt.strftime('%Y-%m-%d') == "2016-01-05" : context.order_target_percent(context.symbol("600593.SHA"), 0)
#     if data.current_dt.strftime('%Y-%m-%d') == "2015-09-02" : context.order_target_percent(context.symbol("000565.SZA"), 0)
#     if data.current_dt.strftime('%Y-%m-%d') == "2015-07-08" : context.order_target_percent(context.symbol("002144.SZA"), 0)
#     if data.current_dt.strftime('%Y-%m-%d') == "2007-06-04" : context.order_target_percent(context.symbol("600993.SHA"), 0)


# 换仓函数
def rebalance(context, data):
    # 当前的日期
    date = data.current_dt.strftime('%Y-%m-%d')
    # 根据日期获取调仓需要买入的股票的列表
    print(date)
        
    if (date[5:7] == "01") :
        stock_to_buy = []
    else :
        try:
            stock_to_buy = get_buy_list(date,portfolio_value=context.portfolio.portfolio_value)
        except:
            stock_to_buy = []     
        
    print(stock_to_buy)

    # 通过positions对象，使用列表生成式的方法获取目前持仓的股票列表
    stock_hold_now = [equity.symbol for equity in context.portfolio.positions]
    # 继续持有的股票：调仓时，如果买入的股票已经存在于目前的持仓里，那么应继续持有
    no_need_to_sell = [i for i in stock_hold_now if i in stock_to_buy]
    # 需要卖出的股票
    stock_to_sell = [i for i in stock_hold_now if i not in no_need_to_sell]
  
    # 卖出
    for stock in stock_to_sell:
        # 如果该股票停牌，则没法成交。因此需要用can_trade方法检查下该股票的状态
        # 如果返回真值，则可以正常下单，否则会出错
        # 因为stock是字符串格式，我们用symbol方法将其转化成平台可以接受的形式：Equity格式

        if data.can_trade(context.symbol(stock)):
            # order_target_percent是平台的一个下单接口，表明下单使得该股票的权重为0，
            #   即卖出全部股票，可参考回测文档
            context.order_target_percent(context.symbol(stock), 0)
    
    # 如果当天没有买入的股票，就返回
    if len(stock_to_buy) == 0:
        return

    # 等权重买入 
#     weight =  1 / len(stock_to_buy)
    weight =  1 / 4
    
    # 买入
    for stock in stock_to_buy:
        if data.can_trade(context.symbol(stock)):
            # 下单使得某只股票的持仓权重达到weight，因为
            # weight大于0,因此是等权重买入
#             print(context.symbol(stock))
            context.order_target_percent(context.symbol(stock), weight)
#             print(stock)

m = M.trade.v3(
    instruments=instruments,
    start_date=start_date,
    end_date=end_date,
    initialize=initialize,
    handle_data=handle_data,
    # 买入订单以开盘价成交
    order_price_field_buy='open',
    # 卖出订单以开盘价成交
    order_price_field_sell='close',
    # 策略本金    
    capital_base= 295056.07,
    # 比较基准：沪深300
    benchmark='000300.INDX',
    # 传入数据给回测模块，所有回测函数里用到的数据都要从这里传入，并通过 context.options 使用，否则可能会遇到缓存问题
    m_cached=False,
    volume_limit=0,    
#     price_type  = "真实价格" ,
#     options={'selected_data': None, 'rebalance_period': None}
)
m.pyfolio_full_tear_sheet()
m.risk_analyze()
            
# m=M.backtest.v5( 
#     instruments=instruments,
#     start_date=start_date, 
#     end_date=end_date,
#     # 必须传入initialize，只在第一天运行
#     initialize=initialize,
#     #  必须传入handle_data,每个交易日都会运行
#     handle_data=handle_data,
#     # 买入以开盘价成交
#     order_price_field_buy='open',
#     # 卖出也以开盘价成交
#     order_price_field_sell='close',
#     # 策略本金
#     capital_base=400000,
#     # 比较基准：沪深300
#     benchmark='000300.INDX',
#     m_cached=False,
#     volume_limit=0,
# )      


# # 4. 策略回测：https://bigquant.com/docs/module_trade.html
# m = M.trade.v1(
#     instruments=instruments,
#     start_date=start_date,
#     end_date=end_date,
#     initialize=initialize,
#     handle_data=handle_data,
#     # 买入订单以开盘价成交
#     order_price_field_buy='open',
#     # 卖出订单以开盘价成交
#     order_price_field_sell='open',
#     capital_base=capital_base,
#     benchmark=benchmark,
#     # 传入数据给回测模块，所有回测函数里用到的数据都要从这里传入，并通过 context.options 使用，否则可能会遇到缓存问题
#     options={'selected_data': selected_data, 'rebalance_period': rebalance_period}
# )