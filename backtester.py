"""
backtester.py — Test strategy on historical data.
Simulates trades and calculates performance metrics.
"""

from config import INITIAL_CAPITAL, MAX_POSITION_SIZE, STOP_LOSS_PCT, TAKE_PROFIT_PCT


def run_backtest(data):
    """
    Simulate trading based on signals in the DataFrame.
    
    Tracks: entries, exits, PnL per trade, and portfolio value.
    """
    capital = INITIAL_CAPITAL
    position = 0          # shares currently held
    entry_price = 0
    trades = []
    portfolio_values = []
    
    for i in range(len(data)):
        close = data["Close"].iloc[i]
        signal = data["Signal"].iloc[i]
        date = data.index[i]
        
        # Check stop-loss and take-profit if in a position
        if position > 0:
            pnl_pct = (close - entry_price) / entry_price
            
            if pnl_pct <= -STOP_LOSS_PCT:
                # Stop-loss hit
                capital += position * close
                trades.append({
                    "entry_date": entry_date,
                    "exit_date": date,
                    "entry_price": entry_price,
                    "exit_price": close,
                    "shares": position,
                    "pnl": position * (close - entry_price),
                    "exit_reason": "STOP_LOSS"
                })
                position = 0
            
            elif pnl_pct >= TAKE_PROFIT_PCT:
                # Take-profit hit
                capital += position * close
                trades.append({
                    "entry_date": entry_date,
                    "exit_date": date,
                    "entry_price": entry_price,
                    "exit_price": close,
                    "shares": position,
                    "pnl": position * (close - entry_price),
                    "exit_reason": "TAKE_PROFIT"
                })
                position = 0
        
        # Process signals
        if signal == "BUY" and position == 0:
            shares_to_buy = min(MAX_POSITION_SIZE, int(capital // float(close)))
            if shares_to_buy > 0:
                position = shares_to_buy
                entry_price = close
                entry_date = date
                capital -= position * close
        
        elif signal == "SELL" and position > 0:
            capital += position * close
            trades.append({
                "entry_date": entry_date,
                "exit_date": date,
                "entry_price": entry_price,
                "exit_price": close,
                "shares": position,
                "pnl": position * (close - entry_price),
                "exit_reason": "SIGNAL"
            })
            position = 0
        
        # Track portfolio value
        total_value = capital + (position * close)
        portfolio_values.append(total_value)
    
    data["Portfolio_Value"] = portfolio_values
    
    return data, trades


def print_results(trades, final_value):
    """Print backtest summary."""
    print("\n" + "=" * 50)
    print("BACKTEST RESULTS")
    print("=" * 50)
    print(f"Initial Capital:  ${INITIAL_CAPITAL:,.2f}")
    print(f"Final Value:      ${final_value:,.2f}")
    print(f"Total Return:     {((final_value / INITIAL_CAPITAL) - 1) * 100:.2f}%")
    print(f"Total Trades:     {len(trades)}")
    
    if trades:
        wins = [t for t in trades if t["pnl"] > 0]
        losses = [t for t in trades if t["pnl"] <= 0]
        print(f"Winning Trades:   {len(wins)}")
        print(f"Losing Trades:    {len(losses)}")
        
        total_pnl = sum(t["pnl"] for t in trades)
        print(f"Total PnL:        ${total_pnl:,.2f}")
        
        print("\nTrade Details:")
        for t in trades:
            print(f"  {t['entry_date'].date()} -> {t['exit_date'].date()} | "
                  f"${t['entry_price']:.2f} -> ${t['exit_price']:.2f} | "
                  f"PnL: ${t['pnl']:,.2f} ({t['exit_reason']})")


if __name__ == "__main__":
    from data_fetcher import fetch_historical_data
    from indicators import add_indicators
    from strategy import generate_signals
    
    df = fetch_historical_data()
    df = add_indicators(df)
    df = generate_signals(df)
    
    df, trades = run_backtest(df)
    final_value = df["Portfolio_Value"].iloc[-1]
    print_results(trades, final_value)