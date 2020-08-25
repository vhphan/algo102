from pprint import pprint

import pandas as pd

from data_providers.finnhub.get_data_finnhub import get_stock_data_db, get_symbol_db
from data_providers.finnhub.initialize import pg_db


def is_consolidating(dataframe, window_percentage=2, window_length=15):
    c_max = dataframe[- window_length:]['c'].max()
    c_min = dataframe[- window_length:]['c'].min()
    if c_min / c_max >= (1 - window_percentage / 100):
        return True
    return False


def is_breaking_out(dataframe, window_percentage=2, window_length=15):
    if is_consolidating(dataframe[:-1]):

        c_max = dataframe[-1 - window_length:-1]['c'].max()
        # if dataframe[-1:].iloc[0, dataframe.columns.get_loc("c")] > c_max:
        if dataframe['c'].values[-1] > c_max:
            return True
    return False


def get_breakout_symbols(window_percentage=2, window_length=15, min_market_cap=100):
    """
    :return: list of symbols breaking out
    """
    results = []
    symbols_df = get_symbol_db(min_market_cap=min_market_cap)
    symbols = symbols_df['symbol'].values
    for i, symbol in enumerate(symbols, start=1):
        if i % 100 == 0:
            print(f'processing {i}/{len(symbols)}')
        df = get_stock_data_db(symbol=symbol)
        if len(df):
            if is_breaking_out(dataframe=df,
                               window_percentage=window_percentage,
                               window_length=window_length):
                results.append(symbol)
    return results


def get_breakout_symbols_db(window_percentage=2, window_length=15, min_market_cap=100):
    """
    :param window_percentage:
    :param window_length:
    :param min_market_cap:
    :return: list of symbols 'breaking' out of 'consolidation' on the latest candle
    """
    sql1 = f"""
        SELECT r.symbol, max(r.c), min(r.c), min(r.c) / nullif( max(r.c), 0) as min_max_ratio FROM
            (SELECT stocks_finn_hub.*,
                    rank() OVER (
                        PARTITION BY symbol
                        ORDER BY date DESC)
            FROM stocks_finn_hub) r WHERE RANK <= {window_length + 1} AND RANK>1
            GROUP BY r.symbol;
    """
    df1 = pg_db.query_df(sql1)
    df1 = df1[df1['min_max_ratio'] >= (1 - window_percentage / 100)]
    sql2 = f"""
            SELECT r.c, biz_fin.* FROM
(SELECT stocks_finn_hub.*,
        rank() OVER (
            PARTITION BY symbol
            ORDER BY date DESC)
FROM stocks_finn_hub) r 
INNER JOIN biz_fin USING (symbol)
WHERE RANK = 1
            """
    df2 = pg_db.query_df(sql2)

    df3 = pd.merge(df1, df2, on='symbol')

    result_df = df3[(df3['c'] > df3['max'])]

    return result_df


if __name__ == '__main__':
    breakouts = get_breakout_symbols_db()
    pprint(breakouts)
