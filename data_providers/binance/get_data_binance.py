# %%
import math
import pathlib
import time
from datetime import datetime

from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.helpers import date_to_milliseconds

import pendulum
from binance.client import Client
from sqlalchemy import create_engine

from data_providers.binance.binance_broker import BinanceBroker
from private.keys import connection_strings, binance_keys
import pandas as pd

import pendulum

bin_minutes = {"1m": 1, "5m": 5, "1h": 60, "4h": 240, "1d": 1440}

bb = BinanceBroker(is_live=True)


# %%
def get_symbol_data(symbol, start=None, num_candles=200, interval=None):
    """

    :param symbol: string
    :param start: datetime e.g pendulum.from_format('2020-01-01', fmt='YYYY-MM-DD')
    :param num_candles: integer
    :param interval: string
    :return: dataframe
    """
    if interval is None:
        interval = bb.client.KLINE_INTERVAL_4HOUR
    now = pendulum.now('UTC')
    end = now.add(minutes=10 * bin_minutes.get(interval))  # add some buffer to end date

    # use num of candles if start is not given
    if start is None:
        start = now.subtract(minutes=num_candles * bin_minutes.get(interval))

    return bb.client.get_historical_data(symbol,
                                         dict(interval=interval,
                                              start_str=start.int_timestamp * 1000,
                                              end_str=end.int_timestamp * 1000,
                                              ))


if __name__ == '__main__':
    # %%
    all_tickers = bb.client.get_all()
    ticket_base_btc = [ticker.get('symbol') for ticker in all_tickers if ticker.get('symbol').endswith('BTC')]
    ticket_base_usdt = [ticker.get('symbol') for ticker in all_tickers if ticker.get('symbol').endswith('USDT')]
