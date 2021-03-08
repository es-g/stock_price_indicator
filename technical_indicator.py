def simple_ma(df, length=10):
    sma = df['Adj Close'].rolling(window=length).mean()
    return sma


def bollinger_bands(df, length=20):
    mid = simple_ma(df, length=length)
    upper = mid + 2*df['Adj Close'].rolling(window=length).std()
    lower = mid - 2*df['Adj Close'].rolling(window=length).std()
    return mid, upper, lower

