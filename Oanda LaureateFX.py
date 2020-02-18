import requests

#account_id = "13417875001"

#key = "12a1f42967bc9ce1cd0ebf8f46da9a02-03ab1a77bb8478b89690ca77adcbf934"



#Get prices:

#Next, we will create an instance of the oandapy.API,
# as the oanda variable with the following code.
# The get_prices method is invoked by passing the instruments parameter with a string value of EUR_USD
# so that the rates of the EUR/USD currency pair are fetched:

# import oandapy
# oanda = oandapy.API(environment="practice", access_token=key)
# response = oanda.get_prices(instruments="EUR_USD")
# response_usdcad = oanda.get_prices(instruments="USD_CAD")

import pandas as pd
import numpy as np
import pandas_datareader as dr
import matplotlib as plot


#chart_sec = "H1"





#data = oanda.get_history(instrument='EUR_USD',
                                   # start='2019-01-01',
                        # end='2020-01-01',
                         #granularity='D')

#df = pd.DataFrame(data['candles'])


#prices = response["prices"]
#prices_usdcad = response_usdcad["prices"]

# bidding_price = float(prices[0]["bid"])
# bidding_price_usdcad = float(prices_usdcad[0]["bid"])
#
# asking_price = float(prices[0]["bid"])
# asking_price_usdcad = float(prices_usdcad[0]["bid"])
#
#
# instrument = prices[0]["instrument"]
# instrument_usdcad = prices_usdcad[0]["instrument"]
#
# time = prices[0]["time"]
# time_usdcad = prices_usdcad[0]["time"]


#datafx = np.array({'EURUSD':[prices_usdcad],'USDCAD':[prices_usdcad]})

#datafx = np.array(['1','2', '3', '4', '5', '6', '7', '8', '9'])

fxseries = pd.Series(['1','2', '3', '4', '5', '6', '7', '8', '9'])
fxseries['Hourly RSI']

fxseriescurrencypairindex = ['EURUSD','USDCAD', 'GBPUSD', 'GBPAUD', 'GBPCHF', 'GBPJPY', 'USDJPY', 'EURCAD', 'EURJPY']
fxseries.index = fxseriescurrencypairindex
fxHourlyRSI =pd.Series(['RSIH1','RSIH2','RSIH3','RSIH4','RSIH5','RSIH6','RSIH7','RSIH8','RSIH'])
print(fxseries)


#print ("[%s] %s bid=%s ask=%s" % (time, instrument, bidding_price, asking_price))

#print ("[%s] %s bid=%s ask=%s" % (time_usdcad, instrument_usdcad, bidding_price_usdcad, asking_price_usdcad))
