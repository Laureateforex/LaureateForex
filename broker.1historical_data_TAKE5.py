from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ContractSamples import ContractSamples
from ibapi.ticktype import TickTypeEnum
import pandas as pd
import datetime
import ibapi.common

df = pd.DataFrame()

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId: int, bar: ibapi.common.BarData):
        return("Historical Data: ", reqId, "Date: ", bar.date, "Open: ", bar.open, "High: ", bar.high, "Low: ", bar.low,
               "Close: ", bar.close, "Volume: ", bar.volume, "Count: ", bar.barCount, "WAP: ", bar.average)


    def handleHistoricalData(self, reqId: int, bar: ibapi.common.BarData):
        str_reqId = str(reqId)
        str_open = str(bar.open)
        str_high = str(bar.high)
        str_low = str(bar.low)
        str_close = str(bar.close)
        str_volume = str(bar.volume)

        histData = bar.date + "," + str_reqId + "," + str_open + "," + str_high + "," + str_low + "," + str_close + "," + str_volume
        print(histData)

def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqHistoricalData(1, contract, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])
    #app.historicalDataOperations_req()

    app.handleHistoricalData(1, contract)

    app.run()


if __name__ == "__main__":
    main()

