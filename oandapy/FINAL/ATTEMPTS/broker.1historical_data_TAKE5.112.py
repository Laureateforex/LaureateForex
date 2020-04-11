from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ContractSamples import ContractSamples
from ibapi.ticktype import TickTypeEnum
import pandas as pd
import datetime
import ibapi.common
import json
import csv

df = pd.DataFrame()


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.hData = {}
        self.hDataColumns = ['Date','Open','High','Low','Close','Volume','BarCount','Average']
        self.hDataIndex = []
        self.hDataRecords = []
        self.lineCount = 0
        self.df = pd.DataFrame()


    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId:int, bar):
        row = []
        row.append(str(bar.date))
        row.append(bar.open)
        row.append(bar.high)
        row.append(bar.low)
        row.append(bar.close)
        row.append(bar.volume)
        row.append(bar.barCount)
        row.append(bar.average)
        self.df.append(row)
        print(df)
        return("HistoricalData. ", reqId, " ,Date:", bar.date, ",Open:", bar.open,",High:", bar.high, ",Low:", bar.low, ",Close:", bar.close, ",Volume:", bar.volume,",Count:", bar.barCount, ",WAP:", bar.average)


def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        self.hData["columns"] = self.hDataColumns
        self.hData["index"] = self.hDataIndex
        self.hData["data"] = self.hDataRecords
        print(df)


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqHistoricalData(1, contract, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])


    app.run()


if __name__ == "__main__":
    main()

