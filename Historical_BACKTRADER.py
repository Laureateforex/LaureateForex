import json
from oandapyV20 import API
import pandas as pd
import numpy
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import csv

client = API(access_token='49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8')
instrument, granularity = "GBP_USD", "H1"
_from = "2019-01-01T00:00:00Z"
_to = "2020-01-01T00:00:00Z"
params = {
"from": _from,
"granularity": granularity,
"to": _to
}
with open("//Users/user/PycharmProjects/LaureateForex/{}.{}".format(instrument+"Hourly", granularity), "w") as OUT:

    #
    # reader = csv.DictReader((open("//Users/user/PycharmProjects/LaureateForex/{}.csv")))
    # for raw in reader:
    #         print(raw)

# The factory returns a generator generating consecutive
# requests to retrieve full history from date 'from' till 'to'
    for r in InstrumentsCandlesFactory(instrument=instrument,params=params):
        client.request(r)
    OUT.write(json.dumps(r.response.get('candles'), indent=2))


try:
    my_file_handle=open("//Users/user/PycharmProjects/LaureateForex/{}.csv")
except IOError:
    print("File not found or path is incorrect")
finally:
    print("exit")