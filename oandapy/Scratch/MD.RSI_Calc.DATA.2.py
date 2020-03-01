import pandas as pd
import statistics
df = pd.DataFrame()
n = 14

data = pd.read_csv(r'../../EUR GBP Historical Data')

Close = data["Price"].astype(float)

df["Change"] = (Close - Close.shift(1)).fillna(0)


"""
df.loc[df['Change'] > 0, 'up'] =  'True'
df.loc[df['Change'] < 0, 'down'] = 'True'
"""

for i in range(len(df['Change'])):
    if df['Change'][i] > 0:
        df['up'] = df['Change'][i]
    else:
        df['down'] = df['Change'][i]

print(df)