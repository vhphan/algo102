# modified from link below:
# https://towardsdatascience.com/how-to-access-stocks-market-data-for-machine-learning-on-python-c69db51e7a0d


from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
import time

import alpaca_trade_api as tradeapi

from private.keys import alpaca_key


def break_period_in_dates_list(start_date, end_date, days_per_step):
    """Break period between start_date and end_date in steps of days_per_step days."""
    step_start_date = start_date
    delta = timedelta(days=days_per_step)
    dates_list = []
    while end_date > (step_start_date + delta):
        dates_list.append((step_start_date, step_start_date + delta))
        step_start_date += delta
    dates_list.append((step_start_date, end_date))
    return dates_list


def format_timestep_list(timestep_list):
    """Format dates in ISO format plus timezone. Note that first day starts at 00:00 and last day ends at 23:00hs."""
    for i, d in enumerate(timestep_list):
        timestep_list[i] = (d[0].isoformat() + '-04:00', (d[1].isoformat().split('T')[0] + 'T23:00:00-04:00'))
    return timestep_list


def get_df_from_barset(barset):
    """Create a Pandas Dataframe from a barset."""
    df_rows = []
    for symbol, bar in barset.items():
        rows = bar.__dict__.get('_raw')
        for i, row in enumerate(rows):
            row['symbol'] = symbol
        df_rows.extend(rows)

    return pd.DataFrame(df_rows)


def download_data(aps, symbols, start_date, end_date, filename='data.csv'):
    """Download data from REST manager for list of symbols, from start_date at 00:00hs to end_date at 23:00hs,
    and save it to filename as a csv file."""
    timesteps = format_timestep_list(break_period_in_dates_list(start_date, end_date, 10))
    df = pd.DataFrame()

    for timestep in tqdm(timesteps):
        barset = aps.get_barset(symbols, '5Min', limit=1000, start=timestep[0], end=timestep[1])
        df = df.append(get_df_from_barset(barset))
        time.sleep(0.1)

    df.to_csv(filename)


if __name__ == '__main__':

    # Call method.
    aps = tradeapi.REST(key_id=alpaca_key['api_key'],
                        secret_key=alpaca_key['secret_key'],
                        base_url='https://paper-api.alpaca.markets')

    download_data(aps=aps,
                  symbols=['AAPL', 'GOOG'],
                  start_date=datetime.strptime('01/01/20', '%d/%m/%y'),
                  end_date=datetime.strptime('01/02/20', '%d/%m/%y'),
                  filename='test.csv')
