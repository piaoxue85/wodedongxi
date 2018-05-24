'''
Created on 2017年9月27日

@author: moonlit
'''
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from numpy import abs 
from numpy import log
from numpy import sign

# 计算alpha时会使用的函数

def signedpower(x,a):
    return x**a 

def ts_sum(df,window=10):
    window = int(round(window))
    return df.rolling(window).sum()

def sum(df,window=10):
    window = int(round(window))
    return df.rolling(window).sum()

def sma(df,window=10):
    return df.rolling(window).mean()

def stddev(df,window=10):
    return df.rolling(window).std()

def correlation(x,y,window=10):
    return x.rolling(int(round(window,0))).corr(y)

def covariance(x,y,window=10):
    return x.rolling(window).cov(y)

def rolling_rank(na):
    return rankdata(na)[-1]

def ts_rank(x,window=10):
    return x.rolling(int(round(window,0))).apply(rolling_rank)

def rolling_prod(na):
    return na.prod(na)
    
def product(df,window=10):
    return df.rolling(window).apply(rolling_prod)

def ts_min(df,window=10):
    window = int(round(window))
    return df.rolling(window).min()
    
def ts_max(df,window=10):
    window = int(round(window))
    return df.rolling(window).max()

def min(x,y):
    x[x > y] = y
    return x
    
def max(x , y):
    x[x < y] = y
    return x

def delta(df,period=1):
    return df.diff(period)
    
def delay(df,period=1):
    return df.shift(period)

def rank(df):
    return df.rank(axis=1,pct=True)

def scale(df,k=1):
    return df.mul(k).div(np.abs(df).sum())

def ts_argmax(df,window=10):
    window = int(round(window))
    return df.rolling(window).apply(np.argmax)+1

def ts_argmin(df,window=10):
    window = int(round(window))
    return df.rolling(window).apply(np.argmin)+1
    
def decay_linear(df, period=10):
    """
    Linear weighted moving average implementation.
    :param df: a pandas DataFrame.
    :param period: the LWMA period
    :return: a pandas DataFrame with the LWMA.
    """
    # Clean data
    if df.isnull().values.any():
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        df.fillna(value=0, inplace=True)
    
    period = int(round(period,0))
    
    na_lwma = np.zeros_like(df)
    na_lwma[:period, :] = df.ix[:period, :]
    na_series = df.as_matrix()

    divisor = period * (period + 1) / 2
    y = (np.arange(period) + 1) * 1.0 / divisor
    # Estimate the actual lwma with the actual close.
    # The backtest engine should assure to be snooping bias free.
    for row in range(period - 1, df.shape[0]):
        x = na_series[row - period + 1: row + 1, :]
        na_lwma[row, :] = (np.dot(x.T, y))
    return pd.DataFrame(na_lwma, index=df.index, columns=df.columns)

# def linear_decay(data, window=10):
#     result = pd.DataFrame(np.nan, index=data.index, columns=data.columns)
#     weight = np.arange(window) + 1.
#     weight = weight / weight.sum()
#     for i in range(window, data.shape[0]):
#         t = data.index[i]
#         result.ix[t, :] = data[i-window:i].T.dot(weight)
#     return result

# 定义计算alpha值的类
class Alphas(object):
    def __init__(self, pn_data):
        """
        :传入参数 pn_data: pandas.Panel
        """
        # 获取历史数据
        self.open    = pn_data['open']
        self.high    = pn_data['high']
        self.low     = pn_data['low']
        self.close   = pn_data['close']
        self.volume  = pn_data['volume']
        self.value   = pn_data['value']
        self.returns = pn_data['return']
        self.cap     = pn_data["cap"]
        
        self.vwap    = self.value/self.volume
        self.adv20   = sma(self.volume, 20)
        self.adv180  = sma(self.volume, 180)
        self.adv40   = sma(self.volume, 40)
        self.adv30   = sma(self.volume, 30)        
        self.adv60   = sma(self.volume, 60)
        self.adv5    = sma(self.volume, 5)
        self.adv15   = sma(self.volume, 15)
    
    #   每个因子的计算公式：
    #   alpha001:(rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) -0.5)     
    def alpha001(self):
        inner = self.close
        inner[self.returns < 0] = stddev(self.returns, 20)
        return rank(ts_argmax(inner ** 2, 5))
#         return (rank(ts_argmax(signedpower((stddev(self.returns, 20) if (self.returns < 0) else self.close), 2.), 5)) -0.5) 
        
        
    #  alpha002:(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))     
    def alpha002(self):
        df = -1 * correlation(rank(delta(log(self.volume), 2)), rank((self.close - self.open) / self.open), 6)
        return df.replace([-np.inf, np.inf], 0).fillna(value=0)

    # alpha003:(-1 * correlation(rank(open), rank(volume), 10))  
    
    def alpha003(self):
        df = -1 * correlation(rank(self.open), rank(self.volume), 10)
        return df.replace([-np.inf, np.inf], 0).fillna(value=0)
    
    # alpha004: (-1 * ts_rank(rank(low), 9)) 
    
    def alpha004(self):
        return -1 * ts_rank(rank(self.low), 9)
    
    #(rank((open - (sum(vwap, 10) / 10)))*(-1*abs(rank((close - vwap)))))
    def alpha005(self):
        return (rank((self.open - (ts_sum(self.vwap, 10) / 10)))*(-1*abs(rank((self.close - self.vwap)))))
    
    #  alpha006: (-1 * correlation(open, volume, 10)) 
    
    def alpha006(self):
        df = -1 * correlation(self.open, self.volume, 10)
        return df.replace([-np.inf, np.inf], 0).fillna(value=0)

    # alpha007: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1* 1)) 

    def alpha007(self):
        #adv20 = sma(self.volume, 20)
        alpha = -1 * ts_rank(abs(delta(self.close, 7)), 60) * sign(delta(self.close, 7))
        alpha[self.adv20 >= self.volume] = -1
        return alpha
    
    # alpha008: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)),10)))) 
    
    def alpha008(self):
        return -1 * (rank(((ts_sum(self.open, 5) * ts_sum(self.returns, 5)) - delay((ts_sum(self.open, 5) * ts_sum(self.returns, 5)), 10))))
    
    # alpha009:((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ?delta(close, 1) : (-1 * delta(close, 1)))) 
    
    def alpha009(self):
        delta_close = delta(self.close, 1)
        cond_1 = ts_min(delta_close, 5) > 0
        cond_2 = ts_max(delta_close, 5) < 0
        alpha = -1 * delta_close
        alpha[cond_1 | cond_2] = delta_close
        return alpha
    
    # alpha010: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0)? delta(close, 1) : (-1 * delta(close, 1)))))     
    def alpha010(self):
        delta_close = delta(self.close, 1)
        cond_1 = ts_min(delta_close, 4) > 0
        cond_2 = ts_max(delta_close, 4) < 0
        alpha = -1 * delta_close
        alpha[cond_1 | cond_2] = delta_close
        return alpha
    
    #((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3)))*rank(delta(volume, 3)))
    def alpha011(self):
        return ((rank(ts_max((self.vwap - self.close), 3)) + rank(ts_min((self.vwap - self.close), 3)))*rank(delta(self.volume, 3)))
    
    #  alpha012:(sign(delta(volume, 1)) * (-1 * delta(close, 1))) 
    
    def alpha012(self):
        return sign(delta(self.volume, 1)) * (-1 * delta(self.close, 1))
    
    # alpha013:(-1 * rank(covariance(rank(close), rank(volume), 5))) 
    
    def alpha013(self):
        return -1 * rank(covariance(rank(self.close), rank(self.volume), 5))

    #  alpha014:((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10)) 
    
    def alpha014(self):
        df = correlation(self.open, self.volume, 10)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * rank(delta(self.returns, 3)) * df

    # alpha015:(-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3)) 
    
    def alpha015(self):
        df = correlation(rank(self.high), rank(self.volume), 3)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * ts_sum(rank(df), 3)

    #  alpha016:(-1 * rank(covariance(rank(high), rank(volume), 5))) 
    
    def alpha016(self):
        return -1 * rank(covariance(rank(self.high), rank(self.volume), 5))

    # alpha017: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) *rank(ts_rank((volume / adv20), 5))) 

    def alpha017(self):
        adv20 = sma(self.volume, 20)
        return -1 * (rank(ts_rank(self.close, 10)) *
                     rank(delta(delta(self.close, 1), 1)) *
                     rank(ts_rank((self.volume / adv20), 5)))
    
    # alpha018: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open,10)))) 
        
    def alpha018(self):
        df = correlation(self.close, self.open, 10)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * (rank((stddev(abs((self.close - self.open)), 5) + (self.close - self.open)) +
                          df))

    #  alpha019:((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns,250)))))

    def alpha019(self):
        return ((-1 * sign((self.close - delay(self.close, 7)) + delta(self.close, 7))) *
                (1 + rank(1 + ts_sum(self.returns, 250))))

    # alpha020: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open -delay(low, 1))))

    def alpha020(self):
        return -1 * (rank(self.open - delay(self.high, 1)) *
                     rank(self.open - delay(self.close, 1)) *
                     rank(self.open - delay(self.low, 1)))

    # alpha021: ((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ? (-1 * 1) : (((sum(close,2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume /adv20) == 1)) ? 1 : (-1 * 1)))) 
    def c_alpha021(self):
        cond_1 = sma(self.close, 8) + stddev(self.close, 8) < sma(self.close, 2)
        cond_2 = sma(self.volume, 20) / self.volume < 1
        alpha = pd.DataFrame(np.ones_like(self.close), index=self.close.index,
                             columns=self.close.columns)
        alpha[cond_1 | cond_2] = -1
        return alpha

    # alpha022:(-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20)))) 

    def alpha022(self):
        df = correlation(self.high, self.volume, 5)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * delta(df, 5) * rank(stddev(self.close, 20))

    # alpha023: (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0) 

    def alpha023(self):
        cond = sma(self.high, 20) < self.high
        alpha = pd.DataFrame(np.zeros_like(self.close), index=self.close.index,
                             columns=self.close.columns)
        alpha[cond] = -1 * delta(self.high, 2)
        return alpha

    # alpha024: ((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) ||((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close,100))) : (-1 * delta(close, 3)))  

    def alpha024(self):
        cond = delta(sma(self.close, 100), 100) / delay(self.close, 100) <= 0.05
        alpha = -1 * delta(self.close, 3)
        alpha[cond] = -1 * (self.close - ts_min(self.close, 100))
        return alpha
    
    #rank(((((-1* returns)* adv20)* vwap)* (high - close)))
    def alpha025(self):
        return rank(((((-1* self.returns)* self.adv20)* self.vwap)* (self.high - self.close)))
    
    
    #   alpha026:(-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3)) 
    def alpha026(self):
        df = correlation(ts_rank(self.volume, 5), ts_rank(self.high, 5), 5)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * ts_max(df, 3)
    
    #((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1* 1) : 1)
    #一个Series：index为成分股代码，values为1或-1，满足条件为-1，不满足为1
    #def c_alpha027(self):

    # alpha028:scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))     
    def alpha028(self):
        adv20 = sma(self.volume, 20)
        df = correlation(adv20, self.low, 5)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return scale(((df + ((self.high + self.low) / 2)) - self.close))
    
    # alpha029:(min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1),5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5)) 
    def alpha029(self):
        return (ts_min(rank(rank(scale(log(ts_sum(rank(rank(-1 * rank(delta((self.close - 1), 5)))), 2))))), 5) +
                ts_rank(delay((-1 * self.returns), 6), 5))
    
    # alpha0230:(((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) +sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20)) 
    
    def alpha030(self):
        delta_close = delta(self.close, 1)
        inner = sign(delta_close) + sign(delay(delta_close, 1)) + sign(delay(delta_close, 2))
        return ((1.0 - rank(inner)) * ts_sum(self.volume, 5)) / ts_sum(self.volume, 20)

    # alpha031:((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 *delta(close, 3)))) + sign(scale(correlation(adv20, low, 12)))) 
    def alpha031(self):
        adv20 = sma(self.volume, 20)
        df = correlation(adv20, self.low, 12)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(self.close, 10)))), 10)))) + rank((-1 * delta(self.close, 3)))) + sign(scale(df)))

    #(scale(((sum(close, 7) / 7) - close)) + (20* scale(correlation(vwap, delay(close, 5), 230))))
    def alpha032(self):
        return (scale(((ts_sum(self.close, 7) / 7) - self.close)) + (20* scale(correlation(self.vwap, delay(self.close, 5), 230))))
    
    # alpha033: rank((-1 * ((1 - (open / close))^1)))     
    def alpha033(self):
        return rank(-1 + (self.open / self.close))
    
    # alpha034: rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1))))) 
    
    def alpha034(self):
        inner = stddev(self.returns, 2) / stddev(self.returns, 5)
        inner = inner.replace([-np.inf, np.inf], 1).fillna(value=1)
        return rank(2 - rank(inner) - rank(delta(self.close, 1)))
    
    # alpha035:((ts_rank(volume, 32) * (1 - ts_rank(((close + high) - low), 16))) * (1 -ts_rank(returns, 32))) 
    
    def alpha035(self):
        return ((ts_rank(self.volume, 32) *
                 (1 - ts_rank(self.close + self.high - self.low, 16))) *
                (1 - ts_rank(self.returns, 32)))
    
    #(((((2.21* rank(correlation((close - open), delay(volume, 1), 15))) + (0.7* rank((open - close)))) + (0.73* rank(ts_rank(delay((-1* returns), 6), 5)))) + rank(abs(correlation(vwap, adv20, 6)))) + (0.6* rank((((sum(close, 200) / 200) - open)* (close - open)))))
    def alpha036(self):
        return (((((2.21* rank(correlation((self.close - self.open), delay(self.volume, 1), 15))) + (0.7* rank((self.open - self.close)))) + (0.73* rank(ts_rank(delay((-1* self.returns), 6), 5)))) + rank(abs(correlation(self.vwap, self.adv20, 6)))) + (0.6* rank((((sum(self.close, 200) / 200) - self.open)* (self.close - self.open)))))
    
    # alpha037:(rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))     
    def alpha037(self):
        return rank(correlation(delay(self.open - self.close, 1), self.close, 200)) + rank(self.open - self.close)
    
    # alpha038: ((-1 * rank(ts_rank(close, 10))) * rank((close / open))) 
    
    def alpha038(self):
        inner = self.close / self.open
        inner = inner.replace([-np.inf, np.inf], 1).fillna(value=1)
        return -1 * rank(ts_rank(self.open, 10)) * rank(inner)

    # alpha039:((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 +rank(sum(returns, 250)))) 

    def alpha039(self):
        adv20 = sma(self.volume, 20)
        return ((-1 * rank(delta(self.close, 7) * (1 - rank(decay_linear(self.volume / adv20, 9))))) *
                (1 + rank(ts_sum(self.returns, 250))))
    
    # alpha040: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10)) 
    
    def alpha040(self):
        return -1 * rank(stddev(self.high, 10)) * correlation(self.high, self.volume, 10)

    #(((high* low)^0.5) - vwap)
    def alpha041(self):
        return (((self.high* self.low)**0.5) - self.vwap)
    
    def alpha042(self):
        return (rank((self.vwap - self.close)) / rank((self.vwap + self.close)))
    
    # alpha43: (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8)) 
    def alpha043(self):
        adv20 = sma(self.volume, 20)
        return ts_rank(self.volume / adv20, 20) * ts_rank((-1 * delta(self.close, 7)), 8)

    # alpha044: (-1 * correlation(high, rank(volume), 5)) 

    def alpha044(self):
        df = correlation(self.high, rank(self.volume), 5)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * df
    
    # alpha045: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) *rank(correlation(sum(close, 5), sum(close, 20), 2)))) 
    
    def alpha045(self):
        df = correlation(self.close, self.volume, 2)
        df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
        return -1 * (rank(sma(delay(self.close, 5), 20)) * df *
                     rank(correlation(ts_sum(self.close, 5), ts_sum(self.close, 20), 2)))

    # alpha046: ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ?(-1 * 1) : (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 :((-1 * 1) * (close - delay(close, 1))))) 

    def c_alpha046(self):
        inner = ((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10)
        alpha = (-1 * delta(self.close))
        alpha[inner < 0] = 1
        alpha[inner > 0.25] = -1
        return alpha
    
    #((((rank((1 / close))* volume) / adv20)* ((high* rank((high - close))) / (sum(high, 5) / 5))) - rank((vwap - delay(vwap, 5))))
    def alpha047(self):
        return ((((rank((1 / self.close))* self.volume) / self.adv20)* ((self.high* rank((self.high - self.close))) / (ts_sum(self.high, 5) / 5))) - rank((self.vwap - delay(self.vwap, 5))))
    
    # alpha049:(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *0.1)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))
    def alpha049(self):
        inner = (((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10))
        alpha = (-1 * delta(self.close))
        alpha[inner < -0.1] = 1
        return alpha
    
    #(-1* ts_max(rank(correlation(rank(volume), rank(vwap), 5)), 5))
    def alpha050(self):
        return (-1* ts_max(rank(correlation(rank(self.volume), rank(self.vwap), 5)), 5))
    
    # alpha051:(((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 *0.05)) ? 1 : ((-1 * 1) * (close - delay(close, 1)))) 
    
    def alpha051(self):
        inner = (((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10))
        alpha = (-1 * delta(self.close))
        alpha[inner < -0.05] = 1
        return alpha

    # alpha052: ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) -sum(returns, 20)) / 220))) * ts_rank(volume, 5)) 

    def alpha052(self):
        return (((-1 * delta(ts_min(self.low, 5), 5)) *
                 rank(((ts_sum(self.returns, 240) - ts_sum(self.returns, 20)) / 220))) * ts_rank(self.volume, 5))

    # alpha053:(-1 * delta((((close - low) - (high - close)) / (close - low)), 9)) 

    def alpha053(self):
        inner = (self.close - self.low).replace(0, 0.0001)
        return -1 * delta((((self.close - self.low) - (self.high - self.close)) / inner), 9)

    # alpha054:((-1* ((low - close)* (open^5))) / ((low - high)* (close^5)))
    def alpha054(self):
        inner = (self.low - self.high).replace(0, -0.0001)
        return -1 * (self.low - self.close) * (self.open ** 5) / (inner * (self.close ** 5))
        
    # alpha055: (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low,12)))), rank(volume), 6)) 
    
    def alpha055(self):
        divisor = (ts_max(self.high, 12) - ts_min(self.low, 12)).replace(0, 0.0001)
        inner = (self.close - ts_min(self.low, 12)) / (divisor)
        df = correlation(rank(inner), rank(self.volume), 6)
        return -1 * df.replace([-np.inf, np.inf], 0).fillna(value=0)
    
    #alpha056: (0 - (1* (rank((sum(returns, 10) / sum(sum(returns, 2), 3)))* rank((returns* cap)))))
    
    def alpha056(self):
        res = (0-(1*(rank((ts_sum(self.returns,10)/ts_sum(ts_sum(self.returns,2),3)))*rank((self.returns*self.cap)))))
        return res  
    
    #(0 - (1* ((close - vwap) / decay_linear(rank(ts_argmax(close, 30)), 2))))
    def alpha057(self):
        return (0 - (1* ((self.close - self.vwap) / decay_linear(rank(ts_argmax(self.close, 30)), 2))))
    
    # alpha060: (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) -scale(rank(ts_argmax(close, 10))))))     
    def alpha060(self):
        divisor = (self.high - self.low).replace(0, 0.0001)
        inner = ((self.close - self.low) - (self.high - self.close)) * self.volume / divisor
        return - ((2 * scale(rank(inner))) - scale(rank(ts_argmax(self.close, 10))))
    
    #(rank((vwap - ts_min(vwap, 16.1219))) < rank(correlation(vwap, adv180, 17.9282)))
    def c_alpha061(self):
        return (rank((self.vwap - ts_min(self.vwap, 16.1219))) < rank(correlation(self.vwap, self.adv180, 17.9282)))
    
    #((rank(correlation(vwap, sum(adv20, 22.4101), 9.91009)) < rank(((rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high)))))*-1)
    def c_alpha062(self):
        return ((rank(correlation(self.vwap, ts_sum(self.adv20, 22.4101), 9.91009)) < rank(((rank(self.open) + rank(self.open)) < (rank(((self.high + self.low) / 2)) + rank(self.high)))))*-1)
        
    #((rank(decay_linear(delta(vwap, 3.51013), 7.23052)) + ts_rank(decay_linear(((((low* 0.96633) + (low* (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611))* -1)
    def alpha066(self):
        res =((rank(decay_linear(delta(self.vwap, 3.51013), 7.23052)) + ts_rank(decay_linear(((((self.low* 0.96633) + (self.low* (1 - 0.96633))) - self.vwap) / (self.open - ((self.high + self.low) / 2))), 11.4157), 6.72611))* -1)
        return res
    
    #max(ts_rank(decay_linear(correlation(ts_rank(close, 3.43976), ts_rank(adv180, 12.0647), 18.0175), 4.20501), 15.6948), ts_rank(decay_linear((rank(((low + open) - (vwap + vwap)))^2), 16.4662), 4.4388))
    def alpha071(self):
        return max(ts_rank(decay_linear(correlation(ts_rank(self.close, 3.43976), ts_rank(self.adv180, 12.0647), 18.0175), 4.20501), 15.6948), ts_rank(decay_linear((rank(((self.low + self.open) - (self.vwap + self.vwap)))**2), 16.4662), 4.4388))
    
    #(rank(decay_linear(correlation(((high + low) / 2), adv40, 8.93345), 10.1519)) / rank(decay_linear(correlation(ts_rank(vwap, 3.72469), ts_rank(volume, 18.5188), 6.86671), 2.95011)))
    def alpha072(self):
        return (rank(decay_linear(correlation(((self.high + self.low) / 2), self.adv40, 8.93345), 10.1519)) / rank(decay_linear(correlation(ts_rank(self.vwap, 3.72469), ts_rank(self.volume, 18.5188), 6.86671), 2.95011)))
    
    #(max(rank(decay_linear(delta(vwap, 4.72775), 2.91864)), ts_rank(decay_linear(((delta(((open* 0.147155) + (low* (1 - 0.147155))), 2.03608) / ((open* 0.147155) + (low* (1 - 0.147155))))* -1), 3.33829), 16.7411))* -1)
    def alpha073(self):
        return (max(rank(decay_linear(delta(self.vwap, 4.72775), 2.91864)), ts_rank(decay_linear(((delta(((self.open* 0.147155) + (self.low* (1 - 0.147155))), 2.03608) / ((self.open* 0.147155) + (self.low* (1 - 0.147155))))* -1), 3.33829), 16.7411))* -1)
    
    #min(rank(decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)), rank(decay_linear(correlation(((high + low) / 2), adv40, 3.1614), 5.64125)))
    def alpha077(self):
        return min(rank(decay_linear(((((self.high + self.low) / 2) + self.high) - (self.vwap + self.high)), 20.0451)), rank(decay_linear(correlation(((self.high + self.low) / 2), self.adv40, 3.1614), 5.64125)))
   
    #(rank(correlation(sum(((low* 0.352233) + (vwap* (1 - 0.352233))), 19.7428), sum(adv40, 19.7428), 6.83313))^rank(correlation(rank(vwap), rank(volume), 5.77492)))
    def alpha078(self):
        return (rank(correlation(ts_sum(((self.low* 0.352233) + (self.vwap* (1 - 0.352233))), 19.7428), sum(self.adv40, 19.7428), 6.83313))**rank(correlation(rank(self.vwap), rank(self.volume), 5.77492)))
    
    #((rank(delay(((high - low) / (sum(close, 5) / 5)), 2))* rank(rank(volume))) / (((high - low) / (sum(close, 5) / 5)) / (vwap - close)))
    def alpha083(self):
        return ((rank(delay(((self.high - self.low) / (ts_sum(self.close, 5) / 5)), 2))* rank(rank(self.volume))) / (((self.high - self.low) / (sum(self.close, 5) / 5)) / (self.vwap - self.close)))
    
    
    #SignedPower(ts_rank((vwap - ts_max(vwap, 15.3217)), 20.7127), delta(close, 4.96796))
    def alpha084(self):
        return signedpower(ts_rank((self.vwap - ts_max(self.vwap, 15.3217)), 20.7127), delta(self.close, 4.96796))
    
    #(rank(correlation(((high* 0.876703) + (close* (1 - 0.876703))), adv30, 9.61331))^rank(correlation(ts_rank(((high + low) / 2), 3.70596), ts_rank(volume, 10.1595), 7.11408)))
    def alpha085(self):
        return (rank(correlation(((self.high* 0.876703) + (self.close* (1 - 0.876703))), self.adv30, 9.61331))**rank(correlation(ts_rank(((self.high + self.low) / 2), 3.70596), ts_rank(self.volume, 10.1595), 7.11408)))
    
    #min(rank(decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))), 8.06882)), ts_rank(decay_linear(correlation(ts_rank(close, 8.44728), ts_rank(adv60, 20.6966), 8.01266), 6.65053), 2.61957))
    def alpha088(self):
        return min(rank(decay_linear(((rank(self.open) + rank(self.low)) - (rank(self.high) + rank(self.close))), 8.06882)), ts_rank(decay_linear(correlation(ts_rank(self.close, 8.44728), ts_rank(self.adv60, 20.6966), 8.01266), 6.65053), 2.61957))
    
    #min(ts_rank(decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221), 18.8683), ts_rank(decay_linear(correlation(rank(low), rank(adv30), 7.58555), 6.94024), 6.80584))
    def alpha092(self):
        return min(ts_rank(decay_linear(((((self.high + self.low) / 2) + self.close) < (self.low + self.open)), 14.7221), 18.8683), ts_rank(decay_linear(correlation(rank(self.low), rank(self.adv30), 7.58555), 6.94024), 6.80584))

    #((rank((vwap - ts_min(vwap, 11.5783)))^ts_rank(correlation(ts_rank(vwap, 19.6462), ts_rank(adv60, 4.02992), 18.0926), 2.70756))* -1)
    def alpha094(self):
        return ((rank((self.vwap - ts_min(self.vwap, 11.5783)))**ts_rank(correlation(ts_rank(self.vwap, 19.6462), ts_rank(self.adv60, 4.02992), 18.0926), 2.70756))* -1)
    
    #(rank((open - ts_min(open, 12.4105))) < ts_rank((rank(correlation(sum(((high + low) / 2), 19.1351), sum(adv40, 19.1351), 12.8742))^5), 11.7584))
    def c_alpha095(self):
        return (rank((self.open - ts_min(self.open, 12.4105))) < ts_rank((rank(correlation(sum(((self.high + self.low) / 2), 19.1351), sum(self.adv40, 19.1351), 12.8742))**5), 11.7584))
       
    #(max(ts_rank(decay_linear(correlation(rank(vwap), rank(volume), 3.83878), 4.16783), 8.38151), ts_rank(decay_linear(Ts_ArgMax(correlation(ts_rank(close, 7.45404), ts_rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143))* -1)
    def alpha096(self):
        return (max(ts_rank(decay_linear(correlation(rank(self.vwap), rank(self.volume), 3.83878), 4.16783), 8.38151), ts_rank(decay_linear(ts_argmax(correlation(ts_rank(self.close, 7.45404), ts_rank(self.adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143))* -1)
        
    #(rank(decay_linear(correlation(vwap, sum(adv5, 26.4719), 4.58418), 7.18088)) - rank(decay_linear(Ts_Rank(Ts_ArgMin(correlation(rank(open), rank(adv15), 20.8187), 8.62571), 6.95668), 8.07206)))
    def alpha098(self):
        return (rank(decay_linear(correlation(self.vwap, sum(self.adv5, 26.4719), 4.58418), 7.18088)) - rank(decay_linear(ts_rank(ts_argmin(correlation(rank(self.open), rank(self.adv15), 20.8187), 8.62571), 6.95668), 8.07206)))
          
    #((close - open) / ((high - low) + .001))  
    def alpha101(self):
        return ((self.close - self.open) / ((self.high - self.low) + .001))
    
    def alpha(self,alpha_id=0):
        if alpha_id ==   1 : return self.alpha001()
        if alpha_id ==   2 : return self.alpha002()
        if alpha_id ==   3 : return self.alpha003()
        if alpha_id ==   4 : return self.alpha004()
        if alpha_id ==   5 : return self.alpha005()
        if alpha_id ==   6 : return self.alpha006()
        if alpha_id ==   7 : return self.alpha007()
        if alpha_id ==   8 : return self.alpha008()
        if alpha_id ==   9 : return self.alpha009()
        if alpha_id ==  10 : return self.alpha010()
        if alpha_id ==  11 : return self.alpha011()
        if alpha_id ==  12 : return self.alpha012()
        if alpha_id ==  13 : return self.alpha013()
        if alpha_id ==  14 : return self.alpha014()
        if alpha_id ==  15 : return self.alpha015()
        if alpha_id ==  16 : return self.alpha016()
        if alpha_id ==  17 : return self.alpha017()
        if alpha_id ==  18 : return self.alpha018()
        if alpha_id ==  19 : return self.alpha019()
        if alpha_id ==  20 : return self.alpha020()
        if alpha_id ==  22 : return self.alpha022()
        if alpha_id ==  23 : return self.alpha023()
        if alpha_id ==  24 : return self.alpha024()
        if alpha_id ==  25 : return self.alpha025()
        if alpha_id ==  26 : return self.alpha026()
        if alpha_id ==  28 : return self.alpha028()
        if alpha_id ==  29 : return self.alpha029()
        if alpha_id ==  30 : return self.alpha030()
        if alpha_id ==  31 : return self.alpha031()
        if alpha_id ==  32 : return self.alpha032()
        if alpha_id ==  33 : return self.alpha033()
        if alpha_id ==  34 : return self.alpha034()
        if alpha_id ==  35 : return self.alpha035()
        if alpha_id ==  36 : return self.alpha036()
        if alpha_id ==  37 : return self.alpha037()
        if alpha_id ==  38 : return self.alpha038()
        if alpha_id ==  39 : return self.alpha039()
        if alpha_id ==  40 : return self.alpha040()
        if alpha_id ==  41 : return self.alpha041()
        if alpha_id ==  42 : return self.alpha042()
        if alpha_id ==  43 : return self.alpha043()
        if alpha_id ==  44 : return self.alpha044()
        if alpha_id ==  45 : return self.alpha045()
        if alpha_id ==  47 : return self.alpha047()
        if alpha_id ==  49 : return self.alpha049()
        if alpha_id ==  50 : return self.alpha050()
        if alpha_id ==  51 : return self.alpha051()
        if alpha_id ==  52 : return self.alpha052()
        if alpha_id ==  53 : return self.alpha053()
        if alpha_id ==  54 : return self.alpha054()
        if alpha_id ==  55 : return self.alpha055()
        if alpha_id ==  56 : return self.alpha056()
        if alpha_id ==  57 : return self.alpha057()
        if alpha_id ==  60 : return self.alpha060()
        if alpha_id ==  66 : return self.alpha066()
        if alpha_id ==  71 : return self.alpha071()
        if alpha_id ==  72 : return self.alpha072()
        if alpha_id ==  73 : return self.alpha073()
        if alpha_id ==  77 : return self.alpha077()
        if alpha_id ==  78 : return self.alpha078()
        if alpha_id ==  83 : return self.alpha083()
        if alpha_id ==  84 : return self.alpha084()
        if alpha_id ==  85 : return self.alpha085()
        if alpha_id ==  88 : return self.alpha088()
        if alpha_id ==  92 : return self.alpha092()
        if alpha_id ==  94 : return self.alpha094()
        if alpha_id ==  96 : return self.alpha096()
        if alpha_id ==  98 : return self.alpha098()
        if alpha_id == 101 : return self.alpha101()
        
        return "id not found"