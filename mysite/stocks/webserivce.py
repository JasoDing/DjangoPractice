# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 18:03:28 2021

@author: dingz
"""

import os
import django
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if path not in sys.path:
    sys.path.append(path)
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, datetime,timedelta 
from stocks.models import Temp_histroy1
from django.db.models import Q

def getdata(tickername:str,startDate,endDate):
    
    qs = Temp_histroy1.objects.all()
    
    #qs = qs.filter(ticker = tickername)
    qs = qs.filter(ticker = tickername,date__gte = startDate,date__lt = endDate).order_by('date')
    if qs.exists():
        
        startDate = str(startDate + ' 00:00:00')
        #print(startDate)
        dt_startdate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        dt_startdate = dt_startdate.replace(tzinfo=None)
        
        endDate = str(endDate + ' 00:00:00')
        #print(endDate)
        dt_endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
        dt_endDate = dt_endDate.replace(tzinfo=None)
        
        
        
        time = date
        #print('timeformat:',dt_startdate)
        #notweekend = (dt_startdate + timedelta(days=5))
        temp = qs.first().date
        temp = temp.replace(tzinfo=None)
        print(temp)
        temmp = qs.last().date
        print(temmp)
        temmp = temmp.replace(tzinfo=None)
        
        #print(temp)
        #print(abs(temp -dt_startdate).days)
        if (abs(temp -dt_startdate).days <= 6) and (abs(temmp -dt_endDate).days <= 3):    # If exist, use data in DataBase
            #print (qs.date)
            print (' Data Found in DB =========')
            #print(qs.count())
            reslst = []
            for obj in qs:
                reslst.append([obj.date,obj.close])
                df = pd.DataFrame(reslst,columns = ['date','close'])
            #print (df)
            return df
        else:
            print(' Data Not in DB !')
            res = requestData(tickername, startDate, endDate)
            return res
        
    else:           # Else, go Tiingo to download
        print(' Data Not in DB !')
        res = requestData(tickername, startDate, endDate)
        return res


def requestData(tickername:str,startDate,endDate):
    # init:
    #tickername = 'amzn'         # string format. Ticker related to the asset.
    #startDate = ''          # DATE format. Parameter must be in YYYY-MM-DD format
    #endDate = ''            # DATE format. Parameter must be in YYYY-MM-DD format
    resampleFreq = 'daily'       # string format."daily""weekly""" Format is # + (min/hour);
    #sort = "sort=date"      # sort=date will sort by date in ascending order. sort=-date will sort by date in descending order.
    format = 'json'          # Sets the response format of the returned data. Acceptable values are "csv" and "json". Defaults to JSON.
    columns = str(['date','close'])
    
    '''
                            #e.g. "15min" or "4hour". If no value is provided, defaults to 5min.
    afterHours = ''         # boolean. If set to true, includes pre and post market data if available.
    forceFill = ''          # Some tickers do not have a trade/quote update for a given time period. if forceFill is set to true, then the previous OHLC will be used to fill the current OHLC.
    '''
    '''
    today = datetime.date(datetime.now())
    prevMonth = datetime.date(datetime.today() - timedelta(days=360))
    startDate = str(prevMonth)
    #startDate = '2020-08-27'
    #endDate = '2020-09-01'
    endDate = str(today)
    print (startDate)
    #print(columns)
    '''
    
    if (tickername != '' and startDate != ''):
        #
        historyRequest = 'https://api.tiingo.com/tiingo/'+resampleFreq+'/' + tickername + '/prices?startDate='+startDate+'&endDate='+endDate+'&format'+format+'&columns'+columns+'&token=7c39770410248a95981a58472b1bf42bda56a0af';
    else: print('ticker and start Date should not be null.')
    
    #print(historyRequest)
    
    headers = {'Content-Type': 'application/json'}
    request2tiingo = requests.get(str(historyRequest), headers = headers)
    res = request2tiingo.json()
    #print(res)
    #print()
    #print(res[0].get)
    #print(tickername)
    
    
    # Save to database:
    history_data = []
    qs = Temp_histroy1.objects.all()
    print(' Storing data into database, please wait...')
    for i in res:
        #print(i)
        disdate = i.get('date')
        temp = qs.filter(ticker = tickername,date = disdate)
        #print('temp ',temp)
        if not temp.exists():
            
            a = Temp_histroy1(ticker = str(tickername),
                              date = i.get('date'),
                              close = i.get('close'),
                              high = i.get('high'),
                              low = i.get('low'),
                              open = i.get('open'),
                              volume = i.get('volume')
                              )
            a.save()
            
        history_data.append([i.get('date'),i.get('close')]) 
        
    '''
    # output result to csv
    df = pd.DataFrame(res)
    df.to_csv('out.csv', sep=',', header=None, index=None)
    #requestResponse = requests.get('https://api.tiingo.com/tiingo/daily/aapl/prices?startDate=2019-01-02&token=7c39770410248a95981a58472b1bf42bda56a0af', headers=headers)
    #print(requestResponse.json())
    '''
    
    # set data
    #print (history_data)
    df = pd.DataFrame(history_data,columns = ['date','close'])
    #print(df)
    #print('hist:',len(history_data))
    #print('df: ',len(df.index))
    return df

def initset(shortwin=4, longwin = 12):
    global SIGNAL_BUY
    SIGNAL_BUY = 'buy'        # 买入信号
    
    global SIGNAL_SELL
    SIGNAL_SELL = 'sell'      # 卖出信号
    
    global SIGNAL_INIT
    SIGNAL_INIT = ''            # 观望信号
    
    global SHORT_WIN
    SHORT_WIN = shortwin               # 短周期窗口 5
    
    global LONG_WIN
    LONG_WIN = longwin               # 长周期窗口, 10, 20, 25, 30
    
    global RES 
    RESULT = []
    

class avg:
    
    def __init__(self):
        self.i = 0                       # 经历过的交易周期
        self.base_price = None           # 初始价格
        self.signal = SIGNAL_INIT        # 交易信号
        #self.set_commission(maker=0.001, taker=0.001)    # 手续费
    
    def data_handle(self, data,portfolio,pos_amount = 0):
        #print(data)
        self.i += 1   # 记录交易周期
        #print (self.i)
        #pos_amount = 0    # 当前持仓数量
        if self.i < LONG_WIN + 2:
            # 
            pack = []
            fin = {}
            pack.append(float(portfolio))
            pack.append(float(pos_amount))
            return pack,fin
        
        short_avgs = data.rolling(window=SHORT_WIN).mean()
        long_avgs = data.rolling(window=LONG_WIN).mean()
        
        three = self.i-3
        two = self.i-2
        #print(two,three)
        savg3 = float(short_avgs.iloc[three])
        lavg3 = float(long_avgs.iloc[three])
        savg2 = float(short_avgs.iloc[two])
        lavg2 = float(long_avgs.iloc[two])
        
        current = int(self.i)
        #print ('current ',current)
        price = float(data.iloc[current,1])
        #print('price: ',price)
        
        # 做多
        if (savg3 < lavg3) and (savg2 >= lavg2) and pos_amount == 0:
            
            pos_amount = (portfolio/price)
            self.signal = SIGNAL_BUY
            
        # 短期线下穿长期=做空
        if (savg3 > lavg3) and (savg2 <= lavg2) and pos_amount > 0:
            # 平仓
            pos_amount = 0
            self.signal = SIGNAL_SELL
    
        # 获取当前的价格
        if self.base_price is None:
            # init
            self.base_price = price
    
        # 计算价格变化百分比，作为基准
        price_change = (price - self.base_price) / self.base_price
    
        if pos_amount > 0:
            portfolio = price * pos_amount
        else:
            portfolio = portfolio
            
        # 记录每个交易周期的信息
        # 1. 价格, 现金, 价格变化率, 快线均值,s 慢线均值
        '''
        record(price=price,
               cash=context.portfolio.cash,
               price_change=price_change,
               short_mavg=short_avgs[-1],
               long_mavg=long_avgs[-1],
               signal=context.signal)
        '''
        # 输出信息
        date = str(data.iloc[current,0])
        #print('date',date)
        prot = 0
        #print('HERE ')
        '''
        fin = {('Date：{}，Close：{:.4f}，cash：{:.2f}，hold：{:.8f},signal:{}'.format(
            date, price,portfolio, pos_amount, self.signal))}
        '''
        fin = {'Date':date,'Close':price,'cash':portfolio,'hold':pos_amount,'signal':self.signal}
        #print(str(fin))
        #print(type(fin))
        #reslst = reslst.append(fin)
        #print(reslst)
        #print('here')
        
        print('Date：{}，Close Price：{:.4f}，资产：{:.2f}，持仓量：{:.8f}, {}'.format(
            date, price,portfolio, pos_amount, self.signal))
    
        # 进行下一次交易前重置交易信号
        self.signal = SIGNAL_INIT
        pack = []
        pack.append(float(portfolio))
        pack.append(float(pos_amount))
        #print('pack',pack)
        #print('fin',fin)
        return pack,fin
        
        
def analyze(context, perf):
    # 保存交易记录
    perf.to_csv('./performance.csv')

    # 获取交易所的计价货币
    exchange = list(context.exchanges.values())[0]
    quote_currency = exchange.quote_currency.upper()

    # 图1：可视化资产值
    ax1 = plt.subplot(411)
    perf['portfolio_value'].plot(ax=ax1)
    ax1.set_ylabel('Portfolio Value\n({})'.format(quote_currency))
    start, end = ax1.get_ylim()
    ax1.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    # 图2：可视化货币价格，均线和买入卖出点
    ax2 = plt.subplot(412, sharex=ax1)
    perf[['price', 'short_mavg', 'long_mavg']].plot(ax=ax2)
    ax2.set_ylabel('{asset}\n({quote})'.format(
        asset=context.asset.symbol,
        quote=quote_currency
    ))
    start, end = ax2.get_ylim()
    ax2.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))
    
    '''
    # 提取交易时间点
    transaction_df = extract_transactions(perf)
    if not transaction_df.empty:
        buy_df = transaction_df[transaction_df['amount'] > 0]   # 买入点
        sell_df = transaction_df[transaction_df['amount'] < 0]  # 卖出点
        ax2.scatter(
            buy_df.index.to_pydatetime(),
            perf.loc[buy_df.index, 'price'],
            marker='^',
            s=100,
            c='green',
            label=''
        )
        ax2.scatter(
            sell_df.index.to_pydatetime(),
            perf.loc[sell_df.index, 'price'],
            marker='v',
            s=100,
            c='red',
            label=''
        )
    '''
    # 图3：比较价格变化率和资产变化率
    ax3 = plt.subplot(413, sharex=ax1)
    perf[['algorithm_period_return', 'price_change']].plot(ax=ax3)
    ax3.set_ylabel('Percent Change')
    start, end = ax3.get_ylim()
    ax3.yaxis.set_ticks(np.arange(start, end, (end - start) / 5))

    # 图4：可视化现金数量
    ax4 = plt.subplot(414, sharex=ax1)
    perf['cash'].plot(ax=ax4)
    ax4.set_ylabel('Cash\n({})'.format(quote_currency))
    start, end = ax4.get_ylim()
    ax4.yaxis.set_ticks(np.arange(0, end, end / 5))

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    df = getdata('amzn','2021-1-8','2021-05-8' )
    #print('df: ',df)
    initset()
    msg = []
    wtf = avg()
    pack = []
    portfolio = 1000
    pos_amount = 0
    a,b = wtf.data_handle(df,portfolio,pos_amount)
    #print('a',a)
    #print('b',b)
    #print(len(df.index))
    for i in range (1,(len(df.index))-1):
            #print(type(pack))
            #print(type(output))
            pack,output = wtf.data_handle(df,portfolio,pos_amount)
            portfolio = pack[0]
            pos_amount = pack[1]
            if output is not {}:
                msg.append(output)
                print(type(output))
    print(type(msg))
    print('total days ',i)

def run(ticker,start,end,prot):
    df = getdata(ticker,start,end)
    #print('df: ',df)
    initset()
    msg = []
    wtf = avg()
    portfolio = prot
    pos_amount = 0
    a,b = wtf.data_handle(df,portfolio,pos_amount)
    for i in range (1,(len(df.index))-1):
            #print(type(pack))
            #print(type(output))
            pack,output = wtf.data_handle(df,portfolio,pos_amount)
            portfolio = float(pack[0])
            pos_amount = float(pack[1])
            if output is not {}:
                msg.append(output)
                print(type(output))
    #print(msg)
    #print('total days ',i)
    return msg
