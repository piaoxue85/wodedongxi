
# coding: utf-8

# AlphaHorizon可以对研究得到的alpha因子做一个比较完整的分析报告，包括alpha因子的回测、IC和换手率等等。需要注意的是，AlphaHorizon的分析和真实的策略交易是不一样的，它**仅仅着眼于alpha因子对于收益率的预测方面**。
# 
# ---
# 

# In[ ]:

import pandas as pd
import numpy as np
from scipy.stats import mstats
from scipy import stats
from datetime import datetime
from CAL.PyCAL import *
font.set_size(12)
import lib.AlphaHorizon as ah


# 本文中，以非流动性因子（[非流动性因子ILLIQ - 寻找市场对弱流动性的收益补偿 ](https://uqer.io/community/share/57ba8b1e228e5b79a575a226)）为例，来说明AlphaHorizon的分析过程。

# # 1. 数据加载
# ---
# AlphaHorizon 分析只需要两个数据：
# 
# - 因子数据，格式为 pd.Series - MultiIndex，MultiIndex包括tradeDate、secID两级
# - 价格数据，格式为 pd.DataFrame, index为tradeDate，columns为各个股票的secID；此处的价格即收盘价
# 
# 本文的分析中，使用从09年至今的超过7年数据进行回测。

# In[ ]:

begin_date = datetime.strptime('2009-01-01', '%Y-%m-%d')    # 起始时间
end_date = datetime.strptime('2016-07-01', '%Y-%m-%d')      # 截止时间
universe = set_universe('A')

# 起始日期至截止日期之间的交易日列表
dates_list = DataAPI.TradeCalGet(exchangeCD='XSHG', beginDate=begin_date, endDate=end_date)
dates_list = dates_list[dates_list['isOpen']==1]['calendarDate'].values.tolist()
dates_list[0:5]


# ## 1.1 因子数据加载
# 
# factor_init 保存因子数据

# In[ ]:

# 提取数据
factor_df = pd.read_csv('Illiquidity_W5_FullA.csv')                              # 5天窗口非流动性因子
# factor_df = pd.read_csv('Illiquidity_Neutral_W5_FullA.csv')                    # 5天窗口非流动性因子-中性化
factor_df['tradeDate'] = pd.to_datetime(factor_df['tradeDate'], format='%Y-%m-%d')
factor_df = factor_df[(factor_df['tradeDate']>begin_date) & (factor_df['tradeDate']<end_date)]
factor_df = factor_df[factor_df.columns[1:]].set_index('tradeDate')
univ = [x for x in universe if x in factor_df.columns]
factor_df = factor_df[univ]
factor_df = factor_df.stack()
factor_df.index.names = [u'tradeDate', 'secID']
factor_init = factor_df
factor_init.head(10)


# ## 1.2 因子数据处理
# 
# 对因子数据进行截面处理：去极值，标准化

# In[ ]:

def winsorize_series(se):
    q = se.quantile([0.025, 0.975])
    if isinstance(q, pd.Series) and len(q) == 2:
        se[se < q.iloc[0]] = q.iloc[0]
        se[se > q.iloc[1]] = q.iloc[1]
    return se

def standardize_series(se):
    se_std = se.std()
    se_mean = se.mean()
    return (se - se_mean)/se_std

factor_init = factor_df.groupby(level='tradeDate').apply(winsorize_series)      # 去极值
factor_init = factor_init.groupby(level='tradeDate').apply(standardize_series)  # 标准化
factor_init.hist(figsize=(12,6), bins=50)


# ## 1.3 价格数据加载
# 
# prices_init 保存价格数据

# In[ ]:

# price_df_1 = DataAPI.MktEqudAdjGet(secID=universe, beginDate='20081201', endDate='20121231', field='tradeDate,secID,closePrice')
# price_df = DataAPI.MktEqudAdjGet(secID=universe, beginDate='20130101', field='tradeDate,secID,closePrice')
# price_df = price_df.append(price_df_1)
# price_df.to_csv('ClosePrice_FullA.csv')  
price_df = pd.read_csv('ClosePrice_FullA.csv')    # 直接DataAPI拿取比较慢，保存成csv文件之后直接读取
price_df = price_df[price_df.columns[1:]]
price_df['tradeDate'] = pd.to_datetime(price_df['tradeDate'], format='%Y-%m-%d')
price_df = price_df.pivot(index='tradeDate', columns='secID', values='closePrice')
prices_init = price_df
prices_init.tail()


# ## 1.3 股票行业数据加载
# 
# ticker_sector 保存行业数据，此处为了简便起见，我们使用固定的行业分类

# In[ ]:

ticker_sector_df = DataAPI.EquIndustryGet(secID=universe, industryVersionCD='010308', intoDate='20160701', field='secID,secShortName,industry,industryID1,industryName1')
ticker_sector_df['industryName1'] = [x.decode('utf8') for x in ticker_sector_df['industryName1']]

# 将行业编号，用数字代替，节省存储空间
sectors = ticker_sector_df[['industryID1','industryName1']]
sectors = sectors.drop_duplicates().sort('industryID1')
sectors['sectorID'] = range(len(sectors))
sectors = sectors[['sectorID', 'industryName1']].set_index('sectorID')
sectors_id2name = sectors['industryName1'].to_dict()
sectors_name2id = {sectors_id2name[id]: id for id in sectors_id2name.keys()}
sector_names = sectors_id2name

ticker_sector_df['sectorID'] = ticker_sector_df['industryName1'].apply(lambda x: sectors_name2id[x])
ticker_sector = ticker_sector_df[['secID','sectorID']].set_index('secID')['sectorID'].to_dict()
ticker_sector['600067.XSHG'] = 6

sectors


# # 2. AlphaHorizon 分析部分
# ---
# ## 2.1 整理输入数据
# 
# get_clean_factor_and_forward_returns 将输入的 factor_init, prices_init 整理成目标格式
# 
# - factor 为因子数据，比初始的 factor_init 在 MultiIndex 多了个行业分类选项group
# - forward_returns 为前瞻收益率数据，columns 为前瞻窗口，默认考虑1、5、10、20，对应于日度、周度、半月度、月度调仓

# In[ ]:

factor, forward_returns = ah.get_clean_factor_and_forward_returns(factor_init, prices_init, groupby=ticker_sector, groupby_labels=sector_names)


# In[ ]:

factor.tail()


# In[ ]:

forward_returns.tail()


# ## 2.2 分位数收益简要分析
# 
# 将股票按照alpha因子分为不同的分位数组合，默认分为5分位

# In[ ]:

quantized_factor = ah.quantize_factor(factor)


# In[ ]:

quantized_factor.tail(10)


# 每天，计算不同分位数组合内股票的平均超额收益（此处的超额收益为超过市场平均的收益，下同）

# In[ ]:

mean_return_by_q_daily, std_err = ah.mean_return_by_quantile(quantized_factor, forward_returns, by_group=False, by_time='D')


# In[ ]:

mean_return_by_q_daily.head()


# 每天计算得到的不同分位数组合内股票的平均超额收益，再取时间序列平均

# In[ ]:

mean_return_by_q, std_err_by_q = ah.mean_return_by_quantile(quantized_factor,forward_returns,by_group=False)


# In[ ]:

mean_return_by_q


# 作图展示不同分位数组合的日平均超额收益情况，图中的纵轴超额收益的单位为bps(0.0001):
# 
# - 无论前瞻时间窗口，第五分位组合的超额收益均为正，第一分位组合超额收益则为负
# - 从一至五，各个分位数组合超额收益呈现递增趋势

# In[ ]:

ah.plot_quantile_returns_bar(mean_return_by_q)


# 还可以计算最好与最坏的分位数组合的平均超额收益之差，并作为时间序列画出来

# In[ ]:

quant_return_spread, std_err_spread = ah.compute_mean_returns_spread(mean_return_by_q_daily, 5, 1, std_err)  # 5分位数最好，1分位数最差


# In[ ]:

ah.plot_mean_quantile_returns_spread_time_series(quant_return_spread, std_err_spread)


# **做多最好的分位数组合，同时做空最坏的分位数组合**；下图给出这一策略的累积收益曲线

# In[ ]:

ah.plot_top_minus_bottom_cumulative_returns(quant_return_spread)


# 做多最好的分位数组合，同时做空最坏的分位数组合；下表给出该策略在不同的调仓周期下的风险指标，包括最大回撤、收益年化波动率、年化alpha、beta、信息比率：
# 
# - 非流动性因子收益很高，回撤也比较大且普遍在15%往上

# In[ ]:

alpha_beta_top_minus_bottom = ah.factor_alpha_beta(factor, forward_returns, factor_returns=quant_return_spread)
alpha_beta_top_minus_bottom


# 简单等权持有不同的分位数组合，其净值走势图（此处净值为超过市场平均的净值）如下，以半月度调仓（10日调仓）为例：
# 
# - 对一个好alpha信号，我们期待不同分位数组合的净值走势随着时间推移单调散开

# In[ ]:

ah.plot_cumulative_returns_by_quantile(mean_return_by_q_daily, period=5)


# 有时，我们希望**以因子值为权重分配多空仓位**（与之前的等权做多top分位组合，做空bottom分位组合的策略形成对比）；下图给出这一策略的累积收益曲，仅给出半月度调仓的净值走势

# In[ ]:

ls_factor_returns = ah.factor_returns(factor, forward_returns)


# In[ ]:

ah.plot_cumulative_returns(ls_factor_returns[10], period=10)


# 不同调仓周期情况下，计算以因子权重分配多空仓位的组合的净值走势

# In[ ]:

ah.plot_cumulative_returns_by_period(ls_factor_returns)


# 因子值为权重构建多空组合，得到的策略净值走势的各个风险指标分析：
# 
# - 以因子值为权重构建多空组合，其最大回撤和收益波动率均有很大好转

# In[ ]:

alpha_beta = ah.factor_alpha_beta(factor, forward_returns, factor_returns=ls_factor_returns)
alpha_beta


# ## 2.3 信息系数分析
# 
# ---
# 
# 信息系数衡量的是因子对股票横截面超额收益率的预测能力；计算方式为当期因子值与下期股票收益率之间的秩相关系数；信息系数越接近于1，说明因子的预测效果越好。

# 对于不同的调仓周期，我们计算了因子信息系数的时间序列如下

# In[ ]:

ic = ah.factor_information_coefficient(factor, forward_returns)


# In[ ]:

ic.head()


# 对于不同的调仓周期，计算得到的因子信息系数的时间序列作图
# 
# - 通过查验因子信息系数的时间序列，可以看到因子的预测能力随着时间的变化
# - 我们希望信息系数序列的均值尽可能的大，且走势稳定

# In[ ]:

ah.plot_ic_ts(ic)


# 对于不同的调仓周期，计算得到的因子信息系数的作分布直方图，可以直观看到信息系数的分布特征，比如是否有厚尾特征等等

# In[ ]:

ah.plot_ic_hist(ic)


# 对于不同的调仓周期，计算得到的因子信息系数的作Q-Q图，同样可以直观看到信息系数的分布特征
# 
# - 信息系数序列表现出一定的左部厚尾特征

# In[ ]:

ah.plot_ic_qq(ic)


# 进一步，可以将因子的IC分月度进行平均，可以看出因子在历史上每个月的预测能力的好坏，观察看是否有显著的季节特性等

# In[ ]:

mean_monthly_ic = ah.mean_information_coefficient(factor, forward_returns, by_time='M')


# In[ ]:

mean_monthly_ic.head()


# 对于不同的调仓周期，IC月度平均后作热度图：
# 
# - 图中颜色越红表示IC越大，也即表示因子在这个月表现良好；颜色越绿表示因子在这个月表现不佳；
# - 注意，2016年7月之后的绿色是因为没有回测数据而IC为nan
# - 可以注意到，2014年11月和12月IC出现显著为绿色的情况，是因为这一段时间小盘股表现明显弱于大盘股，而ILLIQ有小盘股暴露

# In[ ]:

ah.plot_monthly_ic_heatmap(mean_monthly_ic)


# ## 2.4 换手率分析
# 
# ---
# 
# 计算因子换手率可以展示出因子的时间序列稳定性，侧面反映出使用该因子做策略时候的调仓成本等
# 
# - 可以看到，该因子月度调仓，其换手大致在40%附近
# - 多头组合换手率略高于空头组合

# In[ ]:

ah.plot_top_bottom_quantile_turnover(quantized_factor, period=20)


# 因子的自相关系数同样可以展示出因子的时间序列稳定性
# 
# - 当前因子和20天前的因子的自相关系数一直保持在0.8附近

# In[ ]:

factor_autocorrelation = ah.factor_rank_autocorrelation(factor, period=20)
ah.plot_factor_rank_auto_correlation(factor_autocorrelation, period=20)


# # 2.5 分行业表现
# ---
# 上述的IC和超额收益分析，可以很容易的拓展到分行业的情况

# In[ ]:

ic_by_sector = ah.mean_information_coefficient(factor, forward_returns, by_group=True)


# In[ ]:

ic_by_sector.head()


# 分行业的IC均值作图，可以看到该因子在不同行业里的表现相对来说都比较均衡；不同的颜色代表不同的调仓周期

# In[ ]:

ah.plot_ic_by_group(ic_by_sector)


# 对于不同的行业，计算用因子分位数选股构建组合得到的平均超额收益；直方图中不同的颜色代表不同的调仓周期

# In[ ]:

mean_return_quantile_sector, mean_return_quantile_sector_err = ah.mean_return_by_quantile(quantized_factor, forward_returns, by_group=True)


# In[ ]:

mean_return_quantile_sector.head()


# In[ ]:

ah.plot_quantile_returns_bar(mean_return_quantile_sector, by_group=True)


# # 2.6 总结性数据表格

# In[ ]:

periods=(1, 5, 10, 20)
factor_autocorrelations = pd.concat([ah.factor_rank_autocorrelation(factor, period=p) for p in periods], axis=1)


# In[ ]:

returns_table,ic_summary_table,turnover_table,auto_corr = ah.summary_stats_return_dfs(ic, alpha_beta, 
                                                                                   quantized_factor, 
                                                                                   mean_return_by_q, 
                                                                                   factor_autocorrelations, 
                                                                                   quant_return_spread)


# 对不同调仓周期，以因子值为权重构建多空组合，得到的策略回测结果的统计

# In[ ]:

returns_table


# 对不同调仓周期，计算因子IC序列的统计结果

# In[ ]:

ic_summary_table


# 对不同调仓周期，计算因子分位数股票组合的换手率情况

# In[ ]:

turnover_table


# 因子的自相关性，计算了当前因子和n天前的因子的相关系数序列的平均值

# In[ ]:

auto_corr

