import pandas as pd
import matplotlib.pyplot as plt


def plot_candle_chart(df, period=100, short_sma=50, long_sma=200):
    df_plot = df[-period:]
    bullish_df = df_plot[df_plot['Close'] > df_plot['Open']]
    bearish_df = df_plot[df_plot['Close'] < df_plot['Open']]

    plt.style.use('fivethirtyeight')

    plt.figure(figsize=(20, 15))
    plt.vlines(x=df_plot.index, ymin=df_plot['Low'], ymax=df_plot['High'], color='black', linewidth=1.5)
    plt.vlines(x=bullish_df.index, ymin=bullish_df['Open'], ymax=bullish_df['Close'], color='green', linewidth=4)
    plt.vlines(x=bearish_df.index, ymin=bearish_df['Close'], ymax=bearish_df['Open'], color='red', linewidth=4)

    sma = pd.DataFrame()
    sma['{}-day'.format(short_sma)] = df['Close'].rolling(window=short_sma).mean()
    sma['{}-day'.format(long_sma)] = df['Close'].rolling(window=long_sma).mean()
    plt.plot(sma[-period:]['{}-day'.format(short_sma)], label='{}-day simple moving average'.format(short_sma))
    plt.plot(sma[-period:]['{}-day'.format(long_sma)], label='{}-day simple moving average'.format(long_sma))
    plt.legend(loc='upper left')

    plt.show()


def plot_indicator(df, TI, ticker):
    fig = plt.figure(facecolor='white', figsize=(25, 15))

    ax0 = plt.subplot2grid((12, 8), (1, 0), rowspan=6, colspan=4)
    ax0.plot(df[ticker]['Close'], linewidth=2)
    ax0.set_facecolor('ghostwhite')
    ax0.legend(['Adj Close', 'SMA'], ncol=3, loc='upper left', fontsize=12)
    plt.title("{} Close and {}".format(ticker, TI), fontsize=15)

    ax1 = plt.subplot2grid((12, 8), (7, 0), rowspan=3, colspan=4, sharex=ax0)
    ax1.plot(df[ticker][TI], linewidth=1, label=TI)
    ax1.legend(ncol=3, loc='upper left', fontsize=12)
    ax1.set_facecolor('silver')
    plt.subplots_adjust(left=.09, bottom=.09, right=1, top=.95, wspace=.20, hspace=0)
    plt.show()
