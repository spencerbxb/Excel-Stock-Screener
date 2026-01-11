# computations.py - contains computation functions for financial indicators

import pandas as pd
import numpy as np
import math

# is_valid(x) determines if a number is valid for usage or not
# O(1)
def is_valid(x):
        return x is not None and not (isinstance(x, float) and math.isnan(x))

# to_scalar(x) gets the scalar value of data
# O(1)
def to_scalar(x):
    if x is None:
        return None
    if isinstance(x, (pd.Series, pd.DataFrame, np.ndarray)):
        if len(x) == 0:
            return None
        return float(x.iloc[-1] if hasattr(x, "iloc") else x[-1])
    return float(x) if pd.notna(x) else None

# compute_rsi(series, period) computes the RSI using data from Yahoo Finance
# O(n)
def compute_rsi(series, period):
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))