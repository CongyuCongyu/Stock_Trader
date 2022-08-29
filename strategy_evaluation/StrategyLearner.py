import datetime as dt
import random
import pandas as pd
import numpy as np
import util as ut
import indicators
import BagLearner
import RTLearner as rt
from marketsimcode import compute_portvals

class StrategyLearner(object):
    # constructor  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        self.verbose = verbose  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        self.impact = impact  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        self.commission = commission
        self.learner = None
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    def add_evidence(
        self,  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        symbol="IBM",  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        sd=dt.datetime(2008, 1, 1),  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        ed=dt.datetime(2009, 1, 1),  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        sv=10000,  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    ):
        random.seed(1234)
        np.random.seed(123)
        syms = [symbol]
        lookback = 5
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)
        prices = prices_all[syms]
        price_on_sma = indicators.SMA(sd, ed, syms, lookback)
        bbp = indicators.BB(sd, ed, syms, lookback)
        normalized_price, normalized_ema = indicators.ema(sd, ed, syms, lookback)
        ema_minus_price = normalized_ema - normalized_price

        three_indicators = pd.concat((price_on_sma, bbp, ema_minus_price), axis=1)
        three_indicators.columns = ['price_on_sma', 'bbp', 'ema_minus_price']
        three_indicators.fillna(0, inplace=True)
        train_x = three_indicators.values
        train_x = train_x[:-1]

        train_y = []
        for i in range(prices.shape[0] - 1):
            ratio = (prices.ix[i + 1, symbol] - prices.ix[i, symbol]) / prices.ix[i, symbol]
            if ratio < (-0.005-self.impact):
                train_y.append(-1)
            elif ratio > (0.005+self.impact):
                train_y.append(1)
            else:
                train_y.append(0)
        train_y = np.array(train_y)
        self.learner = BagLearner.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": 5}, bags=30, boost=False,verbose=False)
        self.learner.add_evidence(train_x, train_y)

  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    def testPolicy(
        self,  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        symbol="IBM",  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        sd=dt.datetime(2009, 1, 1),  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        ed=dt.datetime(2010, 1, 1),  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
        sv=10000,  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
    ):
        syms = [symbol]
        lookback = 5
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        price_on_sma = indicators.SMA(sd, ed, syms, lookback)
        bbp = indicators.BB(sd, ed, syms, lookback)
        normalized_price, normalized_ema = indicators.ema(sd, ed, syms, lookback)
        ema_minus_price = normalized_ema - normalized_price

        three_indicators = pd.concat((price_on_sma, bbp, ema_minus_price), axis=1)
        three_indicators.columns = ['price_on_sma', 'bbp', 'ema_minus_price']
        three_indicators.fillna(0, inplace=True)
        test_x = three_indicators.values
        prediction_y = self.learner.query(test_x)
        prediction_y = prediction_y[0]
        df_trades = prices.copy(deep=True)
        position = 0
        for i in range(prediction_y.shape[0]):
            if (prediction_y[i] == 1):
                df_trades.ix[i] = 1000 - position
                position = 1000
            elif (prediction_y[i] == -1):
                df_trades.ix[i] = -1000 - position
                position = -1000
            else:
                df_trades.ix[i] = 0
        df_trades.ix[-1] = 0
        return df_trades
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
  		  	   		   	 			  		 			     			  	  		 	  	 		 			  		  			
if __name__ == "__main__":
    print("StrategyLearner main")



