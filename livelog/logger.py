# -*- coding: utf-8 -*-

from os import access, X_OK
from pathlib import Path
from platform import system
from tempfile import gettempdir
from datetime import datetime
from .errors import *


class Logger:
    """Logging handler.

    Attributes:
        LEVELS (dict): Log levels value for fast filtering
        enabled (bool): If logging is enabled
        erase (bool): If preexisting file should be erased
        file (str): Log file path
        level (str): Minimum log level to be displayed

    Raises:
        LogLevelDoesNotExist: If user provide an unknown log level
        LogFileIsADirectory: If user provide a directory as output path
        LogPathDoesNotExist: If user provide a non existing output path
        LogPathInsufficientPermissions: If user does not have permissions to
            write to output path
    """

    _LEVELS = {
        "ERROR": 3,
        "WARNING": 2,
        "INFO": 1,
        "DEBUG": 0,
    }

    def __init__(
        self,
        file: str = None,
        level: str = "DEBUG",
        enabled: bool = True,
        erase: bool = True,
    ):
        """Logger initialization.

        Args:
            file (str, optional): Output file path. Defaults to None.
            level (str, optional): Minimum log level. Defaults to "DEBUG".
            enabled (bool, optional): Is log enabled ? Defaults to True.
            erase (bool, optional): Should preexisting file be erased ? Defaults to True.
        """

        self._enabled = enabled
        self._erase = erase

        if file is None:
            self._file = Path(
                "/tmp/livelog.log"
                if system() == "Darwin"
                else Path(gettempdir()) / "livelog.log"
            )
        else:
            self._file = Path(file)

        self._verify_file()

        level = level.upper()
        if level not in self._LEVELS:
            raise LogLevelDoesNotExist(level)
        self._level = level

    @property
    def file(self):
        return self._file

    @file.setter
    def set_file(self, value: str):
        path = Path(value)
        self._verify_file(file=path)
        self._file = path

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: str):
        level = value.upper()
        if level not in self._LEVELS:
            raise LogLevelDoesNotExist(level)
        self._level = level

    def _verify_file(self):
        """Verify if provided file path is a valid log file and clear its
        preexisting content.
        """

        dir = self._file.parent.resolve()
        try:
            if self._file.is_dir():
                raise LogFileIsADirectory(path=self._file)
            if not dir.is_dir():
                raise LogPathDoesNotExist(path=dir)
        except PermissionError:
            raise LogPathInsufficientPermissions(path=dir)
        if not access(dir, X_OK):
            raise LogPathInsufficientPermissions(path=dir)
        self._clear_file()

    def _clear_file(self):
        """Clear output file content."""

        if not self._erase or not self._file.is_file():
            return
        with open(self._file, "w") as f:
            pass

    def _write(self, level: str, content: str):
        """Write provided content to output file.

        Args:
            level (str); Log level
            content (str): Content to be written
        """

        if not self._enabled:
            return

        time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        with open(self._file, "a") as f:
            f.write(f"{level} | {time} - {content}\n")

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

        self._write(level="ERR!", content=message)

    def warn(self, message: str):
        """Write warning message.

        Args:
            message (str): Log message
        """

        if not self._is_valid_level("WARNING"):
            return
        self._write(level="WARN", content=message)

    def info(self, message: str):
        """Write info message.

        Args:
            message (str): Log message
        """

        if not self._is_valid_level("INFO"):
            return
        self._write(level="INFO", content=message)

    def debug(self, message: str):
        """Write debug message.

        Args:
            message (str): Log message
        """

        if not self._is_valid_level("DEBUG"):
            return
        self._write(level="DBUG", content=message)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggerSingleton(Logger, metaclass=Singleton):
    pass
