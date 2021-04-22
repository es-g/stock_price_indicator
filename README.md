# Predicting the next day’s return of a stock: end-to-end framework

## Motivation

Predicting the stock market has always been an attractive topic, mainly because of its vitality in the economic and ﬁnancial sectors. As long as markets have existed, investors have searched for ways to acquire knowledge about the companies listed in the market to improve their investment returns. Yet, predictions of the stock market pose a challenging exercise, even to the sharpest minds in the business. Prediction of the stock market is never an easy task, due to the complexity and dynamic characteristics of the data it deals with.

There are several unique challenges present in this domain that are not present in other common areas of machine learning such as Natural Language Processing, spam detection, computer vision and others. These challenges include:

- Switching of regimes (non-stationarity)
- Reflexivity (market adaptation)
- Low signal-to-noise ratio

In this project, I tried to predict the next day’s change in the price of an asset using only historical data and technical indicators.

# Results
The main findings of this code are summarised in a [post](https://yesbol.medium.com/predicting-the-next-days-return-of-a-stock-end-to-end-framework-ca52373d68ce)

## Conclusion

From the above, the best method in terms of accuracy was found to be Linear Regression with expanding window approach (form of walk-forward approach) where we were able to predict direction of stock movement 58% of the time. In terms of capture ratio (i.e. ratio of the “edge” we gain by following predictions), XGB Boost expanding window approach showed the best performance where we saw 18% ratio, meaning that we were able to capture 18% of the true movement of the target variable.

However, these results are not sufficient enough to deploy the model for live trading. In the future research section, I will explain the methods that will help improve the accuracy of the model.

As we saw, predicting the stock market is a very challenging task.
Feature Engineering requires years of experience in trading as well as a significant time in experimentation. Due to time constraints and lack of domain knowledge, I only considered some features. However, it may be helpful to build other features based on technical indicators. Quantitative traders spend most of their time trying to extract useful features from noisy market data.

## Licence
MIT License

Copyright (c) 2021 Yesbol Gabdullin

