from __future__ import print_function
import datetime
import time
import requests
import oandapyV20
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


token = '2be2ef1ce081e257033450c98e3c952a-479acbb141133abfbb2cee1c5f41d732'
accountID = "101-004-16435253-001"


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


def atr_calc(pair):
    c = list((df[pair].iloc[:, 4]).astype(float))
    h = list((df[pair].iloc[:, 2]).astype(float))
    l = list((df[pair].iloc[:, 3]).astype(float))

    del c[-1]
    del h[0]
    del l[0]

    trs = pd.DataFrame([c, h, l])
    trs = trs.transpose()
    trs.columns = ["c", "h", "l"]

    trz = []
    for index, row in trs.iterrows():
        tr = max((row['h'] - row['l']), abs(row['h'] - row['c']), abs(row['l'] - row['c']))
        trz.append(tr)
    atr = list(pd.Series(trz).ewm(span=50).mean())[-1]
    return atr


def rsi_h_calc(pair):
    d = {"EUR_USD": 15, "EUR_AUD": 16, "GBP_CHF": 14, "USD_JPY": 16, "GBP_CAD": 12, "EUR_JPY": 11, "USD_CHF": 13,
                   "GBP_USD": 15, "GBP_JPY": 13, "AUD_USD": 13, "EUR_CHF": 12, "USD_CAD": 15, "AUD_JPY": 15}
    n = d.get(pair)
    prices = (df[pair].iloc[:,4]).astype(float)
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi_h = np.zeros_like(prices)
    rsi_h[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1]

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


def open_position():
    r_open = positions.OpenPositions(accountID=accountID)
    api.request(r_open)
    x = r_open.response
    x = x.get('positions')
    y = [z['instrument'] for z in x]
    return y


def order_buy_calc(pair, atr):
    d = {"EUR_USD": 3150, "EUR_AUD": 2100, "GBP_CHF": 2350, "USD_JPY": 3850, "GBP_CAD": 2850, "EUR_JPY": 3150, "USD_CHF": 3250,
                   "GBP_USD": 2850, "GBP_JPY": 2850, "AUD_USD": 3350, "EUR_CHF": 2650, "USD_CAD": 3850, "AUD_JPY": 3350}

    t = {"EUR_USD": 2, "EUR_AUD": 2.2, "GBP_CHF": 2.1, "USD_JPY": 2.25, "GBP_CAD": 2.1, "EUR_JPY": 2, "USD_CHF": 2.25,
                   "GBP_USD": 2.15, "GBP_JPY": 2, "AUD_USD": 2, "EUR_CHF": 2.25, "USD_CAD": 2.1, "AUD_JPY": 2.2}

    s = {"EUR_USD": 3, "EUR_AUD": 2.9, "GBP_CHF": 2.9, "USD_JPY": 3, "GBP_CAD": 2.85, "EUR_JPY": 2.9, "USD_CHF": 3,
                   "GBP_USD": 2.85, "GBP_JPY": 2.9, "AUD_USD": 3, "EUR_CHF": 3, "USD_CAD": 2.9, "AUD_JPY": 2.9}

    f = {"EUR_USD": 5,"EUR_AUD": 5, "GBP_CHF": 5, "USD_JPY": 3, "GBP_CAD": 5, "EUR_JPY": 3,
         "USD_CHF": 5, "GBP_USD": 5, "GBP_JPY": 3, "AUD_USD": 5, "EUR_CHF": 5, "USD_CAD": 5, "AUD_JPY": 3}

    price = list((df[pair].iloc[:,4]).astype(float))[-1]
    r = f.get(pair)
    t_p = t.get(pair)
    s_l = s.get(pair)
    atr_sl = round((s_l * atr), r)
    atr_tp = round((t_p * atr), r)
    sl = price - atr_sl
    tp = price + atr_tp
    u = d.get(pair)

    takeProfitOnFillOrder = TakeProfitDetails(price=tp)
    StopLossOnFillOrder = StopLossDetails(price=sl)


    order_buy = MarketOrderRequest(instrument=pair,
                              units=u,
                              takeProfitOnFill=takeProfitOnFillOrder.data,
                              stopLossOnFill=StopLossOnFillOrder.data)

    r = orders.OrderCreate(accountID, data=order_buy.data)
    print("Processing long order on : {}".format(r))
    print("====================")
    print(r.data)

    try:
        response = api.request(r)
    except V20Error as e:
        print("V20Error:{}".format(e))
    else:
        print("Respose: {}\n{}".format(r.status_code,
                                       json.dumps(response, indent=2)))


def order_sell_calc(pair, atr):
    d = {"EUR_USD": 3150, "EUR_AUD": 2100, "GBP_CHF": 2350, "USD_JPY": 3850, "GBP_CAD": 2850, "EUR_JPY": 3150, "USD_CHF": 3250,
                   "GBP_USD": 2850, "GBP_JPY": 2850, "AUD_USD": 3350, "EUR_CHF": 2650, "USD_CAD": 3850, "AUD_JPY": 3350}

    t = {"EUR_USD": 2.2, "EUR_AUD": 2.15, "GBP_CHF": 2.1, "USD_JPY": 2.25, "GBP_CAD": 2.15, "EUR_JPY": 1.75, "USD_CHF": 2.2,
                   "GBP_USD": 2.15, "GBP_JPY": 1.75, "AUD_USD": 2.2, "EUR_CHF": 2, "USD_CAD": 2.1, "AUD_JPY": 1.85}

    s = {"EUR_USD": 3, "EUR_AUD": 2.85, "GBP_CHF": 2.9, "USD_JPY": 2.9, "GBP_CAD": 2.9, "EUR_JPY": 2.5, "USD_CHF": 3,
                   "GBP_USD": 2.85, "GBP_JPY": 2.5, "AUD_USD": 2.85, "EUR_CHF": 3, "USD_CAD": 3, "AUD_JPY": 2.5}

    f = {"EUR_USD": 5,"EUR_AUD": 5, "GBP_CHF": 5, "USD_JPY": 3, "GBP_CAD": 5, "EUR_JPY": 3,
         "USD_CHF": 5, "GBP_USD": 5, "GBP_JPY": 3, "AUD_USD": 5, "EUR_CHF": 5, "USD_CAD": 5, "AUD_JPY": 3}

    price = list((df[pair].iloc[:,4]).astype(float))[-1]
    r = f.get(pair)
    t_p = t.get(pair)
    s_l = s.get(pair)
    atr_sl = round((s_l * atr), r)
    atr_tp = round((t_p * atr), r)
    sl = price + atr_sl
    tp = price - atr_tp
    u = d.get(pair)

    takeProfitOnFillOrder = TakeProfitDetails(price=tp)
    StopLossOnFillOrder = StopLossDetails(price=sl)

    order_sell = MarketOrderRequest(instrument=pair,
                              units=-u,
                              takeProfitOnFill=takeProfitOnFillOrder.data,
                              stopLossOnFill=StopLossOnFillOrder.data)

    r = orders.OrderCreate(accountID, data=order_sell.data)
    print("Processing selling order of : {}".format(r))
    print("====================")
    print(r.data)

    try:
        response = api.request(r)
    except V20Error as e:
        print("V20Error:{}".format(e))
    else:
        print("Respose: {}\n{}".format(r.status_code,
                                       json.dumps(response, indent=2)))

if __name__ == "__main__":
    api = API(access_token=token, environment="practice")
    instruments = ["EUR_USD","EUR_AUD", "GBP_CHF", "USD_JPY", "GBP_CAD", "EUR_JPY", "USD_CHF",
                   "GBP_USD", "GBP_JPY", "AUD_USD", "EUR_CHF", "USD_CAD", "AUD_JPY"]
    params = {
            "count": 50, "granularity": "M15"
    }
    df = dict()

    for instr in instruments:
        try:
            r = v20instruments.InstrumentsCandles(instrument=instr, params=params)
            api.request(r)
        except Exception as err:
            print("Error: {}".format(err))
            exit(2)
        else:
            df.update({instr: DataFrameFactory(r.response)})

    for i in instruments:
        sell_high = {"EUR_USD": 71, "EUR_AUD": 68, "GBP_CHF": 64, "USD_JPY": 66, "GBP_CAD": 74, "EUR_JPY": 66, "USD_CHF": 62,
                   "GBP_USD": 64, "GBP_JPY": 66, "AUD_USD": 74, "EUR_CHF": 66, "USD_CAD": 68, "AUD_JPY": 66}

        sell_low = {"EUR_USD": 70, "EUR_AUD": 67, "GBP_CHF": 63, "USD_JPY": 65, "GBP_CAD": 73, "EUR_JPY": 65, "USD_CHF": 61,
                   "GBP_USD": 63, "GBP_JPY": 65, "AUD_USD": 73, "EUR_CHF": 65, "USD_CAD": 67, "AUD_JPY": 65}

        buy_high = {"EUR_USD": 33, "EUR_AUD": 32, "GBP_CHF": 32, "USD_JPY": 34, "GBP_CAD": 32, "EUR_JPY": 30, "USD_CHF": 26,
                   "GBP_USD": 34, "GBP_JPY": 28, "AUD_USD": 36, "EUR_CHF": 26, "USD_CAD": 32, "AUD_JPY": 29}

        buy_low = {"EUR_USD": 32, "EUR_AUD": 31, "GBP_CHF": 31, "USD_JPY": 33, "GBP_CAD": 31, "EUR_JPY": 29, "USD_CHF": 25,
                   "GBP_USD": 33, "GBP_JPY": 28, "AUD_USD": 35, "EUR_CHF": 25, "USD_CAD": 31, "AUD_JPY": 28}

        bh = buy_high.get(i)
        bl = buy_low.get(i)
        sh = sell_high.get(i)
        sl = sell_low.get(i)

        if bh > rsi_h_calc(i) > bl and not (i in open_position()):
            order_buy_calc(i, atr_calc(i))
        elif sl < rsi_h_calc(i) < sh and not (i in open_position()):
            order_sell_calc(i, atr_calc(i))
        else:
            print("No opportunities in: ", i + " hourly LRP is: ", rsi_h_calc(i), "ATR: ", atr_calc(i))



print(accounts.AccountSummary)