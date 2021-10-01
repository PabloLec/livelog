# -*- coding: utf-8 -*-

from sys import argv
from platform import system
from tempfile import gettempdir
from pathlib import Path
from livelog.reader import start_reader
from livelog.logger import Logger

if __name__ == "__main__":
    if len(argv) == 1:
        print("! No file specified !")
        file = Path(
            "/tmp/livelog.log"
            if system() == "Darwin"
            else Path(gettempdir()) / "livelog.log"
        )
    else:
        file=Path(argv[1])


    start_reader(file=file)
