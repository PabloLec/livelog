# -*- coding: utf-8 -*-

from typing import Union
from os import _exit, system, name, access, R_OK, SEEK_END
from time import sleep
from shutil import get_terminal_size
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent
from colorama import Style, Fore


class Reader(FileSystemEventHandler):
    """Watchdog handler to monitor file changes."""

    _CLEAR_CMD = "cls" if name == "nt" else "clear"
    _LEVEL_COLORS = {
        "ERR!": Fore.RED,
        "WARN": Fore.YELLOW,
        "INFO": Fore.BLUE,
        "DBUG": Fore.WHITE,
    }

    def __init__(self, file: str):
        """Reader initialization.

        Args:
            file (str): Path of file to monitor
        """

        self._file = file
        self._verify_file()
        while True:
            try:
                self.on_modified(event=None)
                break
            except FileNotFoundError:
                system(self._CLEAR_CMD)
                print("File not found, waiting for creation.")
                sleep(1)

    def _verify_file(self):
        """Verify if the file is a valid log file."""

        dir = self._file.parent.resolve()
        if self._file.is_dir():
            raise LogFileIsADirectory(path=self._file)
        if not dir.is_dir():
            raise LogPathDoesNotExist(path=dir)
        if not access(dir, R_OK):
            raise LogPathInsufficientPermissions(path=dir)


    def tail(self, lines: int):
        """Emulate tail command behavior by printing n last lines.

        Args:
            lines (int): Number of lines to print
        """

        pos = lines + 1
        rows = []
        with open(self._file) as f:
            while len(rows) <= lines:
                try:
                    f.seek(-pos, 2)
                except IOError:
                    f.seek(0)
                    break
                finally:
                    rows = list(f)
                pos *= 2

        colored_lines = map(self.color_line, rows[-lines:])
        output = "".join(list(colored_lines))
        system(self.self._CLEAR_CMD)
        print(output)


    def color_line(self, line: str):
        level = line[:4]

        output = (
            f"{Style.DIM}{line[7:19]}{Style.BRIGHT} - {Style.NORMAL}"
            f"{self.self._LEVEL_COLORS[level]}{line[22:]}{Style.RESET_ALL}"
        )
        return output

    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent, None]):
        """File modification callback.

        Args:
            event (Union[DirModifiedEvent, FileModifiedEvent, None]): Watchdog event
        """

        print(Style.RESET_ALL, end="")
        self.tail(get_terminal_size(fallback=(120, 50))[1])
        print(Style.RESET_ALL, end="")


def start_reader(file: str):
    """Start reader process.

    Args:
        file (str): File to be read
    """

    event_handler = Reader(file=file)
    observer = Observer()
    observer.schedule(event_handler, file, recursive=True)
    observer.start()

    try:
        input("")
        _exit(1)

    finally:
        observer.stop()
        observer.join()
