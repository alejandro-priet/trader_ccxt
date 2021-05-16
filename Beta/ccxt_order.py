import ccxt
import matplotlib.pyplot as plt
import numpy as np


i = 0
y_bid = []
y_ask = []
x_data = []

plt.ion()

fig = plt.figure()

# retrieve data for the BTC/USDT pair on Binance
binance = ccxt.binance()
orderbook = binance.fetch_order_book('BTC/EUR')
ticker = binance.fetch_ticker('BTC/EUR')
print(ticker)
bid = orderbook['bids']
ask = orderbook['asks']

for d in range(len(bid)):

    y_bid.append(bid[d][0]) 
    y_ask.append(ask[d][0]) 

    plt.plot(y_bid)
    plt.plot(y_ask)
    plt.draw()
    plt.pause(0.0001)
    plt.clf()





