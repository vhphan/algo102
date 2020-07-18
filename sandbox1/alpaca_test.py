# %%
import alpaca_trade_api as tradeapi
import pandas as pd

# %%
from private.keys import alpaca_key

api = tradeapi.REST(key_id=alpaca_key['api_key'],
                        secret_key=alpaca_key['secret_key'],
                        base_url='https://paper-api.alpaca.markets')

# %%
# Get a list of all active assets.
active_assets = api.list_assets(status='active')

# %%
# Filter the assets down to just those on NASDAQ.
nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
print(nasdaq_assets)

# %%
active_assets_list_dicts = [a.__dict__.get('_raw') for a in active_assets]
active_assets_df = pd.DataFrame(active_assets_list_dicts)