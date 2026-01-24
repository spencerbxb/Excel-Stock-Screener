# evaluator.py - evaluates stocks based on technical indicators and fundamental data

import datetime as dt
import pandas as pd
import yfinance as yf

import settings
from Code import create_output
from Code import symbol_processor

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

# main_loop(requested_file) takes the Excel file & computes the data for the file. 
# O(n)
def main_loop(requested_file, used_strategy):
    constants = get_constants()

    # Pull data:
    RSI_DAYS = constants["RSI_DAYS"]
    EMA_1, EMA_2 = assign_ema(constants)
    PRICE_USED = constants["PRICE_USED"]

    # Get the stocks from the list
    stocklist = pd.read_excel(requested_file)
    symbols = stocklist["Symbol"].dropna().tolist()

    rows = []

    # Make sure the user has provided a valid price
    if PRICE_USED not in {"Close", "Open", "High", "Low"}:
        print(f"{PRICE_USED} is not a valid input. The following are valid inputs for PRICE_USED:\n")
        print('- "Close" (recommended)\n')
        print('- "Open"\n')
        print('- "High"\n')
        print('- "Low"\n')
        return

    # Pull data to use as a benchmark for comparisons (by default VOO)
    Benchmark = yf.download(settings.BENCHMARK, start=START, end=NOW, progress=False)

    if Benchmark.empty:
        print(f'Benchmark symbol "{settings.BENCHMARK}" could not be found on Yahoo Finance.\n')
        print("S&P500 will be used as symbol for current iterations instead")
        Benchmark = yf.download("VOO", start=START, end=NOW, progress=False)

    for idx, symbol in enumerate(symbols, start=1):
        try:
            element = symbol_processor.process_symbol(
                symbol, idx, START, NOW, PRICE_USED, EMA_1, EMA_2, RSI_DAYS, Benchmark, used_strategy
            )

            if element is None:
                continue
            
            rows.append(element)

        except Exception as e:
            print(f"Skipping {symbol}: {e}")

    columns = []

    match used_strategy:
        case "Momentum":
            columns = [
                "#", "Name", "Symbol", PRICE_USED, "Rating",
                f"EMA {EMA_1}", f"EMA {EMA_2}", f"RSI ({RSI_DAYS})",
                f"Vs. {settings.BENCHMARK}", "52W Low", "52W High"
            ]
        case "Value":
            columns = [
                "#", "Name", "Symbol", PRICE_USED, "Rating",
                "P/E", "Dividend Yield",
                "52W Low", "52W High"
            ]
        case "Growth":
            columns = [
                "#", "Name", "Symbol", PRICE_USED, "Rating",
                "TTM", "EPS Growth", "Dividend Yield",
                "52W Low", "52W High"
            ]
        case "Mixed":
            columns = [
                "#", "Name", "Symbol", PRICE_USED, "Rating",
                f"EMA {EMA_1}", f"EMA {EMA_2}", f"RSI ({RSI_DAYS})",
                f"Vs. {settings.BENCHMARK}",
                "P/E", "Dividend Yield",
                "TTM", "EPS Growth",
                "52W Low", "52W High"
            ]
        case _:
            print("Function failed")

    create_output.output(rows, columns)

# get_constants() pulls constants from settings, updating their values within the script
# O(n)
def get_constants():
    constants = DEFAULT_CONSTANTS.copy()

    for key, default in DEFAULT_CONSTANTS.items():
        value = getattr(settings, key, default)
        constants[key] = value

    return constants

# assign_ema(constants) ensures the first moving average is shorter than the second, deletes the second ema
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