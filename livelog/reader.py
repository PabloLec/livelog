# -*- coding: utf-8 -*-

from typing import Union
from os import _exit, system, name, SEEK_END
from time import sleep
from shutil import get_terminal_size
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent
from colorama import Style, Fore

_CLEAR_CMD = "cls" if name == "nt" else "clear"
_LEVEL_COLORS = {
    "ERR!": Fore.RED,
    "WARN": Fore.YELLOW,
    "INFO": Fore.BLUE,
    "DBUG": Fore.WHITE,
}


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

    colored_lines = map(color_line, rows[-lines:])
    output = "".join(list(colored_lines))
    system(_CLEAR_CMD)
    print(output)


def color_line(line: str):
    level = line[:4]

    output = (
        f"{Style.DIM}{line[7:19]}{Style.BRIGHT} - {Style.NORMAL}"
        f"{_LEVEL_COLORS[level]}{line[22:]}{Style.RESET_ALL}"
    )
    return output


class ReadFile(FileSystemEventHandler):
    """Watchdog handler to monitor file changes."""

    def __init__(self, file: str):
        """ReadFile initialization.

        Args:
            file (str): Path of file to monitor
        """

        self._file = file
        while True:
            try:
                self.on_modified(event=None)
                break
            except FileNotFoundError:
                system(_CLEAR_CMD)
                print("File not found, waiting for creation.")
                sleep(1)

    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent, None]):
        """File modification callback.

        Args:
            event (Union[DirModifiedEvent, FileModifiedEvent, None]): Watchdog event
        """

        print(Style.RESET_ALL, end="")
        tail(self._file, get_terminal_size(fallback=(120, 50))[1])
        print(Style.RESET_ALL, end="")


def start_reader(file: str):
    """Start reader process.

    Args:
        file (str): File to be read
    """

    event_handler = ReadFile(file=file)
    observer = Observer()
    observer.schedule(event_handler, file, recursive=True)
    observer.start()

    try:
        input("")
        _exit(1)

    finally:
        observer.stop()
        observer.join()
