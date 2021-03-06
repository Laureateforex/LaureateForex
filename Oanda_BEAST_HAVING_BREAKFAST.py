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


#headers = {"Authorization": "Bearer " + "Content-type: application/json"}
#headers = {"Authorization": "Bearer " + access_token}
logging.basicConfig(
filename="v20.log",
level=logging.INFO,
format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
)


def DataFrameFactory(r, colmap=None, conv=None):
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
        ('time', 'D'),
        ('mid:o', 'O'),
        ('mid:h', 'H'),
        ('mid:l', 'L'),
        ('mid:c', 'C'),
        ('volume', 'V')
    ])
    cmap = column_map_ohlcv if colmap is None else colmap

    df = pd.DataFrame([list(record_converter(rec, cmap)) for rec in r.get('candles')])
    df.columns = list(cmap.values())
    return df


def DataFrameFactory_h(r, colmap=None, conv=None):
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
        ('time', 'D'),
        ('mid:o', 'O'),
        ('mid:h', 'H'),
        ('mid:l', 'L'),
        ('mid:c', 'C'),
        ('volume', 'V')
    ])
    cmap = column_map_ohlcv if colmap is None else colmap

    df_h = pd.DataFrame([list(record_converter(rec, cmap)) for rec in r.get('candles')])
    df_h.columns = list(cmap.values())
    return df_h


def atr_calc(pair):
    c = list((df[pair].iloc[1:, 4]).astype(float))
    h = list((df[pair].iloc[:, 2]).astype(float))
    l = list((df[pair].iloc[:, 3]).astype(float))

    trs = pd.DataFrame([c, h, l])
    trs = trs.transpose()
    trs.columns = ["c", "h", "l"]

    trz = []
    for index, row in trs.iterrows():
        tr = max((row['h'] - row['l']), abs(row['h'] - row['c']), abs(row['l'] - row['c']))
        trz.append(tr)
    atr = list(pd.Series(trz).ewm(span=14).mean())[0]
    return atr


def rsi_d_calc(pair):
    n = 14
    prices = (df[pair].iloc[:,4]).astype(float)
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi_d = np.zeros_like(prices)
    rsi_d[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi_d[i] = 100. - 100./(1.+rs)

    return rsi_d[-1]


def rsi_h_calc(pair):
    n = 14
    prices = (df_h[pair].iloc[:,4]).astype(float)
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi_h = np.zeros_like(prices)
    rsi_h[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi_h[i] = 100. - 100./(1.+rs)

    return rsi_h[-1]


def order_buy_calc(pair, atr):
    price = (df_h[pair].iloc[:,4]).astype(float)[0]
    sl = price - (1 * (atr * 0.50))
    tp = price + (1 * (atr * 0.50))

    # print("the price for", i, "is: ", price)
    # print("the tp for", i, "is: ", tp)
    # print("the sl for", i, "is: ", sl)

    takeProfitOnFillOrder = TakeProfitDetails(price=tp)
    StopLossOnFillOrder = StopLossDetails(price=sl)

    print(takeProfitOnFillOrder.data)
    print(StopLossOnFillOrder.data)


    #############
    #############
    #############          CHECK ORDER  BELOW ....
    #############
    #############

    # requests.post(url, data=order_b)

    ordr = MarketOrderRequest(instrument=pair,
                              units=1,
                              takeProfitOnFill=takeProfitOnFillOrder.data,
                              stopLossOnFill=StopLossOnFillOrder.data)
    order_buy = json.dumps(ordr.data, indent=4)

    requestdata = requests.post(url=url, data=order_buy)

    # print(requestdata)
    # return requestdata





if __name__ == "__main__":
    api = API(access_token="49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8", environment="practice")
    params = {
            "count": 25, "granularity": "D"
    }
    instruments = ["EUR_USD","EUR_AUD", "GBP_CHF", "USD_JPY", "GBP_CAD", "EUR_GBP", "USD_CHF",
                   "GBP_USD", "GBP_JPY", "AUD_USD", "AUD_JPY", "EUR_CHF", "USD_CAD", "CHF_JPY"]
    df = dict()
#orders.endpoint(url,"GET",200),
    params_h = {
        "count": 25,
        "granularity": "H1"
    }
    df_h = dict()

    for instr in instruments:
        try:
            r = v20instruments.InstrumentsCandles(instrument=instr, params=params)
            api.request(r)
        except Exception as err:
            print("Error: {}".format(err))
            exit(2)
        else:
            df.update({instr: DataFrameFactory(r.response)})

    for instr in instruments:
        try:
            r_h = v20instruments.InstrumentsCandles(instrument=instr, params=params_h)
            api.request(r_h)
        except Exception as err:
            print("Error: {}".format(err))
            exit(2)
        else:
            df_h.update({instr: DataFrameFactory_h(r_h.response)})

    """for i in instruments:
        print("The hourly LRP for ", i, "is:")
        print(rsi_h_calc(i))
        print("The daily LRP for ", i, "is:")
        print(rsi_d_calc(i))
        print("The ATR for ", i, "is:")
        print(atr_calc(i))"""

    for i in instruments:
        if rsi_d_calc(i) > 66 and rsi_h_calc(i) > 66:
            print("buy: ", i) and requests.post(url=url, data=instruments, side="BUY")
        elif rsi_d_calc(i) < 33 and rsi_h_calc(i) < 33:
            print("sell: ", i) and requests.post(url=url, data=instruments, side="SELL")
        else:
            order_buy_calc(i, atr_calc(i))
    #############
    #############
    #############           WE  HAVE  TO  LINK  THE  ABOVE  4 LINES  TO  BELOW ....
#############
#############
#############


orderConf =            [


            {
                "order": {
                    "units": "1",
                    "instrument": "EUR_USD",
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }


]
for O in orderConf:
            r = orders.OrderCreate(accountID, data=O)
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

            # for ob in order_buy_calc(i, atr_calc(i)):
            #     ro = orders.OrderCreate(accountID=accountID,data=p)
            # headers = {'Content-type': 'application/json'}
            #
            # for ob in order_buy_calc(i, atr_calc(i)):
            #     ro = orders.OrderCreate(accountID=accountID, data=ob)
            #     print("REQUEST:{}".format(ro))
            #     print("====================")
            #     print("r.data")
            #
            #     try:
            #         response = api.request(ro)
            #     except V20Error as e:
            #         print("V20Error: {}".format(e))
            #     else:
            #         print("Response: {}\n{}".format(ro.status_code,
            #                                         json.dumps(response, indent=2)))



print(accounts.AccountSummary)

# # list of requests
# lor = []
# # request trades list
# lor.append(trades.TradesList(accountID))
# # request accounts list
# lor.append(accounts.AccountList())
# # request pricing info
# params={"instruments": "DE30_EUR,EUR_GBP"}
# lor.append(pricing.PricingInfo(accountID, params=params))
#
# for r in lor:
#     try:
#         rv = client.request(r)
#         # put request and response in 1 JSON structure
#         print("{}".format(json.dumps({"request": "{}".format(r),
#                                       "response": rv}, indent=2)))
#
#
#     except V20Error as e:
#         print("OOPS: {:d} {:s}".format(e.code, e.msg))


# import oandapyV20.endpoints.accounts as accounts
# #
# # client = oandapyV20.API(access_token=token)
# #
# # r = accounts.AccountChanges(accountID=accountID, params=None)
# # client.request(r)
# # print(r.response)