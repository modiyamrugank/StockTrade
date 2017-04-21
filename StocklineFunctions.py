import pandas as pd
import numpy as np
from math import pi

def calc_trend(quotesClose,period):
    x = pd.Series([j for j in range(1,period+1)])
    n1 = (x.values*quotesClose.values).sum()*12
    n2 = quotesClose.values.sum()*6*(period+1)
    d = period*(period+1)*(period-1)
    return ((n1-n2)/d)

def ema(quotesClose,days):
    if len(quotesClose) < days: return [None]
    a = 2.0 / (days+1)
    kernel = np.ones(days, dtype=float)
    kernel[1:] = 1 - a
    kernel = a * np.cumprod(kernel)
    # The 0.8647 normalizes out that we stop the EMA after a finite number of terms
    return np.convolve(quotesClose[-days:], kernel, mode="valid") / (0.8647)

def rsi(x,y):
    r = x.values-y.values
    RS= sum(i for i in r if i > 0)/abs(sum(i for i in r if i < 0))
    return (100-(100/(1+RS)))

def sma(quotesClose,days):
    if len(quotesClose) < days: return [None]
    return np.convolve(quotesClose[-days:], np.ones(days, dtype=float), mode="valid") / days

def bollinger(quotesClose,days):
    """takes close quotes series and returns sma, std dev"""
    return [sma(quotesClose,days)[0],np.std(quotesClose)]
