# AAPL MA-RSI Algorithmic Trading Strategy

Algorithmic trading system using RSI + Moving Average crossover strategy, backtested on AAPL with risk management. Built for deployment on Interactive Brokers paper trading.

## Strategy Logic

- **BUY** when the 20-day SMA crosses above the 50-day SMA and RSI is not overbought (< 70)
- **SELL** when the 20-day SMA crosses below the 50-day SMA and RSI is not oversold (> 30)
- Stop-loss at 5%, take-profit at 10%
- Max 2% portfolio risk per trade, 30% max exposure per stock

## Backtest Results (5 Years — AAPL)

| Metric | Value |
|---|---|
| Initial Capital | $100,000 |
| Final Value | $103,275 |
| Total Return | 3.27% |
| Total Trades | 13 |
| Win Rate | 38% (5W / 8L) |

## Project Structure

- `config.py` — Central configuration, all tunable parameters
- `data_fetcher.py` — Downloads OHLCV data from Yahoo Finance
- `indicators.py` — Computes RSI and Simple Moving Averages
- `strategy.py` — Generates BUY/SELL/HOLD signals
- `backtester.py` — Simulates trades on historical data
- `risk_manager.py` — Position sizing and exposure limits
- `ib_connection.py` — Interactive Brokers connection (TBD)
- `executor.py` — Order placement on IB (TBD)
- `live_trader.py` — Main trading loop (TBD)
- `monitor.py` — Logging and performance tracking (TBD)

## Setup

```bash