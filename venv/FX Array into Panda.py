import oanda_backtest
from collections import OrderedDict

import oandapyV20
from oandapyV20 import API
import json
import numpy as np
import pandas as pd
import oandapyV20.endpoints.trades as trades


pdata = np.array(['a','e','e','k','s'])


account_id = "13417875001"

key = "3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b"

ser = pd.Series(pdata)


print(ser.get(ser.tail(1)))


resp = requests.get(url, headers=headers, params=params, stream=True)
df = pd.read_json(resp.raw)
df_data = pd.io.json.json_normalize(df.candles)
df_data['time'] = pd.to_datetime(df_data.time)



#Fxdataframe =  ({'date: 15,'})