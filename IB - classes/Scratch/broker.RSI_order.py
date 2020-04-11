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
        self.hData = []
        self.df = pd.DataFrame()
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

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus. ID: ", orderId, ", Status: ", status, ", filled: ", filled,
              ", Remaining: ", remaining, ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID: ", orderId, contract.symbol, contract.secType, "0", contract.exchange,
              "1", order.action, order.orderType, order.totalQuantity)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails: ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def historicalDataOperations_req(self):
        self.reqHistoricalData(1, ContractSamples.EurGbpFx(), "",
                               "1 M", "1 day", "MIDPOINT", 1, 1, False, [])

    def historicalData(self, reqId: int, bar):
        self.hData.append(bar.close)
        return ("HistoricalData. ", reqId, " ,Date:", bar.date, ",Open:", bar.open, ",High:", bar.high, ",Low:", bar.low,
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

    # order = OrderSamples.MarketOrder("buy", 10)

    app.nextValidId(orderId=1)

    Timer(3, app.stop).start()

    app.run()


if __name__ == "__main__":
    main()

