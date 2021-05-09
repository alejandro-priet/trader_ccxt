# Essentials

import ccxt
import os
import re

# Date 

import time
import datetime
import calendar
import matplotlib.dates as mpdates

# Data

import numpy as np
import pandas as pd
from stockstats import StockDataFrame as Sdf

# Plot

import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc


# Constants

a = 0  # while conditional
plott = ''  # prott contidional
i = 0 

if plott == 'y':

    plt.style.use('ggplot') # Aspect of the plot
    plt.ion() #activate interactive plott

# Exchange API Data

exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': '******',
    'secret': '******',
    'timeout': 30000,
    'enableRateLimit': True,
})


#### MAIN FUNCTIONS

# 1 

# Initialize the market, load the coin pairs and validate the user input (active coin pairs vs desired pairs)
# Returns a list with one only pair to use (it can be used with more than one pair, but due to parallel it stay at one)

def initialize_market(regex):

    # list of coin pairs which are active and use '' as base coin
    valid_coin_pairs = []

    # load markets and all coin_pairs
    exchange.load_markets()
    coin_pairs = exchange.symbols

    # load only coin_pairs which match regex and are active

    for coin_pair in coin_pairs:
        if re.match(regex, coin_pair) and exchange.markets[coin_pair]['active']:
            valid_coin_pairs.append(coin_pair)

    return valid_coin_pairs

# 2

# fetch the data frames of the validated coin pais = [time, open, high, low, close, volume]
# as argument timeframe (sampling rate) and limit (how many samples)
# return a pandas data frame with the stock data inside

def get_historical_data(valid_coin_pairs, timeframe, limit):

    
    now = datetime.datetime.utcnow()    # Calculate the current date
    unixtime = calendar.timegm(now.utctimetuple()) # UTC
    since = (unixtime - 60*60) * 1000 # UTC timestamp in milliseconds


    for coin_pair in valid_coin_pairs:

        # respect rate limit
        time.sleep (exchange.rateLimit / 100000)

        # Get Historical data (ohlcv) from a coin_pair
        data = exchange.fetch_ohlcv(coin_pair, timeframe, since, limit)

        # update timestamp to human readable timestamp
        data_t = [[exchange.iso8601(candle[0])] + candle[1:] for candle in data]
        header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(data_t, columns=header)

        stock_data = Sdf.retype(df)
    
    return stock_data

# 3 

# fetch account balance and calculates its value on the selected currency
# as argument the symbol (ex. 'BTC/EUR') and a parameter who describes 
# the state of the coin value to be evaluate ('total', 'free', 'used')
# returns the an aproximate value

def get_current_coin_value(symbol, parameter):

    # Split the parameter

    initial_indicator = re.split('[/]', symbol)[0] 
    final_currency = re.split('[/]', symbol)[1]

    # Fetching

    balance = exchange.fetch_balance()
    your_balance = balance[initial_indicator][parameter]
    remaining_balance = your_balance
    orderbook = exchange.fetch_order_book(symbol)
    cost = 0

    # Calculating the aprox value of the coin base on the actual bid

    for bid in orderbook['bids']:
        if remaining_balance <= bid[1]:
            cost += bid[0] * remaining_balance
            break
        else:
            cost += bid[0] * bid[1]
        remaining_balance = max(0, remaining_balance - bid[1])

    value = ['Your', your_balance, initial_indicator,'is worth', cost, final_currency]

    return value

# 4 

# Get three states as advice SELL, BUY or HOLD. All based on the cross point of the MACD at 9 and 12 periods
# also plot the whole information if the parameter plott = 'y' 
# as input the stock frame, normalized stock frame and the plott conditional
# returns the modified stock data frame with an added column with the advice

def get_advice(stock_data, data_data, plott):

            if plott == 'y':

                ax = plt.axes() # create the frigure to plot
            
                # Setting labels 
                ax.set_xlabel('Date')
                ax.set_ylabel('Price')

                date_format = mpdates.DateFormatter('%Y-%m-%d %H:%M:%S')
                ax.xaxis.set_major_formatter(date_format)

                candlestick_ohlc(ax, data_data.values, width = 0.0005)

            #Temporal data
            date = data_data['timestamp']

            #Vector with s,b,h advice
            advice = ["No data"] 

            # Signal line Moving Average Convergence/Divergence - 9 period
            signal = stock_data['macds'] 
            
            # Signal line Moving Average Convergence/Divergence - 12 period
            macd = stock_data['macd'] 

            # Relative Strengh Index
            rsi_14 = stock_data['rsi_14']

            correlation = 1 + np.correlate(signal,macd)

            normalized_signal = (signal - min(macd))/(max(macd)-min(macd)) 
            normalized_macd = (macd - min(macd))/(max(macd)-min(macd)) 

            for i in range(1, len(signal)):
                # If the MACD crosses the signal line upward
                if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]:
                    advice.append("BUY")
                    if plott == 'y':
                        ax.scatter(date[i],normalized_signal[i],color = 'green')

                # The other way around
                elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
                    advice.append("SELL")
                    if plott == 'y':
                        ax.scatter(date[i],normalized_signal[i],color = 'red')

                # Do nothing if not crossed
                else:
                    advice.append("HOLD")
                    if plott == 'y':
                        ax.scatter(date[i],normalized_signal[i],color = 'black')

            stock_data['advice'] = advice

            if plott == 'y':
                
                #graphic the data in real-time

                # add something to axes    
                ax.plot(date,normalized_signal,'r') 
                ax.plot(date,normalized_macd, 'b')

                # draw the plot
                plt.draw()
                plt.pause(0.001) #is necessary for the plot to update for some reason
                plt.clf()

        
            return stock_data['advice']


### SECONDARY FUNCTIONS

# General normalization of the data, normally used to plot 
# Returns the normalized column

def get_normalize_column(column):

    column = (column - np.amin(column))/(np.amax(column)-np.amin(column))

    return column

# Specific normalization of the pandas data frame for the stock data

def get_normalized_stock(stock_data):

    #Creating a new Array to segment the info and extract the last 100 points 

    data_data = stock_data 
    data_data['timestamp'] = pd.to_datetime(data_data['timestamp'])
    data_data['timestamp'] = mpdates.date2num(list(data_data['timestamp']))
    
    data_data['open'] = get_normalize_column(data_data['open'])
    data_data['high'] = get_normalize_column(data_data['high'])
    data_data['low'] = get_normalize_column(data_data['low'])
    data_data['close'] = get_normalize_column(data_data['close'])
    data_data['volume'] = get_normalize_column(data_data['volume'])

    return data_data


if __name__ == "__main__":

    coin_pair = 'VET/EUR' # Regex tolerant pair of wished currency pairs

    valid_coin_pairs = initialize_market(coin_pair) # Start and validation of the current market

    coin_value = get_current_coin_value(coin_pair, 'total') # Current aproximate digital coin value in '/pair'

    order = exchange.create_order(coin_pair,'limit', 'sell', 20, 0.6, params = {'test': True}) # test if it's valid, but don't actually place it 

    print(order)
    print(coin_value)

    while a < 1:

        stock_data = get_historical_data(valid_coin_pairs, '1m', 50) # Get stock data

        data_data = get_normalized_stock(stock_data) # Normalize

        advice = get_advice(stock_data,data_data,'y') # Get advice and plott if ,,'y'