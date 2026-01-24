import yfinance as yf
import pandas as pd

import settings

from Code.Strategies import computations
from Code.Strategies import momentum
from Code.Strategies import value
from Code.Strategies import growth

# process_symbol(symbol, idx, START, NOW, PRICE_USED, EMA_1, EMA_2, RSI_DAYS, Benchmark) processes the individual
# symbol in regards to the selected strategy, returning numerous values in regards to the symbol as well as a
# rating in respect to those values.
# O(1)
def process_symbol(symbol, idx, START, NOW, PRICE_USED, EMA_1, EMA_2, RSI_DAYS, Benchmark, used_strategy):
    print(f"Processing {symbol}...")

    df = yf.download(symbol, start=START, end=NOW, progress=False)
    if df.empty:
        return None

    price_series = df[PRICE_USED]

    if isinstance(price_series, pd.DataFrame):
        # select first column if df[PRICE_USED] is a DataFrame
        price_series = price_series.iloc[:, 0]

    price_series = price_series.dropna()    # remove any NaNs
    price = price_series.iloc[-1]           # last price scalar

    info = yf.Ticker(symbol).info
    name = info.get("longName")

    low52 = df["Low"].rolling(252).min().iloc[-1]
    if isinstance(low52, pd.Series):
        low52 = low52.iloc[0]

    high52 = df["High"].rolling(252).max().iloc[-1]
    if isinstance(high52, pd.Series):
        high52 = high52.iloc[0]

    div_yield = None
    if used_strategy != "Momentum":
        # Only pull dividend yield if strategy is non-momentum
        div_yield = computations.to_scalar(info.get("dividendYield"))

    match used_strategy:
        case "Momentum":
            rating, ema_s, ema_l, rsi, rel_perf = momentum.calculate(
                price_series, EMA_1, EMA_2, RSI_DAYS, Benchmark
            )

            rating_string = "Strong Sell"

            if rating >= 2:
                rating_string = "Strong Buy"
            elif rating >= 1:
                rating_string = "Buy"
            elif rating > -1:
                rating_string = "Hold"
            elif rating > -2:
                rating_string = "Sell"

            return [
                idx, name, symbol,
                safe_round(price, 2),
                rating_string,
                safe_round(ema_s, 2),
                safe_round(ema_l, 2),
                safe_round(rsi, 1),
                safe_round(rel_perf, 1),
                safe_round(low52, 2),
                safe_round(high52, 2)
            ]

        case "Value":
            rating, pe = value.calculate(div_yield, info)

            rating_string = "Strong Sell"

            if rating >= 2:
                rating_string = "Strong Buy"
            elif rating >= 1:
                rating_string = "Buy"
            elif rating > -1:
                rating_string = "Hold"
            elif rating > -2:
                rating_string = "Sell"

            return [
                idx, name, symbol,
                safe_round(price, 2),
                rating_string,
                safe_round(pe, 2),
                # safe_round(pb, 2),    price to book not reliable
                safe_round(div_yield, 2),
                safe_round(low52, 2),
                safe_round(high52, 2)
            ]

        case "Growth":
            rating, ttm, eps = growth.calculate(div_yield, info)

            rating_string = "Strong Sell"

            if rating >= 2:
                rating_string = "Strong Buy"
            elif rating >= 1:
                rating_string = "Buy"
            elif rating > -1:
                rating_string = "Hold"
            elif rating > -2:
                rating_string = "Sell"

            return [
                idx, name, symbol,
                safe_round(price, 2),
                rating,
                safe_round(ttm, 2),
                safe_round(eps, 2),
                safe_round(div_yield, 2),
                safe_round(low52, 2),
                safe_round(high52, 2)
            ]
        
        case "Mixed":
            # Momentum:
            m_rating, ema_s, ema_l, rsi, rel_perf = momentum.calculate(
                price_series, EMA_1, EMA_2, RSI_DAYS, Benchmark
            )

            # Value:
            v_rating, pe = value.calculate(div_yield, info)

            # Growth:
            g_rating, ttm, eps = growth.calculate(div_yield, info)

            # Final score calculations:
            final_rating = (
                m_rating * settings.MOM_WEIGHT +
                v_rating * settings.VAL_WEIGHT +
                g_rating * settings.GRO_WEIGHT
            )

            total_weight = settings.MOM_WEIGHT + settings.VAL_WEIGHT + settings.GRO_WEIGHT
            weighted = final_rating / total_weight

            rating_string = "Strong Sell"

            if weighted >= 2:
                rating_string = "Strong Buy"
            elif weighted >= 1:
                rating_string = "Buy"
            elif weighted > -1:
                rating_string = "Hold"
            elif weighted > -2:
                rating_string = "Sell"

            return [
                idx,
                name,
                symbol,
                safe_round(price, 2),
                rating_string,

                # Momentum
                safe_round(ema_s, 2),
                safe_round(ema_l, 2),
                safe_round(rsi, 1),
                safe_round(rel_perf, 1),

                # Value
                safe_round(pe, 2),
                # safe_round(pb, 2),        pric to book not reliabl
                safe_round(div_yield, 2),

                # Growth
                safe_round(ttm, 2),
                safe_round(eps, 2),

                # Range
                safe_round(low52, 2),
                safe_round(high52, 2),
            ]

# safe_round(value, ndigits) returns the input variable rounded, if the input variable has no value,
# then nothing is returned
# O(1)
def safe_round(value, ndigits):
    return round(value, ndigits) if value is not None else None