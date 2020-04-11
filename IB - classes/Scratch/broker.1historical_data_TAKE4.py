from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ContractSamples import ContractSamples
import pandas as pd

df = pd.DataFrame()
# new_symbolinput = ['ES', 'NQ']
newDataList = []
dataDownload = []


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def historicalData(self, reqId, bar):
        a = reqId
        d = bar.close
        print(a + d)



def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqHistoricalData(1, contract, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])
    #app.historicalDataOperations_req()

    app.run()


if __name__ == "__main__":
    main()
