from yahooquery import Ticker

from data_providers.binance.binance_broker import ttm_squeeze_indicators
from lib.postgres_db import EPortalPGDB

pg_db = EPortalPGDB.Instance()


class MyYahoo:
    def __init__(self):
        pass

    @staticmethod
    def get_stock_data_db(symbol, num_months_ago=12):
        sql = f"""
            SELECT * FROM yahoo_stock_data 
                WHERE symbol='{symbol}' and 
                date>'now'::timestamp - '{num_months_ago} month'::interval order by date;
            """
        df = pg_db.query_df(sql)
        return df

    @staticmethod
    def get_stock_data(symbol, indicators=None):
        ticker = Ticker(symbol)
        df_ = ticker.history(period='2y', interval='1d')

        df_ = df_[['high', 'open', 'low', 'adjclose', 'volume']]
        df_.rename(columns={'adjclose': 'close'}, inplace=True)

        basic_cols = ['high', 'open', 'low', 'close', 'volume']
        if indicators is not None and 'ttm-squeeze' in indicators:
            df_ = ttm_squeeze_indicators(df_)
            basic_cols += [
                'lower_band',
                'upper_band',
                'lower_keltner',
                'upper_keltner',
                'linreg',
            ]

        return df_[basic_cols]


if __name__ == '__main__':
    df = MyYahoo.get_stock_data('GOOG', indicators='ttm-squeeze')
