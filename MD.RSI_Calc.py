rsi_Indictor(close,n_days):
    rsi_series = pd.DataFrame(close)


    # Change = close[i]-Change[i-1]
    rsi_series["Change"] = (rsi_series["Close"] - rsi_series["Close"].shift(1)).fillna(0)

    # Upword Movement
    rsi_series["Upword Movement"] = (rsi_series["Change"][rsi_series["Change"] >0])
    rsi_series["Upword Movement"] = rsi_series["Upword Movement"].fillna(0)

    # Downword Movement
    rsi_series["Downword Movement"] = (abs(rsi_series["Change"])[rsi_series["Change"] <0]).fillna(0)
    rsi_series["Downword Movement"] = rsi_series["Downword Movement"].fillna(0)

    #Average Upword Movement
    # For first Upword Movement Mean of first n elements.
    rsi_series["Average Upword Movement"] = 0.00
    rsi_series["Average Upword Movement"][n] = rsi_series["Upword Movement"][1:n+1].mean()

    # For Second onwords
    for i in range(n+1,len(rsi_series),1):
        #print(rsi_series["Average Upword Movement"][i-1],rsi_series["Upword Movement"][i])
        rsi_series["Average Upword Movement"][i] = (rsi_series["Average Upword Movement"][i-1]*(n-1)+rsi_series["Upword Movement"][i])/n

    #Average Downword Movement
    # For first Downword Movement Mean of first n elements.
    rsi_series["Average Downword Movement"] = 0.00
    rsi_series["Average Downword Movement"][n] = rsi_series["Downword Movement"][1:n+1].mean()

    # For Second onwords
    for i in range(n+1,len(rsi_series),1):
        #print(rsi_series["Average Downword Movement"][i-1],rsi_series["Downword Movement"][i])
        rsi_series["Average Downword Movement"][i] = (rsi_series["Average Downword Movement"][i-1]*(n-1)+rsi_series["Downword Movement"][i])/n

    #Relative Index
    rsi_series["Relative Strength"] = (rsi_series["Average Upword Movement"]/rsi_series["Average Downword Movement"]).fillna(0)

    #RSI
    rsi_series["RSI"] = 100 - 100/(rsi_series["Relative Strength"]+1)
    return rsi_series.round(2)