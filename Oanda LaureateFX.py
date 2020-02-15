import requests

account_id = "13417875001"

key = "12a1f42967bc9ce1cd0ebf8f46da9a02-03ab1a77bb8478b89690ca77adcbf934"



#Get prices:

#Next, we will create an instance of the oandapy.API,
# as the oanda variable with the following code.
# The get_prices method is invoked by passing the instruments parameter with a string value of EUR_USD
# so that the rates of the EUR/USD currency pair are fetched:

import oandapy
oanda = oandapy.API(environment="practice", access_token=key)
response = oanda.get_prices(instruments="EUR_USD"), oanda.get_prices(instruments="USD_CAD")

prices = response["prices"]
bidding_price = float(prices[0]["bid"])
asking_price = float(prices[0]["bid"])
instrument = prices[0]["instrument"]
time = prices[0]["time"]

print ("[%s] %s bid=%s ask=%s" % (time, instrument, bidding_price, asking_price))

