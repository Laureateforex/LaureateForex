import json
import oandapyV20
import oandapyV20.endpoints.orders as orders
from oandapyV20.exceptions import V20Error
from oandapyV20.contrib.requests import (MarketOrderRequest, TakeProfitDetails, StopLossDetails)
import oandapyV20.endpoints.positions as positions
import pandas as pd
import replace
from collections import OrderedDict


api = oandapyV20.API(environment="practice", access_token="49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8")
accountID = "101-004-13417875-002"


my_list = [1, 2, 3, 5]
my_other_list = [1, 2, 4]

for i in my_list:
    if not (i in my_other_list):
        print(i)



"""def open_position():
    r = positions.OpenPositions(accountID=accountID)
    api.request(r)
    x = r.response
    x = x.get('positions')
    y = [z['instrument'] for z in x]
    return y


print(open_position())"""


"""def get_val(dct,key):
    for k, v in dct.iteritems():
        if key in dct.keys():
            print(dct[key])
        else :
            for d in dct.values():
                get_val(d, key)

z = get_val(x, y)"""


"""
orderConf = MarketOrderRequest(instrument="EUR_USD", units=2)

print(orderConf)


r = orders.OrderCreate(accountID, data=orderConf.data)
print("Processing : {}".format(r))
print("====================")
print(r.data)

try:
    response = api.request(r)
except V20Error as e:
    print("V20Error:{}".format(e))
else:
    print("Respose: {}\n{}".format(r.status_code,
                                    json.dumps(response, indent=2)))


def split_dict(m):
    v = []
    for keys in [x.split(",") for x in m.keys()]:
        _v = r.get(keys[0])
        for k in keys[1:]:
            _v = _v.get(k)
        v.append(_v)

    return v

r = positions.OpenPositions(accountID=accountID)

api.request(r)
x = r.response
x = x.get("positions")

for i in x:
    y = list(i.get('instrument'))
    y = y.replace(",", "")"""




"""def DataFrameFactory(r, colmap=None, conv=None):
    def convrec(r, m):
        v = []
        for keys in [x.split(":") for x in m.keys()]:
            _v = r.get(keys[0])
            for k in keys[1:]:
                _v = _v.get(k)
            v.append(_v)

        return v

    record_converter = convrec if conv is None else conv
    column_map_ohlcv = OrderedDict([
        ('instrument', 'instr'),
    ])
    cmap = column_map_ohlcv if colmap is None else colmap

    df = pd.DataFrame([list(record_converter(rec, cmap)) for rec in r.get('candles')])
    df.columns = list(cmap.values())
    return df

r = positions.OpenPositions(accountID=accountID)
api.request(r)
x = DataFrameFactory(r.response)
print(x)"""


