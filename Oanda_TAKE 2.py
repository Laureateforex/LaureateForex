from __future__ import print_function

import json
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.instruments as v20instruments
import oandapyV20.endpoints.accounts as accounts
import numpy as np
import pandas as pd
client = oandapyV20.API(access_token="3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b")
from collections import OrderedDict

token = "3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b"
accountID = "13417875001"




def DataFrameFactory(r, colmap=None, conv=None):
    def convrec(r, m):
        """convrec - convert OANDA candle record.

        return array of values, dynamically constructed, corresponding with config in mapping m.
        """
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
    # df.rename(columns=colmap, inplace=True)  # no need to use rename, cmap values are ordered
    df.set_index(pd.DatetimeIndex(df['D']), inplace=True)
    del df['D']
    df = df.apply(pd.to_numeric)  # OANDA returns string values: make all numeric
    return df

    dfH  = pd.DataFrame([list(record_converter(rec, cmap)) for rec in r.get('candles')])
    dfH.columns = list(cmap.values())
    # df.rename(columns=colmap, inplace=True)  # no need to use rename, cmap values are ordered
    dfH.set_index(pd.DatetimeIndex(df['D']), inplace=True)
    del dfH['H']
    dfH = df.apply(pd.to_numeric)  # OANDA returns string values: make all numeric
    return dfH

if __name__ == "__main__":
    api = API(access_token=token)
    params = {
        "count": 5,
        "granularity": "D"
    }
    instruments = ["EUR_USD", "EUR_GBP", "AUD_USD"]
    df = dict()

    if __name__ == "__main__":
        api = API(access_token=token)
        params = {
            "count": 5,
            "granularity": "H1"
        }
        instruments = ["EUR_USD", "EUR_GBP", "AUD_USD"]
        dfH = dict()


    for instr in instruments:
        try:
            r = v20instruments.InstrumentsCandles(instrument=instr,
                                                  params=params)
            api.request(r)
        except Exception as err:
            print("Error: {}".format(err))
            exit(2)
        else:
            df.update({instr: DataFrameFactory(r.response)})

    # Do something with the dataframes
    for i in instruments:
        print(df[i].head())

        for instr in instruments:
            try:
                r = v20instruments.InstrumentsCandles(instrument=instr,
                                                      params=params)
                api.request(r)
            except Exception as err:
                print("Error: {}".format(err))
                exit(2)
            else:
                dfH.update({instr: DataFrameFactory(r.response)})


    for i in instruments:
        print(dfH[i].head())

    print(df['EUR_USD'].iloc[4])
    print(df['EUR_GBP'].iloc[4])
    print(df['AUD_USD'].iloc[4])

    print(dfH['EUR_USD'].iloc[4])
    print(dfH['EUR_GBP'].iloc[4])
    print(dfH['AUD_USD'].iloc[4])

    print(accounts.AccountSummary)