#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import statsmodels.api as sm

from strategy import Strategy
from event import SignalEvent

class IntradayOLSMRStrategy(Strategy):
    """Uses ordinary least squares (OLS) to perform a roling linear regression
    to determine the hedge ratio between a pair of equities. The z-score
    of the residuals time series is then calculated in a rolling fashion
    and if it exceeds an interval of thresholds ([zscore_low, zscore_high])
    then a long/short signal pair are generated or an exit signal pair are generated for the low threshold.
    """
    
    def __init__(self, bars, events, ols_window=500, zscore_high=3.0, zscore_low=0.5):
        #Initialize stat arb
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.zscore_low = zscore_low
        self.zscore_high = zscore_high
        
        self.strategy_id = 'intradayOLSMR'
        self.pair = self.symbol_list[0:2]
        self.ols_window = ols_window
        self.bar_index = 0
        self.datetime = datetime.datetime.utcnow()
        
        self.long_market = False
        self.short_market = False
        
        self.data_primed = self.prime_data()
    
    def prime_data(self):
        for i in range(1,self.ols_window+1):
            self.bars.prime_bars()
        return True
    
    def calculate_xy_signals(self, zscore_last):
        #Parameters
        y_signal = None
        x_signal = None
        sid = self.strategy_id
        p0 = self.pair[0]
        p1 = self.pair[1]
        dt = self.datetime
        hr = abs(self.hedge_ratio)
        
        # If we're not long the market and below the negative of the high zs
        if zscore_last <= -self.zscore_high and not self.long_market:
            self.long_market = True
            y_signal = SignalEvent(sid, p0, dt, 'LONG', 1.0)
            x_signal = SignalEvent(sid, p1, dt, 'SHORT', hr)
        
        # if we are long and abs(zs) is above the low threshold
        if abs(zscore_last) <= self.zscore_low and self.long_market:
            self.long_market = False
            y_signal = SignalEvent(sid, p0, dt, 'EXIT', 1.0)
            x_signal = SignalEvent(sid, p1, dt, 'EXIT', 1.0)
        
        # if we are not short and above the high threshold
        if zscore_last >= self.zscore_high and not self.short_market:
            self.short_market = True
            y_signal = SignalEvent(sid, p0, dt, 'SHORT', 1.0)
            x_signal = SignalEvent(sid, p1, dt, 'LONG', hr)
        
        # if we are short and below the low threshold
        if abs(zscore_last) <= self.zscore_low and self.short_market:
            self.short_market = False
            y_signal = SignalEvent(sid, p0, dt, 'EXIT', 1.0)
            x_signal = SignalEvent(sid, p1, dt, 'EXIT', 1.0)
        
        return y_signal, x_signal
    
    def calculate_signals_for_pairs(self):
        """Calculates the hedge ratio between the pairs. Uses OLS
        """
        
        # gets window of values
        y = self.bars.get_latest_bars_values(
            self.pair[0], 'close', N = self.ols_window 
            )
        x = self.bars.get_latest_bars_values(
            self.pair[1], 'close', N = self.ols_window
            )
        
        if y is not None and x is not None:
            # Check that all window periods are avaiable
            if len(y) >= self.ols_window and len(x) >= self.ols_window:
                # Calculate hedge ratio using OLS
                self.hedge_ratio = sm.OLS(y,x).fit().params[0]
        
        # Calculate zscores
        spread = y - self.hedge_ratio * x
        zscore_last = ((spread - spread.mean())/spread.std())[-1]
        
        # Add signals to queue
        y_signal, x_signal = self.calculate_xy_signals(zscore_last)
        if y_signal is not None and x_signal is not None:
            self.events.put(y_signal)
            self.events.put(x_signal)
        self.bar_index +=1
    
    def calculate_signals(self,event):
        """ Calculates SignalEvents based on MarketEvent
        """
        if event.type == 'MARKET' and self.data_primed:
            self.calculate_signals_for_pairs()
            
