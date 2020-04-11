import json
import oandapyV20
import oandapyV20.endpoints.orders as orders
from oandapyV20.exceptions import V20Error

api = oandapyV20.API(environment="practice", access_token="49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8")
accountID = "101-004-13417875-002"


orderConf =            [


            {
                "order": {
                    "units": "1",
                    "instrument": "EUR_USD",
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }

]
for O in orderConf:
            r = orders.OrderCreate(accountID, data=O)
            print("Processing : {}".format(r))
            print("====================")
            print(r.data)

            try:
                response = api.request(r)
            except V20Error as e:
                print("V20Error:{}".format(e))
            else:
                print("Respose: {}\n{}".format(r.status_code,
                                               json.dumps(response, indent=2)))
