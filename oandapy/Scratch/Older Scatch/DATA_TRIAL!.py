import pandas as pd

df2 = pd.DataFrame()

series = pd.read_csv('DATA_trial', header=None, usecols=(0,1))

series = series.drop(columns=0)

df = pd.DataFrame(series)

df.columns = ['Close']
df = df.drop(index=0)
df.reset_index(inplace=True)
df = df.drop(columns='index')

df["Close"] = df["Close"].astype(float)

df["Change"] = (df["Close"] - df["Close"].shift(1)).fillna(0)

print(df)

