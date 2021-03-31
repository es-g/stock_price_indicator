import pandas as pd
import numpy as np


def simple_ma(close, period=10):
    """
    Takes the arithmetic mean of a given set of prices over the specific number of days in the past.
    Usually calculated to identify the trend direction of a stock
    :param close: closing price
    :param period: specified period (default: 10)
    :return: simple moving average
    """
    return close.rolling(window=period).mean()


def exp_ma(close, period=10):
    """
    Gives more weight to recent prices in an attempt to make it more responsive to new information.
    :param close: closing price
    :param period: specified period (default: 10)
    :return: exponential moving average
    """
    return close.ewm(span=period).mean()


def bollinger_bands(close, period=20):
    """
    Set of trendlines plotted two standard deviations (positively and negatively)
    away from a simple moving average (SMA) of a price

    :param close: Closing price
    :param period: specified period (default: 20)
    :return:
        BB_MID: simple moving average,
        BB_UPPER: upper band - 2 standard deviations away from sma,
        BB_LOWER: upper band - 2 standard deviations away from sma
    """

    BB_MID = pd.Series(simple_ma(close, period=period), name='BB_MID')
    BB_UPPER = pd.Series(BB_MID + 2 * close.rolling(window=period).std(), name='BB_UPPER')
    BB_LOWER = pd.Series(BB_MID - 2 * close.rolling(window=period).std(), name='BB_LOWER')
    return pd.concat([BB_MID, BB_UPPER, BB_LOWER], axis=1)


def volume_log(volume):
    """
    Converts to log scale
    :param volume: volume
    :return: volume in log scale
    """
    return volume.apply(np.log)


def rate_of_change(volume):
    """
    Percent change between previous and current
    :param volume: volume
    :return: percent change
    """
    return volume.pct_change()


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
    """
    trend-following momentum indicator that demonstrates the relationship between two moving averages
    - long-term and short-term. MACD is calculated as
    MACD = EMA(26-period) - EMA(12-period)
    The signal line is a 9-day EMA of the MACD Line. As a moving average of the indicator,
    it trails the MACD and makes it easier to spot MACD turns.

    :param close: closing price
    :param period_fast: period for short-term moving average (default: 12)
    :param period_slow: period for long-term moving average (default: 26)
    :param signal_period: period for moving average of the indicator (default: 9)
    :return:
        MACD_vals: difference between long-term and short-term sma
        MACD_signal_line: moving average of the indicator
    """

    EMA_short_term = exp_ma(close, period=period_fast)
    EMA_long_term = exp_ma(close, period=period_slow)

    MACD_vals = pd.Series(EMA_short_term - EMA_long_term, name='MACD')
    MACD_signal_line = pd.Series(MACD_vals.ewm(span=signal_period).mean(), name='MACD_signal')

    return pd.concat([MACD_vals, MACD_signal_line], axis=1)


def stochastic_oscillator(close, high, low, period=14):
    """
    Momentum indicator that compares a specific closing price of a security to its high-low range
     over a certain period of time.
    :param close: closing price
    :param high: highest price
    :param low: lowest price
    :param period: specified period (default: 14)
    :return: STOCHO: stochastic oscillator
    """

    max_high = high.rolling(window=period).max()
    min_low = low.rolling(window=period).min()

    STOCHO = pd.Series((close - min_low) / (max_high - min_low) * 100,
                       name="{} period stochastic oscillator".format(period))

    return STOCHO


def accumulation_distribution(close, low, high, volume):
    """
    Cumulative indicator that makes us of price and volume to assess
    whether an asset is being accumulated or distributed.
    :param close: closing price
    :param low: lowest price
    :param high: highest price
    :param volume: daily volume
    :return: ADI: Accumulation/Distribution Indicator
    """

    # Calculate current money flow volume
    cmfv = (((close - low) - (high - close)) / (high - low)) * volume

    ADI = cmfv.cumsum()

    return ADI


def true_range(high, low, close):
    """

    :param high: highest price
    :param low: lowest price
    :param close: closing price
    :return: TR: true range
    """
    ranges = [high - low, high - close.shift(), close.shift() - low]
    TR = pd.DataFrame(ranges)
    TR = TR.abs().max()

    return TR


def average_true_range(high, low, close, period=14):
    """
    Market volatility indicator.
    Measures market volatility by decomposing the complete range of a security price for that period.

    :param high: highest price
    :param low: lowest price
    :param close: closing price
    :param period: specified period (default: 14)
    :return: ATR: average true range
    """

    TR = true_range(high=high, low=low, close=close)

    return TR.rolling(window=period).mean()


def vortex(high, low, close, period=14):
    """
    Plots two oscillating lines: one to identify positive trend movement and
    the other to identify negative price movement
    :param high: highest price
    :param low: lowest price
    :param close: closing price
    :param period: specified period (default: 14)
    :return:
        VI_up: positive trend movement
        VI_down: negative price movement
    """
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
    """
    Calculates how easily a price can move up or down: subtracts yesterday's average price from
    today's average price and divides the difference by volume
    :param high: highest price
    :param low: lowest price
    :param volume: volume
    :param period: specified period (default: 14)
    :param scale: scaled depending on average daily volume
    :return: EMV: n-day period ease of movement
    """

    distance = ((high + low) / 2) - (high.shift() + low.shift()) / 2
    box_ratio = (volume / scale) / (high - low)

    EMV = distance / box_ratio

    return EMV.rolling(window=period).mean()


def signed_difference(series, initial=None):
    """
    Returns signed difference for series
    """

    sign = series.diff(1)
    sign[sign > 0] = 1
    sign[sign < 0] = -1
    sign.iloc[0] = initial

    return sign


def on_balance_volume(close, volume):
    """
    Uses volume flow to predict changes in stock price
    :param close: closing price
    :param volume: volume
    :return: OBV: on balance volume
    """
    signed_vol = signed_difference(close) * volume
    OBV = signed_vol.cumsum()

    return OBV


def typical_price(high, low, close):
    """
    Calculates arithmetic average of the high, low, and closing prices for a given period
    """

    tp = (high + low + close) / 3

    return tp


def money_flow_index(volume, high, low, close, period=14):
    """
    Uses price and volume data for identifying overbought or oversold signals in an asset.
    It can also be used to spot divergences which warn of a trend change in price.
    The oscillator moves between 0 and 100.

    :param volume: volume
    :param high: highest price
    :param low: lowest price
    :param close: closing price
    :param period: period (default: 14)
    :return: MFI: Money Flow Index
    """

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

