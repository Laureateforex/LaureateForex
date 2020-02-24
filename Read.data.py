import pandas as pd

data = pd.read_csv(r'EUR GBP Historical Data')

Close = data["Price"].astype(float)

LFX_series = pd.Series()

LFX_series["Change"] = (Close - Close.shift(1)).fillna(0)

print(LFX_series)
