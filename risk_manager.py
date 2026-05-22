"""
risk_manager.py — Position sizing and risk controls.
Prevents the strategy from taking oversized or dangerous positions.
"""

from config import (
    INITIAL_CAPITAL, MAX_POSITION_SIZE, RISK_PER_TRADE,
    STOP_LOSS_PCT, MAX_PORTFOLIO_EXPOSURE
)


def calculate_position_size(capital, price, stop_loss_pct=STOP_LOSS_PCT):
    """
    How many shares to buy based on how much we're willing to lose.
    
    Logic: If we risk 2% of capital and stop-loss is 5%,
    then position size = (capital * 0.02) / (price * 0.05)
    
    This means: the dollar amount we lose if stopped out
    equals exactly 2% of our portfolio.
    """
    risk_amount = capital * RISK_PER_TRADE
    per_share_risk = price * stop_loss_pct
    
    if per_share_risk == 0:
        return 0
    
    shares = int(risk_amount / per_share_risk)
    
    # Never exceed max position size
    shares = min(shares, MAX_POSITION_SIZE)
    
    # Never exceed max portfolio exposure
    max_shares_by_exposure = int((capital * MAX_PORTFOLIO_EXPOSURE) / price)
    shares = min(shares, max_shares_by_exposure)
    
    # Can't buy more than we can afford
    max_affordable = int(capital // price)
    shares = min(shares, max_affordable)
    
    return shares


def check_risk_limits(capital, price, current_position_value):
    """
    Returns True if we're allowed to take a new position.
    Returns False if it would exceed our risk limits.
    """
    exposure = current_position_value / capital if capital > 0 else 1
    
    if exposure >= MAX_PORTFOLIO_EXPOSURE:
        print(f"BLOCKED: Portfolio exposure {exposure:.1%} exceeds limit {MAX_PORTFOLIO_EXPOSURE:.1%}")
        return False
    
    return True


if __name__ == "__main__":
    # Test with example values
    test_capital = 100_000
    test_price = 300.0
    
    shares = calculate_position_size(test_capital, test_price)
    cost = shares * test_price
    risk = shares * test_price * STOP_LOSS_PCT
    
    print(f"Capital:        ${test_capital:,.2f}")
    print(f"Stock Price:    ${test_price:.2f}")
    print(f"Shares to Buy:  {shares}")
    print(f"Position Cost:  ${cost:,.2f}")
    print(f"Max Loss (SL):  ${risk:,.2f}")
    print(f"Risk % of Port: {risk/test_capital:.2%}")
    print(f"Exposure:       {cost/test_capital:.2%}")