from __future__ import print_function

import datetime
import time
import json
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as v20instruments
import oandapyV20.endpoints.accounts as accounts
import numpy as np
import pandas as pd
client = oandapyV20.API(environment="practice", access_token="3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b")
from collections import OrderedDict
from oandapyV20.contrib.requests import (MarketOrderRequest, TakeProfitDetails, StopLossDetails)
import oandapyV20.endpoints.orders as orders
from oandapyV20.exceptions import V20Error
import logging

token = "3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b"
accountID = "101-004-13417875-001"

import requests

if __name__ == "__main__":
    api = API(access_token=token, environment="practice")

    domain = 'api-fxpractice.oanda.com'
    access_token = "3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b"
    account_id = "101-004-13417875-001"
    Pair = "EUR_USD"

    url = "https://" + domain + "/v3/accounts/" + account_id + "/orders"
    header = {"Authorization": "Bearer " + access_token}


    ordr = MarketOrderRequest(instrument="EUR_USD",
                              units=100)

    order_buy = json.dumps(ordr.data, indent=4)

    """ro = orders.OrderCreate(accountID=accountID, data=order_buy)
    print("REQUEST:{}".format(ro))
    print("====================")
    print("r.data")

    response = api.request(ro)"""

    requestdata = requests.post(url, headers=header, params=order_buy)
    print(requestdata)

    """try:
        response = api.request(ro)
    except V20Error as e:
        print("V20Error: {}".format(e))
    else:
        print("Response: {}\n{}".format(ro.status_code,
                                        json.dumps(response, indent=2)))"""