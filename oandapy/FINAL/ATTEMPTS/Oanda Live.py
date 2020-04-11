from optparse import OptionParser


def connect_to_stream():
    """

    Environment           <Domain>
    fxTrade               stream-fxtrade.oanda.com
    fxTrade Practice      stream-fxpractice.oanda.com
    sandbox               stream-sandbox.oanda.com
    """
    Environment
    Description
    fxTrade(Live)
    The
    live(real
    money) environment
    fxTrade
    Practice(Demo)
    The
    demo(simulated
    money) environment
    """
    domainDict = { 'live' : 'stream-fxtrade.oanda.com',
               'demo' : 'stream-fxpractice.oanda.com' }

    # Replace the following variables with your personal ones
    domain = 'stream-fxpractice.oanda.com'
    access_token = 'ACCESS-TOKEN'
    account_id = '1234567'
    instruments = "EUR_USD,USD_CAD"
    # Replace the following variables with your personal values 
    environment = "demo" # Replace this 'live' if you wish to connect to the live environment 
    domain = domainDict[environment] 
    access_token = 'REPLACE THIS WITH YOUR ACCESS TOKEN'
    account_id = 'REPLACE THIS WITH YOUR ACCOUNT ID, ie  2252344'
    instruments = 'REPLACE THIS WITH THE INSTRUMENTS YOU WOULD LIKE TO SUBSCRIBE TO.  ie "EUR_USD,USD_JPY,...' 

_from = sys.argv[0]
_to = sys.argv[0]
gran = sys.argv[0]
instr = sys.argv[0]

params = {
    "granularity": gran,
    "from": _from,
    "to": _to
}

def cnv(r, h):
    for candle in r.get('candles'):
        ctime = candle.get('time')[0:19]
        try:
            rec = "{time},{complete},{c}".format(
                time=ctime,
                complete=candle['complete'],
                c=candle['mid']['c']
            )
        except Exception as e:
            print(e, r)
        else:
            h.write(rec+"\n")

client = API(access_token=access_token)


except V20Error as e:
    print("Error: {}".format(e))


try:
    n = 0
    for R in api.request(s):
        print(json.dumps(R, indent=2))
        n += 1
        if n > 10:
            s.terminate("maxrecs received: {}".format(MAXREC))
    try:
        s = requests.Session()
@ -37,30 +39,28 @@ def connect_to_stream():
        params = {'instruments' : instruments, 'accountId' : account_id}
        req = requests.Request('GET', url, headers = headers, params = params)
        pre = req.prepare()
        resp = s.send(pre, stream = True, verify = False)
        resp = s.send(pre, stream = True, verify = True)
        return resp
    except Exception as e:
        s.close()
        print "Caught exception when connecting to stream\n" + str(e) 
        print("Caught exception when connecting to stream\n" + str(e)) 

def demo(displayHeartbeat):
    response = connect_to_stream()
    if response.status_code != 200:
        print response.text
        print(response.text)
        return
    for line in response.iter_lines(1):
        if line:
            try:
                line = line.decode('utf-8')
                msg = json.loads(line)
            except Exception as e:
                print "Caught exception when converting message into json\n" + str(e)
                print("Caught exception when converting message into json\n" + str(e))
                return

            if displayHeartbeat:
                print line
            else:
                if msg.has_key("instrument") or msg.has_key("tick"):
                    print line

            if "instrument" in msg or "tick" in msg or displayHeartbeat:
                print(line)

def main():
    usage = "usage: %prog