# Feel free to modify the variables within this file to customize

# Constants for computation:
RSI_DAYS = 14           # Relative Strength Index: determines if a stock is over/undersold (recommended: 14)
EMA_1 = 50              # Exponential Moving Average 1
EMA_2 = 200             # Exponential Moving Average 2
PRICE_USED = "Close"    # Which price will be used of "HIGH", "LOW", "OPEN", "CLOSE" (recommended: "CLOSE")

FILE_NAME = "Stock Screener"    # "The Excel spreadsheet to be screened (Default: "Stock Screener", Demo: "Canadian Stocks")
OPEN_ON_COMPLETION = True

# The stock rater formula can be viewed & modified within Stock-Screener>Code>rate_file.py