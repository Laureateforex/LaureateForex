from __future__ import print_function
import oandapyV20
import pandas as pd
import oandapyV20.endpoints.positions as positions

token = '49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8'
account = '101-004-13417875-003'


client = oandapyV20.API(access_token=token)
r = positions.PositionList(accountID=account)
client.request(r)

x = r.response
x = x.get('positions')
pair = [z['instrument'] for z in x]
PL = [z['pl'] for z in x]
profit = []
for i in PL:
    u = float(i)
    u = abs(u)
    profit.append(u)

d = {"Underlying": pair, "P&L": profit}
df = pd.DataFrame(d)
df["P&L"] = df["P&L"].astype(float)

"""a = sum(df["P&L"])
new_row = {"Underlying": "Total", "P&L": a}
df = df.append(new_row, ignore_index=True)"""
print(df)