from pathlib import Path
import pandas as pd

import settings

# output(rows, columns) creates the output Excel file within the Stock-Screener directory.
# O(n)
def output(rows, columns):
    BASE_DIR = Path(__file__).resolve().parent.parent  # Stock-Screener
    export_df = pd.DataFrame(rows, columns=columns)

    name = settings.FILE_NAME
    OUTPUT_FILE = BASE_DIR / f"{name} Output.xlsx"
    export_df.to_excel(OUTPUT_FILE, index=False)
