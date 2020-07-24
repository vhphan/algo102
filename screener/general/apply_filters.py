import json
import time
from datetime import datetime
from random import randint

import pandas as pd

from lib.helpers import dict_to_json_zipped
from lib.my_email import send_eri_mail
from screener.alphavantage.get_data_alphavantage import get_company_overview, get_tech_ind
from screener.finnhub.get_data_finnhub import get_symbols, get_basic_financials
from screener.finnhub.initialize import pg_db, finnhub_client


# The current price > SMA50 > SMA150 > SMA200
# The current price must be at least 30% above the 52 week low.
# The current price must be within 25% of the 52 week high.
# price_relative_to_SP500 for 4, 13, 26 weeks > 30%

def apply_the_filters(start_row=0):
    global df_symbol
    # %% 0 get all symbols
    df_symbols = get_symbols()
    df_forecast = pd.read_csv('/home2/eproject/veehuen/python/algo102/fbprophet/growth_stocks.csv')
    # %%
    df_forecast['condition_1'] = False
    df_forecast['condition_2'] = False
    df_forecast['condition_3'] = False
    df_forecast['sma_50'] = None
    df_forecast['sma_150'] = None
    df_forecast['sma_200'] = None
    df_forecast['52WeekHigh'] = None
    df_forecast['52WeekLow'] = None
    df_forecast['priceRelativeToS&P50013Week'] = None
    df_forecast['priceRelativeToS&P50026Week'] = None
    df_forecast['priceRelativeToS&P5004Week'] = None
    # %% 1 get current price per symbol
    filtered_symbol = []
    for i, row in df_forecast[start_row:].iterrows():
        conditions = [False] * 3
        # if i % 1500 == 0 and i > 0:
        #     break
        symbol = row['symbol']
        print(i, symbol, datetime.now())
        moving_averages = []
        for window in [50, 150, 200]:
            sql = f"SELECT * FROM stocks_finn_hub WHERE symbol='{symbol}' order by DATE DESC LIMIT 200"
            df_symbol = pg_db.query_df(sql)
            df_symbol.index = df_symbol['date'].dt.date
            df_symbol.sort_index(inplace=True)
            df_symbol['sma_50'] = df_symbol['c'].rolling(50).mean()
            df_symbol['sma_150'] = df_symbol['c'].rolling(150).mean()
            df_symbol['sma_200'] = df_symbol['c'].rolling(200).mean()
            current = df_symbol.iloc[-1]['c']
            sma_50 = df_symbol.iloc[-1]['sma_50']
            sma_150 = df_symbol.iloc[-1]['sma_150']
            sma_200 = df_symbol.iloc[-1]['sma_200']

            df_forecast.loc[i, 'sma_50'] = sma_50
            df_forecast.loc[i, 'sma_150'] = sma_150
            df_forecast.loc[i, 'sma_200'] = sma_200

            try:
                if current > sma_50 > sma_150 > sma_200:
                    conditions[0] = True
                    df_forecast.loc[i, 'condition_1'] = True
            except TypeError:
                continue
        try:
            bs = get_basic_financials(symbol, 'price')
            data_folder = '/home2/eproject/vee-h-phan.com/algo102/screener/finnhub/data'
            dict_to_json_zipped(bs, f'{data_folder}/bs_{symbol}.json.gzip')

        except Exception as e:
            send_eri_mail('phanveehuen@gmail.com', e.__repr__(), 'finhubb error: bs')

        if i % 3 == 0:
            sleep_time = randint(1, 5)
            print(i, f'sleeping {sleep_time} seconds')
            time.sleep(sleep_time)

        high_52_week = bs.get('metric').get('52WeekHigh')
        low_52_week = bs.get('metric').get('52WeekLow')
        df_forecast.loc[i, '52WeekHigh'] = high_52_week
        df_forecast.loc[i, '52WeekLow'] = low_52_week

        try:
            if current / low_52_week > 1.3 and current / high_52_week > 0.75:
                conditions[1] = True
                df_forecast.loc[i, 'condition_2'] = True
        except TypeError:

            continue

        price_relative_to_SP500 = [
            bs.get('metric').get('priceRelativeToS&P50013Week'),
            bs.get('metric').get('priceRelativeToS&P50026Week'),
            bs.get('metric').get('priceRelativeToS&P5004Week'),
            # bs.get('metric').get('priceRelativeToS&P50052Week'),
        ]
        df_forecast.loc[i, 'priceRelativeToS&P50013Week'] = price_relative_to_SP500[0]
        df_forecast.loc[i, 'priceRelativeToS&P50026Week'] = price_relative_to_SP500[1]
        df_forecast.loc[i, 'priceRelativeToS&P5004Week'] = price_relative_to_SP500[2]
        try:
            if all(i >= 30 for i in price_relative_to_SP500):
                conditions[2] = True
                df_forecast.loc[i, 'condition_3'] = True
        except TypeError:
            continue

        if all(conditions):
            filtered_symbol.append(symbol)
            print(filtered_symbol)
            print(df_forecast.loc[i])

        if i % 1000 == 0 and i > 0:
            df_forecast.to_csv(f'/home2/eproject/vee-h-phan.com/algo102/fbprophet/growth_stocks_filtered_{i}.csv',
                               index=False)
        if i % 100 == 0 and i > 0:
            send_eri_mail('phanveehuen@gmail.com', f'processed {i} symbols', 'finhubb progress: bs')

    df_forecast.to_csv('/home2/eproject/vee-h-phan.com/algo102/fbprophet/growth_stocks_filtered.csv', index=False)


if __name__ == '__main__':
    apply_the_filters(start_row=0)
