from Code import evaluator
from pathlib import Path
import settings

DIRECTORY = Path(__file__).resolve().parent
FILE_NAME = settings.FILE_NAME

if not FILE_NAME.lower().endswith(".xlsx"):
    FILE_NAME += ".xlsx"

requested_file = DIRECTORY / FILE_NAME

# select_strategy() lets the user define a strategy using I/O
# O(1)
def select_strategy():
    valid_strategies = {
        "Mixed",
        "Momentum",
        "Value",
        "Growth"
    }
    
    used_strategy = ""
    
    if settings.STRATEGY == "Ask First":
        used_strategy = input("Please select a strategy from the following list:\n"
                            "'Mixed', 'Momentum', 'Value', 'Growth':\n")
    else:
        used_strategy = settings.STRATEGY
        return used_strategy

    while (True):
        if used_strategy not in valid_strategies:
            used_strategy = input(f"Strategy '{used_strategy}' is not a valid strategy.\n"
                                    "Please select a strategy from the following list:\n"
                                    "'Mixed', 'Momentum', 'Value', 'Growth':\n")
        else:
            return used_strategy

if requested_file.exists():
    used_strategy = select_strategy()

    print(f"Evaluating file {requested_file} with strategy {used_strategy}, please wait")
    evaluator.main_loop(requested_file, used_strategy)
else:
    print(f'File not found: {requested_file},\n'
          'ensure that the file has been properly named in settings.py & that it'
          'has been placed within parent directory "Stock-Screener"')