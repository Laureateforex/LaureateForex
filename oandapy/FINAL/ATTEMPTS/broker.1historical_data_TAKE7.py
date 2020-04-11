from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
import datetime
import threading
import time
import pandas as pd
import array


class TestApp(EClient):
    def __init__(self,TestWrapper):
        EClient.__init__(self,TestWrapper)

class TestWrapper(EWrapper):
    def __init__(self):
        EWrapper.__init__(self)

    def error(self, reqId: TickerId, errorcode: int, errorString: str):
        print("Error= ", reqId, " ", errorcode, " ", errorString)

    def contratDetails(self, reqId: int, contractDetails: ContractDetails):
        print("ContractDetails: ", reqId, " ", contractDetails)

    def historicalData(self, reqId: int, bar: BarData,):
        return("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open,
                "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
                "Count:", bar.barCount, "WAP:", bar.average)
        historical_data = pd.DataFrame
        historical_data["Close"] = bar.close


    def historicalDataEnd(self, reqId: int, start: str, end: str):
        historical_data = pd.DataFrame
        historical_data["Close"] = bar.close
        #super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd ", reqId, "from", start, "to", end)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        print("HistoricalDataUpdate. ", reqId, " Date:", bar.date, "Open:", bar.open,
              "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume,
              "Count:", bar.barCount, "WAP:", bar.average)

    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId
        print("I have nextValidId", orderId)

def main():
    global RUN_FLAG
    global index
    client = TestApp(TestWrapper())
    client.connect("127.0.0.1", 7497, 988)
    print("connected")

    #  this is the biggest "GOTCHA" in the API docs.
    #  When app.run() is called, the reader is launched, and this will block
    #  the main thread, meaning you'll never get to any of the stuff below.
    #  Instead, maybe launch it in a new thread...
    # The thread management here is very rudimentary but should give you the idea.

    threading.Thread(name="TWSAPI_worker", target=client.run).start()

    # while not RUN_FLAG:
    #     time.sleep(1)
    #     print("Sleeping...")

    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.exchange = "IDEALPRO"
    contract.currency = "USD"

    queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
    client.reqHistoricalData(4101, contract, queryTime, "1 M", "1 day", "MIDPOINT", 1, 1,False,[])


    client.disconnect()
    print("All done")

if __name__ == "__main__":
    main()