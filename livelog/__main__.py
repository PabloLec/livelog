# -*- coding: utf-8 -*-

from sys import argv
from platform import system
from tempfile import gettempdir
from pathlib import Path
from argparse import ArgumentParser
from livelog.reader import start_reader
from livelog.logger import Logger


def parse_args():
    parser = ArgumentParser(description='Live read a log file')
    parser.add_argument('-f', '--file', action='store', type=str, required=False)
    parser.add_argument('-l', '--level', action='store', type=str, required=False)
    parser.add_argument('--nocolors', action='store_true', required=False)
    args = parser.parse_args()

    print(args)

    if args.file is not None:
        file=Path(args.file)
    else:
        file = Path(
            "/tmp/livelog.log"
            if system() == "Darwin"
            else Path(gettempdir()) / "livelog.log"
        )

    return file



if __name__ == "__main__":
    file = parse_args()
    
    start_reader(file=file)
