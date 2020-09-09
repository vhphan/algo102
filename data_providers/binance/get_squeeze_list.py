# %%
# import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import sqlalchemy
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# %%
from data_providers.binance.get_all import get_all_tickers
from data_providers.finnhub.initialize import pg_db
from lib.my_email import send_eri_mail
from private.keys import coin_market_cap_keys


def breaking_out_of_squeeze(df):
    df['sma20'] = df['close'].rolling(window=20).mean()
    df['stddev'] = df['close'].rolling(window=20).std()
    df['lower_band'] = df['sma20'] - (2 * df['stddev'])
    df['upper_band'] = df['sma20'] + (2 * df['stddev'])

    df['TR'] = abs(df['high'] - df['low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['sma20'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['sma20'] + (df['ATR'] * 1.5)

    df['squeeze_on'] = df.apply(
        lambda x: x['lower_band'] > x['lower_keltner'] and x['upper_band'] < x['upper_keltner'] and x[
            'lower_band'] > 0 and x['lower_keltner'] > 0,
        axis=1)

    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        return True
    return False


def top_coin_cmc():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coin_market_cap_keys['api_key'],
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        data_df = pd.DataFrame(data['data'])
        pg_db.df_to_db(data_df,
                       name='cmc_listings',
                       if_exists='replace',
                       index=False,
                       dtype={
                           'quote': sqlalchemy.types.JSON,
                           'platform': sqlalchemy.types.JSON,
                       },
                       )

        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def save_top_coins():
    symbols_file = f"{Path(__file__).parent.absolute()}/results/all_tickers_cmc.json"
    top_coins = top_coin_cmc()
    with open(symbols_file, 'w') as fp:
        json.dump(top_coins['data'], fp)


def get_crypto_squeeze_list():
    symbols_file = f"{Path(__file__).parent.absolute()}/results/all_tickers_cmc.json"
    if not os.path.isfile(symbols_file):
        top_coins = top_coin_cmc()
        with open(symbols_file, 'w') as fp:
            json.dump(top_coins['data'], fp)

    symbols_df = pd.read_json(symbols_file, 'r')

    squeeze_list = []
    base_symbols = ['USDT', 'BTC', 'ETH']

    binance_symbols = [{'symbol': symbol + base_symbol,
                        'quote_symbol': symbol}
                       for base_symbol in base_symbols
                       for symbol in symbols_df['symbol'] if symbol != base_symbol]

    for item in binance_symbols:
        # print(symbol)
        symbol = item['symbol']
        try:
            df = pd.read_csv(f'data/{symbol}-1d-data.zip')
            if len(df) > 200 and breaking_out_of_squeeze(df):
                print(f"{symbol} is coming out the squeeze")
                squeeze_list.append(dict(symbol=symbol, quote_symbol=item['quote_symbol']))

        except FileNotFoundError:
            continue

    if squeeze_list:
        with open(f"{Path(__file__).parent.absolute()}/results/squeeze_list.json", 'w') as fp:
            recipient, message, subject = ['phanveehuen@gmail.com',
                                           f'crypto squeeze list successfully generated at {datetime.now()}',
                                           'squeezed']
            send_eri_mail(recipient, message, subject)
            return json.dump(squeeze_list, fp)


if __name__ == '__main__':
    save_top_coins()
    get_crypto_squeeze_list()
