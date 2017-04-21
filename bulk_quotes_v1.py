from __future__ import division
import pandas as pd
import os
from collections import defaultdict
try:
    import cPickle as pickle
except:
    import pickle

'''
Imports all NIFTY 50 daily stock quotes for a specified date range
and dumps to a dictionary.

This should be used for one time historical dump

Subsequent daily quotes can be incrementally added using NSE bhavcopy file to the same dump

Inputs:

Start Date
End Date

Output:
Dictionary (Stockticker as key, Dataframe of open,close,high,low,vol as value)

'''


startyear = '2015'
endyear = '2017'
#error in BAJAJ-AUTO,M&M download CSV and name it as ticker value and load in except clause
#Stock ticker symbol may change in future so keep a watch on that

stocks = ['ACC.NS',
'ADANIPORTS.NS',
'AMBUJACEM.NS',
'ASIANPAINT.NS',
'AUROPHARMA.NS',
'AXISBANK.NS',
'BAJAJ-AUTO.NS',
#'BANKBARODA.NS',
'BHARTIARTL.NS',
'BHEL.NS',
'INFRATEL.NS',
'BOSCHLTD.NS',
'BPCL.NS',
'CIPLA.NS',
'COALINDIA.NS',
'DRREDDY.NS',
'EICHERMOT.NS',
'GAIL.NS',
'GRASIM.NS',
'HCLTECH.NS',
'HDFC.NS',
'HDFCBANK.NS',
'HEROMOTOCO.NS',
'HINDALCO.NS',
'HINDUNILVR.NS',
'ICICIBANK.NS',
'IDEA.NS',
'INDUSINDBK.NS',
'INFY.NS',
'ITC.NS',
'KOTAKBANK.NS',
'LT.NS',
'LUPIN.NS',
'MARUTI.NS',
'NTPC.NS',
'ONGC.NS',
'POWERGRID.NS',
'RELIANCE.NS',
'SBIN.NS',
'SUNPHARMA.NS',
'TATAMOTORS.NS',
'TATAMTRDVR.NS',
'TATAPOWER.NS',
'TATASTEEL.NS',
'TCS.NS',
'TECHM.NS',
'ULTRACEMCO.NS',
'WIPRO.NS',
'YESBANK.NS',
'ZEEL.NS']

quotes = defaultdict(pd.DataFrame)

for k in stocks:
    try:
        quotes[k] = pd.read_csv("http://chart.finance.yahoo.com/table.csv?s="+k+"&a=01&b=01&c="+startyear+"&d=0&e=0&f="+endyear+"&g=d&ignore=.csv",parse_dates=['Date'])
        quotes[k] = quotes[k][quotes[k].Volume > 0] #filter out 0 volume days
        quotes[k] = quotes[k].sort_values('Date').reset_index()
        quotes[k].drop('index',axis=1,inplace=True)
    except:
        print "Error in "+k
        #use already downloaded csv from NSE for BAJAJ AUTO (hyphen is a problem)
        #M&M data is wrong. somehow yahoo returns all wrong data
        #quotes[k] = pd.read_csv(k+'.csv',parse_dates=['Date'])
        #quotes[k] = quotes[k][quotes[k].Volume > 0]
        #quotes[k] = quotes[k].sort_values('Date').reset_index()
        #quotes[k].drop('index',axis=1,inplace=True)

#load M&M separately.Download from NSE and name as M&M.NS.csv
quotes['M&M.NS'] = pd.read_csv('M&M.NS.csv',parse_dates=['Date'])
quotes['M&M.NS'] = quotes['M&M.NS'][quotes['M&M.NS'].Volume > 0]
quotes['M&M.NS'] = quotes['M&M.NS'].sort_values('Date').reset_index()
quotes['M&M.NS'].drop('index',axis=1,inplace=True)

for k in quotes.keys():
    quotes[k].sort_values('Date',inplace=True)

with open (os.getcwd()+'/Quotes_historical.pickle','wb') as f:
    pickle.dump(quotes,f)
