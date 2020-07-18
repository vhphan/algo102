import time
import pendulum
import pandas as pd
import datetime
from datetime import timezone
import finnhub

# Configure API key
from lib.my_email import send_eri_mail
from lib.retry_decorator import Retry
from screener.finnhub.initialize import pg_db, finnhub_client

# Set start date and end date
today = pendulum.today('UTC')
one_year_ago = today.subtract(years=1)
today_u = today.int_timestamp
one_year_ago_u = one_year_ago.int_timestamp
print(today_u, one_year_ago_u)


@Retry(tries=3, delay=30)
def get_stock_data(symbol, start, end, timeframe='D'):
    print(f'getting {symbol}')

    if not isinstance(start, int):
        start = int(start)
    if not isinstance(end, int):
        end = int(end)
    candles = finnhub_client.stock_candles(symbol, timeframe, start, end)
    if getattr(candles, 's') == 'ok':
        candles_df = pd.DataFrame(candles.to_dict())
        candles_df['symbol'] = symbol
        candles_df['date'] = pd.to_datetime(candles_df['t'], unit='s')
        candles_df['granularity'] = timeframe
        candles_df.drop('s', axis=1, inplace=True)
        print(f'got {len(candles_df)} rows....')
        return candles_df
    return None


def get_symbols(return_type='dataframe'):
    stocks = finnhub_client.stock_symbols('US')
    stocks_dict = [stock.to_dict() for stock in stocks]
    if return_type == 'dataframe':
        pd.DataFrame(stocks_dict)
    return stocks_dict


def get_top_picks():
    return pd.read_csv('/home2/eproject/veehuen/python/algo102/fbprophet/growth_stocks.csv')


def comp_prof(symbol, return_type='dict'):
    profile_ = finnhub_client.company_profile2(symbol=symbol)
    if return_type == 'dict':
        return profile_.__dict__
    if return_type == 'html':
        df = pd.DataFrame.from_dict(profile_.__dict__, orient='index')
        df.columns = ['Company Profile']
        df.drop(index='local_vars_configuration', inplace=True)
        df.drop(index='_logo', inplace=True)
        # df.loc[
            # '_weburl', 'Company Profile'] = f"<a href='{df.loc['_weburl', 'Company Profile']}'>{df.loc['_weburl', 'Company Profile']}</a>"
        df.index = [i[1:] for i in df.index]
        return df.to_html(table_id='company-profile')


if __name__ == '__main__':
    r = comp_prof('CLDX', return_type='html')
    print(r)
