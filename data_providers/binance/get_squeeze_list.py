# %%
# import json
import json
import os
from datetime import datetime

import pandas as pd
import talib as ta


# %%
from data_providers.binance.get_all import get_all, get_all_tickers


def breaking_out_of_squeeze(df):
    df['sma20'] = df['close'].rolling(window=20).mean()
    df['stddev'] = df['close'].rolling(window=20).std()
    df['lower_band'] = df['sma20'] - (2 * df['stddev'])
    df['upper_band'] = df['sma20'] + (2 * df['stddev'])

    df['TR'] = abs(df['high'] - df['low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['sma20'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['sma20'] + (df['ATR'] * 1.5)

    df['squeeze_on'] = df.apply(lambda x: x['lower_band'] > x['lower_keltner'] and x['upper_band'] < x['upper_keltner'],
                                axis=1)

    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        return True
    return False


def get_crypto_squeeze_list():

    symbols_file = f"data/all_tickers_{datetime.today().strftime('%Y%m%d')}.json"
    if not os.path.isfile(symbols_file):
        get_all_tickers()

    symbols_df = pd.read_json(symbols_file, 'r')
    squeeze_list = []
    for symbol in symbols_df['symbol']:
        print(symbol)

        try:
            df = pd.read_csv(f'data/{symbol}-1d-data.zip')
            if len(df) > 200 and breaking_out_of_squeeze(df):
                print(f"{symbol} is coming out the squeeze")
                squeeze_list.append(dict(symbol=symbol))

        except FileNotFoundError:
            continue

    if squeeze_list:
        with open(f"data/squeeze_list_{datetime.now().strftime('%Y%m%d')}.json", 'w') as fp:
            return json.dump(squeeze_list, fp)


if __name__ == '__main__':
    get_crypto_squeeze_list()
