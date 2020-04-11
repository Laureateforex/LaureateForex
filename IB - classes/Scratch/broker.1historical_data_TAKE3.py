from datetime import datetime
from time import sleep, strftime, localtime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
import pandas as pd

# Set up IB message handler to dump to pandas dataframe
df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'OpenInterest'])
s = pd.Series()


# define historical data handler for IB - this will populate our pandas data frame
def historical_data_handler(msg):
    global df
    if ('finished' in str(msg.date)) == False:
        s = ([datetime.fromtimestamp(int(msg.date)), msg.open, msg.high, msg.low, msg.close, msg.volume, 0])
        df.loc[len(df)] = s

    else:
        df.set_index('Date', inplace=True)


con = ibConnection(host='127.0.0.1', port=7497, clientId=988)
con.register(historical_data_handler, message.historicalData)
con.connect()

# IBpy - set up contract details and historical data request
qqq = Contract()
qqq.m_symbol = 'ES'
qqq.m_secType = 'FUT'
qqq.m_exchange = 'GLOBEX'
qqq.m_currency = 'USD'
qqq.m_expiry = '201709'
print(qqq.m_symbol)
con.reqHistoricalData(0, qqq, '', '3 W', '1 hour', 'TRADES', 1, 2)
sleep(10)
print('---------------')
print(df)


