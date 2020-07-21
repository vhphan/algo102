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


def get_company_profile(symbol, return_type='dict'):
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


def get_recommendation_trends(symbol):
    recommendations = finnhub_client.recommendation_trends(symbol=symbol)
    results = [r.to_dict() for r in recommendations]
    # results = [dict(sell=r.sell,
    #                 buy=r.buy,
    #                 hold=r.hold,
    #                 period=r.period,
    #                 strong_buy=r.strong_buy,
    #                 strong_sell=r.strong_sell,
    #                 ) for r in recommendations]
    print(results)
    return results


def get_aggregate_indicators(symbol, resolution='D'):
    agg = finnhub_client.aggregate_indicator(symbol, resolution)
    return agg.to_dict();


def update_data_db():
    # get symbols
    stocks_list = get_symbols()
    stocks_df = pd.DataFrame(stocks_list)
    # for i, symbol in enumerate(['GOOG', 'AAPL', ]):
    j = 0
    for i, symbol in enumerate(stocks_df['symbol']):

        # get last date of symbol in database
        sql = f"SELECT Max(t) as max_date FROM stocks_finn_hub WHERE symbol='{symbol}'"
        df_last = pg_db.query_df(sql)

        # only get data if last day is more thn 1 day before today
        start = one_year_ago_u
        if today.day_of_week == 1:
            min_delta_days = 3 * 24 * 60 * 60
        else:
            min_delta_days = 1 * 24 * 60 * 60

        if len(df_last):
            if df_last.loc[0, 'max_date'] is not None:
                last_day_in_db = df_last.loc[0, 'max_date']
                start = last_day_in_db + 1 * 24 * 60 * 60

        # if df_last.loc[0, 'max_date']:
        #     last_day_in_db = df_last.loc[0, 't']
        #     next_day_in_db = pendulum.from_timestamp()
        # else:
        #     start_u = one_year_ago

        # delay => to not break API Limit

        if i % 1000 == 0 and i > 0:
            msg = f"<p>completed {i} stocks....</p>"
            send_eri_mail('phanveehuen@gmail.com', message_=msg, subject='finhubb data progress', message_type='html')

        last_slept_at = -1
        if j % 5 == 0 and j > 0 and j != last_slept_at:
            print('sleeping for 5 seconds...')
            time.sleep(5)
            last_slept_at = j

        if today_u - start > min_delta_days:
            candles_df = get_stock_data(symbol, start, today_u)
            j += 1

            if candles_df is not None and len(candles_df):
                try:
                    pg_db.df_to_db(candles_df, name='stocks_finn_hub', if_exists='append', index=False)
                except Exception as e:
                    print(e)
                    candles_df.to_csv(f'csv/{symbol.csv}')

                print(f'finished {i} {symbol}')
                continue

        print(f'skipping {symbol}')


if __name__ == '__main__':
    # update_data_db()
    r1 = get_aggregate_indicators('DOCU')
    r2 = get_recommendation_trends('DOCU')
