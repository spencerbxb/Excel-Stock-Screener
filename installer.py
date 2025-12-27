# This function installs of the necessary files related to the Stock-Screener. It only needs to be run once
# & does not need to executed ever again.

import subprocess
import sys

def install():
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ])

if __name__ == "__main__":
    install()