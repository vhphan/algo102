import json
from datetime import datetime
from pprint import pprint

import pendulum
from flask import Blueprint, jsonify

from cache import cache
from data_providers.binance.binance_broker import BinanceBroker
from error_decorator import safe_run_flask

today = pendulum.today('UTC').strftime('%Y-%m-%d')
one_year_ago = pendulum.today('UTC').subtract(years=1).strftime('%Y-%m-%d')
default_start_end = dict(start=one_year_ago, end=today, interval='1d')

bb = Blueprint("bb", __name__, url_prefix='/bb')

bot_default = dict(coin='BTCUSDT', timeframe='1minute')
historical_default = dict(coin='BTCUSDT', timeframe='1minute')
binance_broker = BinanceBroker(is_live=True)


@bb.route('/')
def bb_index():
    return f"hello bb {datetime.now()}"


@bb.route('bot/', defaults=bot_default)
@bb.route('bot/<coin>/<timeframe>')
def bot(coin, timeframe):
    pass


@bb.route('squeeze-list')
def squeeze_list():
    with open(
            f"/home2/eproject/vee-h-phan.com/algo102/data_providers/binance/data/squeeze_list_{datetime.now().strftime('%Y%m%d')}.json") as fp:
        parsed = json.load(fp)
    pprint(parsed)
    return jsonify(parsed)


@safe_run_flask
@bb.route("/hist/<symbol>", defaults=default_start_end)
@bb.route("/hist/<symbol>/<interval>/<start>/<end>")
@cache.memoize(timeout=300)
def historical(symbol, start, end, interval):
    print(symbol, start, end, interval)
    df = binance_broker.get_historical_data(symbol, params=dict(start_str=start, end_str=end, interval=interval))
    return df.to_json()
