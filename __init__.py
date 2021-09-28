# -*- coding: utf-8 -*-

from sys import argv
from os import system, name, SEEK_END
from shutil import get_terminal_size
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Style


def tail(file_name, lines):
    pos = lines + 1
    rows = []
    with open(file_name) as f:
        while len(rows) <= lines:
            try:
                f.seek(-pos, 2)
            except IOError:
                f.seek(0)
                break
            finally:
                rows = list(f)
            pos *= 2
    print("".join(rows[-lines:]))


class ReadFile(FileSystemEventHandler):
    def __init__(self, file):
        file = file

    def clear(self):
        _ = system("cls") if name == "nt" else system("clear")

    def on_modified(self, event):
        self.clear()
        tail(file, get_terminal_size(fallback=(120, 50))[1])
        print(Style.RESET_ALL)


if __name__ == "__main__":
    if len(argv) == 1:
        print("! lineso file specified !")
        exit()
    print(" - Observer started -")

    file = argv[1]
    event_handler = ReadFile(file=file)
    observer = Observer()
    observer.schedule(event_handler, file, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)

    finally:
        observer.stop()
        observer.join()
