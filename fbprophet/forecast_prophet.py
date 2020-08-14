##
# Use remote env =  fb102
import concurrent.futures
import pandas as pd
import sys
import os

from fbprophet import Prophet

##
APP_PATH = '/home/eproject/veehuen/python/algo102'
sys.path.append(APP_PATH)
sys.path.append(f"{APP_PATH}/lib")
from postgres_db import EPortalPGDB
from my_email import send_eri_mail
from error_decorator import safe_run


pg_db = EPortalPGDB.Instance()
max_workers = 4

##
stocks_df = pd.read_csv(f'{APP_PATH}/screener/finnhub/data/symbols_fin_hubb.csv')
symbols = stocks_df['symbol'].to_list()


##
def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


##
@safe_run
def forecast(symbols, min_points=120):
    err_symbols = []
    for symbol in symbols:
        try:
            df = pg_db.query_df(f"SELECT * FROM stocks_finn_hub WHERE symbol='{symbol}'")
            if len(df) > min_points:
                print(f'skipped {symbol}')
                df['ds'] = df['date'].dt.date
                df['y'] = df['c']
                model_prophet = Prophet(seasonality_mode='additive')
                model_prophet.add_seasonality(name='monthly', period=30.5,
                                              fourier_order=5)
                model_prophet.fit(df)
                df_future = model_prophet.make_future_dataframe(periods=182)
                weekend_index_f = df_future[df_future['ds'].dt.dayofweek >= 5].index
                df_future.drop(weekend_index_f, inplace=True)

                df_pred = model_prophet.predict(df_future)
                df_pred.to_csv(f'{APP_PATH}/fbprophet/csv_forecast/{symbol}.zip', compression='zip', index=False)
                print(f'completed {symbol}')
            print(f'skipping {symbol}')

        except Exception as e:
            print(f'error on {symbol}')
            err_symbols.append(symbol)

    msg = f'completed {len(symbols)} stocks'
    msg += f'error on {err_symbols}'
    send_eri_mail('phanveehuen@gmail.com', message_=msg, subject='finhubb fbprophet progress', message_type='html')
    return msg


if __name__ == '__main__':

    # for symbol in symbols.copy():
    #     if os.path.isfile(f'{APP_PATH}/fbprophet/csv_forecast/{symbol}.zip'):
    #         symbols.remove(symbol)

    chunks = chunk_it(symbols, max_workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        res = executor.map(forecast, chunks)

    for i in res:
        print(str(i))

    # %%
    symbol = 'DOCU'
    df = pg_db.query_df(f"SELECT * FROM stocks_finn_hub WHERE symbol='{symbol}'")