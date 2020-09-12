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
from oandapyV20.contrib.requests import PositionCloseRequest
import logging
import smtplib, ssl

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


def SMA25(pair):
    prices = (df[pair].iloc[:,4]).astype(float)
    prices = list(prices)
    prices = pd.DataFrame(prices)
    #del prices[-1]

    smas25 = prices.ewm(span=25, adjust=False).mean()
    smas25 = smas25[0].values.tolist()
    return smas25



def SMA20(pair):
    prices = (df[pair].iloc[:,4]).astype(float)
    prices = list(prices)
    prices = pd.DataFrame(prices)
    #del prices[-1]

    smas20 = prices.ewm(span=20, adjust=False).mean()
    smas20 = smas20[0].values.tolist()
    return smas20


def open_position():
    r_open = positions.OpenPositions(accountID=accountID)
    api.request(r_open)
    x = r_open.response
    x = x.get('positions')
    y = [z['instrument'] for z in x]
    return y


def order_buy_calc(pair):
    d = {"XAG_USD": 41, "XAU_USD": 1, "CORN_USD": 300, "BCO_USD": 28, "NATGAS_USD": 493, "SUGAR_USD": 9150, "WHEAT_USD": 204,
         "XCU_USD": 360, "XPT_USD": 1, "SOYBN_USD": 109}
    u = d.get(pair)
    order_buy = MarketOrderRequest(instrument=pair,
                              units=u)

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


def order_sell_calc(pair):
    d = {"XAG_USD": 41, "XAU_USD": 1, "CORN_USD": 300, "BCO_USD": 28, "NATGAS_USD": 493, "SUGAR_USD": 9150, "WHEAT_USD": 204,
         "XCU_USD": 360, "XPT_USD": 1, "SOYBN_USD": 109}
    u = d.get(pair)
    order_sell = MarketOrderRequest(instrument=pair,
                                    units=-u)

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


def close_order_long(pair):
    d = {"XAG_USD": 41, "XAU_USD": 1, "CORN_USD": 300, "BCO_USD": 28, "NATGAS_USD": 493, "SUGAR_USD": 9150, "WHEAT_USD": 204,
         "XCU_USD": 360, "XPT_USD": 1, "SOYBN_USD": 109}
    u = d.get(pair)
    ordr = PositionCloseRequest(longUnits=u)
    r = positions.PositionClose(accountID=accountID, instrument=pair, data=ordr.data)


    try:
        response = api.request(r)
    except V20Error as e:
        print("V20Error:{}".format(e))
    else:
        print("Respose: {}\n{}".format(r.status_code,
                                       json.dumps(response, indent=2)))


def close_order_short(pair):
    d = {"XAG_USD": 41, "XAU_USD": 1, "CORN_USD": 300, "BCO_USD": 28, "NATGAS_USD": 493, "SUGAR_USD": 9150, "WHEAT_USD": 204,
         "XCU_USD": 360, "XPT_USD": 1, "SOYBN_USD": 109}
    u = d.get(pair)
    ordr = PositionCloseRequest(shortUnits=u)
    r = positions.PositionClose(accountID=accountID, instrument=pair, data=ordr.data)


    try:
        response = api.request(r)
    except V20Error as e:
        print("V20Error:{}".format(e))
    else:
        print("Respose: {}\n{}".format(r.status_code,
                                       json.dumps(response, indent=2)))


if __name__ == "__main__":
    api = API(access_token=token, environment="practice")
    instruments = ["XAG_USD", "XAU_USD", "CORN_USD", "BCO_USD", "NATGAS_USD", "SUGAR_USD", "WHEAT_USD", "XCU_USD",
                   "XPT_USD", "SOYBN_USD"]
    params = {
            "count": 50, "granularity": "H1"
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
        if SMA25(i)[-2] > SMA20(i)[-2] and SMA25(i)[-1] < SMA20(i)[-1]:
            if i in open_position():
                close_order_short(i)
                order_buy_calc(i)
            elif not (i in open_position()):
                order_buy_calc(i)
            else:
                pass
        elif SMA25(i)[-2] < SMA20(i)[-2] and SMA25(i)[-1] > SMA20(i)[-1]:
            if i in open_position():
                close_order_long(i)
                order_sell_calc(i)
            elif not (i in open_position()):
                order_sell_calc(i)
            else:
                pass
        else:
            print("wait")



print(accounts.AccountSummary)