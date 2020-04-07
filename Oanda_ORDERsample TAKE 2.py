import json
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest


client = API(access_token="3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b")
accountID = "101-004-13417875-001"


mo = MarketOrderRequest(instrument="EUR_USD", units=1000)
print(json.dumps(mo.data, indent=4))

r = orders.OrderCreate(accountID, data=mo.data)
rv = client.request(r)
print(rv)
print(json.dumps(rv, indent=4))