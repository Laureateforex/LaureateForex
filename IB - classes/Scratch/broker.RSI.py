from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ContractSamples import ContractSamples
import pandas as pd

n = 14


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.hData = []
        self.df = pd.DataFrame()


    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)



############## E U R O ----- G B P    ##############

    def historicalData(self, reqId: int, bar):
        self.hData.append(bar.close)
        return("HistoricalData. ", reqId, " ,Date:", bar.date, ",Open:", bar.open, ",High:", bar.high, ",Low:", bar.low,
              ",Close:", bar.close, ",Volume:", bar.volume, ",Count:", bar.barCount, ",WAP:", bar.average)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        global n
        self.hData["Close"] = self.hData
        self.hData["Change"] = (self.hData["Close"] - self.hData["Close"].shift(1)).fillna(0)

        self.hData["Up"] = (self.hData["Change"][self.hData["Change"] > 0])
        self.hData["Up"] = self.hData["Up"].fillna(0)

        self.hData["Down"] = (abs(self.hData["Change"])[self.hData["Change"] < 0]).fillna(0)
        self.hData["Down"] = self.hData["Down"].fillna(0)

        self.hData["Ave Up"] = 0.00
        self.hData["Ave Up"][n] = self.hData["Up"][1:n + 1].mean()

        for i in range(n + 1, len(self.hData), 1):
            self.hData["Ave Up"][i] = (self.hData["Ave Up"][i - 1] * (n - 1) + self.hData["Up"][i]) / n

        self.hData["Ave Down"] = 0.00
        self.hData["Ave Down"][n] = self.hData["Down"][1:n + 1].mean()

        for i in range(n + 1, len(self.hData), 1):
            self.hData["Ave Down"][i] = (self.hData["Ave Down"][i - 1] * (n - 1) + self.hData["Down"][i]) / n

        self.hData["Speed"] = (self.hData["Ave Up"] / self.hData["Ave Down"]).fillna(0)

        self.hData["LRP"] = 100 - 100 / (self.hData["Speed"] + 1)
        self.hData["FLRP"] = list(self.hData["LRP"][::-1])

        print(self.hData)

############## E U R O ----- G B P    ##############

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

    contract = ContractSamples.EurUsdFx()

    app.reqHistoricalData(1, contract, "", "1 M", "1 day", "MIDPOINT", 0, 1, False, [])

    app.run()


if __name__ == "__main__":
    main()

