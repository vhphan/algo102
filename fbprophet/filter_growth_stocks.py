import glob
from pathlib import Path

import pandas as pd
import pendulum

if __name__ == '__main__':
    result_folder = '/home/eproject/veehuen/python/algo102/fbprophet/csv_forecast'
    df_results = pd.DataFrame(columns=['symbol', 'percent_growth'])
    for file in glob.glob(f'{result_folder}/*.zip'):
        df_forecast = pd.read_csv(file)
        symbol = Path(file).stem
        df_forecast['ds'] = pd.to_datetime(df_forecast['ds']).dt.date
        df_forecast.set_index('ds', inplace=True)
        today = pendulum.today().date()

        i = df_forecast.index.searchsorted(today)

        today_val = df_forecast.iloc[i]['yhat']

        last_val = df_forecast.iloc[-1, df_forecast.columns.get_loc("yhat")]
        last_day = df_forecast.index[-1]
        delta = last_day - today
        delta_days = delta.days
        if delta_days >= 150 and last_val > today_val:
            pc_growth = last_val / today_val
            pc_growth = round(100 * (pc_growth - 1), 2)
            print(f'The growth of {symbol} is {pc_growth}%')
            df_results = df_results.append(pd.DataFrame(dict(symbol=[symbol], percent_growth=[pc_growth])))
            print(df_results)
    df_results.sort_values(by='percent_growth', ascending=False, inplace=True)
    df_results.to_csv('growth_stocks.csv', index=False)
