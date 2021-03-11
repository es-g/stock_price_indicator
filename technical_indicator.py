import pandas as pd
import numpy as np


def simple_ma(close, length=10):
    return close.rolling(window=length).mean()


def exp_ma(close, length=10):
    return close.ewm(span=length).mean()


def bollinger_bands(close, length=20):
    BB_MID = pd.Series(simple_ma(close, length=length), name='BB_MID')
    BB_UPPER = pd.Series(BB_MID + 2*close.rolling(window=length).std(), name='BB_UPPER')
    BB_LOWER = pd.Series(BB_MID - 2*close.rolling(window=length).std(), name='BB_LOWER')
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


