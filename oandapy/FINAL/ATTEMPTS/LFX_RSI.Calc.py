import pandas as pd

LFX_daily = pd.DataFrame()
n = 14

data = pd.read_csv(r'exchange.data.csv')

LFX_daily["Close"] = data["EUR/USD Close"].astype(float)


LFX_daily["Change"] = (LFX_daily["Close"] - LFX_daily["Close"].shift(1)).fillna(0)


LFX_daily["Up"] = (LFX_daily["Change"][LFX_daily["Change"] > 0])
LFX_daily["Up"] = LFX_daily["Up"].fillna(0)


LFX_daily["Down"] = (abs(LFX_daily["Change"])[LFX_daily["Change"] < 0]).fillna(0)
LFX_daily["Down"] = LFX_daily["Down"].fillna(0)


LFX_daily["Ave Up"] = 0.00
LFX_daily["Ave Up"][n] = LFX_daily["Up"][1:n+1].mean()


for i in range(n+1,len(LFX_daily),1):
    LFX_daily["Ave Up"][i] = (LFX_daily["Ave Up"][i-1]*(n-1)+LFX_daily["Up"][i])/n

LFX_daily["Ave Down"] = 0.00
LFX_daily["Ave Down"][n] = LFX_daily["Down"][1:n+1].mean()

for i in range(n+1,len(LFX_daily),1):
    LFX_daily["Ave Down"][i] = (LFX_daily["Ave Down"][i-1]*(n-1)+LFX_daily["Down"][i])/n

LFX_daily["RS"] = (LFX_daily["Ave Up"]/LFX_daily["Ave Down"]).fillna(0)

LFX_daily["RSI"] = 100 - 100/(LFX_daily["RS"]+1)

print(LFX_daily)