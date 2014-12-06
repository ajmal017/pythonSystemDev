#!/usr/bin/python
#-*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def create_sharpe_ratio(returns, periods=252):
 #zero benchmark (risk-free rate = 0)
 # returns = panda % returns series 
 #periods = daily (252), hourly(252*6.5) minutely (252*6.5*60)
 return np.sqrt(periods)*(np.mean(returns)) / np.std(returns)

def create_drawdowns(pnl):
 #pnl - panda series % returns
 #drawdown, duration - max drawdown and duration

 #calc cum. returns and high water mark
 hwm = [0]

 #create drawdown and duration series
 idx = pnl.index
 drawdown=pd.Series(index = idx)
 duration=pd.Series(index = idx)

 for t in range(1, len(idx)):
  hwm.append(max(hwm[t-1],pnl[t]))
  drawdown[t] = (hwm[t]-pnl[t])
  duration[t] = (0 if drawdown[t] == 0 else duration[t-1]+1)
 return drawdown.max(), duration.max()
 
def dd_stats(returns, N=252):
 #initialize
 equitySeries = (returns +1).cumprod()
 equityHighWaterMarkSeries = pd.expanding_max(equitySeries)
 ddPercentSeries = (equitySeries - equityHighWaterMarkSeries)/equityHighWaterMarkSeries
 maxDD = ddPercentSeries.min()
 ddDays = []
 DDs = []
 count = 0
 ddStart= 0

 # calc dd days
 for i,k in enumerate(equityHighWaterMarkSeries):
  if i > 0:
   if equityHighWaterMarkSeries[i-1]==equityHighWaterMarkSeries[i]: # in DD
    if count ==0: #DD Started
     ddStart = i-1
    count +=1
    if i == len(equityHighWaterMarkSeries)-1: #still in drawdown at the end of series
     ddDays.append(count)
     DDs.append(min(ddPercentSeries[ddStart:i]))
   else: #new hwm, DDEnded
    if count != 0:
     ddDays.append(count)
     DDs.append(min(ddPercentSeries[ddStart:i]))
     #ddStart =0
    count =0
    
 total_return = equitySeries[-1] - 1.0
 ccr_total_return = np.log(equitySeries[len(equitySeries)-1])-np.log(equitySeries[1])
 annualised_mar = np.sqrt(N) * returns.mean()/abs(maxDD)
 total_return_mar = ccr_total_return / maxDD
 cagr = equitySeries[-1]**(1.0/((returns.index[-1]-returns.index[0]).days/365.25))-1.0
 
 return annualised_mar,  total_return_mar, maxDD,  max(ddDays), \
  np.mean(ddDays),  len(DDs),  np.mean(DDs),  equitySeries,  ddPercentSeries, \
  ccr_total_return, total_return, cagr #12 stats

def annualised_sharpe(returns, N=252):
 # N = 252 trading days (daily)
 return np.sqrt(N) * returns.mean()/returns.std()

def annualised_sortino(returns, N=252):
 # N = 252 trading days (daily)
 down = []
 for i in returns:
  if i <0:
   down.append(i)
 return np.sqrt(N) * returns.mean()/np.std(down)

def equity_sharpe(pdf, N=252, rf = 0.05):

 
 #use the percent change method to calculate daily returns
 pdf['daily_ret'] = pdf['Close'].pct_change()

 #assume an average annual risk free rate of 5% over the period
 pdf['excess_daily_ret'] = pdf['daily_ret'] - rf/N

 #return the annualised sharpe
 return pdf['excess_daily_ret']

def market_neutral_sharpe(tick, bench):
 #calculates sharpe of a market neutral (long/short) strategy
 #long ticker/ short benchmark

 #calc the % returns on each of the time series
 tick['daily_ret'] = tick['Close'].pct_change()
 bench['daily_ret'] = bench['Close'].pct_change()

 #net returns are (long-short)/2 because there is 2x trading capital
 strat = pd.DataFrame(index=tick.index)
 strat['net_ret'] = (tick['daily_ret'] - bench['daily_ret'])/2.0

 return strat['net_ret']
