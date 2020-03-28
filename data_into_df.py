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
        self.x = []
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
            print("Executing requests ... finished")

    def stop(self):
        self.done = True
        self.disconnect()

    def historicalDataOperations_req(self):
        self.reqHistoricalData(1, ContractSamples.EurGbpFx(), "",
                               "1 M", "1 day", "MIDPOINT", 1, 1, False, [])
        self.reqHistoricalData(2, ContractSamples.EurGbpFx(), "",
                               "1 D", "1 hour", "MIDPOINT", 1, 1, False, [])

    def historicalData(self, reqId: int, bar):
        if reqId == 1:
            self.hData.append(bar.close)
        else:
            pass


    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        self.data()

    def data(self):
        self.df["Close"] = self.hData



def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)

    app.nextValidId(orderId=1)

    Timer(3, app.stop).start()

    app.run()


if __name__ == "__main__":
    main()

