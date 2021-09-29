# -*- coding: utf-8 -*-

from typing import Union
from sys import argv
from os import system, name, SEEK_END, _exit
from shutil import get_terminal_size
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent
from colorama import Style
from pynput import keyboard


def tail(file_name: str, lines: int):
    """Emulate tail command behavior by printing n last lines.

    Args:
        file_name (str): Log file name
        lines (int): Number of lines to print
    """

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
    """Watchdog handler to monitor file changes."""

    def __init__(self, file: str):
        """ReadFile initialization.

        Args:
            file (str): Path of file to monitor
        """

        self._file = file
        self.on_modified(event=None)
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        keyboard_listener.start()

    def on_press(self, key):
        """Button press event handler.

        Args:
            key (Key): Pressed key
        """

        try:
            if key.char in ["Q", "q"]:
                _exit(1)
        except AttributeError:
            return

    def clear(self):
        """Clear terminal."""

        _ = system("cls") if name == "nt" else system("clear")

    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent, None]):
        """File modification callback.

        Args:
            event (Union[DirModifiedEvent, FileModifiedEvent, None]): Watchdog event
        """

        self.clear()
        tail(self._file, get_terminal_size(fallback=(120, 50))[1])
        print(Style.RESET_ALL)


if __name__ == "__main__":
    if len(argv) == 1:
        print("! No file specified !")
        _exit(1)

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
