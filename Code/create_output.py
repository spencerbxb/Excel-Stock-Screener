from pathlib import Path
import pandas as pd

import os
import sys
import subprocess

import settings

# output(rows, columns) creates the output Excel file within the Stock-Screener directory.
# O(n)
def output(rows, columns):
    BASE_DIR = Path(__file__).resolve().parent.parent  # Stock-Screener
    export_df = pd.DataFrame(rows, columns=columns)

    name = settings.FILE_NAME
    OUTPUT_FILE = BASE_DIR / f"{name} Output.xlsx"
    export_df.to_excel(OUTPUT_FILE, index=False)

    if settings.OPEN_ON_COMPLETION:
        if sys.platform.startswith("win"):
            os.startfile(OUTPUT_FILE)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", OUTPUT_FILE])
        else:  # Linux
            subprocess.run(["xdg-open", OUTPUT_FILE])