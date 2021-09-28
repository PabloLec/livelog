from os import access, X_OK
from pathlib import Path
from platform import system
from tempfile import gettempdir
from errors import *


class Logger:
    def __init__(self):
        self._output_file = Path(
            f"/tmp/{__name__}.log"
            if system() == "Darwin"
            else gettempdir() + "{__name__}.log"
        )

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, value):
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
