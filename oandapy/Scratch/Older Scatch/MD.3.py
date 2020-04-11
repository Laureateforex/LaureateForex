from Alphas.RsiAlphaModel import RsiAlphaModel
from G10CurrencySelectionModel import G10CurrencySelectionModel


class RSIAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        # Set our main strategy parameters
        self.SetStartDate(2017, 1, 1)  # Set Start Date
        self.SetEndDate(2018, 1, 1)  # Set End Date
        self.SetCash(10000)  # Set Strategy Cash

        RSI_Period = 14  # RSI Look back period
        self.RSI_OB = 68  # RSI Overbought level
        self.RSI_OS = 33  # RSI Oversold level
        self.Allocate = 0.25  # Percentage of captital to allocate

        # Find more symbols here: http://quantconnect.com/data
        self.AddForex("EURGBP", Resolution.Daily)
        self.AddForex("EURUSD", Resolution.Daily)

        self.RSI_Ind = self.RSI("EURGBP", RSI_Period)
        self.RSI_Ind1 = self.RSI("EURUSD", RSI_Period)

        # Ensure that the Indicator has enough data before trading,.
        self.SetWarmUp(RSI_Period)

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.

        Arguments:
            data: Slice object keyed by symbol containing the stock data
        '''

        # Check if we are in the market
        if not self.Portfolio.Invested:
            # If not, we check the RSI Indicator
            if self.RSI_Ind.Current.Value < self.RSI_OS:
                # Buy Apple
                self.SetHoldings("EURGBP", self.Allocate)
        else:
            if self.RSI_Ind.Current.Value > self.RSI_OB:
                # Sell Apple
                self.Liquidate("EURGBP")

        if not self.Portfolio.Invested:
            # If not, we check the RSI Indicator
            if self.RSI_Ind1.Current.Value < self.RSI_OS:
                # Buy Apple
                self.SetHoldings("EURUSD", self.Allocate)
        else:
            if self.RSI_Ind1.Current.Value > self.RSI_OB:
                # Sell Apple
                self.Liquidate("EURUSD")

    """
    def Initialize(self):
        self.SetStartDate(2019, 8, 3)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        # self.AddEquity("SPY", Resolution.Minute)
        self.AddAlpha(RsiAlphaModel(60, Resolution.Minute))


        self.AddUniverseSelection( G10CurrencySelectionModel())


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''

        # if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1) """