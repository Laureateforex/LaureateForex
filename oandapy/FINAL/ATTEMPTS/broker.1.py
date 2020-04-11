from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ContractSamples import ContractSamples
from ibapi.ticktype import TickTypeEnum


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price, Ticker Id: ", reqId, "tickType: ", TickTypeEnum.to_str(tickType), "Price: ", end=' ')

    def tickSize(self, reqId, tickType, size):
        print("Tick Price, Ticker Id: ", reqId, "tickType: ", TickTypeEnum.to_str(tickType), "size: ", size)


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = ContractSamples.EurGbpFx()

    app.reqMarketDataType(4)
    app.reqMktData(1, contract, "", False, False, [])

    app.run()


if __name__ == "__main__":
    main()