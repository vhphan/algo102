import pendulum
from flask import Blueprint, jsonify
import sys

from screener.finnhub.get_data_finnhub import get_stock_data, get_symbols, get_top_picks, comp_prof

fh = Blueprint("fh", __name__, url_prefix='/fh')

today_ts = pendulum.today('UTC').int_timestamp
current_ts = pendulum.now('UTC').int_timestamp
three_months_ago_ts = pendulum.today('UTC').subtract(months=3).int_timestamp
six_months_ago_ts = pendulum.today('UTC').subtract(months=6).int_timestamp
default_start_end = dict(start=six_months_ago_ts, end=current_ts, timeframe='D')


@fh.route("/hist/<symbol>", defaults=default_start_end)
@fh.route("/hist/<symbol>/<timeframe>/<start>/<end>")
def historical(symbol, start, end, timeframe):
    candles_df = get_stock_data(symbol=symbol, start=start, end=end, timeframe=timeframe)
    candles = candles_df[['t', 'o', 'h', 'l', 'c', 'v']].rename(columns={
        't': 'time',
        'o': 'open',
        'h': 'high',
        'l': 'low',
        'c': 'close',
        'v': 'volume'
    }).to_dict('records')
    return jsonify(candles)


@fh.route('/symbols')
def fh_symbols():
    return jsonify(get_symbols())


@fh.route('/top-picks')
def fh_top_picks():
    return jsonify(get_top_picks().head(100).to_dict(orient='records'))


@fh.route('/')
def fh_index():
    return 'hello fh'


@fh.route('/company-profile/<symbol>')
def company_profile(symbol):
    return comp_prof(symbol, return_type='html')
