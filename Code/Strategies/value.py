# value.py calculates values pertaining to an asset's valuation metrics

from Code.Strategies import computations

import settings

# calculate(div_yield, info) pulls data related to the an asset
# & computes momentum-related data.
# O(1)
def calculate(div_yield, info):
    pe = computations.to_scalar(info.get("trailingPE"))
    # pb = computations.to_scalar(info.get("trailingPB")) price to book isn't reliable

    rating = rate(pe, div_yield)

    return rating, pe

# rate() rates the value of an asset
# O(1)
def rate(pe, div_yield):
    score = 0

    if computations.is_valid(pe):
        if pe < settings.TARGET_PE:
            score += 1
        else:
            score -= 1

    # if computations.is_valid(pb):
    #     if pb < settings.TARGET_PB:
    #         score += 1
    #     else:
    #         score -= 1

    if computations.is_valid(div_yield):
        if div_yield >= settings.VAL_DIV_YIELD:
            score += 1
        else:
            score -= 1
            
    return score