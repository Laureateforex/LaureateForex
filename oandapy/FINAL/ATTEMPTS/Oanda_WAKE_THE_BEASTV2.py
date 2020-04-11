
from __future__ import print_function

import datetime
import time
import json
from distutils.command.config import config

import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as v20instruments
import oandapyV20.endpoints.accounts as accounts
import numpy as np
import pandas as pd
from oandapyV20.endpoints import trades, pricing

from Oanda_WAKE_THE_BEAST import access_token

client = oandapyV20.API(environment="practice",
                        access_token="49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8")
from collections import OrderedDict
from oandapyV20.contrib.requests import (MarketOrderRequest, TakeProfitDetails, StopLossDetails)
import oandapyV20.endpoints.orders as orders
from oandapyV20.exceptions import V20Error
import logging
import requests

token = '49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8'
accountID = "101-004-13417875-002"
#Authorizaion = '49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8'

Bearer = '49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8'

domain = "api-fxpractice.oanda.com"
url =  "https://" + domain + "/v3/accounts/" + accountID + "/orders"
header = {'POST'+'Authorization': 'Bearer: '"49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8"  + 'Content-Type: application/json'}

###header = {'POST'+'Authorization': 'Bearer ' + 'Content-Type: application/json'}


#headers = {"Authorization": "Bearer " + "Content-type: a





# get a list of trades


from oandapyV20 import API
import oandapyV20.endpoints.trades as trades

api = API(access_token=token)
accountID = "101-305-3091856-001"
#class oandapyV20.API(access_token,environment=’practice’,headers=None,request_params=None)

import oandapyV20.endpoints.accounts as accounts

client = oandapyV20.API(access_token=token)

r = accounts.AccountChanges(accountID=accountID, params=params)
client.request(r)
print(r.response)