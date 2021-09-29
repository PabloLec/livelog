# -*- coding: utf-8 -*-

from os import access, X_OK
from pathlib import Path
from platform import system
from tempfile import gettempdir
from datetime import datetime
from colorama import Fore, Style
from .errors import *


class Logger:
    """Main logger object.

    Raises:
        LogLevelDoesNotExist: If user provide an unknown log level
        LogFileIsADirectory: If user provide a directory as output path
        LogPathDoesNotExist: If user provide a non existing output path
        LogPathInsufficientPermissions: If user does not have permissions to
            write to output path
    """

    __instance = None
    _LEVELS = {"ERROR": 3, "WARNING": 2, "INFO": 1, "DEBUG": 0}

    def __new__(cls, *args, **kwargs):
        is_singleton = (len(args) == 6 and args[5] == True) or kwargs.get("singleton")
        if is_singleton and not Logger.__instance or not is_singleton:
            Logger.__instance = object.__new__(cls)
        return Logger.__instance

    def __init__(
        self,
        output_file: str = None,
        level: str = "INFO",
        enabled: bool = True,
        colors: bool = True,
        erase: bool = True,
        singleton: bool = False,
    ):
        """Logger initialization.

        Args:
            output_file (str, optional): Output file path. Defaults to None.
            level (str, optional): Minimum log level. Defaults to "INFO".
            enabled (bool, optional): Is log enabled ? Defaults to True.
            colors (bool, optional): Are colors enabled ? Defaults to True.
            erase (bool, optional): Should preexisting file be erased ? Defaults to True.
            singleton (bool, optional): Is singleton ? Defaults to False.

        Raises:
            LogLevelDoesNotExist: [description]
        """

        self._enabled = enabled
        self._colors = colors
        self._erase = erase

        if output_file is None:
            self._output_file = Path(
                "/tmp/livelog.log"
                if system() == "Darwin"
                else Path(gettempdir()) / "livelog.log"
            )
        else:
            self._output_file = Path(output_file)
        self._verify_file(self._output_file)

        level = level.upper()
        if level not in self._LEVELS:
            raise LogLevelDoesNotExist(level)
        self._level = level

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def set_output_file(self, value: str):
        path = Path(value)
        self._verify_file(file=path)
        self._output_file = path

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: str):
        level = value.upper()
        if level not in self._LEVELS:
            raise LogLevelDoesNotExist(level)
        self._level = level

    def _verify_file(self, file: Path):
        """Verify if the file is a valid log file and clear its preexisting content.

        Args:
            file (Path): File path to verify.
        """

        dir = file.parent.resolve()
        if file.is_dir():
            raise LogFileIsADirectory(path=file)
        if not dir.is_dir():
            raise LogPathDoesNotExist(path=dir)
        if not access(dir, X_OK):
            raise LogPathInsufficientPermissions(path=dir)
        self._clear_file()

    def _clear_file(self):
        """Clear output file content."""

        if not self._erase or not self._output_file.is_file():
            return
        with open(self._output_file, "w") as f:
            pass

    def _write(self, content: str):
        """Write provided content to output file.

        Args:
            content (str): Content to be written
        """

        if not self._enabled:
            return

        if self._colors:
            time = Style.DIM + datetime.now().strftime("%H:%M:%S.%f")[:-3]
            dash = Style.BRIGHT + " - "
            content = f"{Style.NORMAL}{content}{Style.RESET_ALL}"
        else:
            time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            dash = " - "

        with open(self._output_file, "a") as f:
            f.write(f"{time}{dash}{content}\n")

    def _is_valid_level(self, level: str):
        """Verify if the given log level should be written.

        Args:
            level (str): Log level to verify

        Returns:
            bool: Level is valid
        """

        return self._LEVELS[self._level] <= self._LEVELS[level]

    def error(self, message: str):
        """Write error message.

        Args:
            message (str): Log message
        """

        if self._colors:
            self._write(content=Fore.RED + message)
        else:
            self._write(content="error   | " + message)

    def warn(self, message: str):
        """Write warning message.

        Args:
            message (str): Log message
        """

        if not self._is_valid_level("WARNING"):
            return
        if self._colors:
            self._write(content=Fore.YELLOW + message)
        else:
            self._write(content="warning | " + message)

    def info(self, message: str):
        """Write info message.

        Args:
            message (str): Log message
        """

        if not self._is_valid_level("INFO"):
            return
        if self._colors:
            self._write(content=Fore.BLUE + message)
        else:
            self._write(content="info    | " + message)

    def debug(self, message: str):
        """Write debug message.

        Args:
            message (str): Log message
        """

        if not self._is_valid_level("DEBUG"):
            return
        if self._colors:
            self._write(content=Fore.WHITE + message)
        else:
            self._write(content="debug   | " + message)
