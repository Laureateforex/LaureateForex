from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ContractSamples import ContractSamples
import pandas as pd

df = pd.DataFrame()

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        """print("Historical Data: ", reqId, "Date: ", bar.date, "Open: ", bar.open, "High: ", bar.high, "Low: ", bar.low,
                "Close. ", bar.close, "Volume: ", bar.volume, "Count: ", bar.barCount, "WAP: ", bar.average)"""
        df = pd.DataFrame(columns=['Data', 'Date', 'Close'])
        id = reqId
        close = bar.close
        df["ID"] = id
        df["Close"] = close
        print(df)

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

    app.run()


if __name__ == "__main__":
    main()
