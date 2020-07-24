import json

import requests

from private.keys import alpha_vantage_key

api_key = alpha_vantage_key.get('api')

base_url = 'https://www.alphavantage.co'


def get_company_overview(symbol):
    params = {'function': 'OVERVIEW', 'symbol': symbol, 'apikey': api_key}
    url = f'{base_url}/query'
    r = requests.get(url, params)
    return json.loads(r.text)


def get_tech_ind(symbol, time_period, interval='daily', series_type='close', function="SMA"):
    params = dict(function=function,
                  interval=interval,
                  time_period=time_period,
                  series_type=series_type,
                  symbol=symbol,
                  apikey=api_key
                  )
    url = f'{base_url}/query'
    r = requests.get(url, params)
    return json.loads(r.text)


if __name__ == '__main__':
    r = get_tech_ind('DOCU', 50)
