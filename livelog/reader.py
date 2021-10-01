# -*- coding: utf-8 -*-

from typing import Union
from os import _exit, system, name, SEEK_END
from shutil import get_terminal_size
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent
from colorama import Style, Fore

CLEAR_CMD = "cls" if name == "nt" else "clear"


def clear():
    """Clear terminal."""

    system(CLEAR_CMD)


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
    clear()
    print("".join(list(colored_lines)))


LEVEL_COLORS = {
    "ERR!": Fore.RED,
    "WARN": Fore.YELLOW,
    "INFO": Fore.BLUE,
    "DBUG": Fore.WHITE,
}


def color_line(line: str):
    level = line[:4]

    output = (
        f"{Style.DIM}{line[7:19]}{Style.BRIGHT} - {Style.NORMAL}"
        f"{LEVEL_COLORS[level]}{line[26:]}{Style.RESET_ALL}"
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
        self.on_modified(event=None)

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
