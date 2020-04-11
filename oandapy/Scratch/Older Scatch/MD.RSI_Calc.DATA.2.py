import pandas as pd
import statistics
df = pd.DataFrame()
n = 14

data = pd.read_csv(r'../../EUR GBP Historical Data')

Close = data["Price"].astype(float)

df["Change"] = ((Close - Close.shift(1)).fillna(0)).astype(float)


df.loc[df['Change'] > 0, 'up'] = 1.0
df.loc[df['Change'] < 0, 'down'] = 1.0

print(df)

if df['up'] > 0:



    """for i in range(n+1, len(df['Change']), 1):
    if df['up'] > 0:
        df_ave['Ave_up'][i] = df['Change'][i]
    if df['down'] > 0:
        df_ave['Ave_down'][i] = df['Change'][i]




for i in range(len(df['Change'])):
    if df['Change'][i] > 0:
        df['up'] = df['Change'][i]
    else:
        df['down'] = df['Change'][i] """

