# https://medium.com/swlh/retrieving-full-historical-data-for-every-cryptocurrency-on-binance-bitmex-using-the-python-apis-27b47fd8137f

# IMPORTS
import json
from pathlib import Path

import pandas as pd
import math
import os.path
import time

import pendulum as pendulum
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook  # (Optional, used for progress-bars)

### API
from data_providers.finnhub.initialize import pg_db
from lib.my_email import send_eri_mail
from private.keys import binance_keys

binance_api_key = binance_keys['api']  # Enter your own API-key here
binance_api_secret = binance_keys['secret_key']  # Enter your own API-secret here

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "4h": 240, "1d": 1440}
batch_size = 750
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:
        old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance":
        old = datetime.strptime('1 Jan 2017', '%d %b %Y')

    if source == "binance":
        new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0],
                             unit='ms')

    return old, new


def get_all_binance(symbol, kline_size, save=False, save_to_db=False):
    filename = f'data/{symbol}-{kline_size}-data.zip'
    if os.path.isfile(filename):
        data_df = pd.read_csv(filename)
    else:
        data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source="binance")
    delta_min = (newest_point - oldest_point).total_seconds() / 60
    available_data = math.ceil(delta_min / binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'):
        print(f'Downloading all available {kline_size} data for {symbol}. Be patient..!')
    else:
        print(
            f'Downloading {delta_min:d} minutes of new data available for {symbol}, i.e. {available_data:d} instances of {kline_size} data.')
    klines = binance_client.get_historical_klines(symbol,
                                                  kline_size,
                                                  oldest_point.strftime("%d %b %Y %H:%M:%S"),
                                                  newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines,
                        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    temp_df = None
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else:
        data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save:
        archive_name = f'{symbol}-{kline_size}-data.csv'
        compression_options = dict(method='zip', archive_name=archive_name)
        data_df.to_csv(filename, compression=compression_options)
    if save_to_db and temp_df is not None:
        temp_df.set_index('timestamp', inplace=True)
        temp_df['interval'] = kline_size
        temp_df['symbol'] = symbol
        pg_db.df_to_db(temp_df, name='binance', if_exists='append', index=False)

    print('All caught up..!')
    return data_df


def save_files_to_db():
    current_file_path = Path(__file__).parent.absolute()
    for idx, file in enumerate(Path(f"{current_file_path}/data").glob('*-1d-data.zip'), start=1):
        symbol = Path(file).stem.split('-')[0]
        df = pd.read_csv(file, parse_dates=['timestamp'], index_col='timestamp')
        df['interval'] = '1d'
        df['symbol'] = symbol
        if_exists = 'replace' if idx == 1 else 'append'
        pg_db.df_to_db(df, name='binance', if_exists=if_exists, index=True)
        msg = f'finished {idx} symbols'
        print(msg)
        if idx % 1000 == 0:
            send_eri_mail('phanveehuen@gmail.com', msg, 'files 2 db progress')


def get_all():
    symbols = get_all_tickers()
    # tickers_base_usdt = [ticker.get('symbol') for ticker in tickers if ticker.get('symbol').endswith('USDT')]
    for idx, symbol in enumerate(symbols):
        print(f'getting data for {symbol} ...')
        start_time = pendulum.now()
        df = get_all_binance(symbol['symbol'], '1d', save=True)
        end_time = pendulum.now()
        print('time taken in minutes ', end_time.diff(start_time).in_minutes())
        print('time taken in seconds ', end_time.diff(start_time).in_seconds())
        if idx % 3 == 0:
            time.sleep(1)


def get_all_tickers():
    tickers = binance_client.get_all_tickers()
    symbols = [binance_client.get_symbol_info(ticker.get('symbol')) for ticker in tickers]
    with open(f"results/all_tickers_{datetime.today().strftime('%Y%m%d')}.json", 'w') as fp:
        json.dump(symbols, fp)
    return symbols


if __name__ == '__main__':
    # d = get_all_tickers()
    # get_all()

    save_files_to_db()
