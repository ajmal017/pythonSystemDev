#!/usr/bin/python
# -*- coding: utf-8 -*-

# intraday_mr_optemize
from sys import path
import os
path.append(os.getcwd() + '/../engine')
path.append(os.getcwd() + '/../')
import datetime

from itertools import product
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from intraday_ols_mr import IntradayOLSMRStrategy

if __name__ == "__main__":
    csv_dir = os.getcwd() + '/../csv'
    symbol_list = ['CLM14','NGM14']
    initial_capital = 100000.0
    periods = 'M'
    heartbeat = 0.0
    start_date = datetime.datetime(2006,1,3)
    
    """ Create the parameter grid list using cartesian product generator
    [(50, 2.0, 0.5),
    (50, 2.0, 1.0),
    etc... ]
    """

    strat_lookback = [50, 100, 200]
    strat_z_entry = [2.0, 3.0, 4.0]
    strat_z_exit = [0.5, 1.0, 1.5]
    strat_params_list = list(product(
        strat_lookback, strat_z_entry, strat_z_exit
        ))
    
    """ Create a list of dictionaries with the keyword/value pairs
    [{'ols_window': 50, 'zscore_high': 2.0, 'zscore_low': 0.5},
    {'ols_window': 50, 'zscore_high': 2.0, 'zscore_low': 1.0},
    {'ols_window': 50, 'zscore_high': 2.0, 'zscore_low': 1.5},
    etc... ]
    """

    strat_params_dict_list = [
        dict(ols_window=sp[0], zscore_high=sp[1], zscore_low=sp[2])
        for sp in strat_params_list
        ]
    
    backtest = Backtest(
              csv_dir, symbol_list, initial_capital, heartbeat, start_date, 
              HistoricCSVDataHandler , SimulatedExecutionHandler, 
              Portfolio, IntradayOLSMRStrategy, 
              strat_params_dict = strat_params_dict_list
              #periods , header_format = "yahoo", max_iters = None
              )
    backtest.simulate_trading()
