from ibapi.contract import *  # @UnusedWildImport


class ContractSamples:

    @staticmethod
    def EurGbpFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "GBP"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def EurUsdFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def UsdJpyFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "USD"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def UsdChfFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "USD"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def EurJpyFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def EurChfFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "EUR"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def AudChfFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "AUD"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def GbpJpyFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "GBP"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def GbpChfFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "GBP"
        contract.secType = "CASH"
        contract.currency = "CHF"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def ChfJpyFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "CHF"
        contract.secType = "CASH"
        contract.currency = "JPY"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract

    @staticmethod
    def NzdUsdFx():
        # ! [cashcontract]
        contract = Contract()
        contract.symbol = "NZD"
        contract.secType = "CASH"
        contract.currency = "USD"
        contract.exchange = "IDEALPRO"
        # ! [cashcontract]
        return contract


def Test():
    from ibapi.utils import ExerciseStaticMethods
    ExerciseStaticMethods(ContractSamples)


if "__main__" == __name__:
    Test()

