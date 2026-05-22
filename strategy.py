"""
strategy.py — Generate trading signals.
Combines MA crossover + RSI to produce BUY / SELL / HOLD.
"""

from config import RSI_OVERSOLD, RSI_OVERBOUGHT


def generate_signals(data):
    """
    Add a 'Signal' column to the DataFrame.
    
    Version 2 — Relaxed conditions:
    BUY  = Short MA crosses above Long MA (RSI confirms not overbought)
    SELL = Short MA crosses below Long MA (RSI confirms not oversold)
    """
    data["Signal"] = "HOLD"
    
    for i in range(1, len(data)):
        prev_short = data["SMA_Short"].iloc[i - 1]
        prev_long = data["SMA_Long"].iloc[i - 1]
        curr_short = data["SMA_Short"].iloc[i]
        curr_long = data["SMA_Long"].iloc[i]
        
        rsi = data["RSI"].iloc[i]
        
        # Golden cross + RSI not overbought = BUY
        if prev_short <= prev_long and curr_short > curr_long and rsi < RSI_OVERBOUGHT:
            data.iloc[i, data.columns.get_loc("Signal")] = "BUY"
        
        # Death cross + RSI not oversold = SELL
        elif prev_short >= prev_long and curr_short < curr_long and rsi > RSI_OVERSOLD:
            data.iloc[i, data.columns.get_loc("Signal")] = "SELL"
    
    return data


if __name__ == "__main__":
    from data_fetcher import fetch_historical_data
    from indicators import add_indicators
    
    df = fetch_historical_data()
    df = add_indicators(df)
    df = generate_signals(df)
    
    # Show only rows where a signal was generated
    signals = df[df["Signal"] != "HOLD"]
    print(f"\nTotal signals generated: {len(signals)}")
    print(signals[["Close", "SMA_Short", "SMA_Long", "RSI", "Signal"]])