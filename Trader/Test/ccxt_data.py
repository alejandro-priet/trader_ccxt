import ccxt
import os
import re
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from stockstats import StockDataFrame as Sdf

# from variable id
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': '9NfWYUQ3zz781MYQnVnpohkwwUigOBfZ4BEueWzoh1JJKpFAEJkctTbZvAlGO5tt',
    'secret': 'qXlE1ibfEuNgSiWBGF43WZUi0exgCkJUOqFPU7CfIf85mmQjZzGPic2Gc6BR79TH',
    'timeout': 30000,
    'enableRateLimit': True,
})

# load markets and all coin_pairs
exchange.load_markets()
coin_pairs = exchange.symbols

# list of coin pairs which are active and use BTC as base coin
valid_coin_pairs = []
# load only coin_pairs which match regex and are active
regex = 'ETH/BTC'

for coin_pair in coin_pairs:
  if re.match(regex, coin_pair) and exchange.markets[coin_pair]['active']:
    valid_coin_pairs.append(coin_pair)

print(valid_coin_pairs)

def get_historical_data(coin_pair, timeframe):
    """Get Historical data (ohlcv) from a coin_pair
    """
    #data = exchange.fetch_ohlcv(coin_pair, timeframe, since)
    data = exchange.fetch_ohlcv(coin_pair, timeframe)
    # update timestamp to human readable timestamp
    data = [[exchange.iso8601(candle[0])] + candle[1:] for candle in data]
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(data, columns=header)
    return df


def create_stock(historical_data):
    """Create StockData from historical data 
    """
    stock  = Sdf.retype(historical_data)
    return stock


if __name__ == "__main__":
  for coin_pair in valid_coin_pairs:
    # respect rate limit
    time.sleep (exchange.rateLimit / 1000)
    data = get_historical_data(coin_pair, '1m')
    stock_data = create_stock(data)

# Calculate RSI                       
stock_data['rsi_14']                     
print(stock_data)

signal = stock_data['macds'] # Your signal line
macd   = stock_data['macd'] # The MACD that need to cross the signal line

print(signal)


t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2*np.pi*t)
plt.plot(t, s)

plt.title('About as simple as it gets, folks')
plt.show()
                       
# Coment ctrl + K + C
# advice = ["No data"]    # Since you need at least two hours in the for loop

# for i in range(1, len(signal)):
#     # If the MACD crosses the signal line upward
#     if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
#         advice.append("BUY")
#     # The other way around
#     elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
#         advice.append("SELL")
#     # Do nothing if not crossed
#     else:
#         advice.append("HOLD")

# stock_data['advice'] = advice
# print(stock_data['advice'])