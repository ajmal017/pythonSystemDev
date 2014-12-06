#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import pprint
import Queue
import time
import matplotlib.pyplot as plt

class Backtest(object):
	#event driven backtest
	
    def __init__(self, csv_dir, symbol_list, initial_capital, heartbeat, 
				 start_date, data_handler, execution_handler, portfolio, 
				 strategy, strat_params_dict):
		
		self.csv_dir = csv_dir #csv data dir
		self.symbol_list = symbol_list #list of sym strings
		self.initial_capital = initial_capital # starting capital
		self.heartbeat = heartbeat #outer loop refresh in seconds
		self.start_date = start_date # datetime
		self.data_handler_cls = data_handler #class for mkt data feed
		self.execution_handler_cls = execution_handler # class for order/fills
		self.portfolio_cls = portfolio #portfolio class
		self.strategy_cls = strategy #strategy class
		self.strat_params_dict = strat_params_dict
		self.events = Queue.Queue()
		
        # Counts
		self.signals = 0
		self.orders = 0
		self.fills = 0
		self.num_strates = 1
		
		if self.strat_params_dict is None:
			self._generate_trading_instances()
	
    def _generate_trading_instances(self, strat_params_dict):
        #generates trading instances from their respective classes
        print "Creating DataHander, Strategy, Portfolio and Execution Handler."
        print "strategy parameter list: %s..." % strat_params_dict
        self.data_handler = self.data_handler_cls(
        	self.events, self.csv_dir, self.symbol_list
        	# add self.header_strings
            ) 
        self.strategy = self.strategy_cls(
        	self.data_handler, self.events, **strat_params_dict
        	)
        self.portfolio = self.portfolio_cls(
        	self.data_handler, self.events, self.start_date, 
        	self.initial_capital
        	# add self.num_strats, self.periods
        	)
        self.execution_handler = self.execution_handler_cls(self.events)

    def _run_backtest(self):
        i = 0
        while True:  # Outer loop keeps track of heartbeat of system
            i += 1
            #print i
            # Update the market bars
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()
            else:
                break
            
            # Handle the events
            while True:
                # Check if there is an event in the Queue
                try:
                    event = self.events.get(False)
                except Queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == 'MARKET':
                            self.strategy.calculate_signals(event)
                            self.portfolio.update_timeindex(event)
                        
                        elif event.type == 'SIGNAL':
                            self.signals += 1
                            self.portfolio.update_signal(event)
                        
                        elif event.type == 'ORDER':
                            self.orders += 1
                            self.execution_handler.execute_order(event)
                        
                        elif event.type == 'FILL':
                            self.fills += 1
                            self.portfolio.update_fill(event)
            # Heartbeat                
            time.sleep(self.heartbeat)
    
    def _output_performance(self):
        # Outputs the strategy performance
        #self.portfolio.create_equity_curve_dataframe()
        
        print "Creating summary stats..."
        stats = self.portfolio.output_summary_stats()
        
        print "Creating equity curve..."
        x = self.portfolio.equity_curve.index
        y = self.portfolio.equity_curve['equity_curve']
        y2 = self.portfolio.equity_curve['returns']
        y3 = self.portfolio.equity_curve['ddPercentSeries']
        f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
        ax1.plot(x,y)
        ax1.set_title('Equity Curve')
        ax2.plot(x,y2)
        ax2.set_title('Returns')
        ax3.plot(x,y3)
        ax3.set_title('Drawdown')
        plt.show()
        pprint.pprint(stats)
        
        print "Signals: %s" % self.signals
        print "Orders: %s" % self.orders
        print "Fills: %s" % self.fills
        
        return stats
    
    def simulate_trading(self):
        # Simulates backtest and outputs performance statistics
        
        if self.strat_params_dict is not None:
	        out = open("output.csv", "w")
        
    	    # Prepare Columns in file
        	end_col = ''
        	params_s = ''
        	params = len(self.strat_params_dict[0].keys())
        	for x in range(0,params):
				end_col += self.strat_params_dict[0].keys()[x] + ','
				params_s += '%s,'
			
        	cols = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," % (
        		'Total Return','CAGR', 'Sharpe Ratio',
        		'Sortino Ratio','Annualised MAR','Total Return MAR',
	    		'Max Drawdown','Drawdown Duration','Average DD Duration', 
        		'Average Drawdown', 'Number of Drawdowns'
        		) + end_col 
        		
        	out.write(cols)
        	
        	spl = len(self.strat_params_dict)
        	for i, sp in enumerate(self.strat_params_dict):
        		print "Strategy %s out of %s..." % (i+1, spl)
        		self._generate_trading_instances(sp)
        		self._run_backtest()
        		stats = self._output_performance()
        		
        		line = ''
        		for x in stats:
					line += str(x[1]) +','
        		for x in sp:
					line += str(sp[x]) + ','

        		print line
				
        		out.write(line + '\n')
        	
        	out.close()
        	
        else:
			self._run_backtest()
			self._output_performance()
