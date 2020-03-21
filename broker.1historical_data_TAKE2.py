from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ContractSamples import ContractSamples
from ibapi.ticktype import TickTypeEnum
import pandas as pd
import datetime

df = pd.DataFrame()

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        data = {'Data':  [reqId],
                'Date': [bar.date],
                'Close': [bar.close],
                }
        data = pd.DataFrame(data, columns=['Data', 'Date', 'Close'])
        result = pd.concat(data)
        print(result)

"""
    def historicalDataOperations_req(self):
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        self.reqHistoricalData(1, ContractSamples.EurGbpFx(), queryTime,
                               "1 D", "1 hour", "Close", 1, 1, False, [])"""
"""print("Historical Data: ", reqId, "Date: ", bar.date, "Open: ", bar.open, "High: ", bar.high, "Low: ", bar.low,
                "Close. ", bar.close, "Volume: ", bar.volume, "Count: ", bar.barCount, "WAP: ", bar.average)"""


"""
    def data_to_df(self):
        self.df["Change"] = (self.df["Close"] - self.df["Close"].shift(1)).fillna(0)
        print(df)
"""

def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqHistoricalData(1, contract, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])
    #app.historicalDataOperations_req()

    app.run()


if __name__ == "__main__":
    main()

