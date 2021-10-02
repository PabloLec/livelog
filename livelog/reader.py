# -*- coding: utf-8 -*-

from os import system, access, name, R_OK
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Style, Fore
from .errors import *


class Reader(FileSystemEventHandler):
    """Reading handler.

    Attributes:
        CLEAR_CMD (str): OS specific command to clear terminal
        LEVEL_COLORS (dict): Log levels corresponding colors
        LONG_LEVEL_TO_SHORT (dict): Log level long to short format
        LEVELS (dict): Log levels value for fast filtering
        file (str): Log file path
        level (str): Minimum log level to be displayed
        nocolors (bool): If colors should not be printed
        read_index (int): Current position of the cursor in the log file

    Raises:
        LogLevelDoesNotExist: If user provide an unknown log level
        LogFileIsADirectory: If user provide a directory as output path
        LogPathDoesNotExist: If user provide a non existing output path
        LogPathInsufficientPermissions: If user does not have permissions to
            write to output path
    """

    CLEAR_CMD = "cls" if name == "nt" else "clear"
    LEVEL_COLORS = {
        "ERR!": Fore.RED,
        "WARN": Fore.YELLOW,
        "INFO": Fore.BLUE,
        "DBUG": Fore.WHITE,
    }
    LONG_LEVEL_TO_SHORT = {
        "ERROR": "ERR!",
        "WARN": "WARNING",
        "INFO": "INFO",
        "DEBUG": "DBUG",
    }
    LEVELS = {
        "ERR!": 3,
        "WARN": 2,
        "INFO": 1,
        "DBUG": 0,
    }

    def __init__(self, file: str, level: str, nocolors: bool):
        """Reader initialization.

        Args:
            file (str): Path of file to monitor
            level (str): Minimum log level to be displayed
            nocolors (bool): If colors should not be printed
        """

        self.file = file
        self.verify_file()
        level = level.upper()
        if level not in self.LONG_LEVEL_TO_SHORT:
            raise LogLevelDoesNotExist(level)
        self.level = self.LONG_LEVEL_TO_SHORT[level]
        self.nocolors = nocolors

        self.read_index = 0

        system(self.CLEAR_CMD)
        while not self.file_exists():
            print("File not found, waiting for creation.")
            sleep(1)
            system(self.CLEAR_CMD)

        self.on_modified()

    def verify_file(self):
        """Verify if provided file path is a valid log file."""

        dir = self.file.parent.resolve()
        if self.file.is_dir():
            raise LogFileIsADirectory(path=self.file)
        if not dir.is_dir():
            raise LogPathDoesNotExist(path=dir)
        if not access(dir, R_OK):
            raise LogPathInsufficientPermissions(path=dir)

    def file_exists(self):
        """Check if file exists.

        Returns:
            bool: File exists
        """

        return self.file.is_file()

    def print_output(self):
        """Drive the printing process by getting new lines, filtering log
        level and coloring the output.
        """

        rows = self.get_new_lines()
        if rows is None:
            return
        rows = self.filter_log_level(rows)

        if self.nocolors:
            output = "".join(rows)
            print(output, end="")
        else:
            colored_lines = map(self.color_line, rows)
            output = "".join(list(colored_lines))
            print(Style.RESET_ALL + output + Style.RESET_ALL, end="")

    def get_new_lines(self):
        """Get newly created lines in log file based on stored cursor index.

        Returns:
            list: List of new lines
        """

        with open(self.file, "r") as f:
            f.seek(self.read_index)
            rows = list(f)
            if not rows and self.read_index > 0:
                # If a modification event was triggered without any
                # new rows, we should verify if there is content just before
                # current cursor position to determine if file have been reset
                # or just a false positive.
                f.seek(self.read_index - 1)
                if len(list(f)) > 0:
                    return None
                self.read_index = 0
                return self.get_new_lines()
            self.read_index += sum(map(len, rows))

        return rows

    def filter_log_level(self, lines: list):
        """Remove lines based on log level.

        Args:
            lines (list): Lines to be filtered

        Returns:
            list: Filtered lines
        """

        for i, line in enumerate(lines):
            level = line[:4]
            if self.LEVELS[self.level] > self.LEVELS[level]:
                del lines[i]
        return lines

    def color_line(self, line: str):
        """Parse and color a line based on its log level.

        Args:
            line (str): Line to be colored

        Returns:
            str: Colored line
        """

        level = line[:4]

        output = (
            f"{Style.DIM}{line[7:19]}{Style.BRIGHT} - {Style.NORMAL}"
            f"{self.LEVEL_COLORS[level]}{line[22:]}{Style.RESET_ALL}"
        )
        return output

    def on_modified(self, *args, **kwargs):
        """File modification callback."""

        self.print_output()

    def loop_without_event(self):
        """If inotify instance limit reached, loop without watching file."""

        while True:
            self.print_output()
            sleep(1)


def start_reader(file: str, level: str, nocolors: bool):
    """Start reader process.

    Args:
        file (str): File to be read
        level (str): Minimum log level to be displayed
        nocolors (bool): If colors should not be printed
    """

    event_handler = Reader(file=file, level=level, nocolors=nocolors)
    observer = Observer()
    observer.schedule(event_handler, file, recursive=True)
    try:
        observer.start()
        input("")
        observer.stop()
        observer.join()
    except OSError:
        # Handle "OSError: [Errno 24] inotify instance limit reached" exception
        event_handler.loop_without_event()
