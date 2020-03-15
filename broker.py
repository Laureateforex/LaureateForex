#IG rest API parameters
import sys

import requests

rest_api_key = "3f53e9f321bb5aaed46724a5539083aa661bc58b"
rest_identifier = "impulse2585"
rest_password = "Algobroz599"
# IG rest login request
rest_url = "https://api.ig.com/gateway/deal/session"
headers = {}
headers["Content-Type"] = "application/json; charset=UTF-8"
headers["Accept"] = "application/json; charset=UTF-8"
headers ["Version"] = "2"
headers ["X-IG-API-KEY"] = rest_api_key
request_json = {}
request_json["identifier"] = rest_identifier
request_json["password"] = rest_password
rest_response = requests.request("POST", rest_url, headers=headers, json=request_json)
if rest_response.status_code != 200:
    print("error", rest_response.status_code, rest_url, rest_response.text)
sys.exit(0)
# collect params from IG rest login response
xst = rest_response.headers["X-SECURITY-TOKEN"]
cst	= rest_response.headers["CST"]
response_json = rest_response.json()
current_account = response_json["currentAccountId"]
lightstreamer_endpoint = response_json["lightstreamerEndpoint"]
# IG streaming login request
streaming_url = "{}/lightstreamer/create_session.txt".format(lightstreamer_endpoint)
steaming_user = current_account;
steaming_password = "CST-{}|XST-{}".format(cst, xst)
query = {}
query["LS_op2"] = "create"
query["LS_cid"] = "mgQkwtwdysogQz2BJ4Ji kOj2Bg"
query["LS_user"] = steaming_user
query["LS_password"] = steaming_password
streaming_response = requests.request("POST", streaming_url, data=query, stream=True)
if streaming_response.status_code != 200:
    print("error", streaming_response.status_code, streaming_url, streaming_response.text)
sys.exit(0)
# collect params from streaming response
streaming_session = None
control_domain = None
streaming_iterator = streaming_response.iter_lines(chunk_size=80, decode_unicode=True)
for line in streaming_iterator:
    print("line", line)
if ":" not in line:
    Continue
[param,value] = line.split(":",1)
if param == "SessionId":
    streaming_session = value
if param == "ControlAddress":
    control_domain = value
if streaming_session and control_domain:
    Break
# open control connection and subscribe EURUSD
control_url = "https://{}/lightstreamer/control.txt".format(control_domain)
query = {}
query["LS_session"] = streaming_session
query["LS_op"]="add"
query["LS_table"]="1"
query["LS_id"]="MARKET:CS.D.EURUSD.MINI.IP"
query["LS_schema"]="BID OFFER"
query["LS_mode"]="MERGE"
control_response = requests.request("POST", control_url, data=query)
if control_response.status_code != 200:
    print("error", control_response.status_code, control_url, control_response.text)
sys.exit(0)
# stream prices
for line in streaming_iterator:
    print("line", line)