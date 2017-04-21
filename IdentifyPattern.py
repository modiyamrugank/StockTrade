from CandlestickFunctions import *
from StocklineFunctions import *
from collections import defaultdict
from StockCharts_v1 import *
try:
    import cPickle as pickle
except:
    import pickle

with open ('Quotes_historical.pickle','rb') as f:
    quotes = pickle.load(f)
f.close()

ls = quotes.keys()
patterns= defaultdict(pd.DataFrame)

for k in ls:
    patternlist = []
    df = quotes[k].tail(20)

    last = df.index.max()
    #trend detection and display for last trade only
    TRENDPERIOD = 15 #days to use in trend calculation, for multiple candle stick patterns
    trend = calc_trend(df[-TRENDPERIOD:].Close,TRENDPERIOD)

    if check_marubuzo(df.ix[last]):
        patternlist.append("Marubuzo")

    if check_doji(df.ix[last]) and abs(trend) >= 1:
        patternlist.append("Doji")

    if check_spinningTop(df.ix[last]) and abs(trend) >= 1:
        patternlist.append("Spinning Top")

    if check_paperUmbrella(df.ix[last]) and trend >= 1:
        patternlist.append("Hangman")

    if check_paperUmbrella(df.ix[last]) and trend <= -1:
        patternlist.append("Hammer")

    if check_shootingStar(df.ix[last]) and trend >= 1:
        patternlist.append("Shooting Star")

    if check_bullishEngulfing(df.ix[last-1],df.ix[last]) and trend <= -1:
        patternlist.append("Bullish Engulfing")

    if check_bearishEngulfing(df.ix[last-1],df.ix[last]) and trend >= 1:
        patternlist.append("Bearish Engulfing")

    if check_piercing(df.ix[last-1],df.ix[last]) and trend <= -1:
        patternlist.append("Piercing Pattern")

    if check_darkCloud(df.ix[last-1],df.ix[last]) and trend >= 1:
        patternlist.append("Dark Cloud Cover")

    if check_bullishHarami(df.ix[last-1],df.ix[last]) and trend <= -1:
        patternlist.append("Bullish Harami")

    if check_bearishHarami(df.ix[last-1],df.ix[last]) and trend >= 1:
        patternlist.append("Bearish Harami")

    if check_morningStar(df.ix[last-2],df.ix[last-1],df.ix[last]) and trend <= -1:
        patternlist.append("Morning Star")

    if check_eveningStar(df.ix[last-2],df.ix[last-1],df.ix[last]) and trend >= 1:
        patternlist.append("Evening Star")

    patterns[k] = patternlist

for key,value in patterns.iteritems():
    print key + ":" + str(value)

chartlist = [i for i in patterns.keys() if not len(patterns[i])==0]
print chartlist
stockChart(chartlist)
