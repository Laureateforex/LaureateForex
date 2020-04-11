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
from oandapyV20.exceptions import V20Error

api = API(access_token="3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b")

accountID = "101-004-13417875-001"

access_token="3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b"

instruments = "EUR_GBP,EUR_USD,EUR_JPY, AUD_USD, EUR_AUD, GBP_CHF"
s = PricingStream(accountID=accountID, params={"Instruments": instruments})

import sys
import json

from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from oandapyV20 import API

access_token = "3943fda13fb4e7085832a01eadfee5ef-3a1a62e075a3e0301b996ae8a632e63b"

client = API(access_token=access_token)

_from = sys.argv[0]
_to = sys.argv[0]
gran = sys.argv[0]
instr = sys.argv[0]

params = {
    "granularity": gran,
    "from": _from,
    "to": _to
}

def cnv(r, h):
    for candle in r.get('candles'):
        ctime = candle.get('time')[0:19]
        try:
            rec = "{time},{complete},{c}".format(
                time=ctime,
                complete=candle['complete'],
                c=candle['mid']['c']
            )
        except Exception as e:
            print(e, r)
        else:
            h.write(rec+"\n")




try:
    n = 0
    for R in api.request(s):
        print(json.dumps(R, indent=2))
        n += 1
        if n > 10:
            s.terminate("maxrecs received: {}".format(MAXREC))

except V20Error as e:
    print("Error: {}".format(e))


def get_data_oanda(num_periods, **keyword_parameters):

    #Sess_t = requests.get('https://github.com', timeout=20)

    domainDict = {"https://api-fxpractice.oanda.com/v3/accounts/101-004-13417875-001/pricing?instruments=AUD_USD"} # Lfx: change when ready: 'live': 'api-fxtrade.oanda.com',
    environment = 'practice'
    domain = domainDict[environment]
    df_data = pd.DataFrame
    instruments = "AUD_USD"
    count = num_periods
    granularity = "H1"

    r = requests.get('https://api-fxpractice.oanda.com/v3/accounts/101-004-13417875-001/', stream=True, timeout=None)

    for line in r.iter_lines():

        # filter out keep-alive new lines
        if line:
            print(json.loads(line))

    while r:
        r.iter_lines()

    try:
        s = requests.Session()
        url = "https://" + domain + "/v3/candles"
        headers = {'Authorization' : 'Bearer' + access_token,
                   # 'X-Accept-Datetime-Format' : 'unix'
                  }
        params = {instruments, accountID, count, granularity}
        req = requests.get(url, timeout=None, headers = headers, params = params, Stream = True)
        pre = req.prepare()
        resp = s.send(pre, stream = True, verify = True, timeout = None)
        return resp
    except Exception as e:
        s.close()
        print()
        print("Caught exception when connecting to stream\n" + str(e))

    num_periods = 50
    my_date = datetime.datetime.now(pytz.timezone('Local Time Zone')).strftime('%Y-%m-%dT%H:%M:%S')
    timezone = 'Local Time Zone'
    response = get_data_oanda(num_periods)
    msg = json.loads(response.text)
    candles = msg['candles']
    for candle in candles:
        df_data.append({
            'date': datetime.datetime.strptime(candle['time'], '%Y-%m-%dT%H:%M:%S.000000Z').replace(tzinfo=pytz.utc).astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S'),
            'instrument': msg['instrument'],
            "close": candle['closeAsk'],
            "volume": candle['volume']
        },ignore_index=True)

r = trades.TradesList(accountID, instruments)
# show the endpoint as it is constructed for this call
print("REQUEST:{}".format(r))
rv = api.request(r)
print("RESPONSE:\n{}".format(json.dumps(rv, indent=20))) #Lfx: these work
print(r)
def demo(displayHeartbeat):
    response = get_data_oanda()
    if response.status_code != 200:

        print(response.text)
        return
    for line in response.iter_lines(1):
        if line:
            try:
                line = line.decode('utf-8')
                msg = json.loads(line)
            except Exception as e:
                print ("Caught exception when converting message into json\n" + str(e))
                print("Caught exception when converting message into json\n" + str(e))
                return

            if displayHeartbeat:
                print(line)
            else:
                if msg.has_key("instrument") or msg.has_key("tick"):
                    print(line)

            if "instrument" in msg or "tick" in msg or displayHeartbeat:
                print(line)



