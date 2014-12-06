#!/usr/bin/python
# -*- coding: utf-8 -*-

# intraday_mr_backtest
from sys import path
import os
path.append(os.getcwd() + '/../engine')
path.append(os.getcwd() + '/../')
import datetime

from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from intraday_ols_mr import IntradayOLSMRStrategy

if __name__ == "__main__":
    csv_dir = os.getcwd() + '/../csv'
    symbol_list = ['HOM14','NGM14']
    initial_capital = 100000.0
    heartbeat = 0.0
    start_date = datetime.datetime(2006,1,3)
    
    backtest = Backtest(
              csv_dir, symbol_list, initial_capital, heartbeat, start_date, 
              HistoricCSVDataHandler , SimulatedExecutionHandler, 
              Portfolio, IntradayOLSMRStrategy,
              #periods , header_format = "yahoo", max_iters = None
              )
    backtest.simulate_trading()
