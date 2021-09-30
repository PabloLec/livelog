# -*- coding: utf-8 -*-

from sys import argv
from os import _exit
from livelog.reader import start_reader

if __name__ == "__main__":
    if len(argv) == 1:
        print("! No file specified !")
        _exit(1)

    start_reader(file=argv[1])
