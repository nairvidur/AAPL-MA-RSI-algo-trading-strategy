"""
indicators.py — Calculate technical indicators.
Computes RSI and Moving Averages from raw price data.
"""

import pandas as pd
from config import SHORT_MA_PERIOD, LONG_MA_PERIOD, RSI_PERIOD


def compute_sma(data, period):
    """Simple Moving Average — average of last 'period' closing prices."""
    return data["Close"].rolling(window=period).mean()


def compute_rsi(data, period=RSI_PERIOD):
    """
    Relative Strength Index.
    
    Steps:
    1. Calculate price changes
    2. Separate gains and losses
    3. Average them over the period
    4. Compute RS = avg_gain / avg_loss
    5. RSI = 100 - (100 / (1 + RS))
    """
    delta = data["Close"].diff()
    
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    avg_gain = gains.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = losses.ewm(com=period - 1, min_periods=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def add_indicators(data):
    """Add all indicators as new columns to the DataFrame."""
    data["SMA_Short"] = compute_sma(data, SHORT_MA_PERIOD)
    data["SMA_Long"] = compute_sma(data, LONG_MA_PERIOD)
    data["RSI"] = compute_rsi(data)
    
    # Drop rows where indicators haven't warmed up yet
    data.dropna(inplace=True)
    
    return data


if __name__ == "__main__":
    from data_fetcher import fetch_historical_data
    
    df = fetch_historical_data()
    df = add_indicators(df)
    
    print("\nLast 5 rows with indicators:")
    print(df[["Close", "SMA_Short", "SMA_Long", "RSI"]].tail())