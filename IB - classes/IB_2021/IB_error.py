from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import *
from ibapi.contract import *
import pandas as pd
import numpy as np
import threading
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []

    def historicalData(self, reqId, bar):
        #print(f'Time: {bar.date} Close: {bar.close}')
        self.data.append([bar.date, bar.close, bar.high, bar.low])

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


def EurGbpFx_con():
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    return contract


def BracketOrder(parentOrderId:int, action:str, quantity:float,
                 takeProfitLimitPrice:float, stopLossPrice:float):

    parent = Order()
    parent.orderId = parentOrderId
    parent.action = action
    parent.orderType = "MKT"
    parent.totalQuantity = quantity
    parent.transmit = False

    takeProfit = Order()
    takeProfit.orderId = parent.orderId + 1
    takeProfit.action = "SELL" if action == "BUY" else "BUY"
    takeProfit.orderType = "LMT"
    takeProfit.totalQuantity = quantity
    takeProfit.lmtPrice = takeProfitLimitPrice
    takeProfit.parentId = parentOrderId
    takeProfit.transmit = False

    stopLoss = Order()
    stopLoss.orderId = parent.orderId + 2
    stopLoss.action = "SELL" if action == "BUY" else "BUY"
    stopLoss.orderType = "STP"
    stopLoss.auxPrice = stopLossPrice
    stopLoss.totalQuantity = quantity
    stopLoss.parentId = parentOrderId
    stopLoss.transmit = True

    bracketOrder = [parent, takeProfit, stopLoss]
    return bracketOrder


def atr_calc(close, high, low):
    c = list((close).astype(float))
    h = list((high).astype(float))
    l = list((low).astype(float))

    del c[-1]
    del h[0]
    del l[0]

    trs = pd.DataFrame([c, h, l])
    trs = trs.transpose()
    trs.columns = ["c", "h", "l"]

    trz = []
    for index, row in trs.iterrows():
        tr = max((row['h'] - row['l']), abs(row['h'] - row['c']), abs(row['l'] - row['c']))
        trz.append(tr)
    atrr = list(pd.Series(trz).ewm(span=50).mean())[-1]
    return atrr


def rsi_calc(prices):
    n = 14
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi_h = np.zeros_like(prices)
    rsi_h[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1]

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi_h[i] = 100. - 100./(1.+rs)

    return rsi_h[-1]


contracts = {"EurGbpFx": EurGbpFx_con()}

def run_loop():
    app.run()

app = IBapi()
app.connect("127.0.0.1", 7497, 988)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()


for x, y in contracts.items():
    time.sleep(1) #sleep to allow enough time for data to be returned
    app.reqHistoricalData(1, y, "", "7 D", "1 hour", "MIDPOINT", 0, 1, False, [])
    time.sleep(5)
    df_T1 = pd.DataFrame(app.data, columns=['DateTime', 'Close', 'High', 'Low'])
    time.sleep(1)
    app.reqHistoricalData(1, y, "", "2 D", "15 mins", "MIDPOINT", 0, 1, False, [])
    time.sleep(5)
    df_T2 = pd.DataFrame(app.data, columns=['DateTime', 'Close', 'High', 'Low'])

    atr = atr_calc(df_T1["Close"], df_T1["High"], df_T1["Low"])
    price = list((df_T1["Close"]).astype(float))[-1]
    sl = round((20 * atr), 3)
    tp = round((20 * atr), 3)

    #print(x)
    #print("Hourly RSI:", rsi_calc(df_T1["Close"]))
    #print("15 min RSI:", rsi_calc(df_T2["Close"]))
    #print(atr, sl, tp)

    if rsi_calc(df_T1["Close"]) < 67 and rsi_calc(df_T2["Close"]) < 67:
        bracket = BracketOrder(app.nextorderId, "BUY", 1000, price - sl, price + tp)
        for o in bracket:
            app.placeOrder(o.orderId, y, o)
        time.sleep(3)
    elif rsi_calc(df_T1["Close"]) < 33 and rsi_calc(df_T2["Close"]) < 33:
        bracket = BracketOrder(app.nextorderId, "SELL", 1000, price + sl, price - tp)
        for o in bracket:
            app.placeOrder(o.orderId, y, o)
        time.sleep(3)
    else:
        pass


app.disconnect()