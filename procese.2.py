import pandas as pd
import json
import datetime
import numpy as np


class LFX:
    def run(self):
        fields = ['D', 'O', 'H', 'L', 'C']
        self.read = pd.read_csv('EURUSD_D', usecols=fields)

        def rsi_daily():
            n = 14
            prices = self.read["C"]
            deltas = np.diff(prices)
            seed = deltas[:n + 1]
            up = seed[seed >= 0].sum() / n
            down = -seed[seed < 0].sum() / n
            rs = up / down
            rsi_d = np.zeros_like(prices)
            rsi_d[:n] = 100. - 100. / (1. + rs)

            for i in range(n, len(prices)):
                delta = deltas[i - 1]

                if delta > 0:
                    upval = delta
                    downval = 0.
                else:
                    upval = 0.
                    downval = -delta

                up = (up * (n - 1) + upval) / n
                down = (down * (n - 1) + downval) / n

                rs = up / down
                rsi_d[i] = 100. - 100. / (1. + rs)

                rsi_d = list(rsi_d)

            return rsi_d

        self.read["RSI"] = rsi_daily()
        return self.read

    def backtest(self, end_date=datetime.date.today()):
        df = self.read

        short = {}
        transactions = []
        shorted = []
        cumyield = 0

        for i in range(len(list(df["RSI"]))):
            if df["RSI"][i] > 66:
                v = df.iloc[i, 4]
                # this needs be if right and TP first? based on high value?
                for i in range(len(transactions)):
                    transactions[i]['open_value'] = v
                    transactions[i]['stop_value'] = v * 1.02  # Change to ATR at later date!
                    transactions[i]['yield'] = (transactions[i]['stop_value'] - transactions[i]['open_value']) * 100 / transactions[i]['open_value']
                    cumyield += transactions[i]['yield']
                    print(' Yield: ', transactions[i]['yield'], 'Cumyield:',
                          cumyield)
            else:
                pass
                # this needs to be if wrong and stoploss first? based low value?
                #transactions[i]['last_value'] = v
                #transactions[i]['yield'] = (transactions[i]['short_value'] - transactions[i]['last_value']) * 100 / transactions[i]['short_value']

        graph = {}

        json.dump(transactions, open('transactions.json', 'w'))
        if transactions != []:
            graph = pd.DataFrame.from_dict(graph, orient='index')
            graph = graph.reset_index()
            graph['index'] = pd.to_datetime(graph['index'])
            graph = graph.set_index('index')
            graph = graph.sort_index()
            graph = graph.cumsum()
            plt = graph.plot(title='% yield')
            plt.get_figure().savefig('yield.png')
        return transactions

if __name__ == "__main__":
    lfx = LFX()
    lfx.run()
    lfx.backtest()


