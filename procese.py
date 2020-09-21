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
        print(df)

        short = {}
        transactions = []
        shorted = []
        cumyield = 0

        for i in range(605):
            # if i % 100 == 0:
            #             #     json.dump(transactions, open('transactions.json', 'w'))
            #             # date = end_date - datetime.timedelta(days=605 - i)
            #             # datestr = date.strftime('%Y-%m-%d')
            #             # print(date)
            #             # wl = self.get_52_week_stocks(date)

            for i in range(len(transactions)):
                if transactions[i]['status'] == 'open':
                    stock = transactions[i]['stock']
                    if not self.stocks[stock][datestr:datestr].empty:
                        v = self.stocks[stock].loc[datestr]['Close']
                        last_value = transactions[i]['last_value']
                        if v > last_value:
                            # Stop
                            transactions[i]['last_value'] = v
                            transactions[i]['stop_value'] = v
                            transactions[i]['close_date'] = datestr
                            transactions[i]['status'] = 'closed'
                            transactions[i]['yield'] = (transactions[i]['short_value'] - transactions[i]['last_value']) * 100 / transactions[i]['short_value']
                            cumyield += transactions[i]['yield']
                            print('**Closed: ', transactions[i]['stock'], ' Yield: ', transactions[i]['yield'], 'Cumyield:', cumyield)
                            shorted.remove(stock)
                        else:
                            transactions[i]['last_value'] = v
                            transactions[i]['yield'] = (transactions[i]['short_value'] - transactions[i]['last_value']) * 100 / transactions[i]['short_value']

            for stock in [stock for stock in wl.keys() if stock not in shorted]:
                v = wl[stock]['Close'].loc[datestr]
                transactions.append({'stock': stock, 'short_value': v, 'open_date': datestr, 'last_value': v, 'status': 'open', 'yield': 0.0})
                print('**Opening:', transactions[-1]['stock'], ' Value:', transactions[-1]['last_value'])
                shorted.append(stock)

        graph = {}
        yield_ = 0

        for transaction in transactions:
            diff = (transaction['short_value'] - transaction['last_value']) * 100 / transaction['short_value']
            if 'close_date' not in transaction.keys():
                print('Opened: ', transaction['stock'], 'on:', transaction['open_date'], ' Yield: ', diff)
                transaction['close_date'] = datetime.date.today().strftime('%Y-%m-%d')
            if not transaction['close_date'] in graph.keys():
                graph[transaction['close_date']] = diff
            else:
                graph[transaction['close_date']] += diff
            yield_ += diff

        print('Yield:', yield_)

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
    #lfx.backtest()


