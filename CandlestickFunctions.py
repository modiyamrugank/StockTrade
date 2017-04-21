from math import pi
import pandas as pd
import numpy as np

"""
functions for detecting single candlestick patterns

All definitions and terminology from Zerodha Varsity material

Except Marubuzo, all the others need to be checked in conjunction with prior trend
"""
def check_marubuzo(quote): #relative to High and Low
    if quote.Close > quote.Open and ((quote.High-quote.Close)/quote.High <= 0.002 and (quote.Open-quote.Low)/quote.Open <= 0.002):
        return True
    elif quote.Open > quote.Close and ((quote.High-quote.Open)/quote.High <= 0.002 and (quote.Close-quote.Low)/quote.Close <= 0.002):
        return True
    else:
        return False

def check_marubuzo_2(quote):#relative to real body
    if quote.Close > quote.Open and ((quote.High-quote.Close)/max(quote.Close-quote.Open,0.0001) <= 0.1 and (quote.Open-quote.Low)/max(quote.Close-quote.Open,0.0001) <= 0.1):
        return True
    elif quote.Open > quote.Close and ((quote.High-quote.Open)/max(quote.Open-quote.Close,0.0001) <= 0.1 and (quote.Close-quote.Low)/max(quote.Open-quote.Close,0.0001) <= 0.1):
        return True
    else:
        return False

def check_doji(quote):
    if abs(quote.Open-quote.Close)/quote.Close<=0.001:
        return True
    else:
        return False

def check_spinningTop(quote):

    if quote.Close > quote.Open and (quote.Close-quote.Open)/quote.Close <=0.01:
        if 0.66 <= (quote.High-quote.Close)/max(quote.Open-quote.Low,0.0001) <= 1.5 and (quote.High-quote.Close)/max(quote.Close-quote.Open,0.0001)>=0.85 and (quote.Open-quote.Low)/max(quote.Close-quote.Open,0.0001)>=0.85:
            return True
        else:
            return False

    elif quote.Open > quote.Close and (quote.Open-quote.Close)/quote.Open <= 0.01:
        if 0.66<=(quote.High-quote.Open)/max(quote.Close-quote.Low,0.0001) <= 1.5 and (quote.High-quote.Open)/max(quote.Open-quote.Close,0.0001)>=0.85 and (quote.Close-quote.Low)/max(quote.Open-quote.Close,0.0001)>=0.85 :
            return True
        else:
            return False
    else:
        return False

def check_paperUmbrella(quote):
    if quote.Close > quote.Open and (quote.Close-quote.Open)/quote.Close <=0.02:
        if (quote.Open-quote.Low)/max(quote.Close-quote.Open,0.0001) >=2 and (quote.High-quote.Close)/max(quote.Close-quote.Open,0.0001) < 0.3:
            return True
        else:
            return False
    elif quote.Open > quote.Close and (quote.Open-quote.Close)/quote.Open <=0.02:
        if (quote.Close-quote.Low)/(max(quote.Open-quote.Close,0.0001))>=2 and (quote.High-quote.Open)/max(quote.Open-quote.Close,0.0001) < 0.3:
            return True
        else:
            return False
    else:
        return False

def check_shootingStar(quote):
    if quote.Close > quote.Open and (quote.Close-quote.Open)/quote.Close <=0.02:
        if (quote.High-quote.Close)/max(quote.Close-quote.Open,0.0001) >=2 and (quote.Open-quote.Low)/max(quote.Close-quote.Open,0.0001) < 0.3:
            return True
        else:
            return False
    elif quote.Open > quote.Close and (quote.Open-quote.Close)/quote.Open <=0.02:
        if (quote.High-quote.Open)/(max(quote.Open-quote.Close,0.0001))>=2 and (quote.Close-quote.Low)/max(quote.Open-quote.Close,0.0001) < 0.3:
            return True
        else:
            return False
    else:
        return False

"""
functions for detecting multiple candlestick patterns

All in conjunction with prior trend
"""

def check_bullishEngulfing(p1,p2):
    if p1.Close < p1.Open and p2.Close > p2.Open: # check red candle precedes blue candle
        if p2.Open < p1.Close and p2.Close > p1.Open:
            return True
        else:
            return False
    else:
        return False

def check_bearishEngulfing(p1,p2):
    if p1.Open < p1.Close and p2.Open > p2.Close:
        if p2.Open > p1.Close and p2.Close < p1.Open:
            return True
        else:
            return False
    else:
        return False

def check_bullishHarami(p1,p2):
    if p1.Close < p1.Open and p2.Close > p2.Open:
        if p2.Open > p1.Close and p2.Close <= p1.Open:
            return True
        else:
            return False
    else:
        return False


def check_bearishHarami(p1,p2):
    if p1.Open < p1.Close and p2.Open > p2.Close:
        if p2.Open < p1.Close and p2.Close > p1.Open:
            return True
        else:
            return False
    else:
        return False


def check_piercing(p1,p2):
    if p1.Close < p1.Open and p2.Close > p2.Open:
        if abs(p1.Close-p2.Open)/p2.Open <= 0.05 and abs(p1.Open-p2.Close)/p2.Close <= 0.05 and ((p1.Open < p2.Open and p1.Close > p2.Close) or (p1.Open > p2.Open and p1.Close < p2.Close)):
            range_overlap = (p1.Open-p1.Close)/(p2.Close-p2.Open)
            mids_p1 = p1.Open - (p1.Open-p1.Close)/2
            mids_p2 = p2.Close - (p2.Close-p2.Open)/2
            mids_distance = abs(mids_p1-mids_p2)/max((p1.Open-p1.Close),(p2.Close-p2.Open))
            if range_overlap >= .6 and range_overlap < 1 and mids_distance <= .5:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def check_darkCloud(p1,p2):
    if p1.Open < p1.Close and p2.Open > p2.Close:
        if abs(p1.Close-p2.Open)/p2.Open <= 0.05 and abs(p1.Open-p2.Close)/p2.Close <= 0.05 and ((p1.Open < p2.Open and p1.Close > p2.Close) or (p1.Open > p2.Open and p1.Close < p2.Close)) :
            range_overlap = (p1.Close-p1.Open)/(p2.Open-p2.Close)
            mids_p1 = p1.Close - (p1.Close-p1.Open)/2
            mids_p2 = p2.Open - (p2.Open-p2.Close)/2
            mids_distance = abs(mids_p1-mids_p2)/max((p1.Close-p1.Open),(p2.Open-p2.Close))
            if range_overlap >= .6 and range_overlap < 1 and mids_distance <= .5:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def check_morningStar(p1,p2,p3):
    #original literature at zerodha only compares engulfing between p1 and p3, plus p3.Close has to be > p1.Open
    # here I have also included bullish harami and relaxed p3.Close > p1.Open criterion , update based on performance
    if(check_bullishEngulfing(p1,p3) or check_piercing(p1,p3) or check_bullishHarami(p1,p3)) and (check_doji(p2) or check_spinningTop(p2)) and p2.Open < p1.Close and p3.Open > (max(p2.Close,p2.Open)) and p3.Close > p1.Open:
        return True
    else:
        return False

def check_eveningStar(p1,p2,p3):
    #original literature at zerodha only compares engulfing between p1 and p3, plus p3.Close has to be < p1.Open
    # here I have also included bearish harami and relaxed p3.Close < p1.Open criterion , update based on performance
    if(check_bearishEngulfing(p1,p3) or check_darkCloud(p1,p3) or check_bearishHarami(p1,p3)) and (check_doji(p2) or check_spinningTop(p2)) and p2.Open > p1.Close and p3.Open < (min(p2.Close,p2.Open)) and p3.Close < p1.Open :
        return True
    else:
        return False
