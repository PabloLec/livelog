#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import argv
from os import system, name
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Style


class ReadFile(FileSystemEventHandler):
    def __init__(self, file):
        file = file

    def clear(self):
        _ = system("cls") if name == "nt" else system("clear")

    def on_modified(self, event):
        self.clear()
        with open(file, "r") as f:
            print(f.read())
            print(Style.RESET_ALL)


if __name__ == "__main__":
    if len(argv) == 1:
        print("! No file specified !")
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
