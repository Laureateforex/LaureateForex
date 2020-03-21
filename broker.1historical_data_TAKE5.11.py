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
        self.currentSymbol = "SPY"
        self.hDataCurrent = False
        self.hDataMonthly = False
        self.cDataPrice = 0


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
        self.hDataRecords.append(row)
        self.hDataIndex.append(self.lineCount)
        self.lineCount += 1
        return("HistoricalData. ", reqId, " ,Date:", bar.date, ",Open:", bar.open,",High:", bar.high, ",Low:", bar.low, ",Close:", bar.close, ",Volume:", bar.volume,",Count:", bar.barCount, ",WAP:", bar.average)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        self.hData["columns"] = self.hDataColumns
        self.hData["index"] = self.hDataIndex
        self.hData["data"] = self.hDataRecords

        if(self.currentSymbol == 'SPY'):
            current_file = 'data/spy_current.json'
            month_file = 'data/spy_month.json'
            all_file = 'data/spy.json'
            all_file_csv = 'data/spy.csv'
        elif(self.currentSymbol == 'IWM'):
            current_file = 'data/iwm_current.json'
            month_file = 'data/iwm_month.json'
            all_file = 'data/iwm.json'
            all_file_csv = 'data/iwm.csv'

        jsonDump = json.dumps(self.hData)
        if(self.hDataCurrent):
            with open(current_file, 'w') as f:
                f.write(jsonDump)
            self.hDataCurrent = False
        elif(self.hDataMonthly):
            with open(month_file, 'w') as f:
                f.write(jsonDump)
            self.hDataMonthly = False
        else:
            with open(all_file, 'w') as f:
                #writer = csv.writer(f, delimiter=',', lineterminator='\r\n', quotechar="'")
                f.write(jsonDump)
            w = csv.writer(open(all_file_csv, "wt", newline=''), quoting=csv.QUOTE_NONE, escapechar=' ', quotechar='')
            #w = csv.writer(fw, delimiter=',', lineterminator='\r\n', quotechar="'")

            for item in self.hData.items():
                w.writerow([item[1]])
        #clear hData
        self.hData.clear()
        self.hDataRecords.clear()
        self.hDataIndex.clear()
        self.lineCount = 0

        print("HistoricalDataEnd ", reqId, "from", start, "to", end)
        if(self.isConnected()):
            self.disconnect()

def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqHistoricalData(1, contract, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])

    app.run()


if __name__ == "__main__":
    main()

