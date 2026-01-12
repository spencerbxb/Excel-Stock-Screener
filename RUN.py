from Code import evaluator
from pathlib import Path
import settings

DIRECTORY = Path(__file__).resolve().parent
FILE_NAME = settings.FILE_NAME

if not FILE_NAME.lower().endswith(".xlsx"):
    FILE_NAME += ".xlsx"

requested_file = DIRECTORY / FILE_NAME

if requested_file.exists():
    print(f"evaluating file {requested_file} with strategy {settings.STRATEGY}, please wait")
    evaluator.main_loop(requested_file)
else:
    print(f'File not found: {requested_file},\n'
          'ensure that the file has been properly named in settings.py & that it'
          'has been placed within parent directory "Stock-Screener"')