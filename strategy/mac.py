#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import path
import os
path.append(os.getcwd() + '/../engine')
path.append(os.getcwd() + '/../')
import datetime
import numpy as np

import pandas.io.data as web
from backtest import Backtest
from data import HistoricCSVDataHandler
from event import SignalEvent
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from strategy import Strategy

class MovingAverageCrossStrategy(Strategy):
    """Carries out MA cross over with a short/long simple wma. 
    """
    def __init__(self, bars, events, short_window=100, long_window=400):
        self.bars = bars # DataHandler object
        self.symbol_list = self.bars.symbol_list 
        self.events = events # Event Queue object
        self.short_window = short_window # short ma lookback
        self.long_window = long_window # long ma lookback
        
        self.bought = self._calculate_initial_bought() # "OUT"/"LONG"/"SHORT"
        self.data_primed = self.prime_data()
    
    def prime_data(self):
        for i in range(1,self.long_window+1):
            self.bars.prime_bars()
        return True
    
    def _calculate_initial_bought(self):
        """Adds keys to the bought dictionary for all symbols and sets them to 
        'OUT'"""
        bought = {}
        for s in self.symbol_list:
            bought[s] = 'OUT'
        return bought
        
    def calculate_signals(self, event):
        """Generates a new set of signals based on the MAC SMA.
        Long: short SMA > long SMA
        """
        if event.type == 'MARKET' and self.data_primed:
            for symbol in self.symbol_list:
                bars = self.bars.get_latest_bars_values(symbol, "close", 
                     N=self.long_window)
                
                if bars is not None and bars != []:
                    short_sma = np.mean(bars[-self.short_window:])
                    long_sma = np.mean(bars[-self.long_window:])
                    
                    dt = self.bars.get_latest_bar_datetime(symbol)
                    sig_dir = "" #direction of signal
                    strength = 1.0  #useful for Mean Reversion
                    strategy_id = 1 #identifier for the strategy
                    
                    if short_sma > long_sma and self.bought[symbol] == "OUT":
                        sig_dir = 'LONG'
                        signal = SignalEvent(strategy_id, symbol, dt, sig_dir,
                                strength)
                        self.events.put(signal)
                        self.bought[symbol] = 'LONG'
                    
                    elif short_sma < long_sma and \
                            self.bought[symbol] == "LONG":
                        sig_dir = 'EXIT'
                        signal = SignalEvent(strategy_id, symbol, dt, sig_dir,
                                strength)
                        self.events.put(signal)
                        self.bought[symbol] = 'OUT'
                
if __name__ == "__main__":
    csv_dir = os.getcwd() + '/../csv'
    symbol_list = ['AAPL']
    initial_capital = 100000.0
    periods = "D"
    start_date = datetime.datetime(1990,1,1,0,0,0)
    end_date = datetime.date.today()
    
    for s in symbol_list:
        if not os.path.isfile(csv_dir + '/%s.csv' % s):
            temp = web.DataReader(s, 'yahoo', start_date, end_date)
            temp.to_csv(csv_dir + '/%s.csv' % s)
    
    backtest = Backtest(
              csv_dir, symbol_list, initial_capital, 0, start_date, 
              HistoricCSVDataHandler , SimulatedExecutionHandler, 
              Portfolio, MovingAverageCrossStrategy,
              #periods , header_format = "yahoo", max_iters = None
              )
    backtest.simulate_trading()
