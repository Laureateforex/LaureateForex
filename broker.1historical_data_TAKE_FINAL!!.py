from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ContractSamples import ContractSamples
from ibapi.ticktype import TickTypeEnum
import pandas as pd
import json
import datetime
import ibapi.common
import json
import csv

df = pd.DataFrame()


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.hData = []


    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId: int, bar):
        self.hData.append(bar.close)
        return("HistoricalData. ", reqId, " ,Date:", bar.date, ",Open:", bar.open, ",High:", bar.high, ",Low:", bar.low,
              ",Close:", bar.close, ",Volume:", bar.volume, ",Count:", bar.barCount, ",WAP:", bar.average)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        df = pd.DataFrame(self.hData)
        df.columns = ["Close"]
        print(df)


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqHistoricalData(1, contract, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])

    app.run()


if __name__ == "__main__":
    main()

