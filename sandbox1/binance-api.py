from binance.client import Client
from sqlalchemy import create_engine

from private.keys import binance_keys, connection_strings
import pandas as pd

binance_client = Client(binance_keys.get('api'), binance_keys.get('secret_key'))


def get_historical_data(symbol, params):
    crypto_data = binance_client.get_historical_klines(symbol=symbol, **params)
    columns = ['datetime',
               'open',
               'high',
               'low',
               'close',
               'volume',
               'close time',
               'quote asset volume',
               'number of trades',
               'taker buy base asset volume',
               'taker buy quote asset volume',
               'ignore']

    df = pd.DataFrame(crypto_data, columns=columns)
    df['symbol'] = symbol
    df['granularity'] = params.get('interval')
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric,
                                                                                                          errors='coerce')
    df.dropna(inplace=True)
    df.set_index(['symbol', 'datetime', 'granularity'], inplace=True)
    return df[['open', 'high', 'low', 'close', 'volume']]


# prices = client.get_all_tickers()
# symbol = 'BTCUSDT'
# candles = binance_client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE)
# columns = ['Open time',
#            'Open',
#            'High',
#            'Low',
#            'Close',
#            'Volume',
#            'Close time',
#            'Quote asset vol',
#            'Number of trade',
#            'Taker buy base',
#            'Taker buy quote',
#            'Can be ignored']
# df = pd.DataFrame(candles, columns=columns)
# connection = connection_strings.get('ep_fx')
# engine = create_engine(connection, echo=False)
# df['granularity'] = '15m'
# df.to_sql('btcusdt', con=engine)

# candles format
# [
#     [
#         1499040000000,      # Open time
#         "0.01634790",       # Open
#         "0.80000000",       # High
#         "0.01575800",       # Low
#         "0.01577100",       # Close
#         "148976.11427815",  # Volume
#         1499644799999,      # Close time
#         "2434.19055334",    # Quote asset volume
#         308,                # Number of trades
#         "1756.87402397",    # Taker buy base asset volume
#         "28.46694368",      # Taker buy quote asset volume
#         "17928899.62484339" # Can be ignored
#     ]
# ]

if __name__ == '__main__':
    params = dict(interval='4h', start_str='2017-01-01', end_str='2020-06-30')
    symbol = 'BTCUSDT'
    df = get_historical_data(symbol, params)
    connection = connection_strings.get('ep_fx')
    engine = create_engine(connection, echo=False)
    df.to_sql(symbol.lower(), con=engine, if_exists='replace')
