# Feel free to modify the variables within this file to customize

# Trading strategy:
STRATEGY = "Mixed"      # Which strategy should be used ("Mixed", "Momentum", "Value", "Growth")

# Momentum Constants:
RSI_DAYS = 14           # Relative Strength Index: determines if a stock is over/undersold (recommended: 14)
EMA_1 = 50              # Exponential Moving Average 1 (recommended: 50)
EMA_2 = 200             # Exponential Moving Average 2 (recommended: 200)
BENCHMARK = "VOO"       # Which symbol should be used as the benchmark
                        # (recommended: "VOO" (S&P500) or "QQQ" (NASDAQ) for USD-listed assets, 
                        # "VFV.TO" (CAD-Hedged S&P500) or "XIU.TO" (Toronto Stock Exchange) for CAD-listed assets

# Value Constants:
TARGET_PE = 20          # Target Price to Earnings ratio (recommended: 20)
VAL_DIV_YIELD = 0.03    # Dividend Yield %: should greater than or equal to this (recommended: 0.03 (3%))

# Growth Constants:
TTM = 10                # Trailing Twelve Month earnings growth (recommended: )
YOY_EPS = 10            # Earnings Per Share growth Year over Year (recommended: )
GROW_DIV_YIELD = 0.01   # Dividend Yield %: should be less than this value (recommended: 0.01 (1%))

# Weight Constants:
MOM_WEIGHT = 1          # Weight assigned to momentum-based metrics
VAL_WEIGHT = 1          # Weight assigned to valuation-based metrics
GRO_WEIGHT = 1          # Weight assigned to growth-based metrics

PRICE_USED = "Close"    # Which price will be used of "HIGH", "LOW", "OPEN", "CLOSE" (recommended: "CLOSE")

FILE_NAME = "Stock Screener"    # "The Excel spreadsheet to be screened (Default: "Stock Screener", Demo: "Canadian Stocks")
OPEN_ON_COMPLETION = True

# Style
TOP_COLOR = "FFFFF2CC"
ROW_1_COLOR = "FFF9F9F9"
ROW_2_COLOR = "FFFFFFFF"

# Colors for ratings
STRONG_BUY   = "FF086218"
BUY          = "FF048910"
HOLD         = "FFEC9C01"
SELL         = "FFE10D0D"
STRONG_SELL  = "FF800101"