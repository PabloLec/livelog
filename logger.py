# -*- coding: utf-8 -*-

from os import access, X_OK
from pathlib import Path
from platform import system
from tempfile import gettempdir
from datetime import datetime
from errors import *
from colorama import Fore, Style


class Logger:
    __instance = None
    _LEVELS = {"ERROR": 3, "WARNING": 2, "INFO": 1, "DEBUG": 0}

    def __new__(cls, *args, **kwargs):
        is_singleton = (len(args) == 5 and args[4] == True) or kwargs.get("singleton")
        if is_singleton and not Logger.__instance or not is_singleton:
            Logger.__instance = object.__new__(cls)
        return Logger.__instance

    def __init__(
        self,
        output_file: str = None,
        level: str = "INFO",
        enabled: bool = True,
        colors: bool = True,
        singleton: bool = False,
    ):
        if output_file is None:
            self._output_file = Path(
                f"/tmp/{__name__}.log"
                if system() == "Darwin"
                else Path(gettempdir()) / f"{__name__}.log"
            )
        else:
            self._output_file = output_file

        level = level.upper()
        if level not in self._LEVELS:
            raise LogLevelDoesNotExist(level)
        self._level = level

        self._enabled = enabled
        self._colors = colors

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, value: str):
        if value == "local":
            dir = Path(__file__).parent.resolve()
            path = dir / "output.log"
        else:
            path = Path(value)
            dir = path.parent.resolve()
            if path.is_dir():
                raise LogFileIsADirectory(path=path)
            if not dir.is_dir():
                raise LogPathDoesNotExist(path=dir)
            if not access(dir, X_OK):
                raise LogPathInsufficientPermissions(path=dir)

        self._output_file = path

        if path.is_file():
            self._clear_file()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: str):
        level = value.upper()
        if level not in self._LEVELS:
            raise LogLevelDoesNotExist(level)
        self._level = level

    def _clear_file(self):
        with open(self._output_file, "w") as f:
            pass

    def _write(self, content: str):
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
        return self._LEVELS[self._level] <= self._LEVELS[level]

    def error(self, message: str):
        if self._colors:
            self._write(content=Fore.RED + message)
        else:
            self._write(content="error   | " + message)

    def warn(self, message: str):
        if not self._is_valid_level("WARNING"):
            return
        if self._colors:
            self._write(content=Fore.YELLOW + message)
        else:
            self._write(content="warning | " + message)

    def info(self, message: str):
        if not self._is_valid_level("INFO"):
            return
        if self._colors:
            self._write(content=Fore.BLUE + message)
        else:
            self._write(content="info    | " + message)

    def debug(self, message: str):
        if not self._is_valid_level("DEBUG"):
            return
        if self._colors:
            self._write(content=Fore.WHITE + message)
        else:
            self._write(content="debug   | " + message)
