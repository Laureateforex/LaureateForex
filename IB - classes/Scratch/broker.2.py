from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ContractSamples import ContractSamples
import datetime
import numpy as np
import json
import requests

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

    contracts = [ContractSamples.EurGbpFx(), ContractSamples.AudChfFx(), ContractSamples.ChfJpyFx(),
                 ContractSamples.EurChfFx(), ContractSamples.EurJpyFx(), ContractSamples.EurUsdFx(),
                 ContractSamples.GbpChfFx(), ContractSamples.GbpJpyFx(), ContractSamples.NzdUsdFx(),
                 ContractSamples.UsdJpyFx()]

    JSONContent = requests.get(contracts).json()
    content = json.dumps(JSONContent, indent = 4, sort_keys=True)

    print(content)

    for i in contracts:
        app.reqContractDetails(1, i)

    app.run()


if __name__ == "__main__":
    main()