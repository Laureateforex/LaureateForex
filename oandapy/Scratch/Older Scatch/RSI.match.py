import pandas as pd

LFX_daily = pd.DataFrame()
LFX_hourly = pd.DataFrame()
LFX_match = pd.DataFrame()
n = 14

data_daily = pd.read_csv(r'Daily_data.csv')
data_hourly = pd.read_csv(r'hourly_data.csv')


def rsi_daily(price):
    LFX_daily["Close"] = data_daily[price].astype(float)
    LFX_daily["Close"] = list(LFX_daily["Close"][::-1])

    LFX_daily["Change"] = (LFX_daily["Close"] - LFX_daily["Close"].shift(1)).fillna(0)

    LFX_daily["Up"] = (LFX_daily["Change"][LFX_daily["Change"] > 0])
    LFX_daily["Up"] = LFX_daily["Up"].fillna(0)

    LFX_daily["Down"] = (abs(LFX_daily["Change"])[LFX_daily["Change"] < 0]).fillna(0)
    LFX_daily["Down"] = LFX_daily["Down"].fillna(0)

    LFX_daily["Ave Up"] = 0.00
    LFX_daily["Ave Up"][n] = LFX_daily["Up"][1:n + 1].mean()

    for i in range(n + 1, len(LFX_daily), 1):
        LFX_daily["Ave Up"][i] = (LFX_daily["Ave Up"][i - 1] * (n - 1) + LFX_daily["Up"][i]) / n

    LFX_daily["Ave Down"] = 0.00
    LFX_daily["Ave Down"][n] = LFX_daily["Down"][1:n + 1].mean()

    for i in range(n + 1, len(LFX_daily), 1):
        LFX_daily["Ave Down"][i] = (LFX_daily["Ave Down"][i - 1] * (n - 1) + LFX_daily["Down"][i]) / n

    LFX_daily["RS"] = (LFX_daily["Ave Up"] / LFX_daily["Ave Down"]).fillna(0)

    LFX_daily["RSI"] = 100 - 100 / (LFX_daily["RS"] + 1)

    LFX_daily.loc[LFX_daily["RSI"] < 33, "match"] = "sell"
    LFX_daily.loc[LFX_daily["RSI"] < 15, "match"] = "wait"
    LFX_daily.loc[LFX_daily["RSI"] > 66, "match"] = "buy"
    LFX_daily.loc[LFX_daily["RSI"] > 80, "match"] = "wait"
    LFX_daily["match"] = LFX_daily["match"].fillna("wait")
    return LFX_daily


def rsi_hourly(price):
    LFX_hourly["Close"] = data_hourly[price].astype(float)
    LFX_hourly["Close"] = list(LFX_hourly["Close"][::-1])

    LFX_hourly["Change"] = (LFX_hourly["Close"] - LFX_hourly["Close"].shift(1)).fillna(0)

    LFX_hourly["Up"] = (LFX_hourly["Change"][LFX_hourly["Change"] > 0])
    LFX_hourly["Up"] = LFX_hourly["Up"].fillna(0)

    LFX_hourly["Down"] = (abs(LFX_hourly["Change"])[LFX_hourly["Change"] < 0]).fillna(0)
    LFX_hourly["Down"] = LFX_hourly["Down"].fillna(0)

    LFX_hourly["Ave Up"] = 0.00
    LFX_hourly["Ave Up"][n] = LFX_hourly["Up"][1:n + 1].mean()

    for i in range(n + 1, len(LFX_daily), 1):
        LFX_hourly["Ave Up"][i] = (LFX_hourly["Ave Up"][i - 1] * (n - 1) + LFX_hourly["Up"][i]) / n

    LFX_hourly["Ave Down"] = 0.00
    LFX_hourly["Ave Down"][n] = LFX_hourly["Down"][1:n + 1].mean()

    for i in range(n + 1, len(LFX_daily), 1):
        LFX_hourly["Ave Down"][i] = (LFX_hourly["Ave Down"][i - 1] * (n - 1) + LFX_hourly["Down"][i]) / n

    LFX_hourly["RS"] = (LFX_hourly["Ave Up"] / LFX_hourly["Ave Down"]).fillna(0)

    LFX_hourly["RSI"] = 100 - 100 / (LFX_hourly["RS"] + 1)

    LFX_hourly.loc[LFX_hourly["RSI"] < 33, "match"] = "sell"
    LFX_hourly.loc[LFX_hourly["RSI"] < 15, "match"] = "wait"
    LFX_hourly.loc[LFX_hourly["RSI"] > 66, "match"] = "buy"
    LFX_hourly.loc[LFX_hourly["RSI"] > 80, "match"] = "wait"
    LFX_hourly["match"] = LFX_hourly["match"].fillna("wait")
    return LFX_hourly()


def open_position():
    if LFX_daily["match"][0] == "buy" and LFX_hourly["match"][0] == "buy":
        print("go long")
    elif LFX_daily["match"][0] == "sell" and LFX_hourly["match"][0] == "sell":
        print("go short")
    else:
        print("wait")
    return print("this is too easy")


print(rsi_daily("EUR/USD Close"))
print(rsi_hourly("EUR/USD Close"))
open_position()
print(open_position)
