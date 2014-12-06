#!/usr/bin/python

from sys import path
import os
path.append(os.getcwd() + '/../engine')
path.append(os.getcwd() + '/../')
import pandas as pd
import performance

if __name__ == "__main__":
  data = pd.io.parsers.read_csv(
    'AAPL.csv', header=0, index_col=0, parse_dates=True, 
    names=['datetime','open','low','high','close','volume','oi']
    ).sort()

  returns = data['close'].pct_change()
  data['returns'] = returns
  sharpe_ratio = performance.annualised_sharpe(returns, N=252)
  sortino_ratio = performance.annualised_sortino(returns, N=252)
  ddstats = performance.dd_stats(returns, N=252)
  annualised_mar = ddstats[0]
  total_return_mar = ddstats[1]
  maxDD = ddstats[2]
  maxDDduration = ddstats[3]
  averageDDduration = ddstats[4]
  numberDDs = ddstats[5]
  averageDD = ddstats[6]
  data['equity_curve'] = ddstats[7]
  data['ddPercentSeries'] = ddstats[8]
  ccr_total_return = ddstats[9]
  total_return = ddstats[10]
  cagr = ddstats[11]

  stats = [('Total Return', '%0.2f%%' % ((total_return)*100.0)), 
        ('CAGR', '%0.2f%%' % ((cagr)*100.0)),
        ('Sharpe Ratio', '%0.2f' % sharpe_ratio), 
        ('Sortino Ratio', '%0.2f' % sortino_ratio), 
        ('Annualised MAR', '%0.2f' % annualised_mar), 
        ('Total Return MAR', '%0.2f' % total_return_mar), 
	    ('Max Drawdown', '%0.2f%%' % (maxDD*100.0)), 
	    ('Drawdown Duration', '%d'% maxDDduration , ' periods' ),
        ('Average DD Duration', '%0.2f' % averageDDduration, ' periods' ), 
        ('Average Drawdown', '%0.2f%%' % averageDD), 
	    ('Number of Drawdowns', '%d' % numberDDs)
        ]
