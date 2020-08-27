import json

import pandas as pd
from datetime import datetime

from data_providers.binance.get_squeeze_list import breaking_out_of_squeeze
from data_providers.finnhub.get_data_finnhub import get_symbol_db, get_stock_data_db


def get_stock_squeeze_list():
    symbols_df = get_symbol_db()
    squeeze_list = []
    for symbol in symbols_df['symbol']:
        print(symbol)
        try:
            df = get_stock_data_db(symbol, num_months_ago=3)
            df.rename(columns={
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
            }, inplace=True)
            if len(df) > 200 and breaking_out_of_squeeze(df):
                print(f"{symbol} is coming out the squeeze")
                squeeze_list.append(symbol)

        except Exception as e:
            print(e)
            continue

    if squeeze_list:
        with open(f"results/squeeze_list_stocks.json", 'w') as fp:
            json.dump(squeeze_list, fp)


if __name__ == '__main__':
    get_stock_squeeze_list()
