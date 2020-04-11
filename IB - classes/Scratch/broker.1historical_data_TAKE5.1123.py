from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ContractSamples import ContractSamples
import pandas as pd

df = pd.DataFrame()


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.hData = {}
        self.hDataColumns = ['Date','Open','High','Low','Close','Volume','BarCount','Average']
        self.hDataIndex = []
        self.hDataRecords = []
        self.lineCount = 0

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId: int, bar):
        # row = []
        # row.append(str(bar.date))
        # row.append(bar.open)
        # row.append(bar.high)
        # row.append(bar.low)
        # row.append(bar.close)
        # row.append(bar.volume)
        # row.append(bar.barCount)
        # row.append(bar.average)
        self.hDataRecords.append(bar.close)
        return("HistoricalData. ", reqId, " ,Date:", bar.date, ",Open:", bar.open, ",High:", bar.high, ",Low:", bar.low,
              ",Close:", bar.close, ",Volume:", bar.volume, ",Count:", bar.barCount, ",WAP:", bar.average)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        df = pd.DataFrame(self.hDataRecords)
        df.columns = ["Close"]
        print(df)



        # print(self.hDataRecords)
        """self.hData = self.hDataRecords

        with open('data.json', 'w') as fp:
            json.dump(self.hData, fp)

        json_str = json.dumps(self.hDataRecords)
        self.hDataRecords = json.loads(json_str)
        df = pd.read_json(self.hDataRecords)
        print(df)
        print(self.hData)

        df = pd.read_json(json_str)
        print(df)"""


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqHistoricalData(1, contract, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])

    app.run()


if __name__ == "__main__":
    main()

