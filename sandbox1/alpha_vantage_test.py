# company overview
# https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
import json

import requests

from private.keys import alpha_vantage_key
api_key = alpha_vantage_key.get('api')

symbol = 'DOCU'
url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
r = requests.get(url)
res = json.loads(r.text)