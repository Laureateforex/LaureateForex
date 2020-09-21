import json
import pandas as pd
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import logging
from datetime import datetime

token = '49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8'
accountID = "101-004-13417875-007"
api = API(access_token=token, environment="practice")

logging.basicConfig(
    filename="v20.log",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
)

params = {"instruments": "USD_CAD"}

r = pricing.PricingInfo(accountID=accountID, params=params)
rv = api.request(r)
json_str = json.dumps(rv, indent=4)
new_json_str = json_str(["prices"])


json_data = json.loads(rv)
time = json_data['prices'][0]['time']

print(rv)
