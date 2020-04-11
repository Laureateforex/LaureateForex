from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ContractSamples import ContractSamples
import pandas as pd
import logging
from threading import Timer

n = 14


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.hDataD = []
        self.hData = []
        self.x = pd.DataFrame()
        self.y = pd.DataFrame()
        self.df = pd.DataFrame()
        self.dfd = pd.DataFrame()
        self.globalCancelOnly = False
        self.started = False
        self.nextValidOrderId = None
        self.started = False
        self.done = False

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)
        self.start()

    def start(self):
        if self.started:
            return
        self.started = True

        if self.globalCancelOnly:
            print("Executing GlobalCancel only")
            self.reqGlobalCancel()
        else:
            print("Executing requests")
            self.historicalDataOperations_req()
            print("Executing requests ... finished")

    def stop(self):
        self.done = True
        self.disconnect()

    def historicalDataOperations_req(self):
        self.reqHistoricalData(10, ContractSamples.EurGbpFx(), "",
                               "1 D", "1 hour", "MIDPOINT", 1, 1, True, [])
        self.reqHistoricalData(20, ContractSamples.EurUsdFx(), "",
                               "1 D", "1 hour", "MIDPOINT", 1, 1, False, [])

    def historicalData(self, reqId: int, bar):
        if reqId == 10:
            self.hData.append(bar.close)
        elif reqId == 20:
            self.hDataD.append(bar.close)
        else:
            pass

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        self.data()

    def data(self):
        x = pd.DataFrame(self.hData)
        y = pd.DataFrame(self.hDataD)

        if x.empty:
            del x
        else:
            self.df = pd.DataFrame(x)
            self.hourly()

        if y.empty:
            del y
        else:
            self.x = pd.DataFrame(y)
            self.daily()

    def hourly(self):
        self.df = self.df.rename(columns={0: "Close"})
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

        self.df.loc[self.df["FLRP"] < 33, "match"] = "sell"
        self.df.loc[self.df["FLRP"] < 15, "match"] = "wait"
        self.df.loc[self.df["FLRP"] > 66, "match"] = "buy"
        self.df.loc[self.df["FLRP"] > 80, "match"] = "wait"
        self.df["match"] = self.df["match"].fillna("wait")
        print(self.df)

    def daily(self):
        self.x = self.x.rename(columns={0: "Close"})
        self.x["Change"] = (self.x["Close"] - self.x["Close"].shift(1)).fillna(0)
        print(self.x)

def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)

    app.nextValidId(orderId=1)

    Timer(3, app.stop).start()

    app.run()


if __name__ == "__main__":
    main()

