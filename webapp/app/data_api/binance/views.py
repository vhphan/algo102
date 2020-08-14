from flask import Blueprint

bb = Blueprint("bb", __name__, url_prefix='/bb')

bot_default = dict(coin='BTCUSDT', timeframe='1minute')
historical_default = dict(coin='BTCUSDT', timeframe='1minute')


@bb.route('bot/', defaults=bot_default)
@bb.route('bot/<coin>/<timeframe>')
def bot(coin, timeframe):
    pass
