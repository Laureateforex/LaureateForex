import datetime
from collections import OrderedDict
from oandapyV20.endpoints.pricing import PricingStream

import oandapyV20
import pytz
from oandapyV20 import API
import json
import numpy as np
import pandas as pd
import oandapyV20.endpoints.trades as trades
import requests
from oandapyV20.endpoints.responses import orders
from oandapyV20.exceptions import V20Error

from oandapyV20.contrib.requests import (MarketOrderRequest, TakeProfitDetails, TrailingStopLossDetails)

accountID = "101-004-13417875-001"
client = API(access_token="3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b")

sld = 1.08006 - 1.0690

takeProfitOnFillOrder = TakeProfitDetails(price=1.08006)
trailingStopLossOnFill = TrailingStopLossDetails(distance=sld)
print(takeProfitOnFillOrder.data)
print(trailingStopLossOnFill)

#
# {
#     "timeInForce": "GTC",
#     "distance": "0.00500"
# }

ordr = MarketOrderRequest(instrument="EUR_USD",
                          units=1,
                          takeProfitOnFill=takeProfitOnFillOrder.data)
print(json.dumps(ordr.data, indent=4))

# {
#     "order": {
#         "timeInForce": "FOK",
#         "instrument": "EUR_USD",
#         "units": "10000",
#         "positionFill": "DEFAULT",
#         "type": "MARKET",
#         "takeProfitOnFill": {
#             "timeInForce": "GTC",
#             "price": "1.10000"
#         }
#     }
# }


rv = client.request(r)

from oandapyV20 import API
import oandapyV20.endpoints.trades as trades

api = API(access_token="3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b")
accountID = "101-305-3091856-001"

r = trades.TradesList(accountID)
# show the endpoint as it is constructed for this call
print("REQUEST:{}".format(r))
rv = api.request(r)
print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))