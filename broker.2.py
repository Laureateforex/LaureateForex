from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)


def main():
    app = TestApp()

    app.connect("127.0.0.1", 7497, 988)  # LFX comment - this needs to be host, port, client ID

    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.currency = "GBP"
    contract.exchange = "IDEALPRO"

    app.reqContractDetails(1, contract)

    app.run()


if __name__ == "__main__":
    main()