# -*- coding: utf-8 -*-

from typing import Union
from os import _exit, system, name, SEEK_END
from shutil import get_terminal_size
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent
from colorama import Style


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

    def clear(self):
        """Clear terminal."""

        _ = system("cls") if name == "nt" else system("clear")

    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent, None]):
        """File modification callback.

        Args:
            event (Union[DirModifiedEvent, FileModifiedEvent, None]): Watchdog event
        """

        self.clear()
        print(Style.RESET_ALL)
        tail(self._file, get_terminal_size(fallback=(120, 50))[1])
        print(Style.RESET_ALL)


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
