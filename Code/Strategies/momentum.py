# momentum.py calculates values pertaining to an asset's momentum.

from Code.Strategies import computations

import settings
import pandas as pd
    
# calculate(price, EMA_SHORT, EMA_LONG, RSI_DAYS, Benchmark) pulls data related to the an asset
# & computes momentum-related data.
# O(1)
def calculate(price, EMA_SHORT, EMA_LONG, RSI_DAYS, Benchmark):
    # Calculate EMA & RSI
    EMA_SHORT_val = price.ewm(span=EMA_SHORT).mean().iloc[-1]
    EMA_LONG_val = price.ewm(span=EMA_LONG).mean().iloc[-1]

    delta = price.diff()
    gain = delta.clip(lower=0).rolling(RSI_DAYS).mean()
    loss = -delta.clip(upper=0).rolling(RSI_DAYS).mean()
    RSI = 100 - (100 / (1 + gain.iloc[-1]/loss.iloc[-1]))

    # Returns since beginning of the period
    benchmark_series = Benchmark[settings.PRICE_USED]

    # Ensure it's a Series, not a DataFrame
    if isinstance(benchmark_series, pd.DataFrame):
        benchmark_series = benchmark_series.iloc[:, 0]

    stock_return = (price.iloc[-1] / price.iloc[0]) - 1
    benchmark_return = (benchmark_series.iloc[-1] / benchmark_series.iloc[0]) - 1

    rel_performance = stock_return - benchmark_return

    # Relative Performance
    rel_performance = stock_return - benchmark_return

    curr_price = price.iloc[-1]

    rating = rate(curr_price, EMA_SHORT_val, EMA_LONG_val, RSI, rel_performance)

    return rating, EMA_SHORT_val, EMA_LONG_val, RSI, rel_performance

# rate() rates the momentum of an asset
# O(1)
def rate(price, EMA_SHORT, EMA_LONG, RSI, rel_performance):
    score = 0

    # Trend
    if computations.is_valid(EMA_LONG) and price > EMA_LONG:
        score += 1
    if computations.is_valid(EMA_SHORT) and price > EMA_SHORT:
        score += 1
    if computations.is_valid(EMA_SHORT) and computations.is_valid(EMA_LONG) and EMA_SHORT > EMA_LONG:
        score += 1

    # Momentum
    if computations.is_valid(RSI):
        if RSI < 30:
            score += 1
        elif RSI > 70:
            score -= 1

    if computations.is_valid(rel_performance):
        if rel_performance > 50:
            score += 3
        elif rel_performance > 30:
            score += 2
        elif rel_performance > 10:
            score += 1
        elif rel_performance > -10:
            # in-line performance, no change
            pass
        elif rel_performance > -30:
            score -= 1
        elif rel_performance > -50:
            score -= 2
        else:
            score -= 3

    return score