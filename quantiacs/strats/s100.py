### Quantiacs Mean Reversion Trading System Example
# import necessary Packages below:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

bars=set();
symbols=('F_CL','F_NG');
sym0_idx=1;
sym1_idx=2;
isInTrade=False;

pairs=pd.DataFrame({}, columns=['datetime','open','high','low','close','volume','na']);
#datadir = 'tickerData'  # Change this to reflect your data path!
#pairs = create_pairs_dataframe(datadir, symbols)

def create_pairs_dataframe(datadir, symbols):
    """Creates a pandas DataFrame containing the closing price
    of a pair of symbols based on CSV files containing a datetime
    stamp and OHLCV data."""

    # Open the individual CSV files and read into pandas DataFrames
    print "Importing CSV data..."
    sym1 = pd.io.parsers.read_csv(os.path.join(datadir, '%s.txt' % symbols[0]),
                                  header=0, index_col=0,
                                  names=['datetime','open','high','low','close','volume','na'])
    sym2 = pd.io.parsers.read_csv(os.path.join(datadir, '%s.txt' % symbols[1]),
                                  header=0, index_col=0,
                                  names=['datetime','open','high','low','close','volume','na'])

    # Create a pandas DataFrame with the close prices of each symbol
    # correctly aligned and dropping missing entries
    print "Constructing dual matrix for %s and %s..." % symbols
    pairs = pd.DataFrame(index=sym1.index)
    pairs['%s_close' % symbols[0].lower()] = sym1['close']
    pairs['%s_close' % symbols[1].lower()] = sym2['close']
    pairs = pairs.dropna()
    return pairs

def calculate_spread_zscore(pairs, symbols, lookback=100):
    """Creates a hedge ratio between the two symbols by calculating
    a rolling linear regression with a defined lookback period. This
    is then used to create a z-score of the 'spread' between the two
    symbols based on a linear combination of the two."""

    # Use the pandas Ordinary Least Squares method to fit a rolling
    # linear regression between the two closing price time series
    #print "Fitting the rolling Linear Regression..."
    model = pd.ols(y=pairs['%s_close' % symbols[0].lower()],
                   x=pairs['%s_close' % symbols[1].lower()],
                   window=lookback)

    # Construct the hedge ratio and eliminate the first
    # lookback-length empty/NaN period
    pairs['hedge_ratio'] = model.beta['x']
    #pairs = pairs.dropna()

    # Create the spread and then a z-score of the spread
    #print "Creating the spread/zscore columns..."
    pairs['spread'] = pairs['%s_close' % symbols[0].lower()] - pairs['hedge_ratio']*pairs['%s_close' % symbols[1].lower()]
    pairs['zscore'] = (pairs['spread'] - np.mean(pairs['spread']))/np.std(pairs['spread'])
   
    return pairs

##### Do not change this function definition #####
def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    global pairs;
    global symbols;
    global isInTrade;
    # This system uses mean reversion techniques to allocate capital into the desired equities

    # This strategy evaluates two averages over time of the close over a long/short
    # scale and builds the ratio. For each day, "smaQuot" is an array of "nMarkets"
    # size.
    nMarkets = np.shape(CLOSE)[1]
    nDates=DATE;
    closePrices=pd.DataFrame(CLOSE, columns=settings['markets']); 
    #print 'nmarkets: %s closePrices: %s' % (symbols[0], closePrices[symbols[0]])
    #print 'nmarkets: %s ' % (nMarkets)
    pairs['%s_close' % symbols[0].lower()] = closePrices[symbols[0]]; #np.take(CLOSE, sym0_idx, axis=1);
    pairs['%s_close' % symbols[1].lower()] = closePrices[symbols[1]]; #np.take(CLOSE, sym1_idx, axis=1);
    pairs = calculate_spread_zscore(pairs, symbols, 200)
    z_entry_threshold=2.0
    z_exit_threshold=1.0

    # Calculate when to be long, short and when to exit
    pos= np.zeros((1,nMarkets))
    if pairs['zscore'] is None:
	return pos, settings;

    #print 'zscore: %5.3f ' % (pairs['zscore'].iget(-1))
    if isInTrade is False and pairs['zscore'].iget(-1) <= -z_entry_threshold:
    	pos[0,sym0_idx] = 1
    	pos[0,sym1_idx] = -1
	print 'date: %d entry, zscore: %5.3f' % (nDates[sym0_idx], pairs['zscore'].iget(-1))
	isInTrade=True
    if isInTrade is False and pairs['zscore'].iget(-1)  >= z_entry_threshold:
	pos[0,sym0_idx] = -1
        pos[0,sym1_idx] = 1
	print 'date: %d entry 2, zscore: %5.3f' % (nDates[sym0_idx], pairs['zscore'].iget(-1))
	isInTrade=True
    if isInTrade and np.abs(pairs['zscore'].iget(-1)) <= z_exit_threshold:
	pos[0,sym0_idx] = 0
        pos[0,sym1_idx] = 0 
	print 'date: %d exit, zscore: %5.3f' % (nDates[sym0_idx], pairs['zscore'].iget(-1))
	isInTrade=False
    #periodLong= 200
    #periodShort= 40

    #smaLong=   np.sum(CLOSE[-periodLong:,:], axis=0)/periodLong
    #smaRecent= np.sum(CLOSE[-periodShort:,:],axis=0)/periodShort
    #smaQuot= smaRecent / smaLong

    # For each day, scan the ratio of moving averages over the markets and find the
    # market with the maximum ratio and the market with the minimum ratio:
    #longEquity = np.where(smaQuot == np.nanmin(smaQuot))
    #shortEquity= np.where(smaQuot == np.nanmax(smaQuot))

    # Take a contrarian view, going long the market with the minimum ratio and
    # going short the market with the maximum ratio. The array "pos" will contain
    # all zero entries except for those cases where we go long (1) and short (-1):
    #pos= np.zeros((1,nMarkets))
    #pos[0,longEquity[0][0]] = 1
    #pos[0,shortEquity[0][0]]= -1

    # For the position sizing, we supply a vector of weights defining our
    # exposure to the markets in settings['markets']. This vector should be
    # normalized.
    pos= pos/np.nansum(abs(pos))

    return pos, settings


##### Do not change this function definition #####
def mySettings():
    # Default competition and evaluation mySettings
    settings= {}

    # S&P 100 stocks
    # settings['markets']=['CASH','AAPL','ABBV','ABT','ACN','AEP','AIG','ALL', \
    # 'AMGN','AMZN','APA','APC','AXP','BA','BAC','BAX','BK','BMY','BRKB','C', \
    # 'CAT','CL','CMCSA','COF','COP','COST','CSCO','CVS','CVX','DD','DIS','DOW',\
    # 'DVN','EBAY','EMC','EMR','EXC','F','FB','FCX','FDX','FOXA','GD','GE', \
    # 'GILD','GM','GOOGL','GS','HAL','HD','HON','HPQ','IBM','INTC','JNJ','JPM', \
    # 'KO','LLY','LMT','LOW','MA','MCD','MDLZ','MDT','MET','MMM','MO','MON', \
    # 'MRK','MS','MSFT','NKE','NOV','NSC','ORCL','OXY','PEP','PFE','PG','PM', \
    # 'QCOM','RTN','SBUX','SLB','SO','SPG','T','TGT','TWX','TXN','UNH','UNP', \
    # 'UPS','USB','UTX','V','VZ','WAG','WFC','WMT','XOM']

    # Futures Contracts
    settings['markets']  = ['CASH','F_CL','F_NG'] #, 'F_AD', 'F_BO', 'F_BP', 'F_C', 'F_CD',  \
    #'F_DJ', 'F_EC', 'F_ES', 'F_FV', 'F_GC', 'F_HG', 'F_HO', 'F_LC', \
    #'F_LN', 'F_NQ', 'F_RB', 'F_S', 'F_SF', 'F_SI', 'F_SM', 'F_SP', \
    #'F_TY', 'F_US', 'F_W', 'F_YM']


    settings['lookback']= 504
    settings['budget']= 10**6
    settings['slippage']= 0.05

    return settings

