'''

LSTM Networks应用于股票市场探究之Sequential Model

    整个模型只有一个input（6 features * 30 time series）
    LSTM future_return_5作为output（time series=30,features=['close','open','high','low','amount','volume']）

https://community.bigquant.com/t/LSTM-Networks%E5%BA%94%E7%94%A8%E4%BA%8E%E8%82%A1%E7%A5%A8%E5%B8%82%E5%9C%BA%E4%B9%8BSequential-Model/320
'''

# 导入包
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from keras.layers import Input, Dense, LSTM, merge
from keras.models import Model
import numpy as np
import pandas as pd


# 基础参数配置
class conf:
    instrument = '000300.SHA'  #股票代码
    #设置用于训练和回测的开始/结束日期
    start_date = '2005-01-01'
    split_date = '2015-01-01'
    end_date = '2017-05-01'
    fields = ['close', 'open', 'high', 'low', 'amount', 'volume']  # features
    seq_len = 30 #每个input的长度
    batch = 100 #整数，指定进行梯度下降时每个batch包含的样本数,训练时一个batch的样本会被计算一次梯度下降，使目标函数优化一步

# 数据导入以及初步处理
data = D.history_data(conf.instrument, conf.start_date, conf.end_date, conf.fields)
data['return'] = data['close'].shift(-5) / data['open'].shift(-1) - 1 #计算未来5日收益率（未来第五日的收盘价/明日的开盘价）
data=data[data.amount>0]
data.dropna(inplace=True)
datatime = data['date'][data.date>=conf.split_date]  #记录predictions的时间，回测要用
data['return'] = data['return'].apply(lambda x:np.where(x>=0.2,0.2,np.where(x>-0.2,x,-0.2)))  #去极值
data['return'] = data['return']*10  # 适当增大return范围，利于LSTM模型训练
data.reset_index(drop=True, inplace=True)
scaledata = data[conf.fields]
traindata = data[data.date<conf.split_date]

# 数据处理：设定每个input（30time series×6features）以及数据标准化
train_input = []
train_output = []
test_input = []
test_output = []
for i in range(conf.seq_len-1, len(traindata)):
    a = scale(scaledata[i+1-conf.seq_len:i+1])
    train_input.append(a)
    c = data['return'][i]
    train_output.append(c)
for j in range(len(traindata), len(data)):
    b = scale(scaledata[j+1-conf.seq_len:j+1])
    test_input.append(b)
    c = data['return'][j]
    test_output.append(c)

# LSTM接受数组类型的输入
train_x = np.array(train_input)
train_y = np.array(train_output)
test_x = np.array(test_input) 
test_y = np.array(test_output)

# 自定义激活函数
import tensorflow as tf
def atan(x): 
    return tf.atan(x)

# 构建神经网络层 1层LSTM层+3层Dense层
# 用于1个输入情况
lstm_input = Input(shape=(30,6), name='lstm_input')
lstm_output = LSTM(128, activation=atan, dropout_W=0.2, dropout_U=0.1)(lstm_input)
Dense_output_1 = Dense(64, activation='linear')(lstm_output)
Dense_output_2 = Dense(16, activation='linear')(Dense_output_1)
predictions = Dense(1, activation=atan)(Dense_output_2)

model = Model(input=lstm_input, output=predictions)

model.compile(optimizer='adam', loss='mse', metrics=['mse'])
    
model.fit(train_x, train_y, batch_size=conf.batch, nb_epoch=10, verbose=2)

# 预测
predictions = model.predict(test_x)

# 预测值和真实值的关系
data1 = test_y
data2 = predictions
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(data2,data1, 'o', label="data")
ax.legend(loc='best')

# 如果预测值>0,取为1；如果预测值<=0,取为-1.为回测做准备
for i in range(len(predictions)):
    if predictions[i]>0:
        predictions[i]=1
    elif predictions[i]<=0:
        predictions[i]=-1

# 将预测值与时间整合作为回测数据
cc = np.reshape(predictions,len(predictions), 1)
databacktest = pd.DataFrame()
databacktest['date'] = datatime
databacktest['direction']=np.round(cc)

# 在沪深300上回测
def initialize(context):
    # 系统已经设置了默认的交易手续费和滑点，要修改手续费可使用如下函数
    context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    # 传入预测数据和真实数据
    context.predictions=databacktest
    
    context.hold=conf.split_date

# 回测引擎：每日数据处理函数，每天执行一次
def handle_data(context, data):
    current_dt = data.current_dt.strftime('%Y-%m-%d') 
    sid = context.symbol(conf.instrument)
    cur_position = context.portfolio.positions[sid].amount    # 持仓
    if cur_position==0:
        if databacktest['direction'].values[databacktest.date==current_dt]==1:
            context.order_target_percent(sid, 0.9)
            context.date=current_dt
            
    else:
        if databacktest['direction'].values[databacktest.date==current_dt]==-1:
            if context.trading_calendar.session_distance(pd.Timestamp(context.date), pd.Timestamp(current_dt))>=5:
                context.order_target(sid, 0)

# 调用回测引擎
m8 = M.backtest.v5(
    instruments=conf.instrument,
    start_date=conf.split_date,
    end_date=conf.end_date,
    initialize=initialize,
    handle_data=handle_data,
    order_price_field_buy='open',       # 表示 开盘 时买入
    order_price_field_sell='close',     # 表示 收盘 前卖出
    capital_base=10000, 
    benchmark='000300.SHA', 
    m_cached=False
)    

# LSTM与stockranker配合回测

# 基础参数配置
class conf:
    start_date = '2010-01-01'
    end_date='2017-05-01'
    # split_date 之前的数据用于训练，之后的数据用作效果评估
    split_date = '2015-01-01'
    # D.instruments: https://bigquant.com/docs/data_instruments.html
    instruments = D.instruments(start_date, end_date)

    # 机器学习目标标注函数
    # 如下标注函数等价于 min(max((持有期间的收益 * 100), -20), 20) + 20 (后面的M.fast_auto_labeler会做取整操作)
    # 说明：max/min这里将标注分数限定在区间[-20, 20]，+20将分数变为非负数 (StockRanker要求标注分数非负整数)
    label_expr = ['return * 100', 'where(label > {0}, {0}, where(label < -{0}, -{0}, label)) + {0}'.format(20)]
    # 持有天数，用于计算label_expr中的return值(收益)
    hold_days = 5

    # 特征 https://bigquant.com/docs/data_features.html，你可以通过表达式构造任何特征
    features = [
        'close_5/close_0',  # 5日收益
        'close_10/close_0',  # 10日收益
        'close_20/close_0',  # 20日收益
        'avg_amount_0/avg_amount_5',  # 当日/5日平均交易额
        'avg_amount_5/avg_amount_20',  # 5日/20日平均交易额
        'rank_avg_amount_0/rank_avg_amount_5',  # 当日/5日平均交易额排名
        'rank_avg_amount_5/rank_avg_amount_10',  # 5日/10日平均交易额排名
        'rank_return_0',  # 当日收益
        'rank_return_5',  # 5日收益
        'rank_return_10',  # 10日收益
        'rank_return_0/rank_return_5',  # 当日/5日收益排名
        'rank_return_5/rank_return_10',  # 5日/10日收益排名
        'pe_ttm_0',  # 市盈率TTM
    ]

# 给数据做标注：给每一行数据（样本）打分，一般分数越高表示越好
m1 = M.fast_auto_labeler.v5(
    instruments=conf.instruments, start_date=conf.start_date, end_date=conf.end_date,
    label_expr=conf.label_expr, hold_days=conf.hold_days,
    benchmark='000300.SHA', sell_at='open', buy_at='open')
# 计算特征数据
m2 = M.general_feature_extractor.v5(
    instruments=conf.instruments, start_date=conf.start_date, end_date=conf.end_date,
    features=conf.features)
# 数据预处理：缺失数据处理，数据规范化，T.get_stock_ranker_default_transforms为StockRanker模型做数据预处理
m3 = M.transform.v2(
    data=m2.data, transforms=T.get_stock_ranker_default_transforms(),
    drop_null=True, astype='int32', except_columns=['date', 'instrument'],
    clip_lower=0, clip_upper=200000000)
# 合并标注和特征数据
m4 = M.join.v2(data1=m1.data, data2=m3.data, on=['date', 'instrument'], sort=True)

# 训练数据集
m5_training = M.filter.v2(data=m4.data, expr='date < "%s"' % conf.split_date)
# 评估数据集
m5_evaluation = M.filter.v2(data=m4.data, expr='"%s" <= date' % conf.split_date)
# StockRanker机器学习训练
m6 = M.stock_ranker_train.v2(training_ds=m5_training.data, features=conf.features)
# 对评估集做预测
m7 = M.stock_ranker_predict.v2(model_id=m6.model_id, data=m5_evaluation.data)


## 量化回测 https://bigquant.com/docs/strategy_backtest.html
# 回测引擎：初始化函数，只执行一次
def initialize(context):
    # 系统已经设置了默认的交易手续费和滑点，要修改手续费可使用如下函数
    context.set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    # 预测数据，通过options传入进来，使用 read_df 函数，加载到内存 (DataFrame)
    context.ranker_prediction = context.options['ranker_prediction'].read_df()
    # 设置买入的股票数量，这里买入预测股票列表排名靠前的5只
    stock_count = 5
    # 每只的股票的权重，如下的权重分配会使得靠前的股票分配多一点的资金，[0.339160, 0.213986, 0.169580, ..]
    context.stock_weights = T.norm([1 / math.log(i + 2) for i in range(0, stock_count)])
    # 设置每只股票占用的最大资金比例
    context.max_cash_per_instrument = 0.2
    
    context.date={}

# 回测引擎：每日数据处理函数，每天执行一次
def handle_data(context, data):
    # 按日期过滤得到今日的预测数据
    ranker_prediction = context.ranker_prediction[context.ranker_prediction.date == data.current_dt.strftime('%Y-%m-%d')]
    current_dt = data.current_dt.strftime('%Y-%m-%d')
    # 1. 资金分配
    # 平均持仓时间是hold_days，每日都将买入股票，每日预期使用 1/hold_days 的资金
    # 实际操作中，会存在一定的买入误差，所以在前hold_days天，等量使用资金；之后，尽量使用剩余资金（这里设置最多用等量的1.5倍）
    is_staging = context.trading_day_index < context.options['hold_days'] # 是否在建仓期间（前 hold_days 天）
    cash_avg = context.portfolio.portfolio_value / context.options['hold_days']
    cash_for_buy = min(context.portfolio.cash, (1 if is_staging else 1.5) * cash_avg)
    cash_for_sell = cash_avg - (context.portfolio.cash - cash_for_buy)
    positions = {e.symbol: p.amount * p.last_sale_price         for e, p in context.perf_tracker.position_tracker.positions.items()}
    equities = {e.symbol: e for e, p in context.perf_tracker.position_tracker.positions.items()}
    buy_dates = {}
    for e in equities:
        if e in context.date:
            buy_dates[e] = context.date[e]
    
    # 2. 生成卖出订单：hold_days天之后才开始卖出；对持仓的股票，按StockRanker预测的排序末位淘汰
    if databacktest['direction'].values[databacktest.date==current_dt]==-1:    # LSTM择时卖
        instruments = list(reversed(list(ranker_prediction.instrument[ranker_prediction.instrument.apply(
                lambda x: x in equities and not context.has_unfinished_sell_order(equities[x]))])))
        for instrument in instruments:
            if context.trading_calendar.session_distance(pd.Timestamp(context.date[instrument]), pd.Timestamp(current_dt))>=5:
                context.order_target(context.symbol(instrument), 0)
    
    if not is_staging and cash_for_sell > 0:
        instruments = list(reversed(list(ranker_prediction.instrument[ranker_prediction.instrument.apply(
                lambda x: x in equities and not context.has_unfinished_sell_order(equities[x]))])))
        # print('rank order for sell %s' % instruments)
        for instrument in instruments:
            context.order_target(context.symbol(instrument), 0)
            cash_for_sell -= positions[instrument]
            if cash_for_sell <= 0:
                break

    # 3. 生成买入订单：按StockRanker预测的排序，买入前面的stock_count只股票
    if databacktest['direction'].values[databacktest.date==current_dt]==1:    # LSTM择时买
        buy_dt = data.current_dt.strftime('%Y-%m-%d')
        context.date=buy_dt
        buy_cash_weights = context.stock_weights
        buy_instruments = list(ranker_prediction.instrument[:len(buy_cash_weights)])
        max_cash_per_instrument = context.portfolio.portfolio_value * context.max_cash_per_instrument
        for i, instrument in enumerate(buy_instruments):
            cash = cash_for_buy * buy_cash_weights[i]
            if cash > max_cash_per_instrument - positions.get(instrument, 0):
                # 确保股票持仓量不会超过每次股票最大的占用资金量
                cash = max_cash_per_instrument - positions.get(instrument, 0)
            if cash > 0:
                context.order_value(context.symbol(instrument), cash)
                buy_dates[instrument] = current_dt
            
    context.date = buy_dates

# 调用回测引擎
m8 = M.backtest.v5(
    instruments=m7.instruments,
    start_date=m7.start_date,
    end_date=m7.end_date,
    initialize=initialize,
    handle_data=handle_data,
    order_price_field_buy='open',       # 表示 开盘 时买入
    order_price_field_sell='close',     # 表示 收盘 前卖出
    capital_base=100000,               # 初始资金
    benchmark='000300.SHA',             # 比较基准，不影响回测结果
    # 通过 options 参数传递预测数据和参数给回测引擎
    options={'ranker_prediction': m7.predictions, 'hold_days': conf.hold_days},
    m_cached=False
)

