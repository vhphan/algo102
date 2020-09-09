import json
from pathlib import Path

import pandas as pd
from datetime import datetime

from data_providers.binance.get_squeeze_list import breaking_out_of_squeeze
from data_providers.finnhub.get_data_finnhub import get_symbol_db, get_stock_data_db
from lib.my_email import send_eri_mail


def get_stock_squeeze_list():
    symbols_df = get_symbol_db()
    squeeze_list = []
    for symbol in symbols_df['symbol']:
        try:
            df = get_stock_data_db(symbol, num_months_ago=9)
            df.rename(columns={
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
            }, inplace=True)
            if len(df) > 90 and breaking_out_of_squeeze(df):
                print(f"{symbol} is coming out the squeeze")
                squeeze_list.append(symbol)

        except Exception as e:
            print(e)
            continue

    if squeeze_list:
        with open(f"{Path(__file__).parent.absolute()}/results/squeeze_list_stocks.json", 'w') as fp:
            recipient, message, subject = ['phanveehuen@gmail.com',
                                           f'stocks squeeze list successfully generated at {datetime.now()}',
                                           'squeezed']
            send_eri_mail(recipient, message, subject)
            json.dump(squeeze_list, fp)


if __name__ == '__main__':
    get_stock_squeeze_list()
