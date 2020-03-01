import pandas as pd
import statistics
LFX_hourly = pd.DataFrame()
n = 14

data = pd.read_csv(r'EUR GBP Historical Data')

Close = data["Price"].astype(float)

LFX_hourly["Change"] = (Close - Close.shift(1)).fillna(0)

print(LFX_hourly)

if (LFX_hourly["Change"] > 0):
    LFX_hourly["Up"] = LFX_hourly["Change"]

else:
    LFX_hourly["Down"] = LFX_hourly["Change"]

"""
LFX_hourly["Up"] = [LFX_hourly["Change"] > 0]
LFX_hourly["Down"] = [LFX_hourly["Change"] < 0]"""

LFX_hourly["Average Up"] = statistics.mean(LFX_hourly["Up"][1:n+1])
for i in range(n+1, len(LFX_hourly), 1):
    LFX_hourly["Average Up"][i] = (LFX_hourly["Average Up"][i-1]*(n-1)+LFX_hourly["Up"][i])/n

LFX_hourly["Average Down"] = statistics.mean(LFX_hourly["Down"][1:n+1])
for i in range(n+1, len(LFX_hourly), 1):
    LFX_hourly["Average Down"][i] = (LFX_hourly["Average Down"][i-1]*(n-1)+LFX_hourly["Down"][i])/n

LFX_hourly["RS"] = (LFX_hourly["Average Up"]/LFX_hourly["Average Down"]).fillna(0)

LFX_hourly["RSI"] = 100 - 100/(LFX_hourly["RS"]+1)

print(LFX_hourly)


"""
up, down = LFX_hourly["Change"].copy(), LFX_hourly["Change"].copy()
up[up < 0] = 0
down[down > 0] = 0
roll_up = up.rolling(n)
roll_down = down.abs().rolling(n)
RS = roll_up / roll_down
RSI = 100.0 - (100.0 / (1.0 + RS))

print(RSI)
"""
