import pandas as pd
import numpy as np


def simple_ma(close, period=10):
    return close.rolling(window=period).mean()


def exp_ma(close, period=10):
    return close.ewm(span=period).mean()


def bollinger_bands(close, period=20):
    BB_MID = pd.Series(simple_ma(close, period=period), name='BB_MID')
    BB_UPPER = pd.Series(BB_MID + 2 * close.rolling(window=period).std(), name='BB_UPPER')
    BB_LOWER = pd.Series(BB_MID - 2 * close.rolling(window=period).std(), name='BB_LOWER')
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
    """
    Calculates Relative Strength Index.
    This indicator measures the magnitude of recent price changes.
    Commonly used in technical analysis to evaluate overbought or oversold conditions in the price of a stock.
    A stock is considered overbought when the RSI is above 70% and oversold when it is below 30%.
    :param close: (pandas Series) Closing price
    :param period: (int) specified period (default=14)
    :return: rsi: (pandas Series) Relative Strength Index
    """
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


def vortex(high, low, close, period=14):
    positive_vortex = abs(high - low.shift())  # Upward movement
    negative_vortex = abs(low - high.shift())  # Downward movement

    # Calculating sum for a specified period (typically, 14-day period is used)
    positive_vortex_sum = positive_vortex.rolling(window=period).sum()
    negative_vortex_sum = negative_vortex.rolling(window=period).sum()

    TR = true_range(high=high, low=low, close=close).rolling(window=period).sum()

    VI_up = pd.Series(positive_vortex_sum / TR, name='VI_up')
    VI_down = pd.Series(negative_vortex_sum / TR, name='VI_down')

    return pd.concat([VI_up, VI_down], axis=1)


def ease_of_movement(high, low, volume, period=14, scale=1e6):
    distance = ((high + low) / 2) - (high.shift() + low.shift()) / 2
    box_ratio = (volume / scale) / (high - low)

    EMV = distance / box_ratio

    return EMV.rolling(window=period).mean()


def commodity_channel(high, low, close, period=20, const=.015):
    typical_price = (high + low + close) / 3
    typical_price_rolling = typical_price.rolling(window=period, min_periods=0)
    mean_deviation = typical_price_rolling.apply(lambda series: np.fabs(series - series.mean()).mean())

    CCI = (typical_price - typical_price_rolling.mean()) / (const * mean_deviation)

    return CCI


def signed_difference(series, initial=None):
    sign = series.diff(1)
    sign[sign > 0] = 1
    sign[sign < 0] = -1
    sign.iloc[0] = initial

    return sign


def on_balance_volume(close, volume):
    signed_vol = signed_difference(close) * volume
    OBV = signed_vol.cumsum()

    return OBV


def typical_price(high, low, close):
    tp = (high + low + close) / 3

    return tp


def money_flow_index(volume, high, low, close, period=14):
    tp = pd.Series(typical_price(high=high, low=low, close=close), name='tp')
    rmf = pd.Series(tp * volume, name='rmf')
    mf = pd.concat([tp, rmf], axis=1)
    mf['delta'] = mf['tp'].diff(1)

    def pos(row):
        if row['delta'] > 0:
            return row['rmf']
        else:
            return 0

    def neg(row):
        if row['delta'] < 0:
            return row['rmf']
        else:
            return 0

    mf["neg"] = mf.apply(neg, axis=1)
    mf["pos"] = mf.apply(pos, axis=1)

    # Calculate Money Flow Ratio
    mfr = mf['pos'].rolling(window=period).sum() / mf["neg"].rolling(window=period).sum()
    MFI = 100 - (100 / (1 + mfr))

    return MFI

