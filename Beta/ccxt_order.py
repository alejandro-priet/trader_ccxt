import ccxt
import matplotlib.pyplot as plt
import numpy as np


i = 0
y_bid = []
y_ask = []

while i < 3: 
    # retrieve data for the BTC/USDT pair on Binance
    binance = ccxt.binance()
    orderbook = binance.fetch_order_book('BTC/USDT')
    bid = orderbook['bids']
    ask = orderbook['asks']

    for d in range(len(bid)):
    
        y_bid.append(bid[d][0]) 
        y_ask.append(ask[d][0]) 
    
    i += 1

x_data = np.array(range(len(y_bid)))


fig = plt.plot()
plt.plot(x_data,y_bid) 
plt.show()