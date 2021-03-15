import pandas as pd
import matplotlib.pyplot as plt


def plot_candle_chart(df, period=100):
    df_plot = df[-period:]
    bullish_df = df_plot[df_plot['Close'] > df_plot['Open']]
    bearish_df = df_plot[df_plot['Close'] < df_plot['Open']]

    plt.style.use('fivethirtyeight')

    plt.figure(figsize=(20, 15))
    plt.vlines(x=df_plot.index, ymin=df_plot['Low'], ymax=df_plot['High'], color='black', linewidth=1.5)
    plt.vlines(x=bullish_df.index, ymin=bullish_df['Open'], ymax=bullish_df['Close'], color='green', linewidth=4)
    plt.vlines(x=bearish_df.index, ymin=bearish_df['Close'], ymax=bearish_df['Open'], color='red', linewidth=4)

    sma = pd.DataFrame()
    sma['20-day'] = df['Close'].rolling(window=20).mean()
    sma['200-day'] = df['Close'].rolling(window=200).mean()
    plt.plot(sma[-period:]['20-day'], label='20-day simple moving average')
    plt.plot(sma[-period:]['200-day'], label='200-day simple moving average')
    plt.legend(loc='upper left')

    plt.show()
