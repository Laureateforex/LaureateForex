import json
import pandas
import alpha_vantage


from alpha_vantage.alpha_vantage.timeseries import TimeSeries
from pprint import pprint


import json
from oandapyV20 import API
import oandapyV20.endpoints.instruments as v20instruments
import oandapyV20.endpoints.accounts as accounts
import numpy as np
import pandas as pd
from collections import OrderedDict
from oandapyV20.contrib.requests import (MarketOrderRequest, TakeProfitDetails, StopLossDetails)
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
from oandapyV20.exceptions import V20Error
import logging

token = '49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8'
accountID = "101-004-13417875-002"


ts = TimeSeries(key='L1Y06XZSDBOAH1OH',output_format='pandas')
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday(symbol='EURUSD',interval='1min', outputsize='full')
pprint(data.head(5))




import os
import requests
import pandas as pd

# api_key = os.getenv('L1Y06XZSDBOAH1OH')
#
# base_url = 'https://www.alphavantage.co/query?'
# params = {'function': 'FX_INTRADAY',
#   'from_symbol': 'EUR',
#   'to_symbol': 'USD',
#   'interval': '15min',
#   'apikey': api_key}
#
# response = requests.get(base_url, params=params)
#
#
#
# print(response)


