Stock Tracker Tool for Excel (pour les directions en français, veuillez voir « LISMOI.txt »)

Spencer Neumayer, 2025 (https://github.com/spencerbxb)

This project requires Python 3.13 to run. If Python 3.13 is not installed to the current OS, please
download it via the following link:

https://www.python.org/downloads/release/python-3130/?featured_on=pythonbytes

It may also be downloaded via the Microsoft Store for Windows 10 & 11 devices.

Directions:

1. Open the Excel file "Stock Screener" within the same directory (Stock-Screener)
2. Under "Symbol", list the symbols you would like to track from finance.yahoo.com.
3. Right click "RUN.py". In the drawdown, select "Open with", then "Python 3.13"
4. The function will run & evaluate all symbols one-by-one then upload the data to the Excel file

To see a demonstration of the the program's functionality, change the setting "FILE_NAME" in "settings.py" to "Canadian Stocks"

NOTES: 
- All stocks MUST be listed on Yahoo Finance in order to be viewed (finance.yahoo.com)
- TSX listed securities ALWAYS end in suffix .TO (check the Yahoo Finance listing to ensure)
- Currency pairs must be formatted as symbol 1-symbol 2 (ie. CAD-USD, CHF-CAD, BTC-USD)

Settings may be changed within the file "settings.py". Simply redefine variables with desired values
