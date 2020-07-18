import pandas as pd
from screener.finnhub.initialize import pg_db, finnhub_client

#  1. Aggregate Indicator
# print(finnhub_client.aggregate_indicator('AAPL', 'D'))
# {'technical_analysis': {'count': {'buy': 10, 'neutral': 5, 'sell': 2},
#                         'signal': 'buy'},
#  'trend': {'adx': 41.09818099887694}}

#  2. Use talib to calculate SMA 20, 50, 200

# 1. get symbols
stocks_df = pd.read_csv('../data/symbols_fin_hubb.csv')