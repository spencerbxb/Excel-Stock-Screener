# growth.py calculates values pertaining to an asset's growth metrics

from Code.Strategies import computations

import settings

# calculate(price, EMA_SHORT, EMA_LONG, RSI_DAYS, Benchmark) pulls data related to the an asset
# & computes growth-related data
# O(1)
def calculate(div_yield, info):
    # Trailing Twelve Months earnings growth
    TTM = computations.to_scalar(info.get("earningsQuarterlyGrowth"))

    # Year Over Year Earnings Per Share growth
    YOY_eps = computations.to_scalar(info.get("earningsGrowth"))

    rating = rate(TTM, YOY_eps, div_yield)
    return rating, TTM, YOY_eps

# rate() rates the momentum of an asset
# O(1)
def rate(TTM, YOY_eps, div_yield): 
    score = 0

    if computations.is_valid(TTM):
        if TTM >= settings.TTM:
            score += 1
        else:
            score -= 1
    
    if computations.is_valid(YOY_eps):
        if YOY_eps >= settings.YOY_EPS:
            score += 1
        else:
            score -= 1

    if computations.is_valid(div_yield):
        if div_yield <= settings.GROW_DIV_YIELD:
            score += 1
        else:
            score -= 1

    return score


