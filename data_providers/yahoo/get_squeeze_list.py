import json
from pathlib import Path

import pandas as pd
from datetime import datetime

from data_providers.binance.get_squeeze_list import breaking_out_of_squeeze
from data_providers.yahoo.my_yahoo import MyYahoo
from lib.my_email import send_eri_mail
from get_all_tickers import get_tickers as gt


# my_yahoo = MyYahoo()


def get_stock_squeeze_list():
    squeeze_list = []
    symbols = gt.get_tickers(NYSE=True, NASDAQ=True, AMEX=True)
    for symbol in symbols:
        df = MyYahoo.get_stock_data_db(symbol)
        if len(df) > 120 and breaking_out_of_squeeze(df):
            print(f"{symbol} is coming out the squeeze")
            squeeze_list.append(dict(symbol=symbol))
    if squeeze_list:
        with open(f"{Path(__file__).parent.absolute()}/results/squeeze_list.json", 'w') as fp:
            recipient, message, subject = ['phanveehuen@gmail.com',
                                           f'yahoo stock squeeze list successfully generated at {datetime.now()}',
                                           'squeezed']
            send_eri_mail(recipient, message, subject)
            json.dump(squeeze_list, fp)
            return True


if __name__ == '__main__':
    get_stock_squeeze_list()
