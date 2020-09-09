import json
import time
from datetime import datetime
from random import randint

import pandas as pd

from lib.helpers import dict_to_json_zipped
from lib.my_email import send_eri_mail
from data_providers.alphavantage.get_data_alphavantage import get_company_overview, get_tech_ind
from data_providers.finnhub.get_data_finnhub import get_symbols, get_basic_financials
from data_providers.finnhub.initialize import pg_db, finnhub_client


# The current price > SMA50 > SMA150 > SMA200
# The current price must be at least 30% above the 52 week low.
# The current price must be within 25% of the 52 week high.
# price_relative_to_SP500 for 4, 13, 26 weeks > 30%

def apply_the_filters(start_row=0, use_forecast=False, pc_higher_sp=10, min_to_52w_low=1.3, min_52w_high=0.75):
    global df_symbol
    # %% 0 get all symbols
    df_symbols = get_symbols()
    df_forecast = pd.read_csv('/home2/eproject/veehuen/python/algo102/fbprophet/growth_stocks.csv')
    # %%
    df = df_forecast if use_forecast else df_symbols
    df_metric_list = []
    df['condition_1'] = False
    df['condition_2'] = False
    df['condition_3'] = False
    df['sma_50'] = None
    df['sma_150'] = None
    df['sma_200'] = None
    # df['52WeekHigh'] = None
    # df['52WeekLow'] = None
    # df['priceRelativeToS&P50013Week'] = None
    # df['priceRelativeToS&P50026Week'] = None
    # df['priceRelativeToS&P5004Week'] = None
    # %% 1 get current price per symbol
    filtered_symbol = []
    for i, row in df[start_row:].iterrows():
        symbol = row['symbol']
        try:
            conditions = [False] * 3
            # if i % 1500 == 0 and i > 0:
            #     break
            print(i, symbol, datetime.now())
            sql = f"SELECT * FROM stocks_finn_hub WHERE symbol='{symbol}' order by DATE DESC LIMIT 200"

            df_symbol = pg_db.query_df(sql)

            # skip if data less than 200 samples
            if len(df_symbol) < 200:
                continue

            df_symbol.index = df_symbol['date'].dt.date
            df_symbol.sort_index(inplace=True)

            df_symbol[f'sma_50'] = df_symbol['c'].rolling(50).mean()
            df_symbol['sma_150'] = df_symbol['c'].rolling(150).mean()
            df_symbol['sma_200'] = df_symbol['c'].rolling(200).mean()
            current = df_symbol.iloc[-1]['c']
            sma_50 = df_symbol.iloc[-1]['sma_50']
            sma_150 = df_symbol.iloc[-1]['sma_150']
            sma_200 = df_symbol.iloc[-1]['sma_200']

            df.loc[i, 'sma_50'] = sma_50
            df.loc[i, 'sma_150'] = sma_150
            df.loc[i, 'sma_200'] = sma_200

        except Exception as e:
            print(symbol, e)
            continue

        try:
            if current > sma_50 > sma_150 > sma_200:
                conditions[0] = True
                df.loc[i, 'condition_1'] = True
        except TypeError:
            continue

        try:
            bs = get_basic_financials(symbol, 'price')
            data_folder = '/home2/eproject/vee-h-phan.com/algo102/data_providers/finnhub/data'
            dict_to_json_zipped(bs, f'{data_folder}/bs_{symbol}.json.gzip')

        except Exception as e:
            send_eri_mail('phanveehuen@gmail.com', e.__repr__(), 'finhubb error: bs')
            continue

        if i % 3 == 0:
            sleep_time = randint(3, 8)
            print(i, f'sleeping {sleep_time} seconds')
            time.sleep(sleep_time)

        high_52_week = bs.get('metric').get('52WeekHigh')
        low_52_week = bs.get('metric').get('52WeekLow')

        try:
            if current / low_52_week > min_to_52w_low and current / high_52_week > min_52w_high:
                conditions[1] = True
                df.loc[i, 'condition_2'] = True
        except TypeError:
            continue

        price_relative_to_SP500 = [
            bs.get('metric').get('priceRelativeToS&P50013Week'),
            bs.get('metric').get('priceRelativeToS&P50026Week'),
            bs.get('metric').get('priceRelativeToS&P5004Week'),
            # bs.get('metric').get('priceRelativeToS&P50052Week'),
        ]

        # save metric to df
        row_metric = pd.DataFrame.from_dict(bs.get('metric'), orient='index').T
        row_metric.index = [i]
        df_metric_list.append(row_metric)

        try:
            if all(i >= pc_higher_sp for i in price_relative_to_SP500):
                conditions[2] = True
                df.loc[i, 'condition_3'] = True
        except TypeError:
            continue

        if all(conditions):
            filtered_symbol.append(symbol)
            print(filtered_symbol)
            print(df.loc[i])

        if i % 1000 == 0 and i > 0:
            df.to_csv(f'/home2/eproject/vee-h-phan.com/algo102/data_providers/finnhub/data/growth_stocks_filtered_{i}.csv',
                      index=False)
        if i % 100 == 0 and i > 0:
            send_eri_mail('phanveehuen@gmail.com', f'processed {i} symbols', 'finhubb progress: bs')

    df_metric = pd.concat(df_metric_list)
    final_df_filtered = pd.concat([df, df_metric], axis=1)
    final_df_filtered.to_csv(
        '/home2/eproject/vee-h-phan.com/algo102/data_providers/finnhub/data/growth_stocks_filtered.csv', index=False)
    pg_db.df_to_db(final_df_filtered, name='biz_fin', if_exists='replace', index=False)


if __name__ == '__main__':
    apply_the_filters(start_row=0, use_forecast=False)
