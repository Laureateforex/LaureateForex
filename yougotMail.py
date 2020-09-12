from __future__ import print_function
import smtplib, ssl
import oandapyV20
import pandas as pd
import oandapyV20.endpoints.positions as positions
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import sys


def mail(message):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "LaureateEmails@gmail.com"
    receiver_email = "laureatefx@gmail.com"
    password = "HackersNotToday"
    message_to_send = MIMEMultipart()

    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(message.to_html())

    part1 = MIMEText(html, 'html')
    message_to_send.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message_to_send.as_string())
    return


token = '49c68257ae0870c5b76bbe63d4c79803-bc876dfcc6b0ebcc31ef73e45ebdbab8'
accounts = ["101-004-13417875-001", "101-004-13417875-002", "101-004-13417875-003", "101-004-13417875-004",
            "101-004-13417875-005", "101-004-13417875-006", "101-004-13417875-007", "101-004-13417875-008",
            "101-004-13417875-009", "101-004-13417875-010"]
for i in accounts:
    client = oandapyV20.API(access_token=token)
    r = positions.PositionList(accountID=i)
    client.request(r)

    x = r.response
    x = x.get('positions')
    pair = [z['instrument'] for z in x]
    PL = [z['pl'] for z in x]

    d = {"Underlying": pair, "P&L": PL}
    df = pd.DataFrame(d)
    df["P&L"] = df["P&L"].astype(float)

    a = sum(df["P&L"])
    new_row = {"Underlying": "Total", "P&L": a}
    df = df.append(new_row, ignore_index=True)
    b = (a/1000)*100
    s = str(b)
    s = s + "%"
    new_row2 = {"Underlying": "Yield", "P&L": s}
    df = df.append(new_row2, ignore_index=True)
    mail(df)