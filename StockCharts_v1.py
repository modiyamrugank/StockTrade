from CandlestickFunctions import *
from StocklineFunctions import *
from bokeh.models import HoverTool
from bokeh.plotting import figure, show,ColumnDataSource,output_file
from bokeh.layouts import gridplot
import os

try:
    import cPickle as pickle
except:
    import pickle

def stockChart(stocklist):
    with open ('Quotes_historical.pickle','rb') as f:
        quotes = pickle.load(f)
    f.close()

    #ls = quotes.keys()
    ls = stocklist
    ls.sort()

    ls_line=[]
    ls_candle=[]
    ls_volume = []
    ls_trend = []
    ls_rsi = []
    ls_macd = []

    WIDE = 750
    for i in ls:

        df_org = quotes[i]
        df = df_org.tail(180) #last 180 days for candle stick and related calculations

        #line charts for long duration
        p = figure(title = i, width=WIDE, height=225, x_axis_type="datetime")
        p.line(df_org['Date'], df_org['Close'], color='navy', alpha=0.5)
        p.grid.grid_line_alpha=0.3
        p.title.text_font_size="10pt"

        ls_line.append(p)

        #candlestick charts

        """Plots a lot of different things on candlestick charts
        1.Candlestick chart
        2.Single candlestick patterns
        3.Multiple candlestick patterns
        4.Trend indicator
        5.EMA (25d, 50d and 100d)
        6.Bollinger Bands
        """

        inc = df['Close'] > df['Open']
        dec = df['Open'] > df['Close']

        w = 12*60*60*1500 # half day in ms, for bar width

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

        s = figure(x_axis_type="datetime", tools=TOOLS, plot_width=WIDE,plot_height=400,toolbar_location='left')
        s.xaxis.major_label_orientation = pi/4
        s.grid.grid_line_alpha=0.3

        s.segment(df.Date, df.High, df.Date, df.Low, color="black")
        s.vbar(df.Date[inc], w, df.Open[inc], df.Close[inc], fill_color="#4D4DFF", line_color="#4D4DFF")
        s.vbar(df.Date[dec], w, df.Open[dec], df.Close[dec], fill_color="#F2583E", line_color="#F2583E")

        #trend detection and display for last trade only
        TRENDPERIOD = 15 #days to use in trend calculation, for multiple candle stick patterns
        trend = calc_trend(df[-TRENDPERIOD:].Close,TRENDPERIOD)

        trend_magnitude = abs(trend)
        if 0 < trend_magnitude <= 1:
            a=0.3
        elif 1 < trend_magnitude <= 3:
            a=0.6
        else:
            a=1

        if trend < 0 :
                s.inverted_triangle(df[-1:].Date,df[-1:].Low-5,size=10,fill_color='red',line_color='red',alpha=a)
        else:
                s.triangle(df[-1:].Date,df[-1:].High+5,size=10,fill_color='green',line_color='green',alpha=a)


        #Check single candle stick patterns
        """Denotes single candle stick patterns with circles of different colors
        Marubuzo: Blue circle
        Doji: dark red circle
        Spinning top : light red circle
        Paper umbrella : green cross
        Shooting star : red asterisk
        """

        #Pattern1 MARUBUZO
        xcoord_maru = []
        ycoord_maru = []
        for j in df.index:
            if check_marubuzo(df.ix[j]):
                xcoord_maru.append(df.ix[j].Date)
                ycoord_maru.append(df.ix[j].High+1)
        s.circle(xcoord_maru,ycoord_maru,size=10,color='navy',alpha=0.5)

        #Pattern 2 Doji
        xcoord_doji = []
        ycoord_doji = []
        for j in df.index:
            if check_doji(df.ix[j]) and abs(calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD)) > 1:
                xcoord_doji.append(df.ix[j].Date)
                ycoord_doji.append(df.ix[j].High+1)
        s.circle(xcoord_doji,ycoord_doji,size=10,color='red',alpha=0.8)

        #Pattern 3 Spinning Top
        xcoord_spin = []
        ycoord_spin = []
        for j in df.index:
            if check_spinningTop(df.ix[j]) and abs(calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD)) > 1:
                xcoord_spin.append(df.ix[j].Date)
                ycoord_spin.append(df.ix[j].High+1)
        s.circle(xcoord_spin,ycoord_spin,size=10,color='red',alpha=0.45)

        #pattern 4 Paper Umbrella
        xcoord_umbrella= []
        ycoord_umbrella = []
        for j in df.index:
            if check_paperUmbrella(df.ix[j]) and abs(calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD)) > 1:
                xcoord_umbrella.append(df.ix[j].Date)
                ycoord_umbrella.append(df.ix[j].High+1)
        s.cross(xcoord_umbrella,ycoord_umbrella,size=10,color='green')

        #pattern 5 Shooting Star
        xcoord_shootstar= []
        ycoord_shootstar = []
        for j in df.index:
            if check_shootingStar(df.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) > 1:
                xcoord_shootstar.append(df.ix[j].Date)
                ycoord_shootstar.append(df.ix[j].High+1)
        s.asterisk(xcoord_shootstar,ycoord_shootstar,size=10,color='red')

        """Single Candlestick plotting ends"""

        #pattern 6 bullish engulfing
        xcoord_bullengulf = []
        ycoord_bullengulf = []
        for j in df.index:
            if check_bullishEngulfing(df_org.ix[j-1],df_org.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) <= -1:
                xcoord_bullengulf.append(df.ix[j].Date)
                ycoord_bullengulf.append(df.ix[j].Low-1)
        s.square(xcoord_bullengulf,ycoord_bullengulf,size=7,color='navy',alpha=0.6)

        #pattern 7 bearish engulfing
        xcoord_bearengulf = []
        ycoord_bearengulf = []
        for j in df.index:
            if check_bearishEngulfing(df_org.ix[j-1],df_org.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) >= 1:
                xcoord_bearengulf.append(df.ix[j].Date)
                ycoord_bearengulf.append(df.ix[j].Low-1)
        s.square(xcoord_bearengulf,ycoord_bearengulf,size=7,color='red',alpha=0.6)

        #pattern 8 piercing
        xcoord_pierce = []
        ycoord_pierce = []
        for j in df.index:
            if check_piercing(df_org.ix[j-1],df_org.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) <= -1:
                xcoord_pierce.append(df.ix[j].Date)
                ycoord_pierce.append(df.ix[j].Low-1)
        s.triangle(xcoord_pierce,ycoord_pierce,size=7,color='navy',alpha=0.6)

        #pattern 9 dark cloud
        xcoord_darkcloud = []
        ycoord_darkcloud = []
        for j in df.index:
            if check_darkCloud(df_org.ix[j-1],df_org.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) >= 1:
                xcoord_darkcloud.append(df.ix[j].Date)
                ycoord_darkcloud.append(df.ix[j].Low-1)
        s.triangle(xcoord_darkcloud,ycoord_darkcloud,size=7,color='red',alpha=0.6)


        #pattern 10 bullish Harami
        xcoord_bullharami = []
        ycoord_bullharami = []
        for j in df.index:
            if check_bullishHarami(df_org.ix[j-1],df_org.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) <= -1:
                xcoord_bullharami.append(df.ix[j].Date)
                ycoord_bullharami.append(df.ix[j].Low-1)
        s.circle(xcoord_bullharami,ycoord_bullharami,size=7,color='navy',alpha=0.6)

        #pattern 11 bearish Harami
        xcoord_bearharami = []
        ycoord_bearharami = []
        for j in df.index:
            if check_bearishHarami(df_org.ix[j-1],df_org.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) >= 1:
                xcoord_bearharami.append(df.ix[j].Date)
                ycoord_bearharami.append(df.ix[j].Low-1)
        s.circle(xcoord_bearharami,ycoord_bearharami,size=7,color='red',alpha=0.6)

        #pattern 12 morning star
        xcoord_mstar = []
        ycoord_mstar = []
        for j in df.index:
            if check_morningStar(df_org.ix[j-2],df_org.ix[j-1],df_org.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) <= -1:
                xcoord_mstar.append(df.ix[j].Date)
                ycoord_mstar.append(df.ix[j].Low-1)
        s.asterisk(xcoord_mstar,ycoord_mstar,size=7,color='navy',alpha=0.6)

        #pattern 13 evening star
        xcoord_estar = []
        ycoord_estar = []
        for j in df.index:
            if check_eveningStar(df_org.ix[j-2],df_org.ix[j-1],df_org.ix[j]) and calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD) >= 1:
                xcoord_estar.append(df.ix[j].Date)
                ycoord_estar.append(df.ix[j].Low-1)
        s.asterisk(xcoord_estar,ycoord_estar,size=7,color='red',alpha=0.6)


        #25day , 50 day and 100 day EMA
        """
        25 day ema : black
        50 day ema : green
        100 day ema : pink
        """
        xcoord_ema25d = []
        ycoord_ema25d = []
        for j in df.index:
            xcoord_ema25d.append(df.ix[j].Date)
            ycoord_ema25d.append(ema(df_org.ix[(j-(25-1)):j].Close,25)[0])

        xcoord_ema50d = []
        ycoord_ema50d = []
        for j in df.index:
            xcoord_ema50d.append(df.ix[j].Date)
            ycoord_ema50d.append(ema(df_org.ix[(j-(50-1)):j].Close,50)[0])

        xcoord_ema100d = []
        ycoord_ema100d = []
        for j in df.index:
            xcoord_ema100d.append(df.ix[j].Date)
            ycoord_ema100d.append(ema(df_org.ix[(j-(100-1)):j].Close,100)[0])

        s.line(xcoord_ema50d,ycoord_ema50d,color='green',alpha=0.8)
        s.line(xcoord_ema100d,ycoord_ema100d,color='pink',alpha=0.8)
        s.line(xcoord_ema25d,ycoord_ema25d,color='black',alpha=0.8)

        #Bollinger bands
        xcoord_bollinger=[]
        ycoord_bollinger = []
        for j in df.index:
            xcoord_bollinger.append(df.ix[j].Date)
            ycoord_bollinger.append(bollinger(df_org.ix[(j-(20-1)):j].Close,20))

        band_x=np.append(xcoord_bollinger,xcoord_bollinger[::-1])
        band_y=np.append([k[0]-2*k[1] for k in ycoord_bollinger],[k[0]+2*k[1] for k in ycoord_bollinger][::-1])

        s.patch(band_x, band_y, color='#7570B3', fill_alpha=0.050,line_alpha=0.1)

        ls_candle.append(s)


        #volume bar charts
        #10 days avg volume
        mean_vol_10days = df.Volume[-10:].mean()
        v = figure(title="Volume",width=WIDE,height=50,x_axis_type="datetime",x_range=s.x_range)
        v.vbar(x=df['Date'],width=w,bottom=0,top=df['Volume'],fill_color='navy',alpha=0.3,line_color='navy')
        v.line(df['Date'],mean_vol_10days,color='grey',alpha=0.5)
        v.yaxis.visible=False
        v.xaxis.visible=False
        v.grid.visible=False
        v.title.text_font_size="6pt"
        v.min_border=0
        ls_volume.append(v)

        #trend line chart
        #display trend behaviour for this scrip.helpful in checking whether trend is about to reverse
        xcoord_trend = []
        ycoord_trend = []
        for j in df.index:
            xcoord_trend.append(df.ix[j].Date)
            ycoord_trend.append(calc_trend(df_org.ix[(j-(TRENDPERIOD-1)):j].Close,TRENDPERIOD))

        t = figure(title="Trend",width=WIDE,height=70,x_axis_type="datetime",x_range=s.x_range)
        t.line(xcoord_trend,ycoord_trend,color='blue',alpha=0.6)
        t.line(df['Date'],0,color='grey')
        t.xaxis.visible=False
        t.grid.grid_line_alpha=0.3
        t.title.text_font_size = "6pt"
        ls_trend.append(t)

        #RSI line chart
        xcoord_rsi = []
        ycoord_rsi = []
        for j in df.index:
            xcoord_rsi.append(df.ix[j].Date)
            ycoord_rsi.append(rsi(df_org.ix[j-13:j].Close,df_org.ix[j-14:j-1].Close))

        rsi_line = figure(title="RSI",width=WIDE,height=70,x_axis_type="datetime",x_range=s.x_range)
        rsi_line.line(xcoord_rsi,ycoord_rsi,color='red',alpha=0.8)
        rsi_line.line(df['Date'],75,color='grey')
        rsi_line.line(df['Date'],25,color='grey')
        rsi_line.xaxis.visible=False
        rsi_line.grid.grid_line_alpha=0.3
        rsi_line.title.text_font_size = "6pt"
        ls_rsi.append(rsi_line)

        #MACD line chart
        xcoord_macd = []
        ycoord_macd = []
        for j in df.index:
            xcoord_macd.append(df.ix[j].Date)
            ycoord_macd.append(ema(df_org.ix[(j-(12-1)):j].Close,12)[0]-ema(df_org.ix[(j-(26-1)):j].Close,26)[0])

        ycoord_macd = pd.Series(ycoord_macd)
        ycoord_signal_macd = []
        for j in ycoord_macd.index:
            ycoord_signal_macd.append(ema(ycoord_macd.ix[max(j-8,0):j],9)[0])

        macd_line = figure(title="MACD",width=WIDE,height=75,x_axis_type="datetime",x_range=s.x_range)
        macd_line.line(xcoord_macd,ycoord_macd,color='black',alpha=0.8)
        macd_line.line(xcoord_macd,ycoord_signal_macd,color='red',alpha=0.8)
        macd_line.line(xcoord_macd,0,color='grey')
        macd_line.xaxis.visible=False
        macd_line.grid.grid_line_alpha=0.3
        macd_line.title.text_font_size = "6pt"
        ls_macd.append(macd_line)


    output_file("Charts.html")

    grid = gridplot([[i for i in ls_line],[i for i in ls_volume],[i for i in ls_trend],[i for i in ls_rsi],[i for i in ls_macd],[i for i in ls_candle]])
    show(grid)  # open a browse
