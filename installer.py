# This function installs of the necessary files related to the Stock-Screener. It only needs to be run once
# & does not need to executed ever again.

import subprocess
import sys

def install():
    packages = ["numpy", "pandas", "yfinance", "openpyxl"]
    subprocess.check_call([sys.executable, "-m", "pip", "install", *packages])

if __name__ == "__main__":
    install()