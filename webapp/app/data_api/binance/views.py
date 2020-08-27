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
from lib.error_decorator import safe_run_flask

today = pendulum.today('UTC').strftime('%Y-%m-%d')
one_year_ago = pendulum.today('UTC').subtract(years=1).strftime('%Y-%m-%d')
default_start_end = dict(start=one_year_ago, end=today, interval='1d')

bb = Blueprint("bb", __name__, url_prefix='/bb')

bot_default = dict(coin='BTCUSDT', timeframe='1minute')
historical_default = dict(coin='BTCUSDT', timeframe='1minute')
binance_broker = BinanceBroker(is_live=True)


@bb.route('/')
def bb_index():
    return f"hello bb {datetime.now()}" \
 \
           @ bb.route('bot/', defaults=bot_default)


@bb.route('bot/<coin>/<timeframe>')
def bot(coin, timeframe):
    pass


@bb.route('squeeze-list')
def squeeze_list():
    squeeze_file = f"/home2/eproject/vee-h-phan.com/algo102/data_providers/binance/results/squeeze_list.json"
    with open(squeeze_file) as fp:
        parsed = json.load(fp)
    file_mtime = pendulum.from_timestamp(os.path.getmtime(squeeze_file), tz='UTC').strftime('%Y-%m-%d %H:%M UTC')
    pprint(dict(data=parsed, last_update=file_mtime))
    return dict(data=parsed, last_update=file_mtime)


@safe_run_flask
@bb.route("/hist/<symbol>", defaults=default_start_end)
@bb.route("/hist/<symbol>/<interval>/<start>/<end>")
@cache.memoize(timeout=300)
def historical(symbol, start, end, interval):
    indicators = request.args.get('indicators')

    pprint(indicators)
    df = binance_broker.get_historical_data(symbol, params=dict(start_str=start, end_str=end, interval=interval),
                                            indicators=indicators)
    df.reset_index(inplace=True)
    df['time'] = (df['datetime'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
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

    return df[final_cols].to_json(orient='records')
