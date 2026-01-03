# rate_stock.py - rates a stock based on technical and fundamental indicators

import math

# rate(price, ema_1, ema_2, pe, rsi) calculates a symbol's rating using ema_1, ema_2, pe, & rsi
# (if available) returning a string "BUY", "HOLD", or "SELL" depending on the calculated rating.
# O(1)
def rate(price, ema_1, ema_2, pe, rsi):
    def is_valid(x):
        return x is not None and not (isinstance(x, float) and math.isnan(x))
    
    score = 0

    # Trend
    if is_valid(ema_2) and price > ema_2:
        score += 1
    if is_valid(ema_1) and price > ema_1:
        score += 1
    if is_valid(ema_1) and is_valid(ema_2) and ema_1 > ema_2:
        score += 1

    # P/E ratio
    if is_valid(pe):
        if pe < 20:
            score += 1
        elif pe > 30:
            score -= 1

    # Momentum
    if is_valid(rsi):
        if rsi < 30:
            score += 1
        elif rsi > 70:
            score -= 1

    if score >= 4:
        return "BUY"
    elif score >= 2:
        return "HOLD"
    else:
        return "SELL"
