import datetime as dt
import pandas as pd
import yfinance as yf
import numpy as np

import settings
from Code import rate_stock
from Code import create_output

# ---- TIME CONFIG ----
START = dt.datetime(2017, 12, 1)
NOW = dt.datetime.now()

# ---- DEFAULT CONSTANTS ----
DEFAULT_CONSTANTS = {
    "RSI_DAYS": 14,
    "EMA_1": 50,
    "EMA_2": 200,
    "PRICE_USED": "Close",
}

# get_constants() pulls constants from settings, updating their values within the script
# O(n)
def get_constants():
    constants = DEFAULT_CONSTANTS.copy()

    for key, default in DEFAULT_CONSTANTS.items():
        value = getattr(settings, key, default)
        constants[key] = value

    return constants

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

# assign_ema(constants) ensure the first moving average is shorter than the second, deletes the second ema
# if they are equal.
# O(1)
def assign_ema(constants):
    if (constants["EMA_1"] < constants["EMA_2"]):
        # Moving average 1 is shorter than 2

        return constants["EMA_1"], constants["EMA_2"]
    elif (constants["EMA_1"] > constants["EMA_2"]):
        # Moving average 2 is shorter than moving average 1
        
        return constants["EMA_2"], constants["EMA_1"]
    else:
        # Both moving averages are equal, discard the second
        return constants["EMA_1"], NotImplemented

# safe_round(value, ndigits) returns the input variable rounded, if the input variable has no value,
# then nothing is returned
# O(1)
def safe_round(value, ndigits):
    return round(value, ndigits) if value is not None else None

# main_loop(requested_file) takes the Excel file & computes the data for the file. 
# O(n)
def main_loop(requested_file):
    constants = get_constants()

    # Pull data:
    RSI_DAYS = constants["RSI_DAYS"]
    EMA_1, EMA_2 = assign_ema(constants)
    PRICE_USED = constants["PRICE_USED"]

    # Get the stocks from the list
    stocklist = pd.read_excel(requested_file)
    symbols = stocklist["Symbol"].dropna().tolist()

    rows = []

    for idx, symbol in enumerate(symbols, start=1):
        try:
            print(f"Processing {symbol}...")

            df = yf.download(symbol, start=START, end=NOW, progress=False) # pull data from yahoo finance
            if df.empty:
                # skip the symbol if we couldn't find data
                print(f"No data found on yahoo finance for symbol: {symbol} \n"
                      "ensure that it has been entered correctly")
                continue

            # Get data related to the symbol
            price = df[PRICE_USED].iloc[-1, 0]                          # price data
            df[f"EMA{EMA_1}"] = df[PRICE_USED].ewm(span=EMA_1).mean()   # EMA_1 data
            df[f"EMA{EMA_2}"] = df[PRICE_USED].ewm(span=EMA_2).mean()   # EMA_2
            df["RSI"] = compute_rsi(df[PRICE_USED], RSI_DAYS)           # RSI data

            ema1 = df[f"EMA{EMA_1}"].iloc[-1]
            ema2 = df[f"EMA{EMA_2}"].iloc[-1]
            rsi = df["RSI"].iloc[-1]

            low52 = df["Low"].rolling(252).min().iloc[-1, 0]
            high52 = df["High"].rolling(252).max().iloc[-1, 0]

            info = yf.Ticker(symbol).info

            name = info.get("longName")
            dividend = to_scalar(info.get("dividendYield"))
            pe = to_scalar(info.get("trailingPE"))
            peg = to_scalar(info.get("pegRatio"))

            rating = rate_stock.rate(price, ema1, ema2, pe, peg, rsi)

            rows.append([
                idx,
                name,
                symbol,
                safe_round(price, 2),
                rating,
                dividend,
                safe_round(pe, 2),
                safe_round(ema1, 2),
                safe_round(ema2, 2),
                safe_round(rsi, 1),
                safe_round(low52, 2),
                safe_round(high52, 2),
                peg
            ])

        except Exception as e:
            print(f"Skipping {symbol}: {e}")

        columns = [
            "#",
            "Name",
            "Symbol",
            PRICE_USED,
            "Rating",
            "Dividend Yield",
            "P/E",
            f"EMA {EMA_1}",
            f"EMA {EMA_2}",
            f"RSI ({RSI_DAYS})",
            "52W Low",
            "52W High",
            "PEG",
        ]

    create_output.output(rows, columns)