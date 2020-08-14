##
import pandas as pd
import pendulum
import talib

##
from lib.helpers import get_pattern
from lib.postgres_db import EPortalPGDB
from screener.finnhub.get_data_finnhub import get_stock_data, get_symbols, get_stock_data_db
from screener.references.pattern_names import candlestick_patterns

# %%
APP_PATH = '/home/eproject/veehuen/python/algo102'
max_workers = 4
pg_db = EPortalPGDB.Instance()


##
def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def save_to_db(df, name):
    pg_db.df_to_db(df, if_exists='append', name=name, index=False)


def delete_dup_db(name, dup_cols=[]):
    criteria = [f't1.{col} = t2.{col}' for col in dup_cols]

    sql = f"""
    DELETE FROM {name} t1d
        USING {name} t2
        WHERE
            t1.id < t2.id AND
            {' AND '.join(criteria)};
    """

    # sql = f"""
    #     DELETE FROM {name}
    #     USING (
    #       SELECT
    #         ctid,
    #         (ctid != min(ctid) OVER (PARTITION BY {','.join(dup_cols)})) AS is_duplicate
    #       FROM {name}
    #     ) dups_find_duplicates
    #     WHERE {name}.ctid == dups_find_duplicates.ctid
    #     AND dups_find_duplicates.is_duplicate
    #
    # """

    return pg_db.execute(sql)


if __name__ == '__main__':
    # for symbol in symbols.copy():
    #     if os.path.isfile(f'{APP_PATH}/fbprophet/csv_forecast/{symbol}.zip'):
    #         symbols.remove(symbol)

    # chunks = chunk_it(symbols, max_workers)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     res = executor.map(func, chunks)
    #
    # for i in res:
    #     print(str(i))
    today = pendulum.today('UTC')
    one_year_ago = today.subtract(years=1)
    today_u = today.int_timestamp
    one_year_ago_u = one_year_ago.int_timestamp
    stocks_df = get_symbols()
    symbols = stocks_df['symbol'].to_list()

    candle_names = talib.get_function_groups()['Pattern Recognition']
    results = []
    for i, symbol in enumerate(symbols, start=1):
        df = get_stock_data_db(symbol)
        if not len(df):
            continue
        for candle in candle_names:
            df[candle] = get_pattern(df, candle)
        results.append(df)
        if i > 0 and i % 20 == 0:
            pg_db.df_to_db(pd.concat(results), if_exists='append', name='candlestick', index=False)
            results = []
        print(f'completed {i} of {len(symbols)}')
    res = delete_dup_db('candlestick', dup_cols=['date', 'symbol', 'granularity'])