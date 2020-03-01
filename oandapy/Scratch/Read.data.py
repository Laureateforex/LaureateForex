import pandas as pd
LFX_series = pd.Series()

data = pd.read_csv(r'../../EUR GBP Historical Data')

Close = data["Price"].astype(float)

LFX_series["Change"] = (Close - Close.shift(1)).fillna(0)

print(LFX_series)

