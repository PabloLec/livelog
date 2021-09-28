from os import access, X_OK
from pathlib import Path
from platform import system
from tempfile import gettempdir
from errors import *


class Logger:
    def __init__(self):
        self._output_file = None

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, value):
        if value == "tmp":
            path = Path("/tmp" if system() == "Darwin" else gettempdir())
        else:
            path = Path(value)
            if not path.is_dir():
                raise LogPathDoesNotExist(path=value)
            if not access(path, X_OK):
                raise LogPathInsufficientPermissions(path=value)

        self._output_file = path
