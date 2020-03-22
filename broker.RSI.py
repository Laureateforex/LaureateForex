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

n = 14


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.hData = []
        self.df = pd.DataFrame()

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId: int, bar):
        self.hData.append(bar.close)
        return("HistoricalData. ", reqId, " ,Date:", bar.date, ",Open:", bar.open, ",High:", bar.high, ",Low:", bar.low,
              ",Close:", bar.close, ",Volume:", bar.volume, ",Count:", bar.barCount, ",WAP:", bar.average)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        global n
        self.df["Close"] = self.hData
        self.df["Change"] = (self.df["Close"] - self.df["Close"].shift(1)).fillna(0)

        self.df["Up"] = (self.df["Change"][self.df["Change"] > 0])
        self.df["Up"] = self.df["Up"].fillna(0)

        self.df["Down"] = (abs(self.df["Change"])[self.df["Change"] < 0]).fillna(0)
        self.df["Down"] = self.df["Down"].fillna(0)

        self.df["Ave Up"] = 0.00
        self.df["Ave Up"][n] = self.df["Up"][1:n + 1].mean()

        for i in range(n + 1, len(self.df), 1):
            self.df["Ave Up"][i] = (self.df["Ave Up"][i - 1] * (n - 1) + self.df["Up"][i]) / n

        self.df["Ave Down"] = 0.00
        self.df["Ave Down"][n] = self.df["Down"][1:n + 1].mean()

        for i in range(n + 1, len(self.df), 1):
            self.df["Ave Down"][i] = (self.df["Ave Down"][i - 1] * (n - 1) + self.df["Down"][i]) / n

        self.df["Speed"] = (self.df["Ave Up"] / self.df["Ave Down"]).fillna(0)

        self.df["LRP"] = 100 - 100 / (self.df["Speed"] + 1)
        self.df["FLRP"] = list(self.df["LRP"][::-1])

        print(self.df)


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqHistoricalData(1, contract, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])

    app.run()


if __name__ == "__main__":
    main()

