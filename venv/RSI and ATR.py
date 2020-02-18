class RSIATR(LaureateForex):



self.SetStartDate(2018, 1, 1)
self.SetEndDate(2019, 1, 1)
self.SetCash(10000)

RSI_Period = 14
self.RSI_OB = 63
self.RSI_OS = 33
self.Allocate = 0.25

# Check if we are in the market
        if not self.Portfolio.Invested:
            # If not, we check the RSI Indicator
            if self.RSI_Ind.Current.Value < self.RSI_OS:
                # Buy Apple
                self.SetHoldings("AAPL", self.Allocate)
        else:
            if self.RSI_Ind.Current.Value > self.RSI_OB:
                # Sell Apple
                self.Liquidate("AAPL")

if self.rsi.Current.Value > 63 and self.Portfolio["EURGBP"].Invested <= 0:
    self.Debug("RSI is less then 30")
    self.MarketOrder("EURGBP", "EURUSD", "AUDUSD", "USDCAD", "USDCHF", 25000)
    self.Debug("Market order was placed")
