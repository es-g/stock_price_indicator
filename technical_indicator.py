import pandas as pd
import numpy as np
from finta import TA

def simple_ma(close, period=10):
    return close.rolling(window=period).mean()


def exp_ma(close, period=10):
    return close.ewm(span=period).mean()


def bollinger_bands(close, period=20):
    BB_MID = pd.Series(simple_ma(close, length=period), name='BB_MID')
    BB_UPPER = pd.Series(BB_MID + 2 * close.rolling(window=length).std(), name='BB_UPPER')
    BB_LOWER = pd.Series(BB_MID - 2 * close.rolling(window=length).std(), name='BB_LOWER')
    return pd.concat([BB_MID, BB_UPPER, BB_LOWER], axis=1)


def daily_return(close):
    daily_r = close.pct_change()
    return daily_r


def volume_log(volume):
    return volume.apply(np.log)


def rate_of_change(volume):
    return volume.pct_change()


def price_diff(close, periods=1):
    return close.diff(periods=periods)


def RSI(close, period=14):
    delta = close.diff(1)  # Price difference

    gain, loss = delta.copy(), delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    # EMA for gains and losses
    mean_gain = gain.ewm(alpha=1.0 / period).mean()
    mean_loss = loss.ewm(alpha=1.0 / period).mean()

    rs = abs(mean_gain / mean_loss)
    rsi = 100 - 100 / (1 + rs)
    return pd.Series(rsi, name="{}-day period".format(period))


def MACD(close, period_fast=12, period_slow=26, signal_period=9):
    EMA_short_term = exp_ma(close, period=period_fast)
    EMA_long_term = exp_ma(close, period=period_slow)

    MACD_vals = pd.Series(EMA_short_term - EMA_long_term, name='MACD')
    MACD_signal_line = pd.Series(MACD_vals.ewm(span=signal_period).mean(), name='MACD_signal')

    return pd.concat([MACD_vals, MACD_signal_line], axis=1)


def stochastic_oscillator(close, high, low, period=14):
    max_high = high.rolling(window=period).max()
    min_low = low.rolling(window=period).min()

    STOCHO = pd.Series((close - min_low) / (max_high - min_low) * 100,
                       name="{} period stochastic oscillator".format(period))

    return STOCHO


def accumulation_distribution(close, low, high, volume):
    # Calculate current money flow volume
    cmfv = (((close - low) - (high - close)) / (high - low)) * volume
    ADI = cmfv.cumsum()

    return ADI


def true_range(high, low, close):
    ranges = [high - low, high - close.shift(), close.shift() - low]
    TR = pd.DataFrame(ranges)
    TR = TR.abs().max()

    return TR


def average_true_range(high, low, close, period=14):
    TR = true_range(high=high, low=low, close=close)

    return TR.rolling(window=period).mean()

