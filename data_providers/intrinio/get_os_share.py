from __future__ import print_function

import datetime
import json
import pathlib
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from pprint import pprint

from private.keys import intrinio_keys

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
key = intrinio_keys['sb_key']
intrinio_sdk.ApiClient().configuration.api_key['api_key'] = key

from get_all_tickers import get_tickers as gt

symbols = gt.get_tickers(NYSE=True, NASDAQ=True, AMEX=True)

company_api = intrinio_sdk.CompanyApi()
for i, symbol in enumerate(symbols):
    try:
        shares_os = company_api.get_company_historical_data(symbol, tag='adjweightedavebasicsharesos',
                                                            start_date='2000-01-01').to_dict()


        def my_converter(o):
            if isinstance(o, datetime.date):
                return o.__str__()


        with open(f'{CURRENT_PATH}/data/{symbol}_shares_os.json', 'w') as f:
            json.dump(shares_os, f, default=my_converter)
        print(f'completed {symbol}')

    except ApiException as e:
        print(e)
        print(f'skipping {symbol}')
        continue

    if i == 50:
        break
