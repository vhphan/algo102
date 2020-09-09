import json
from pathlib import Path

import pandas as pd
from datetime import datetime

from data_providers.binance.get_squeeze_list import breaking_out_of_squeeze
from data_providers.yahoo.my_yahoo import MyYahoo
from lib.my_email import send_eri_mail

my_yahoo = MyYahoo()


def get_stock_squeeze_list():
    pass


if __name__ == '__main__':
    get_stock_squeeze_list()
