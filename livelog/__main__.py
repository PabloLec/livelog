# -*- coding: utf-8 -*-

from platform import system
from tempfile import gettempdir
from pathlib import Path
from argparse import ArgumentParser
from livelog.reader import start_reader


def _parse_args():
    """Parse CLI arguments.

    Returns:
        tuple: Provided arguments
    """

    parser = ArgumentParser(description="Live read a log file")
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        type=str,
        required=False,
        help="Log file to be read",
    )
    parser.add_argument(
        "-l",
        "--level",
        action="store",
        type=str,
        default="DEBUG",
        required=False,
        help="Minimum log level. Default: DEBUG",
    )
    parser.add_argument(
        "--nocolors",
        action="store_true",
        required=False,
        help="Do not color lines",
    )
    args = parser.parse_args()

    if args.file is not None:
        file = Path(args.file)
    else:
        file = Path(
            "/tmp/livelog.log"
            if system() == "Darwin"
            else Path(gettempdir()) / "livelog.log"
        )

    return file, args.level, args.nocolors


if __name__ == "__main__":
    file, level, nocolors = _parse_args()
    start_reader(file=file, level=level, nocolors=nocolors)
