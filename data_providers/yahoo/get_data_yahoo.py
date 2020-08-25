# %%
import yfinance as yf
from get_all_tickers import get_tickers as gt

# %%
tickers = gt.get_tickers(NYSE=True, NASDAQ=True, AMEX=True)
print(len(tickers))
