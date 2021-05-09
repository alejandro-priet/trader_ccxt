import shrimpy
import plotly.graph_objects as go# sign up for the Shrimpy Developer APIs for your free API keys
public_key = '...'
secret_key = '...'# collect the historical candlestick data
client = shrimpy.ShrimpyApiClient(public_key, secret_key)
candles = client.get_candles(
    'bittrex', # exchange
    'XRP',     # base_trading_symbol
    'BTC',     # quote_trading_symbol
    '1d'       # interval
)
dates = []
open_data = []
high_data = []
low_data = []
close_data = []# format the data to match the plotting library
for candle in candles:
    dates.append(candle['time'])
    open_data.append(candle['open'])
    high_data.append(candle['high'])
    low_data.append(candle['low'])
    close_data.append(candle['close'])# plot the candlesticks
fig = go.Figure(data=[go.Candlestick(x=dates,
                       open=open_data, high=high_data,
                       low=low_data, close=close_data)])
fig.show()