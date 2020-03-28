from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ContractSamples import ContractSamples
from OrderSamples import OrderSamples
from ibapi.ticktype import TickTypeEnum
import pandas as pd
import logging
from threading import Timer
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
        self.hDataD = []
        self.df = pd.DataFrame()
        self.df1 = pd.DataFrame()
        self.atr = pd.DataFrame()
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
            # self.newsOperations_req()
            """contract = ContractSamples.EurGbpFx()
            order = OrderSamples.MarketOrder("buy", 10)
            self.placeOrder(self.nextValidOrderId, contract, order)"""
            print("Executing requests ... finished")

    def stop(self):
        self.done = True
        self.disconnect()
        print("Executing cancels")
        # self.tickDataOperations_cancel()
        # self.marketDepthOperations_cancel()
        print("Executing cancels ... finished")

    def historicalDataOperations_req(self):
        self.reqHistoricalData(1, ContractSamples.EurGbpFx(), "",
                               "1 M", "1 day", "MIDPOINT", 1, 1, False, [])
        self.reqHistoricalData(2, ContractSamples.EurGbpFx(), "",
                               "1 W", "1 hour", "MIDPOINT", 1, 1, False, [])

    def historicalData(self, reqId: int, bar):
        if reqId == 1:
            self.hData.append(bar.close)
        else:
            self.hDataD.append(bar.close)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        self.lrp_hourly()
        self.lrp_daily()
        self.atr_calc()

    def lrp_hourly(self):
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

    def lrp_daily(self):
        global n
        self.df1["CloseD"] = self.hDataD
        self.df1["ChangeD"] = (self.df1["CloseD"] - self.df1["CloseD"].shift(1)).fillna(0)

        self.df1["UpD"] = (self.df1["ChangeD"][self.df1["ChangeD"] > 0])
        self.df1["UpD"] = self.df1["UpD"].fillna(0)

        self.df1["DownD"] = (abs(self.df1["ChangeD"])[self.df1["ChangeD"] < 0]).fillna(0)
        self.df1["DownD"] = self.df1["DownD"].fillna(0)

        self.df1["Ave UpD"] = 0.00
        self.df1["Ave UpD"][n] = self.df1["UpD"][1:n + 1].mean()

        for i in range(n + 1, len(self.df1), 1):
            self.df1["Ave UpD"][i] = (self.df1["Ave UpD"][i - 1] * (n - 1) + self.df1["UpD"][i]) / n

        self.df1["Ave DownD"] = 0.00
        self.df1["Ave DownD"][n] = self.df1["DownD"][1:n + 1].mean()

        for i in range(n + 1, len(self.df1), 1):
            self.df1["Ave DownD"][i] = (self.df1["Ave DownD"][i - 1] * (n - 1) + self.df1["DownD"][i]) / n

        self.df1["SpeedD"] = (self.df1["Ave UpD"] / self.df1["Ave DownD"]).fillna(0)

        self.df1["LRPD"] = 100 - 100 / (self.df1["SpeedD"] + 1)
        self.df1["FLRPD"] = list(self.df1["LRPD"][::-1])

        print(self.df1)

    def atr_calc(self):
        start = (datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(days=n)).strftime('%Y-%m-%d')
        df = self.date[stock][start:date]
        trs = []
        for index, row in df.iterrows():
            tr = max(row['_high'], row['_close']) - min(row['_low'], row['_close'])
            trs.append(tr)
        atr = list(pandas.Series(trs[::-1]).ewm(span=len(trs)).mean())[0]
        return atr_calc()

def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    # order = OrderSamples.MarketOrder("buy", 10)

    app.nextValidId(orderId=1)

    Timer(3, app.stop).start()

    app.run()


if __name__ == "__main__":
    main()

