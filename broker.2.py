from ib.opt import Connection
from ib.ext.Contract import Contract
from ib.ext.Order import Order


def make_contract(symbol, sec_type, exchange, primary_exchange, currency):
    Contract.M_symbol = symbol
    Contract.M_secType = sec_type
    Contract.M_exchange = exchange
    Contract.M_primaryExch = primary_exchange
    Contract.M_currency = currency
    return Contract


def make_order(action, quantity, price = None):
    if price is not None:
        order = Order()
        order.m_orderType = 'LMT'
        order.m_totalQuantity = quantity
        order.m_action = action
        order.m_lmtPrice = price

    else:
        order = Order()
        order.m_orderType = 'MKT'
        order.m_totalQuantity = quantity
        order.m_action = action

    return order


def main():
    conn = Connection.create(port=7497, clientId=998)
    conn.connect()
    oid = 1
    cont = make_contract('EUR', 'CASH', 'SMART', 'SMART', 'USD')
    offer = make_order('BUY', 1, 200)

    conn.placeOrder(oid, cont, offer)

    conn.disconnect()