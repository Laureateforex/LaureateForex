from datetime import datetime
import backtrader as bt
import matplotlib


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

                cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

                # Create a data feed
                data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                                 fromdate=datetime(2016, 1, 1),
                                                 todate=datetime(2019, 5, 31))

                cerebro.adddata(data)  # Add the data feed

                cerebro.addstrategy(SmaCross)  # Add the trading strategy
                cerebro.run()  # run it all
                cerebro.plot()  # and plot it with a single command\