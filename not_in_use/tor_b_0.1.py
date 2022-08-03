"""
first version of bot ever
v: 0.1
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time

#This is the trading object that has to be instantiated to trade.
class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self)
        
    def error(self, reqId, errorCode, errorString):
        print("Error {} {} {}".format(reqId,errorCode,errorString))
        
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

# This is where we establish a connection with the TWS client.
def websocket_con():
    app.run()
    


# this is where we instantiate the trading object and establish the connection with the right port for the websocket connection.
app = TradingApp()
"""client ID of 2 will be used for testing of bots from here on, use different ID's
    to have multiple different bots and strategies running at the same time."""
app.connect("127.0.0.1", 7497, clientId=2)


# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1) # some latency added to ensure that the connection is established

#########################################################################################
#########################################################################################

# Need both a contract object which specifies which type of security we want to trade with and a order object which will tell TWS what we wish to do with the security.

############# contracts #####################
#"ISLAND" is the name used in TWS for New York stock exchange.

def stk_default_us(symbol, sec_type = "STK", currency = "USD", exchange= "ISLAND")
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
 
    return contract

############# Orders ##########################

#this is the basic order of buying a stock
def market_order(direction, quantity):
    order = Order()
    order.action = direction
    order.orderType = "MKT"
    order.totalQuantity = quantity

    return order




