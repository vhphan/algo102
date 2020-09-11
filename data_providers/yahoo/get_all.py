# %%
# import yfinance as yf
from yahooquery import Ticker
from get_all_tickers import get_tickers as gt
from data_providers.finnhub.initialize import pg_db
import pandas as pd

DB_COLUMNS = [
    'date',
    'low',
    'close',
    'open',
    'high',
    'volume',
    'adjclose',
    'dividends',
    'symbol',
    'splits',
]


def get_all(symbols):
    # %%

    print(len(symbols))
    # %%
    all_tickers = Ticker(symbols)
    df2 = all_tickers.history(period='2y', interval='1d')

    if isinstance(df2, pd.core.frame.DataFrame) and not df2.empty:
        pg_db.df_to_db(df2.reset_index()[DB_COLUMNS], name='temp_yahoo_stock_data', if_exists='replace', index=False)

    # %%
    else:
        final_df = pd.DataFrame()
        for idx, (symbol, dataframe) in enumerate(df2.items(), start=1):
            print(symbol)
            if isinstance(dataframe, pd.core.frame.DataFrame) and not dataframe.empty:
                print(dataframe.head())
                dataframe['symbol'] = symbol
                dataframe.reset_index(inplace=True)
                dataframe.rename(columns={'index': 'date'}, inplace=True)

                final_df = pd.concat([final_df, dataframe])
            if idx % 100 == 0 or idx == len(df2):
                if_exists = 'replace' if idx == 100 else 'append'
                try:
                    if if_exists == 'replace' and 'splits' not in final_df.columns:
                        final_df['splits'] = None

                    pg_db.df_to_db(final_df[DB_COLUMNS], name='temp_yahoo_stock_data', if_exists=if_exists, index=False)

                except AttributeError:
                    print(final_df)

            print(f'completed {symbol}, {idx} of {len(df2)}')


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    symbols = gt.get_tickers(NYSE=True, NASDAQ=True, AMEX=True)
    for i, chunk in enumerate(chunks(symbols, 200), start=1):
        get_all(chunk)

        sql = f"""
                  INSERT INTO yahoo_stock_data
                    (SELECT t.date,
                            t.low,
                            t.close,
                            t.open,
                            t.high,
                            t.volume,
                            t.adjclose,
                            t.dividends,
                            t.symbol,
                            t.splits
                     FROM temp_yahoo_stock_data t
                     WHERE NOT EXISTS(SELECT *
                                      FROM yahoo_stock_data y
                                      WHERE t.symbol = y.symbol
                                        and t.date = y.date))
            """
        res = pg_db.query(sql)
        print(f'finished {i} batch = {i * 200}')


if __name__ == '__main__':
    main()
