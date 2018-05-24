# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 17:38:39 2017

@author: LZJF
"""

import pandas as pd
import numpy as np


# def import_data(name):
#     data = pd.read_csv('%s.csv' % name, index_col=0)
#     data.index = pd.to_datetime([str(i) for i in data.index])
#     return data


def pearson(x, y, skipna=False):
    upside = ((x - x.mean()) * (y - y.mean())).sum(skipna=skipna)
    downside = np.sqrt((np.square(x - x.mean()).sum()) *
                       (np.square(y - y.mean()).sum(skipna=skipna)))
    return upside / downside


# def save_factor(factor, factor_id, no_zdt):
#     if no_zdt:
#         factor_name = 'alpha#%s_no_zdt_1D' % factor_id
#     else:
#         factor_name = 'alpha#%s_origin_1D' % factor_id
#     factor.index.name = factor_name
#     to_file = 'F:\Strategies\World_Quant_Alphas/#%s' % factor_id
#     if not os.path.exists(to_file):
#         os.mkdir(to_file)
#     else:
#         pass
#     factor.to_csv(to_file + '/%s.csv' % factor_name)
#     print ('保存完成')


def rolling_stop(stop, window):
    temp = pd.DataFrame(index=stop.columns)
    for i in stop.index:
        one = stop[:i][-window:].notnull().any(axis=0)
        temp[i] = one
    return temp.T


def rolling_rank(data, window):
    temp = pd.DataFrame(index=data.columns)
    for i in data.index:
        one = data[:i][-window:].rank(axis=0, pct=True).iloc[-1]
        temp[i] = one
    return temp.T


def rolling_null(data, window):
    temp = pd.DataFrame(index=data.columns)
    for i in data.index:
        one = data[:i][-window:].isnull().any(axis=0)
        temp[i] = one
    return temp.T


def linear_decay(data, window):
    result = pd.DataFrame(np.nan, index=data.index, columns=data.columns)
    weight = np.arange(window) + 1.
    weight = weight / weight.sum()
    for i in range(window, data.shape[0]):
        t = data.index[i]
        result.ix[t, :] = data[i-window:i].T.dot(weight)
    return result


def ind_neutral(data, ind):
    temp = pd.DataFrame(index=data.columns)
    for i in data.index:
        temp[i] = data.ix[i].groupby(ind.ix[i]).apply(lambda x: x - x.mean())
    return temp.T

unrealized = [
                "048",
                "058",
                "059",
                "063",
                "067",
                "068",
                "069",
                "070",
                "076",
                "079",
                "080",
                "081",
                "082",
                "084",
                "087",
                "089",
                "090",
                "091",
                "093",
                "097",
                "100",
             ]


def factor_cal(data, factor_id, no_zdt=False, no_st=False, no_new=False, ):
    if factor_id in unrealized :
        return "id not found"
    
    high = data['high']
    low = data['low']
    close = data['close']
    OPEN = data['open']
    value = data['value']
    volume = data['volume']
#     volume.replace(0, np.nan, inplace=True)
    cap = data['cap']
#     stop = data['stop']
    returns = data["return"]
#     st = data['st']
#     ind = data['ind']
#     fcf = data['fcf']
#     asset_debt = data['asset_debt']
#     price_adj_f = data['price_adj_f']

    # 将新股（上市小于63天）的所有数据设为na
    if no_new:
        high[rolling_null(close, 63)]  = np.nan
        low[rolling_null(close, 63)]   = np.nan
        close[rolling_null(close, 63)] = np.nan
        OPEN[rolling_null(close, 63)]  = np.nan
        value[rolling_null(close, 63)] = np.nan
        volume[rolling_null(close, 63)]= np.nan
        cap[rolling_null(close, 63)]   = np.nan
    
    adj_OPEN   = OPEN  
    adj_close  = close 
    adj_high   = high  
    adj_low    = low   
    adj_volume = volume
    returns = returns
    vwap = value / adj_volume
    
    print( '开始计算%s号因子' % factor_id)
    if factor_id == '001':
        #(rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) -0.5)   
        df = pd.DataFrame(adj_close)  
        df[returns < 0] = returns.rolling(window=20).std(skipna=False)
        ts_argmax = np.square(df).rolling(window=5).apply(np.argmax) + 1
#         ts_argmax[rolling_null(close, 5)] = np.nan
#         ts_argmax[rolling_stop(stop, 20)] = np.nan
        ts_argmax = ts_argmax.rank(axis=1, pct=True)
        factor = ts_argmax - 0.5
    elif factor_id == '002':
        #  alpha002:(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))  
        temp1 = np.log(adj_volume).diff(2)
        temp1_rank = temp1.rank(axis=1, pct=True)
        temp2 = (close - OPEN) / OPEN
        temp2_rank = temp2.rank(axis=1, pct=True)
        factor = -1 * temp1_rank.rolling(window=6).corr(temp2_rank)
        #factor[rolling_null(close, 6)] = np.nan
        #factor[rolling_stop(stop, 6)] = np.nan
    elif factor_id == '003':
        # alpha003:(-1 * correlation(rank(open), rank(volume), 10))  
        open_rank = OPEN.rank(axis=1, pct=True)
        volume_rank = volume.rank(axis=1, pct=True)
        factor = -1 * open_rank.rolling(window=10).corr(volume_rank)
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '004':
        # alpha004: (-1 * ts_rank(rank(low), 9)) 
        low_rank = adj_low.rank(axis=1, pct=True)
        factor = -1 * rolling_rank(low_rank, 9)
        #factor[rolling_null(close, 9)] = np.nan
        #factor[rolling_stop(stop, 9)] = np.nan
    elif factor_id == '005':
        #(rank((open - (sum(vwap, 10) / 10)))*(-1*abs(rank((close - vwap)))))
        be_half = (adj_OPEN - vwap.rolling(window=10).mean()).rank(axis=1, pct=True)
        af_half = (adj_close - vwap).rank(axis=1, pct=True)
        factor = -1 * be_half * af_half
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '006':
        #  alpha006: (-1 * correlation(open, volume, 10)) 
        factor = -1 * adj_OPEN.rolling(window=10).corr(adj_volume)
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '007':
        # alpha007: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1* 1))
        factor = -1 * rolling_rank(np.abs(adj_close.diff(7)), 60) * np.sign(adj_close.diff(7))
        factor[adj_volume.rolling(window=20).mean() > volume] = -1
        #factor[rolling_null(close, 60)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '008':
        # alpha008: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)),10)))) 
        temp = OPEN.rolling(window=5).sum() * returns.rolling(window=5).sum()
        factor = -1 * (temp - temp.diff(10)).rank(axis=1, pct=True)
        # temp - temp.diff(10) 不就是10日前的temp吗？ SB啊！
        #factor[rolling_null(close, 15)] = np.nan
        #factor[rolling_stop(stop, 15)] = np.nan
    elif factor_id == '009':
        #alpha009:((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ?delta(close, 1) : (-1 * delta(close, 1))))
        cond_1 = adj_close.diff().rolling(window=5).min() > 0
        cond_2 = adj_close.diff().rolling(window=5).max() < 0
        factor = -1 * adj_close.diff()
        factor[cond_1 | cond_2] = adj_close.diff()
        #factor[rolling_null(close, 6)] = np.nan
        #factor[rolling_stop(stop, 6)] = np.nan
    elif factor_id == '010':
        # alpha010: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0)? delta(close, 1) : (-1 * delta(close, 1)))))  
        cond_1 = adj_close.diff().rolling(window=4).min() > 0
        cond_2 = adj_close.diff().rolling(window=4).max() < 0
        factor = -1 * adj_close.diff()
        factor[cond_1 | cond_2] = adj_close.diff()
        factor = factor.rank(axis=1, pct=True)
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '011':
        #((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3)))*rank(delta(volume, 3)))
        temp1 = (vwap - adj_close).rolling(window=3).max().rank(axis=1, pct=True)
        temp2 = (vwap - adj_close).rolling(window=3).min().rank(axis=1, pct=True)
        temp3 = adj_volume.diff(3).rank(axis=1, pct=True)
        factor = (temp1 + temp2) * temp3
        #factor[rolling_null(close, 3)] = np.nan
        #factor[rolling_stop(stop, 3)] = np.nan
    elif factor_id == '012':
        #  alpha012:(sign(delta(volume, 1)) * (-1 * delta(close, 1)))
        factor = -1 * np.sign(adj_volume.diff()) * adj_close.diff()
        #factor[rolling_null(close, 2)] = np.nan
        #factor[rolling_stop(stop, 2)] = np.nan
    elif factor_id == '013':
        # alpha013:(-1 * rank(covariance(rank(close), rank(volume), 5))) 
        close_rank = adj_close.rank(axis=1, pct=True)
        volume_rank = adj_volume.rank(axis=1, pct=True)
        factor = -1 * (close_rank.rolling(window=5).cov(volume_rank)).rank(axis=1, pct=True)
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '014':
        #  alpha014:((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10)) 
        temp1 = adj_OPEN.rolling(window=10).corr(adj_volume)
        temp2 = returns.diff(3).rank(axis=1, pct=True)
        factor = -1 * temp2 * temp1
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '015':
        # alpha015:(-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3)) 
        high_rank = adj_high.rank(axis=1, pct=True)
        volume_rank = adj_volume.rank(axis=1, pct=True)
        temp1 = high_rank.rolling(window=3).corr(volume_rank)
        factor = -1 * temp1.rank(axis=1, pct=True).rolling(window=3).sum()
        #factor[rolling_null(close, 6)] = np.nan
        #factor[rolling_stop(stop, 6)] = np.nan
    elif factor_id == '016':
        #  alpha016:(-1 * rank(covariance(rank(high), rank(volume), 5))) 
        high_rank = adj_high.rank(axis=1, pct=True)
        volume_rank = adj_volume.rank(axis=1, pct=True)
        factor = -1 * high_rank.rolling(window=5).cov(volume_rank)
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '017':
        # alpha017: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) *rank(ts_rank((volume / adv20), 5)))
        temp1 = rolling_rank(adj_close, 10).rank(axis=1, pct=True)
        temp2 = adj_close.diff(1).diff(1).rank(axis=1, pct=True)
        temp3 = rolling_rank(adj_volume / adj_volume.rolling(window=20).mean(), 5).rank(axis=1, pct=True)
        factor = -1 * temp1 * temp2 * temp3
        #factor[rolling_null(close, 25)] = np.nan
        #factor[rolling_stop(stop, 25)] = np.nan
    elif factor_id == '018':
        # alpha018: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open,10))))
        temp1 = adj_close.rolling(window=10).corr(adj_OPEN).replace([-np.inf, np.inf], np.nan)
        temp2 = np.abs(adj_close - adj_OPEN).rolling(window=5).std()
        factor = -1 * (temp2 + temp1 + adj_close - adj_OPEN).rank(axis=1, pct=True)
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '019':
        #  alpha019:((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns,250)))))
        factor = -1 * np.sign(adj_close.diff(7)) * ((1 + returns.rolling(window=250).sum()).rank(axis=1, pct=True) + 1)
        #factor[rolling_null(close, 250)] = np.nan
        #factor[rolling_stop(stop, 8)] = np.nan
    elif factor_id == '020':
        # alpha020: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open -delay(low, 1))))
        temp1 = (adj_OPEN - adj_high.diff(1)).rank(axis=1, pct=True)
        temp2 = (adj_OPEN - adj_close.diff(1)).rank(axis=1, pct=True)
        temp3 = (adj_OPEN - adj_low.diff(1)).rank(axis=1, pct=True)
        factor = -1 * temp1 * temp2 * temp3
        #factor[rolling_null(close, 2)] = np.nan
        #factor[rolling_stop(stop, 2)] = np.nan
    elif factor_id == '021':
        # alpha021: ((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ? (-1 * 1) : (((sum(close,2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume /adv20) == 1)) ? 1 : (-1 * 1))))
        cond_1 = adj_close.rolling(window=8).mean() + adj_close.rolling(window=8).std() < adj_close.rolling(window=2).mean()
        cond_2 = adj_close.rolling(window=8).mean() - adj_close.rolling(window=8).std() > adj_close.rolling(window=2).mean()
        cond_3 = adj_volume / adj_volume.rolling(window=20).mean() >= 1
        cond_4 = adj_volume / adj_volume.rolling(window=20).mean() < 1
        factor = pd.DataFrame(np.nan, index=adj_close.index, columns=adj_close.columns)
        factor[cond_1] = -1
        factor[cond_2] = 1
        factor[np.logical_and(np.logical_not(np.logical_or(cond_1, cond_2)), cond_3)] = 1
        factor[np.logical_and(np.logical_not(np.logical_or(cond_1, cond_2)), cond_4)] = -1
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '022':
        # alpha022:(-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20)))) 
        part_1 = adj_high.rolling(window=5).corr(adj_volume).diff(5)
        part_2 = adj_close.rolling(window=20).std().rank(axis=1, pct=True)
        factor = -1 * part_1 * part_2
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '023':
        # alpha023: (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0) 
        factor = pd.DataFrame(np.nan, index=adj_high.index, columns=adj_high.columns)
        factor[adj_high > adj_high.rolling(window=20).mean()] = -1 * adj_high.diff(2)
        factor[adj_high <= adj_high.rolling(window=20).mean()] = 0
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '024':
        # alpha024: ((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) ||((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close,100))) : (-1 * delta(close, 3)))
        cond_1 = adj_close.rolling(window=100).mean().diff(100) / adj_close.shift(100) <= 0.05
        factor = -1 * adj_close.diff(3)
        factor[cond_1] = -1 * (adj_close - adj_close.rolling(window=100).min())
        #factor[rolling_null(close, 100)] = np.nan
        #factor[rolling_stop(stop, 3)] = np.nan
    elif factor_id == '025':
        #rank(((((-1* returns)* adv20)* vwap)* (high - close)))
        part_1 = -1 * returns * adj_volume.rolling(window=20).mean()
        part_2 = vwap * (adj_high - adj_close)
        factor = (part_1 * part_2).rank(axis=1, pct=True)
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '026':
        #   alpha026:(-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3)) 
        volume_rank = rolling_rank(adj_volume, 5)
        high_rank = rolling_rank(adj_high, 5)
        factor = -1 * volume_rank.rolling(window=5).corr(high_rank).rolling(window=3).max()
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '027':
        #((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1* 1) : 1)
        factor = pd.DataFrame(np.nan, index=volume.index, columns=volume.columns)
        volume_rank = adj_volume.rank(axis=1, pct=True)
        vwap_rank = vwap.rank(axis=1, pct=True)
        corr_ = volume_rank.rolling(window=6).corr(vwap_rank)
        corr_rank = corr_.rolling(window=2).mean().rank(axis=1, pct=True)
        cond_1 = corr_rank > 0.5
        cond_2 = corr_rank <= 0.5
        factor[cond_1] = -1
        factor[cond_2] = 1
        #factor[rolling_null(close, 6)] = np.nan
        #factor[rolling_stop(stop, 6)] = np.nan
    elif factor_id == '028':
        # alpha028:scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))  
        part_1 = adj_volume.rolling(window=20).mean().rolling(window=5).corr(adj_low)
        part_2 = (adj_high + adj_low) / 2 - adj_close
        factor = part_1 + part_2
        factor = (factor.T / factor.sum(axis=1)).T
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '029':
        # alpha029:(min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1),5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))
        temp1 = rolling_rank(-1 * returns.shift(6), 5)
        close_rank = (-1 * (adj_close - 1).diff(5).rank(axis=1, pct=True)).rank(axis=1, pct=True)
        temp2 = np.log(close_rank.rolling(window=2).min())
        temp3 = (temp2.T / temp2.sum(axis=1)).T.rank(axis=1, pct=True)
        factor = temp3.rolling(window=5).min() + temp1
        #factor[rolling_null(close, 6)] = np.nan
        #factor[rolling_stop(stop, 6)] = np.nan
    elif factor_id == '030':
        # alpha030:(((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))
        sign_1 = np.sign(adj_close.diff())
        sign_2 = np.sign(adj_close.diff().shift())
        sign_3 = np.sign(adj_close.diff().shift(2))
        sign_rank = (sign_1 + sign_2 + sign_3)
        factor = (1 - sign_rank) * adj_volume.rolling(window=5).sum() / adj_volume.rolling(window=20).sum()
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '031':
        # alpha031:((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 *delta(close, 3)))) + sign(scale(correlation(adv20, low, 12))))
        close_rank_1 = adj_close.diff(10).rank(axis=1, pct=True)
        decay_linear_rank = linear_decay(-1 * close_rank_1, 10).rank(axis=1, pct=True)
        close_rank_2 = (-1 * adj_close.diff(3)).rank(axis=1, pct=True)
        corr_ = adj_volume.rolling(window=20).mean().rolling(window=12).corr(adj_low)
        corr_sign = np.sign((corr_.T / corr_.sum(axis=1)).T)
        factor = decay_linear_rank + close_rank_2 + corr_sign
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '032':
        #(scale(((sum(close, 7) / 7) - close)) + (20* scale(correlation(vwap, delay(close, 5), 230))))
        temp1 = adj_close.rolling(window=7).mean() - adj_close
        part_1 = (temp1.T / temp1.sum(axis=1)).T
        temp2 = vwap.rolling(window=230).corr(adj_close.shift(5))
        part_2 = (temp2.T / temp2.sum(axis=1)).T
        factor = part_1 + 20 * part_2
        #factor[rolling_null(close, 230)] = np.nan
        #factor[rolling_stop(stop, 7)] = np.nan
    elif factor_id == '033':
        # alpha033: rank((-1 * ((1 - (open / close))^1)))   
        factor = (OPEN / close - 1).rank(axis=1, pct=True)
        #factor[stop.notnull()] = np.nan
    elif factor_id == '034':
        # alpha034: rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1))))) 
        temp1 = returns.rolling(window=2).std() / returns.rolling(window=5).std()
        close_rank = adj_close.diff().rank(axis=1, pct=True)
        factor = (1 - temp1.rank(axis=1, pct=True) + 1 - close_rank).rank(axis=1, pct=True)
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '035':
        # alpha035:((ts_rank(volume, 32) * (1 - ts_rank(((close + high) - low), 16))) * (1 -ts_rank(returns, 32))) 
        volume_rank = rolling_rank(adj_volume, 32)
        xx_rank = rolling_rank(adj_close + adj_high - adj_low, 16)
        returns_rank = rolling_rank(returns, 32)
        factor = volume_rank * (1 - xx_rank) * (1 - returns_rank)
        #factor[rolling_null(close, 32)] = np.nan
        #factor[rolling_stop(stop, 32)] = np.nan
    elif factor_id == '036':
        #(((((2.21* rank(correlation((close - open), delay(volume, 1), 15))) + (0.7* rank((open - close)))) + (0.73* rank(ts_rank(delay((-1* returns), 6), 5)))) + rank(abs(correlation(vwap, adv20, 6)))) + (0.6* rank((((sum(close, 200) / 200) - open)* (close - open)))))
        part_1 = (adj_close - adj_OPEN).rolling(window=15).corr(adj_volume.shift(1)).rank(axis=1, pct=True)
        part_2 = (adj_OPEN - adj_close).rank(axis=1, pct=True)
        part_3 = rolling_rank(-1 * returns.shift(6), 5).rank(axis=1, pct=True)
        part_4 = vwap.rolling(window=6).corr(adj_volume.rolling(window=20).mean()).rank(axis=1, pct=True)
        part_5 = ((adj_close.rolling(window=200).mean() - adj_OPEN) * (adj_close - adj_OPEN)).rank(axis=1, pct=True)
        factor = 2.21 * part_1 + 0.7 * part_2 + 0.73 * part_3 + part_4 + 0.6 * part_5
        #factor[rolling_null(close, 200)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '037':
        # alpha037:(rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))
        corr_ = (adj_OPEN - adj_close).shift().rolling(window=200).corr(adj_close)
        factor = corr_.rank(axis=1, pct=True) + (adj_OPEN - adj_close).rank(axis=1, pct=True)
        #factor[rolling_null(close, 200)] = np.nan
        #factor[stop.notnull()] = np.nan
    elif factor_id == '038':
        # alpha038: ((-1 * rank(ts_rank(close, 10))) * rank((close / open))) 
        part_1 = rolling_rank(adj_close, 10).rank(axis=1, pct=True)
        part_2 = (close / OPEN).rank(axis=1, pct=True)
        factor = -1 * part_1 * part_2
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '039':
        # alpha039:((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 +rank(sum(returns, 250)))) 
        temp1 = adj_volume / adj_volume.rolling(window=20).mean()
        decay_linear_rank = linear_decay(temp1, 9).rank(axis=1, pct=True)
        part_1 = (adj_close.diff(7) * (1 - decay_linear_rank)).rank(axis=1, pct=True)
        part_2 = returns.rolling(window=250).sum().rank(axis=1, pct=True)
        factor = -1 * part_1 * (1 + part_2)
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '040':
        # alpha040: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10)) 
        factor = -1 * adj_high.rolling(window=10).std().rank(axis=1, pct=True) * adj_high.rolling(window=10).corr(adj_volume)
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '041':
        #(((high* low)^0.5) - vwap)
        factor = ((adj_high * adj_low) ** 0.5 - vwap * 10) / adj_close
        factor = np.abs(factor.T - factor.mean(axis=1)).T
        #factor[stop.notnull()] = np.nan
    elif factor_id == '042':
        #(rank((self.vwap - self.close)) / rank((self.vwap + self.close)))
        factor = (vwap - adj_close).rank(axis=1, pct=True) / (vwap + adj_close).rank(axis=1, pct=True)
        #factor[stop.notnull()] = np.nan
    elif factor_id == '043':
        # alpha43: (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8)) 
        part_1 = rolling_rank(adj_volume / adj_volume.rolling(window=20).mean(), 20)
        part_2 = rolling_rank(-1 * adj_close.diff(7), 8)
        factor = part_1 * part_2
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '044':
        # alpha044: (-1 * correlation(high, rank(volume), 5)) 
        factor = -1 * adj_high.rolling(window=5).corr(adj_volume.rank(axis=1, pct=True))
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '045':
        # alpha045: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *rank(correlation(sum(close, 5), sum(close, 20), 2)))) 
        part_1 = adj_close.shift(5).rolling(window=20).mean().rank(axis=1, pct=True)
        part_2 = adj_close.rolling(window=2).corr(adj_volume)
        temp1 = adj_close.rolling(window=5).sum()
        temp2 = adj_close.rolling(window=20).sum()
        part_3 = temp1.rolling(window=2).corr(temp2).rank(axis=1, pct=True)
        factor = -1 * part_1 * part_2 * part_3
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '046':
        # alpha046: ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ?(-1 * 1) : (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 :((-1 * 1) * (close - delay(close, 1)))))
        factor = -1 * adj_close.diff(1)
        temp1 = (adj_close.shift(20) - adj_close.shift(10)) / 10
        temp2 = (adj_close.shift(10) - adj_close) / 10
        cond_1 = temp1 - temp2 > 0.25
        cond_2 = temp1 - temp2 < 0
        factor[cond_2] = 1
        factor[cond_1] = -1
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '047':
        #((((rank((1 / close))* volume) / adv20)* ((high* rank((high - close))) / (sum(high, 5) / 5))) - rank((vwap - delay(vwap, 5))))
        part_1 = (1 / adj_close).rank(axis=1, pct=True) * adj_volume / adj_volume.rolling(window=20).mean()
        part_2 = adj_high * (adj_high - adj_close).rank(axis=1, pct=True) / adj_high.rolling(window=5).mean()
        part_3 = vwap.diff(5).rank(axis=1, pct=True)
        factor = part_1 * part_2 * part_3
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '048':
#         temp1 = adj_close.diff().rolling(window=250).corr(adj_close.shift().diff())
#         temp2 = temp1 * adj_close.diff() / adj_close
#         part_1 = ind_neutral(temp2, ind)
#         part_2 = ((adj_close.diff() / adj_close.shift()) ** 2).rolling(window=250).sum()
#         factor = part_1 / part_2
        #factor[rolling_null(close, 250)] = np.nan
        #factor[rolling_stop(stop, 2)] = np.nan
        factor = "id not found"
    elif factor_id == '049':
        # alpha049:(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *0.1)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))
        factor = -1 * adj_close.diff()
        temp1 = (adj_close.shift(20) - adj_close.shift(10)) / 10
        temp2 = (adj_close.shift(10) - adj_close) / 10
        factor[temp1 - temp2 < 0.1] = 1
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '050':
        #(-1* ts_max(rank(correlation(rank(volume), rank(vwap), 5)), 5))
        volume_rank = adj_volume.rank(axis=1, pct=True)
        vwap_rank = vwap.rank(axis=1, pct=True)
        corr_ = volume_rank.rolling(window=5).corr(vwap_rank)
        factor = -1 * rolling_rank(corr_.rank(axis=1, pct=True), 5)
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '051':
        # alpha051:(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *0.05)) ? 1 : ((-1 * 1) * (close - delay(close, 1)))) 
        factor = -1 * adj_close.diff()
        temp1 = (adj_close.shift(20) - adj_close.shift(10)) / 10
        temp2 = (adj_close.shift(10) - adj_close) / 10
        cond = temp1 - temp2 < -0.05
        factor[cond] = 1
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '052':
        # alpha052: ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) -sum(returns, 20)) / 220))) * ts_rank(volume, 5)) 
        part_1 = -1 * adj_low.rolling(window=5).min().diff(5)
        part_2 = (returns.rolling(window=240).sum() - returns.rolling(window=20).sum()) / 220
        factor = part_1 * part_2.rank(axis=1, pct=True) * rolling_rank(adj_volume, 5)
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '053':
        # alpha053:(-1 * delta((((close - low) - (high - close)) / (close - low)), 9)) 
        temp = ((close - low) - (high - close)) / (close - low)
        factor = -1 * temp.diff(9)
        #factor[rolling_null(close, 9)] = np.nan
        #factor[rolling_stop(stop, 9)] = np.nan
    elif factor_id == '054':
        # alpha054:((-1* ((low - close)* (open^5))) / ((low - high)* (close^5)))
        factor = -1 * (low - close) * (OPEN ** 5) / ((low - high) * (close ** 5))
        #factor[stop.notnull()] = np.nan
    elif factor_id == '055':
        # alpha055: (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low,12)))), rank(volume), 6)) 
        numerator = adj_close - adj_low.rolling(window=12).min()
        denominator = adj_high.rolling(window=12).max() - adj_low.rolling(window=12).min()
        fraction = numerator / denominator
#         fraction[rolling_stop(stop, 12)] = np.nan
        fraction_rank = fraction.rank(axis=1, pct=True)
        volume_rank = volume.replace(0, np.nan).rank(axis=1, pct=True)
        factor = -1 * fraction_rank.rolling(window=6).corr(volume_rank)
        #factor[rolling_null(close, 12)] = np.nan
        #factor[rolling_stop(stop, 12)] = np.nan
    elif factor_id == '056':
        #alpha056: (0 - (1* (rank((sum(returns, 10) / sum(sum(returns, 2), 3)))* rank((returns* cap)))))
        temp1 = returns.rolling(window=10).sum()
        temp2 = returns.rolling(window=2).sum().rolling(window=3).sum()
        part_1 = (temp1 / temp2).rank(axis=1, pct=True)
        part_2 = (returns * cap).rank(axis=1, pct=True)
        factor = -1 * part_1 * part_2
        #factor[rolling_null(close, 12)] = np.nan
        #factor[rolling_stop(stop, 12)] = np.nan
    elif factor_id == '057':
        #(0 - (1* ((close - vwap) / decay_linear(rank(ts_argmax(close, 30)), 2))))
        part_1 = adj_close - vwap
        temp = adj_close.rolling(window=30).apply(np.argmax).rank(axis=1, pct=True)
        part_2 = linear_decay(temp, 2)
        factor = -1 * part_1 / part_2
        #factor[rolling_null(close, 30)] = np.nan
        #factor[rolling_stop(stop, 30)] = np.nan
    elif factor_id == '058':        
#         temp1 = ind_neutral(vwap, ind)
#         temp2 = temp1.rolling(window=3).corr(adj_volume)
#         temp3 = linear_decay(temp2, 7)
#         factor = -1 * rolling_rank(temp3, 5)
        #factor[rolling_null(close, 7)] = np.nan
        #factor[rolling_stop(stop, 7)] = np.nan
        factor = "id not found"
    elif factor_id == '059':
#         temp1 = vwap * 0.728317 + vwap * (1 - 0.728317)
#         temp2 = ind_neutral(temp1, ind)
#         temp3 = temp2.rolling(window=4).corr(adj_volume)
#         factor = -1 * rolling_rank(linear_decay(temp3, 16), 8)
        #factor[rolling_null(close, 16)] = np.nan
        #factor[rolling_stop(stop, 16)] = np.nan
        factor = "id not found"
    elif factor_id == '060':
        # alpha060: (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) -scale(rank(ts_argmax(close, 10))))))     
        temp1 = adj_volume * ((adj_close - adj_low) - (adj_high - adj_close)) / (adj_high - adj_low)
        temp2 = temp1.rank(axis=1, pct=True)
        part_1 = (temp2.T / temp2.sum(axis=1)).T
        temp3 = adj_close.rolling(window=10).apply(np.argmax).rank(axis=1, pct=True)
        part_2 = (temp3.T / temp3.sum(axis=1)).T
        factor = -1 * (2 * part_1 - part_2)
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
    elif factor_id == '061':
        #(rank((vwap - ts_min(vwap, 16.1219))) < rank(correlation(vwap, adv180, 17.9282)))
        adv180 = adj_volume.rolling(window=180).mean()
        part_1 = (vwap - vwap.rolling(window=16).min()).rank(axis=1, pct=True)
        part_2 = vwap.rolling(window=18).corr(adv180).rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] = 0
        #factor[rolling_null(close, 180)] = np.nan
        #factor[rolling_stop(stop, 16)] = np.nan
    elif factor_id == '062':
        adv20 = adj_volume.rolling(window=20).mean()
        part_1 = vwap.rolling(window=9).corr(adv20.rolling(window=22).sum()).rank(axis=1, pct=True)
        temp1 = 2 * adj_OPEN.rank(axis=1, pct=True)
        temp2 = ((adj_high + adj_low) / 2).rank(axis=1, pct=True) + adj_high.rank(axis=1, pct=True)
        temp3 = temp1
        temp3[temp1 < temp2] = 1
        temp3[temp1 >= temp2] = 0
        part_2 = temp3.rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] = 0
        factor = -1 * factor
        #factor[rolling_null(close, 22)] = np.nan
        #factor[rolling_stop(stop, 22)] = np.nan
    elif factor_id == '063':
#         temp1 = ind_neutral(adj_close, ind).diff(2)
#         part_1 = linear_decay(temp1, 8).rank(axis=1, pct=True)
#         temp2 = vwap * 0.318108 + adj_OPEN * (1 - 0.318108)
#         temp3 = adj_volume.rolling(window=180).mean().rolling(window=37).sum()
#         temp4 = temp2.rolling(window=13).corr(temp3)
#         part_2 = linear_decay(temp4, 12).rank(axis=1, pct=True)
#         factor = -1 * (part_1 - part_2)
        #factor[rolling_null(close, 180)] = np.nan
        #factor[rolling_stop(stop, 13)] = np.nan
        factor = "id not found"
    elif factor_id == '064':
        #((rank(correlation(sum(((open* 0.178404) + (low* (1 - 0.178404))), 12.7054), sum(adv120, 12.7054), 16.6208)) < rank(delta(((((high + low) / 2)* 0.178404) + (vwap* (1 - 0.178404))), 3.69741)))* -1)
        adv120 = adj_volume.rolling(window=120).mean()
        temp1 = (adj_OPEN * 0.178404 + adj_low * (1 - 0.178404)).rolling(window=13).sum()
        temp2 = adv120.rolling(window=13).sum()
        part_1 = temp1.rolling(window=17).corr(temp2).rank(axis=1, pct=True)
        temp3 = (adj_high + adj_low) / 2 * 0.178404 + vwap * (1 - 0.178404)
        part_2 = temp3.diff(4).rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] = 0
        factor = -1 * factor
        #factor[rolling_null(close, 120)] = np.nan
        #factor[rolling_stop(stop, 16)] = np.nan
    elif factor_id == '065':
        #((rank(correlation(((open* 0.00817205) + (vwap* (1 - 0.00817205))), sum(adv60, 8.6911), 6.40374)) < rank((open - ts_min(open, 13.635))))* -1)
        adv60 = adj_volume.rolling(window=60).mean()
        temp1 = adj_OPEN * 0.00817205 + vwap * (1 - 0.00817205)
        temp2 = adv60.rolling(window=9).sum()
        part_1 = temp1.rolling(window=6).corr(temp2).rank(axis=1, pct=True)
        part_2 = (adj_OPEN - adj_OPEN.rolling(window=14).min()).rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] = 0
        factor = -1 * factor
        #factor[rolling_null(close, 60)] = np.nan
        #factor[rolling_stop(stop, 13)] = np.nan
    elif factor_id == '066':
        #((rank(decay_linear(delta(vwap, 3.51013), 7.23052)) + Ts_Rank(decay_linear(((((low* 0.96633) + (low* (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611))* -1)
        part_1 = linear_decay(vwap.diff(4), 7).rank(axis=1, pct=True)
        temp1 = (adj_low - vwap) / (adj_OPEN - (high + low) / 2)
        temp2 = linear_decay(temp1, 11)
        part_2 = rolling_rank(temp2, 7)
        factor = -1 * (part_1 + part_2)
        #factor[rolling_null(close, 11)] = np.nan
        #factor[rolling_stop(stop, 11)] = np.nan
    elif factor_id == '067':
        #((rank((high - ts_min(high, 2.14593)))^rank(correlation(IndNeutralize(vwap, IndClass.sector), IndNeutralize(adv20, IndClass.subindustry), 6.02936)))* -1)
#         part_1 = (adj_high - adj_high.rolling(window=2).min()).rank(axis=1, pct=True)
#         temp1 = ind_neutral(vwap, ind)
#         temp2 = ind_neutral(adj_volume.rolling(window=20).mean(), ind)
#         part_2 = temp1.rolling(window=6).corr(temp2).rank(axis=1, pct=True)
#         factor = -1 * (part_1 ** part_2)
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
        factor = "id not found"
    elif factor_id == '068':
        #((Ts_Rank(correlation(rank(high), rank(adv15), 8.91644), 13.9333) < rank(delta(((close* 0.518371) + (low* (1 - 0.518371))), 1.06157)))* -1)
        '''
        adv15 = adj_volume.rolling(window=15).mean()
        high_rank = adj_high.rank(axis=1, pct=True)
        adv15_rank = adv15.rank(axis=1, pct=True)
        part_1 = rolling_rank(high_rank.rolling(window=9).corr(adv15_rank), 14)
        temp = adj_close * 0.518371 + adj_low * (1 - 0.518371)
        part_2 = temp.diff(1).rank(axis=1, pct=True)
        factor = part_1.sort_values(axis=1)
        factor[part_1.sort_values(axis=1) < part_2.sort_values(axis=1)] = 1
        factor[part_1.sort_values(axis=1) >= part_2.sort_values(axis=1)] = 0
        '''
        factor = "id not found"
        #factor[rolling_null(close, 15)] = np.nan
        #factor[rolling_stop(stop, 15)] = np.nan
    elif factor_id == '069':
        #((rank(ts_max(delta(IndNeutralize(vwap, IndClass.industry), 2.72412), 4.79344))^Ts_Rank(correlation(((close* 0.490655) + (vwap* (1 - 0.490655))), adv20, 4.92416), 9.0615))* -1)
#         temp1 = ind_neutral(vwap, ind).diff(2)
#         part_1 = temp1.rolling(window=4).max().rank(axis=1, pct=True)
#         temp2 = adj_close * 0.490655 + vwap * (1 - 0.490655)
#         temp3 = adj_volume.rolling(window=20).mean()
#         part_2 = rolling_rank(temp2.rolling(window=4).corr(temp3), 9)
#         factor = -1 * (part_1 ** part_2)
        #factor[rolling_null(close, 20)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
        factor = "id not found"
    elif factor_id == '070':
        #((rank(delta(vwap, 1.29456))^Ts_Rank(correlation(IndNeutralize(close, IndClass.industry), adv50, 17.8256), 17.9171))* -1)
#         part_1 = vwap.diff(1).rank(axis=1, pct=True)
#         temp1 = ind_neutral(adj_close, ind)
#         temp2 = adj_volume.rolling(window=50).mean()
#         part_2 = rolling_rank(temp1.rolling(window=17).corr(temp2), 17)
#         factor = -1 * (part_1 ** part_2)
        #factor[rolling_null(close, 50)] = np.nan
        #factor[rolling_stop(stop, 17)] = np.nan
        factor = "id not found"
    elif factor_id == '071':
        #max(Ts_Rank(decay_linear(correlation(Ts_Rank(close, 3.43976), Ts_Rank(adv180, 12.0647), 18.0175), 4.20501), 15.6948), Ts_Rank(decay_linear((rank(((low + open) - (vwap + vwap)))^2), 16.4662), 4.4388))
        adv180 = adj_volume.rolling(window=180).mean()
        adv180_rank = rolling_rank(adv180, 12)
        close_rank = rolling_rank(adj_close, 3)
        corr_ = close_rank.rolling(window=18).corr(adv180_rank)
        part_1 = rolling_rank(linear_decay(corr_, 4), 16)
        temp = (((adj_low + adj_OPEN) - (vwap + vwap)).rank(axis=1, pct=True)) ** 2
        part_2 = rolling_rank(linear_decay(temp, 16), 4)
        factor = part_1
        factor[part_1 < part_2] = part_2
        #factor[rolling_null(close, 180)] = np.nan
        #factor[rolling_stop(stop, 18)] = np.nan
    elif factor_id == '072':
        #(rank(decay_linear(correlation(((high + low) / 2), adv40, 8.93345), 10.1519)) / rank(decay_linear(correlation(Ts_Rank(vwap, 3.72469), Ts_Rank(volume, 18.5188), 6.86671), 2.95011)))
        adv40 = adj_volume.rolling(window=40).mean()
        corr_1 = ((adj_high + adj_low) / 2).rolling(window=9).corr(adv40)
        part_1 = linear_decay(corr_1, 10).rank(axis=1, pct=True)
        corr_2 = (rolling_rank(vwap, 4).rolling(window=7).corr(rolling_rank(volume, 19)))
        part_2 = linear_decay(corr_2, 3).rank(axis=1, pct=True)
        factor = part_1 / part_2
        #factor[rolling_null(close, 40)] = np.nan
        #factor[rolling_stop(stop, 18)] = np.nan
    elif factor_id == '073':
        #(max(rank(decay_linear(delta(vwap, 4.72775), 2.91864)), Ts_Rank(decay_linear(((delta(((open* 0.147155) + (low* (1 - 0.147155))), 2.03608) / ((open* 0.147155) + (low* (1 - 0.147155))))* -1), 3.33829), 16.7411))* -1)
        part_1 = linear_decay(vwap.diff(5), 3).rank(axis=1, pct=True)
        temp1 = adj_OPEN * 0.147155 + adj_low * (1 - 0.147155)
        part_2 = rolling_rank(linear_decay(-1 * temp1.diff(2) / temp1, 3), 17)
        temp2 = adj_OPEN * 0.147155 + adj_low * (1 - 0.147155)
        factor = part_1
        factor[part_1 < part_2] = part_2
        factor = -1 * factor
        #factor[rolling_null(close, 16)] = np.nan
        #factor[rolling_stop(stop, 16)] = np.nan
    elif factor_id == '074':
        #((rank(correlation(close, sum(adv30, 37.4843), 15.1365)) < rank(correlation(rank(((high* 0.0261661) + (vwap* (1 - 0.0261661)))), rank(volume), 11.4791)))* -1)
        adv30 = adj_volume.rolling(window=30).mean()
        sum_adv30 = adv30.rolling(window=37).sum()
        corr_1 = adj_close.rolling(window=15).corr(sum_adv30)
        part_1 = corr_1.rank(axis=1, pct=True)
        temp1 = (adj_high * 0.0261661 + vwap * (1 - 0.0261661)).rank(axis=1, pct=True)
        volume_rank = adj_volume.rank(axis=1, pct=True)
        corr_2 = temp1.rolling(window=11).corr(volume_rank)
        part_2 = corr_2.rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] = 0
        factor = -1 * factor
        #factor[rolling_null(close, 67)] = np.nan
        #factor[rolling_stop(stop, 30)] = np.nan
    elif factor_id == '075':
        #(rank(correlation(vwap, volume, 4.24304)) < rank(correlation(rank(low), rank(adv50), 12.4413)))
        part_1 = vwap.rolling(window=4).corr(adj_volume).rank(axis=1, pct=True)
        low_rank = adj_low.rank(axis=1, pct=True)
        adv50_rank = adj_volume.rolling(window=50).mean().rank(axis=1, pct=True)
        part_2 = low_rank.rolling(window=12).corr(adv50_rank).rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] = 0
        #factor[rolling_null(close, 50)] = np.nan
        #factor[rolling_stop(stop, 12)] = np.nan
    elif factor_id == '076':
#         adv81 = adj_volume.rolling(window=81).mean()
#         part_1 = linear_decay(vwap.diff(1), 11).rank(axis=1, pct=True)
#         low_ind = ind_neutral(adj_low, ind)
#         corr_ = low_ind.rolling(window=8).corr(adv81)
#         part_2 = rolling_rank(linear_decay(rolling_rank(corr_, 19), 17), 19)
#         factor = part_1
#         factor[part_1 < part_2] = part_2
#         factor = -1 * factor
        #factor[rolling_null(close, 81)] = np.nan
        #factor[rolling_stop(stop, 19)] = np.nan
        factor = "id not found"
    elif factor_id == '077':
        #min(rank(decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)), rank(decay_linear(correlation(((high + low) / 2), adv40, 3.1614), 5.64125)))
        adv40 = adj_volume.rolling(window=40).mean()
        temp1 = (adj_high + adj_low) / 2 + adj_high - (vwap +adj_high)
        part_1 = linear_decay(temp1, 20).rank(axis=1, pct=True)
        temp2 = (adj_high + adj_low) / 2
        corr_ = temp2.rolling(window=3).corr(adv40)
        part_2 = linear_decay(corr_, 6).rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 > part_2] = part_2
        #factor[rolling_null(close, 43)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '078':
        #(rank(correlation(sum(((low* 0.352233) + (vwap* (1 - 0.352233))), 19.7428), sum(adv40, 19.7428), 6.83313))^rank(correlation(rank(vwap), rank(volume), 5.77492)))
        temp1 = (adj_low * 0.352233 + vwap * (1 - 0.352233)).rolling(window=20).sum()
        temp2 = adj_volume.rolling(window=40).mean().rolling(window=20).sum()
        part_1 = temp1.rolling(window=6).corr(temp2).rank(axis=1, pct=True)
        vwap_rank = vwap.rank(axis=1, pct=True)
        volume_rank = volume.rank(axis=1, pct=True)
        part_2 = vwap_rank.rolling(window=5).corr(volume_rank).rank(axis=1, pct=True)
        factor = part_1 ** part_2
        #factor[rolling_null(close, 59)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '079':
        #(rank(delta(IndNeutralize(((close* 0.60733) + (open* (1 - 0.60733))), IndClass.sector), 1.23438)) < rank(correlation(Ts_Rank(vwap, 3.60973), Ts_Rank(adv150, 9.18637), 14.6644)))
#         adv150 = adj_volume.rolling(window=150).mean()
#         temp = adj_close * 0.60733 + adj_OPEN * (1 - 0.60733)
#         part_1 = ind_neutral(temp, ind).diff(1).rank(axis=1, pct=True)
#         vwap_rank = rolling_rank(vwap, 3)
#         adv150_rank = rolling_rank(adv150, 9)
#         part_2 = vwap_rank.rolling(window=3).corr(adv150_rank).rank(axis=1, pct=True)
#         factor = part_1
#         factor[part_1 < part_2] = 1
#         factor[part_1 >= part_2] = 0
        #factor[rolling_null(close, 150)] = np.nan
        #factor[rolling_stop(stop, 9)] = np.nan
        factor = "id not found"
    elif factor_id == '080':
        #((rank(Sign(delta(IndNeutralize(((open* 0.868128) + (high* (1 - 0.868128))), IndClass.industry), 4.04545)))^Ts_Rank(correlation(high, adv10, 5.11456), 5.53756))* -1)
#         temp1 = ind_neutral(adj_OPEN * 0.868128 + adj_high * (1 - 0.868128), ind)
#         part_1 = np.sign(temp1.diff(4)).rank(axis=1, pct=True)
#         adv10 = adj_volume.rolling(window=10).mean()
#         part_2 = rolling_rank(adj_high.rolling(window=5).corr(adv10), 5)
#         factor = -1 * (part_1 ** part_2)
        #factor[rolling_null(close, 10)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
        factor = "id not found"
    elif factor_id == '081':
        #((rank(Log(product(rank((rank(correlation(vwap, sum(adv10, 49.6054), 8.47743))^4)), 14.9655))) < rank(correlation(rank(vwap), rank(volume), 5.07914)))* -1)
#         adv10 = adj_volume.rolling(window=10).mean()
#         sum_adv10 = adv10.rolling(window=49).sum()
#         corr_ = vwap.rolling(window=8).corr(sum_adv10)
#         corr_rank = corr_.rank(axis=1, pct=True)
#         part_1 = np.log(corr_rank.rolling(window=14).apply(np.prod)).rank(axis=1, pct=True)
#         vwap_rank = vwap.rank(axis=1, pct=True)
#         volume_rank = volume.rank(axis=1, pct=True)
#         part_2 = vwap_rank.rolling(window=5).corr(volume_rank).rank(axis=1, pct=True)
#         factor = part_1
#         factor[part_1 < part_2] = 1
#         factor[part_1 >= part_2] = 0
#         factor = -1 * factor
#         #factor[rolling_null(close, 59)] = np.nan
#         #factor[rolling_stop(stop, 14)] = np.nan
        factor = "id not found"
    elif factor_id == '082':
        #(min(rank(decay_linear(delta(open, 1.46063), 14.8717)), Ts_Rank(decay_linear(correlation(IndNeutralize(volume, IndClass.sector), ((open* 0.634196) + (open* (1 - 0.634196))), 17.4842), 6.92131), 13.4283))* -1)
#         part_1 = linear_decay(adj_OPEN.diff(), 14).rank(axis=1, pct=True)
#         volume_ind = ind_neutral(adj_volume, ind)
#         corr_ = volume_ind.rolling(window=17).corr(adj_OPEN)
#         part_2 = rolling_rank(linear_decay(corr_, 6), 13)
#         factor = part_1
#         factor[part_1 > part_2] = part_2
#         factor = -1 * factor
        #factor[rolling_null(close, 17)] = np.nan
        #factor[rolling_stop(stop, 17)] = np.nan
        factor = "id not found"
    elif factor_id == '083':
        #((rank(delay(((high - low) / (sum(close, 5) / 5)), 2))* rank(rank(volume))) / (((high - low) / (sum(close, 5) / 5)) / (vwap - close)))
        temp1 = (adj_high - adj_low) / adj_close.rolling(window=5).mean()
        part_1 = temp1.shift(2).rank(axis=1, pct=True) * adj_volume.rank(axis=1, pct=True)
        part_2 = temp1 / (vwap - adj_close)
        factor = part_1 / part_2
        #factor[rolling_null(close, 5)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
    elif factor_id == '084':        
        #SignedPower(Ts_Rank((vwap - ts_max(vwap, 15.3217)), 20.7127), delta(close, 4.96796))
        '''
        part_1 = rolling_rank(vwap - vwap.rolling(window=15).max(), 21)
        part_2 = adj_close.diff(5)
        factor = part_1 ** part_2
        #factor[rolling_null(close, 35)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
        '''
        factor = "id not found"
    elif factor_id == '085':
        #(rank(correlation(((high* 0.876703) + (close* (1 - 0.876703))), adv30, 9.61331))^rank(correlation(Ts_Rank(((high + low) / 2), 3.70596), Ts_Rank(volume, 10.1595), 7.11408)))
        temp1 = adj_high * 0.876703 + adj_close * (1 - 0.876703)
        adv30 = adj_volume.rolling(window=30).mean()
        corr_1 = temp1.rolling(window=10).corr(adv30)
        part_1 = corr_1.rank(axis=1, pct=True)
        hl_rank = rolling_rank((adj_high + adj_low) / 2, 4)
        volume_rank = rolling_rank(volume, 10)
        corr_2 = hl_rank.rolling(window=7).corr(volume_rank)
        part_2 = corr_2.rank(axis=1, pct=True)
        factor = part_1 ** part_2
        #factor[rolling_null(close, 30)] = np.nan
        #factor[rolling_stop(stop, 30)] = np.nan
    elif factor_id == '086':
        #((Ts_Rank(correlation(close, sum(adv20, 14.7444), 6.00049), 20.4195) < rank(((open + close) - (vwap + open))))* -1)
        adv20 = adj_volume.rolling(window=20).mean()
        sum_adv20 = adv20.rolling(window=15).sum()
        part_1 = rolling_rank(adj_close.rolling(window=6).corr(sum_adv20), 20)
        part_2 = (adj_close - vwap).rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] =0
        factor = -1 * factor
        #factor[rolling_null(close, 60)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '087':
        #(max(rank(decay_linear(delta(((close* 0.369701) + (vwap* (1 - 0.369701))), 1.91233), 2.65461)), Ts_Rank(decay_linear(abs(correlation(IndNeutralize(adv81, IndClass.industry), close, 13.4132)), 4.89768), 14.4535))* -1)
#         adv81 = adj_volume.rolling(window=81).mean()
#         temp1 = adj_close * 0.369701 + vwap * (1 - 0.369701)
#         part_1 = linear_decay(temp1.diff(1), 2).rank(axis=1, pct=True)
#         adv81_ind = ind_neutral(adv81, ind)
#         corr_ = np.abs(adv81_ind.rolling(window=13).corr(adj_close))
#         part_2 = rolling_rank(linear_decay(corr_, 4), 14)
#         factor = part_1
#         factor[part_1 < part_2] = part_2
#         factor = -1 * factor
        #factor[rolling_null(close, 108)] = np.nan
        #factor[rolling_stop(stop, 14)] = np.nan
        factor = "id not found"
    elif factor_id == '088':
        #min(rank(decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))), 8.06882)), Ts_Rank(decay_linear(correlation(Ts_Rank(close, 8.44728), Ts_Rank(adv60, 20.6966), 8.01266), 6.65053), 2.61957))
        temp1 = (adj_OPEN.rank(axis=1, pct=True) + adj_low.rank(axis=1, pct=True) - 
                 adj_high.rank(axis=1, pct=True) - adj_close.rank(axis=1, pct=True))
        part_1 = linear_decay(temp1, 8).rank(axis=1, pct=True)
        close_rank = rolling_rank(adj_close, 8)
        adv60 = adj_volume.rolling(window=60).mean()
        adv60_rank = rolling_rank(adv60, 21)
        corr_ = close_rank.rolling(window=8).corr(adv60_rank)
        part_2 = rolling_rank(linear_decay(corr_, 7), 3)
        factor = part_1
        factor[part_1 > part_2] = part_2
        #factor[rolling_null(close, 88)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '089':
        #(Ts_Rank(decay_linear(correlation(((low* 0.967285) + (low* (1 - 0.967285))), adv10, 6.94279), 5.51607), 3.79744) - Ts_Rank(decay_linear(delta(IndNeutralize(vwap, IndClass.industry), 3.48158), 10.1466), 15.3012))
#         adv10 = adj_volume.rolling(window=10).mean()
#         corr_ = adj_low.rolling(window=6).corr(adv10)
#         part_1 = rolling_rank(linear_decay(corr_, 5), 3)
#         vwap_ind = ind_neutral(vwap, ind)
#         part_2 = rolling_rank(linear_decay(vwap_ind.diff(3), 10), 15)
#         factor = part_1 - part_2
        #factor[rolling_null(close, 28)] = np.nan
        #factor[rolling_stop(stop, 10)] = np.nan
        factor = "id not found"
    elif factor_id == '090':
        #((rank((close - ts_max(close, 4.66719)))^Ts_Rank(correlation(IndNeutralize(adv40, IndClass.subindustry), low, 5.38375), 3.21856))* -1)
#         part_1 = (adj_close - adj_close.rolling(window=4).max()).rank(axis=1, pct=True)
#         adv_ind = ind_neutral(adj_volume.rolling(window=40).mean(), ind)
#         corr_ = adv_ind.rolling(window=5).corr(adj_low)
#         part_2 = rolling_rank(corr_, 3)
#         factor = -1 * (part_1 ** part_2)
        #factor[rolling_null(close, 48)] = np.nan
        #factor[rolling_stop(stop, 5)] = np.nan
        factor = "id not found"
    elif factor_id == '091':
        #((Ts_Rank(decay_linear(decay_linear(correlation(IndNeutralize(close, IndClass.industry), volume, 9.74928), 16.398), 3.83219), 4.8667) - rank(decay_linear(correlation(vwap, adv30, 4.01303), 2.6809)))* -1)
#         close_ind = ind_neutral(adj_close, ind)
#         corr_1 = close_ind.rolling(window=9).corr(adj_volume)
#         part_1 = rolling_rank(linear_decay(linear_decay(corr_1, 16), 3), 4)
#         corr_2 = (value / adj_volume).rolling(window=4).corr(adj_volume.rolling(window=30).mean())
#         part_2 = linear_decay(corr_2, 2).rank(axis=1, pct=True)
#         factor = -1 * (part_1 - part_2)
        #factor[rolling_null(close, 32)] = np.nan
        #factor[rolling_stop(stop, 32)] = np.nan
        factor = "id not found"
    elif factor_id == '092':
        #min(Ts_Rank(decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221), 18.8683), Ts_Rank(decay_linear(correlation(rank(low), rank(adv30), 7.58555), 6.94024), 6.80584))
        temp1 = (adj_high + adj_low) / 2 + adj_close
        temp2 = adj_low + adj_OPEN
        temp3 = temp1
        temp3[temp1 < temp2] = 1
        temp3[temp1 >= temp2] = 0
        part_1 = rolling_rank(linear_decay(temp3, 15), 19)
        low_rank = adj_low.rank(axis=1, pct=True)
        adv30_rank = adj_volume.rolling(window=30).mean().rank(axis=1, pct=True)
        corr_ = low_rank.rolling(window=8).corr(adv30_rank)
        part_2 = rolling_rank(linear_decay(corr_, 7), 7)
        factor = part_1
        factor[part_1 > part_2] = part_2
        #factor[rolling_null(close, 43)] = np.nan
        #factor[rolling_stop(stop, 18)] = np.nan
    elif factor_id == '093':
        #(Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.industry), adv81, 17.4193), 19.848), 7.54455) / rank(decay_linear(delta(((close* 0.524434) + (vwap* (1 - 0.524434))), 2.77377), 16.2664)))
#         ind_vwap = ind_neutral(vwap, ind)
#         corr_ = ind_vwap.rolling(window=17).corr(adj_volume.rolling(window=81).mean())
#         part_1 = rolling_rank(linear_decay(corr_, 19), 7)
#         temp1 = (adj_close * 0.52434 + vwap * (1 - 0.524434)).diff(2)
#         part_2 = linear_decay(temp1, 16).rank(axis=1, pct=True)
#         factor = part_1 / part_2
        #factor[rolling_null(close, 43)] = np.nan
        #factor[rolling_stop(stop, 19)] = np.nan
        factor = "id not found"
    elif factor_id == '094':
        #((rank((vwap - ts_min(vwap, 11.5783)))^Ts_Rank(correlation(Ts_Rank(vwap, 19.6462), Ts_Rank(adv60, 4.02992), 18.0926), 2.70756))* -1)
        part_1 = (vwap - vwap.rolling(window=12).min()).rank(axis=1, pct=True)
        vwap_rank = rolling_rank(vwap, 20)
        adv_rank = rolling_rank(adj_volume.rolling(window=60).mean(), 4)
        corr_ = vwap_rank.rolling(window=18).corr(adv_rank)
        part_2 = rolling_rank(corr_, 3)
        factor = -1 * (part_1 ** part_2)
        #factor[rolling_null(close, 82)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '095':
        #(rank((open - ts_min(open, 12.4105))) < Ts_Rank((rank(correlation(sum(((high + low) / 2), 19.1351), sum(adv40, 19.1351), 12.8742))^5), 11.7584))
        adv40 = adj_volume.rolling(window=40).mean()
        part_1 = (adj_OPEN - adj_OPEN.rolling(window=12).min()).rank(axis=1, pct=True)
        temp1 = ((adj_high + adj_low) / 2).rolling(window=19).sum()
        temp2 = adv40.rolling(window=19).sum()
        corr_ = temp1.rolling(window=13).corr(temp2)
        part_2 = rolling_rank(corr_.rank(axis=1, pct=True) ** 5, 12)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] = 0
        #factor[rolling_null(close, 71)] = np.nan
        #factor[rolling_stop(stop, 19)] = np.nan
    elif factor_id == '096':
        #(max(Ts_Rank(decay_linear(correlation(rank(vwap), rank(volume), 3.83878), 4.16783), 8.38151), Ts_Rank(decay_linear(Ts_ArgMax(correlation(Ts_Rank(close, 7.45404), Ts_Rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143))* -1)
        vwap_rank = vwap.rank(axis=1, pct=True)
        volume_rank = adj_volume.rank(axis=1, pct=True)
        corr_1 = vwap_rank.rolling(window=4).corr(volume_rank)
        part_1 = rolling_rank(linear_decay(corr_1, 4), 8)
        adv60 = adj_volume.rolling(window=60).mean()
        close_rank = rolling_rank(adj_close,7)
        adv60_rank = rolling_rank(adv60, 4)
        corr_2 = close_rank.rolling(window=4).corr(adv60_rank)
        part_2 = rolling_rank(linear_decay(corr_2.rolling(window=13).apply(np.argmax), 14), 13)
        part_1[part_1 < part_2] = part_2
        factor = -1 * part_1
        #factor[rolling_null(close, 80)] = np.nan
        #factor[rolling_stop(stop, 12)] = np.nan
    elif factor_id == '097':
        #((rank(decay_linear(delta(IndNeutralize(((low* 0.721001) + (vwap* (1 - 0.721001))), IndClass.industry), 3.3705), 20.4523)) - Ts_Rank(decay_linear(Ts_Rank(correlation(Ts_Rank(low, 7.87871), Ts_Rank(adv60, 17.255), 4.97547), 18.5925), 15.7152), 6.71659))* -1)
#         temp = adj_low * 0.721001 + vwap * (1 - 0.721001)
#         indneu_diff = ind_neutral(temp, ind).diff(3)
#         part_1 = linear_decay(indneu_diff, 20).rank(axis=1, pct=True)
#         low_rank = rolling_rank(adj_low, 7)
#         adv_rank = rolling_rank(adj_volume.rolling(window=60).mean(), 17)
#         corr_ = low_rank.rolling(4).corr(adv_rank)
#         corr_rank = rolling_rank(corr_, 18)
#         part_2 = rolling_rank(linear_decay(corr_rank, 15), 6)
#         factor = -1 * (part_1 - part_2)
        #factor[rolling_null(close, 103)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
        factor = "id not found"
    elif factor_id == '098':
#         ('000001 :', -0.56321269211700542)
#         ('000002 :', -0.94050570153693602)
#         ('000004 :', 0.21318790282597921) 
#         ('000005 :', -0.37828458106098162)
#         ('000006 :', -0.68864650470996525)

        
        #(rank(decay_linear(correlation(vwap, sum(adv5, 26.4719), 4.58418), 7.18088)) - rank(decay_linear(Ts_Rank(Ts_ArgMin(correlation(rank(open), rank(adv15), 20.8187), 8.62571), 6.95668), 8.07206)))
        
        adv5 = adj_volume.rolling(window=5).mean()   
        sum_adv5 = adv5.rolling(window=26).sum()     
        temp1 = vwap.rolling(window=5).corr(sum_adv5,)
        part_1 = linear_decay(temp1, 7).rank(axis=1, pct=True)
        
        open_rank = adj_OPEN.rank(axis=1, pct=True)
        adv_rank = adj_volume.rolling(window=15).mean().rank(axis=1, pct=True)
#         print(open_rank)
#         print(adv_rank)
        corr_ = open_rank.rolling(window=21,min_periods=None).corr(adv_rank)
#         print(corr_)
#         print(open_rank)
#         print(adv_rank)
#         print(corr_)        
        ts_argmin = corr_.rolling(window=9).apply(np.argmin)
#         print(ts_argmin)
#         print((rolling_rank(ts_argmin, 7)))
#         print(linear_decay(rolling_rank(ts_argmin, 7), 8))
        part_2 = linear_decay(rolling_rank(ts_argmin, 7), 8).rank(axis=1, pct=True)
        factor = part_1 - part_2
        
#         print(part_1)
#         print(part_2)
        
        #factor[rolling_null(close, 42)] = np.nan
        #factor[rolling_stop(stop, 20)] = np.nan
    elif factor_id == '099':
        #((rank(correlation(sum(((high + low) / 2), 19.8975), sum(adv60, 19.8975), 8.8136)) < rank(correlation(low, volume, 6.28259)))* -1)
        adv60 = adj_volume.rolling(window=60).mean()
        temp1 = ((adj_high + adj_low) / 2).rolling(window=20).sum()
        temp2 = adv60.rolling(window=20).sum()
        part_1 = temp1.rolling(window=9).corr(temp2).rank(axis=1, pct=True)
        part_2 = adj_low.rolling(window=6).corr(adj_volume).rank(axis=1, pct=True)
        factor = part_1
        factor[part_1 < part_2] = 1
        factor[part_1 >= part_2] =0
        factor = -1 * factor
        #factor[rolling_null(close, 87)] = np.nan
        #factor[rolling_stop(stop, 19)] = np.nan
    elif factor_id == '100':
#         temp1 = adj_volume * ((adj_close - adj_low) - (adj_high - adj_close)) / (adj_high - adj_low)
#         temp2 = ind_neutral(temp1.rank(axis=1, pct=True), ind)
#         part_1 = (temp2.T / temp2.sum(axis=1)).T
#         temp3 = adj_volume.rolling(window=20).mean()
#         corr_ = adj_close.rolling(window=5).corr(temp3)
#         close_rank = adj_close.rolling(30).apply(np.argmin).rank(axis=1, pct=True)
#         temp4 = ind_neutral(corr_ - close_rank, ind)
#         part_2 = (temp4.T / temp4.sum(axis=1)).T
#         factor = -1 * (1.5 * part_1 - part_2) * (adj_volume / adj_volume.rolling(window=20).mean())
        #factor[rolling_null(close, 30)] = np.nan
        #factor[rolling_stop(stop, 30)] = np.nan
        factor = "id not found"
    elif factor_id == '101':
        #((close - open) / ((high - low) + .001))
        factor = (close - OPEN) / ((high - low) + 0.001)
        #factor[stop.notnull()] = np.nan
    elif factor_id == 'vol':
#         returns = adj_close.pct_change()
#         factor = pd.DataFrame()
#         for t in returns.index:
#             not_stop = stop[:t][-21:].isnull().all(axis=0)
#             vol = adj_close[:t][-21:].pct_change()[1:].std(skipna=False)
#             vol = pd.Series(np.where(not_stop, vol, np.nan), index=not_stop.index)
#             vol.index.name = t
#             factor[t] = vol
#         factor = factor.T
        factor = "id not found"
    elif factor_id == 'PeterLynch':
#         fcf[fcf < 0] = np.nan
#         asset_debt[asset_debt < 0] = np.nan
#         factor = (close / fcf).rank(axis=1, pct=True) * asset_debt.rank(axis=1, pct=True)
        factor = "id not found"
    else:
        factor = "id not found"
    # 将涨跌停股票的因子设为na
    if no_zdt:
        increase_stop = np.round(close * 1.1, 2).shift(1)
        decrease_stop = np.round(close * 0.9, 2).shift(1)
        bool_temp = np.logical_or(close == increase_stop, decrease_stop == close)
        factor = np.where(bool_temp, np.nan, factor)
        factor = pd.DataFrame(factor, columns=close.columns, index=close.index)
    # 将st股票的因子值设为na
    if no_st:
        pass
#         factor[st.notnull()] = np.nan
    print( factor_id , ' 计算完成' )
    return factor


def factor_summary(factor, period=1):
    percentiles = np.arange(0.1, 1, 0.1)
    summary = pd.DataFrame()
    for i in range(0, len(factor.index), period):
        t = factor.index[i]
        summary[t] = factor.ix[t].dropna().describe(percentiles)
    return summary.T


def ic(factor, return_mode, period, data, by_day=False):
    close = data['close']
    OPEN = data['OPEN']
    price_adj_f = data['price_adj_f']
    adj_close = close * price_adj_f
    adj_OPEN = OPEN * price_adj_f
    if return_mode == 'close-close':
        returns = adj_close.pct_change(period).shift(-period).stack()
    elif return_mode == 'close-open':
        returns = (adj_close.shift(-(period-1)) / adj_OPEN - 1).shift(-period).stack()
    elif return_mode == 'open-open':
        returns = adj_OPEN.pct_change(period).shift(-(period + 1)).stack()
    else:
        print( 'mode must be \'close-close\', \'close-open\', \'open-open\'')
    returns.name = 'returns'
    factor = factor.stack()
    factor.name = 'factor'
    temp = pd.concat([returns, factor], axis=1).dropna(axis=0, how='any')
    if by_day:
        ic_list = []
        days = temp.index.levels[0]
        for t in days:
            ic_list.append(temp.ix[t].corr().iloc[0][1])
        ic_series = pd.Series(ic_list, index=days)
        return ic_series
    else:
        return temp.corr().iloc[0][1]


def group_analysis(factor, data, return_mode, period=1, bins=10, cut_mode='quantile'):
    close = data['close']
    OPEN = data['OPEN']
    price_adj_f = data['price_adj_f']
    adj_close = close * price_adj_f
    adj_OPEN = OPEN * price_adj_f
    if return_mode == 'close-close':
        returns = adj_close.pct_change()
    # elif return_mode == 'close-open':
    #    returns = (adj_close.shift / adj_OPEN - 1)
    elif return_mode == 'open-open':
        returns = adj_OPEN.pct_change()
    else:
        print ('mode must be \'close-close\', \'close-open\', \'open-open\'')
    days = len(factor.index)
    group_mean = pd.DataFrame()
    group_return = pd.DataFrame()
    stock_num = pd.DataFrame()
    for i in range(0, days, period):
        t = factor.index[i]
        temp = factor.ix[t].dropna()
        if cut_mode == 'quantile':
            temp.sort_values(ascending=True, inplace=True)
            temp[:] = range(len(temp))
            # 根据实际数值大小分组，可能某一个数值的股票数量太多，两个bin的边界相同
            # 这里把因子排序，并用一个从1开始的序列替代原数值，在分组较多时，可能不准确
            groups = pd.qcut(temp, bins, labels=False)
        elif cut_mode == 'interval':
            groups = pd.cut(temp, bins, labels=False)
        group_mean[t] = factor.ix[t].dropna().groupby(groups).mean()
        stock_num[t] = factor.ix[t].dropna().groupby(groups).count()
        if return_mode == 'close-close':
            period_returns = returns.ix[t:].ix[1: period+1].groupby(groups, axis=1).mean()
        elif return_mode == 'open-open':
            period_returns = returns.ix[t:].ix[2: period+2].groupby(groups, axis=1).mean()
        group_return = pd.concat([group_return, period_returns])
    a_return = returns.mean(axis=1)
    a_mean = factor.mean(axis=1)
    # group_mean.index = group_mean.index + 1
    # group_return.index = group_return.index + 1
    group_mean.index.name = 'Group'
    group_mean = group_mean.T
    group_mean['Factor Average'] = a_mean
    group_return.columns.name = 'Group'
    group_return['Simple Average'] = a_return
    stock_num.index.name = 'Group'
    stock_num = stock_num.T
    return {'group_mean': group_mean, 'group_return': group_return, 'stock_num': stock_num}


def _analysis(factor, data, return_mode, stock_number, ascending=True, period=1):
    close = data['close']
    OPEN = data['OPEN']
    price_adj_f = data['price_adj_f']
    adj_close = close * price_adj_f
    adj_OPEN = OPEN * price_adj_f
    if return_mode == 'close-close':
        returns = adj_close.pct_change(period).shift(-period)
    elif return_mode == 'close-open':
        returns = (adj_close.shift(-(period-1)) / adj_OPEN - 1).shift(-period)
    elif return_mode == 'open-open':
        returns = adj_OPEN.pct_change(period).shift(-(period + 1))
    else:
        print( 'mode must be \'close-close\', \'close-open\', \'open-open\'')
    days = len(factor.index)
    _mean = []
    _return = []
    _t = []
    stocks = pd.DataFrame()
    factors = pd.DataFrame()
    for i in range(0, days, period):
        t = factor.index[i]
        _t.append(t)
        temp = factor.ix[t].dropna()
        temp.sort_values(ascending=ascending, inplace=True)
        stock_to_hold = temp[:stock_number].index
        stocks[t] = stock_to_hold
        factors[t] = temp[stock_to_hold]
        _return.append(returns.ix[t][stock_to_hold].mean())
        _mean.append(temp[stock_to_hold].mean())
    _mean = pd.Series(_mean, index=_t, name='factor_mean')
    _return = pd.Series(_return, index=_t, name='mean_return')
    return {'factor_mean': _mean, 'mean_return': _return,
            'stocks': stocks.T, 'factors': factors.T}


