"""
data_fetcher.py — Fetch historical market data.
Uses yfinance for free historical data (backtesting).
Later we'll add IB for live data.
"""

import yfinance as yf
import pandas as pd
from config import SYMBOL, TIMEFRAME, LOOKBACK_PERIOD


def fetch_historical_data(symbol=SYMBOL, period=LOOKBACK_PERIOD, interval=TIMEFRAME):
    """
    Download historical OHLCV data from Yahoo Finance.
    
    Returns a DataFrame with columns:
    Open, High, Low, Close, Volume
    """
    print(f"Fetching {period} of {interval} data for {symbol}...")
    
    data = yf.download(symbol, period=period, interval=interval)
    
    if hasattr(data.columns, 'levels'):
        data.columns = data.columns.get_level_values(0)
    # Drop any rows with missing values
    data.dropna(inplace=True)
    
    # Keep only the columns we need
    data = data[["Open", "High", "Low", "Close", "Volume"]]
    
    print(f"Got {len(data)} rows of data")
    print(f"Date range: {data.index[0]} to {data.index[-1]}")
    
    return data


# This block runs ONLY when you execute this file directly
# It does NOT run when another file imports from here
if __name__ == "__main__":
    df = fetch_historical_data()
    print(df.head())
    print(df.tail())