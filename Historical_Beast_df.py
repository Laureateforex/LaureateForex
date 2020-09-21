import pandas as pd
import numpy as np
import json
import ijson
from pandas.io.json import json_normalize
import json
import matplotlib.pyplot as plot

with open('//Users/user/PycharmProjects/LaureateForex/GBP_AUDDaily.D') as f:
    d = json.load(f)

Dynamicdf = pd.json_normalize(d[:])
# GBPUSD_Hourly.head(1)

# StartingCapital = 1000
# for i in Dynamicdf.iloc(i:,5):
#
# NextTradeClose = Dynamicdf.iloc(i:,5)
# Yield = NextTradeClose - PreviousTradeClose
# FinisingCapital = Yield + StartingCapital
# PrecentageYield = (FinalTradeYiled + StartingCapital)/StartingCapital * 100


Dynamicdf.columns = ['complete', 'volume', 'Daily_Candle', 'O', 'H', 'L', 'C']

Dynamicdf.drop(Dynamicdf.columns[[0, 1]], axis=1, inplace=True, )

print(Dynamicdf)

Dynamicdf['C'] = Dynamicdf['C'].astype(float)

# pf.id=pd.to_numeric(pf.id)

buypair = Dynamicdf.iloc[0, 4]


Capital = 1000

Balance = buypair + Capital

print(buypair)

print("Finishing Capital is", Balance)



# ********  P    L     O    T   **************

# close = Dynamicdf[['C']].astype(float)
# date = Dynamicdf[['Daily_Candle']].astype(str)
# # rename the column with symbol name
# # close = close.rename(columns={'close': symbol})
# ax = close.plot(title='GBPAUD Daily 2019/20')
# ax.set_xlabel('date')
# ax.set_ylabel('close price')
# ax.grid()
# plot.show()
