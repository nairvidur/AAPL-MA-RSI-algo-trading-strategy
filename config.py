"""
config.py — Central configuration for the trading system.
Every tunable parameter lives here. No magic numbers in other files.
"""

# ============================================================
# STRATEGY PARAMETERS
# ============================================================
SYMBOL = "AAPL"                # Ticker to trade
TIMEFRAME = "1d"               # Candle interval: 1m, 5m, 15m, 1h, 1d
LOOKBACK_PERIOD = "5y"         # How much history to fetch

# Moving Average settings
SHORT_MA_PERIOD = 20           # Fast moving average window
LONG_MA_PERIOD = 50            # Slow moving average window

# RSI settings
RSI_PERIOD = 14                # RSI lookback window
RSI_OVERSOLD = 30              # Buy threshold
RSI_OVERBOUGHT = 70            # Sell threshold

# ============================================================
# RISK MANAGEMENT
# ============================================================
MAX_POSITION_SIZE = 100        # Max shares per trade
RISK_PER_TRADE = 0.02          # Risk 2% of portfolio per trade
STOP_LOSS_PCT = 0.05           # 5% stop-loss
TAKE_PROFIT_PCT = 0.10         # 10% take-profit
MAX_PORTFOLIO_EXPOSURE = 0.30  # Max 30% of capital in one stock

# ============================================================
# INTERACTIVE BROKERS CONNECTION
# ============================================================
IB_HOST = "127.0.0.1"         # localhost (IB Gateway runs locally)
IB_PORT = 7497                 # 7497 = TWS paper trading
                               # 4002 = IB Gateway paper trading
IB_CLIENT_ID = 1               # Unique ID for this connection

# ============================================================
# ACCOUNT
# ============================================================
INITIAL_CAPITAL = 100_000      # Starting capital for backtesting

# ============================================================
# LOGGING
# ============================================================
LOG_FILE = "trading.log"
LOG_LEVEL = "INFO"