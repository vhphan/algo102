import json
import os
import time
from datetime import datetime
from pprint import pprint

import pendulum
from flask import Blueprint, jsonify, request
import pandas as pd

from cache import cache
from data_providers.binance.binance_broker import BinanceBroker
from data_providers.yahoo.my_yahoo import MyYahoo
from lib.error_decorator import safe_run_flask

today = pendulum.today('UTC').strftime('%Y-%m-%d')
one_year_ago = pendulum.today('UTC').subtract(years=1).strftime('%Y-%m-%d')
default_start_end = dict(start=one_year_ago, end=today, interval='1d')

yh = Blueprint("yh", __name__, url_prefix='/yh')


@yh.route('/')
def yh_index():
    return f"hello yh {datetime.now()}"


@yh.route('squeeze-list')
def squeeze_list():
    squeeze_file = f"/home2/eproject/vee-h-phan.com/algo102/data_providers/yahoo/results/squeeze_list.json"
    with open(squeeze_file) as fp:
        parsed = json.load(fp)
    file_mtime = pendulum.from_timestamp(os.path.getmtime(squeeze_file), tz='UTC').strftime('%Y-%m-%d %H:%M UTC')
    pprint(dict(data=parsed, last_update=file_mtime))
    return dict(data=parsed, last_update=file_mtime)


@safe_run_flask
@yh.route("/hist/<symbol>")
@cache.memoize(timeout=300)
def historical(symbol, start, end, interval):
    indicators = request.args.get('indicators')

    pprint(indicators)
    df = MyYahoo.get_stock_data(symbol)

    df.reset_index(inplace=True)
    df['time'] = (df['date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    final_cols = ['time', 'open', 'high', 'low', 'close', 'volume']
    if indicators is not None:
        if ',' in indicators:
            indicators = indicators.split(',')
        if 'ttm-squeeze' in indicators:
            final_cols += ['lower_band',
                           'upper_band',
                           'lower_keltner',
                           'upper_keltner',
                           'linreg',
                           ]

    final_df = df[final_cols]
    return final_df.to_json(orient='records')
