# C4RM Homework 6 - cz2990
# Questions from the Homework tab of C4RM_Class_06: WhoAmI, qGetReturns, qVaR, qES

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm

# Q1. WhoAmI

# Identify yourself for grading
def WhoAmI():
    return('cz2990')

print(WhoAmI())

# Q2. get_returns
# Pull GS prices with yfinance, compute the return series (price today / price yesterday - 1), then print the average, max, min and standard deviation of returns.

def get_stock_data(symbol):
    data = yf.download(symbol, period="max")   # without period="max" yfinance only returns the last month
    prices = data['Close'][symbol]             # data['Close'] has one column per ticker -> select ours
    return prices

def get_returns(pricevec):
    n = len(pricevec)
    ratiovec = pricevec[1:n] / pricevec[:n-1]   # price today / price yesterday
    returns = ratiovec - 1
    return returns

prices = get_stock_data('GS')
print(type(prices))
pricevec = prices.values

returns = get_returns(pricevec)
print(returns)

#1 Average return
print('Average return:', np.mean(returns))
#2 Max return
print('Max return:', np.max(returns))
#3 Min return
print('Min return:', np.min(returns))
#4 Standard deviation of returns
print('Std of returns:', np.std(returns))

# Q3. VaR
# Percentile VaR: the positively stated return at the (1 - alpha) percentile.

def percent_var(r, alpha):
    # This function returns the left tail value and displays a histogram
    # alpha = risk level
    # r = a vector of stock returns
    # out = positively stated value of r at the 1-alpha percentile

    plt.hist(r, bins=50, alpha=0.75)
    plt.show()
    out = np.percentile(r, (1 - alpha) * 100)  # Calculate the percentile
    return abs(out)  # Return the absolute value of the calculated percentile

# Example tools: percentile
z = np.random.normal(0, 1, 10000)
print(np.percentile(z, 97.72))   # ~2, i.e. 2 SD

# Unit test
r = np.random.normal(0.05, 0.03, 1000000)
probability2SD = norm.cdf(2)  # Probability under normal curve within 2 standard deviations

myalpha = probability2SD
my_percent_var = percent_var(r, myalpha)
print(np.round(my_percent_var, 2) == 0.01)   # 0.05 - 2*0.03 = -0.01

# VaR of the GS return series from Q2
gs_var95 = percent_var(returns, 0.95)
gs_var99 = percent_var(returns, 0.99)
print('GS 1-day 95% VaR:', gs_var95)
print('GS 1-day 99% VaR:', gs_var99)

# Q4. Expected Shortfall
# Average of the losses beyond VaR.

def es(losses, alpha=None, VaR=None):
    """
    Calculate the Expected Shortfall (ES) of losses.

    :param losses: array of positively stated loss values
    :param alpha: risk level (e.g., 0.99 for 99%)
    :param VaR: dollar value or percentage specifying the VaR threshold
    :return: Expected Shortfall as the average of losses exceeding VaR
    """
    if VaR is None:
        # Losses are positively stated, so the tail is the top end: VaR is the alpha percentile
        # (the template's 100 * (1 - alpha) picks the wrong tail and fails its own unit test)
        VaR = np.percentile(losses, 100 * alpha)

    # Calculate ES as the average of losses exceeding the VaR threshold
    es_value = np.mean(losses[losses > VaR])
    return es_value

# Unit test
u = np.random.uniform(0, 100, 100000)

# Test the ES function with an alpha of 0.8
es_alpha = es(losses=u, alpha=0.8)
print('ES with alpha:', np.round(es_alpha, 0) == 90)

# Test the ES function with a VaR of 80
es_var = es(losses=u, VaR=80)
print('ES with VaR:', np.round(es_var, 0) == 90)

# ES of the GS return series from Q2 (losses = negative returns)
gs_losses = -returns
print('GS 1-day 97.5% ES:', es(gs_losses, alpha=0.975))
print('GS 1-day 99% ES:', es(gs_losses, alpha=0.99))
print('GS 1-day 99% ES (VaR from Q3):', es(gs_losses, VaR=gs_var99))
