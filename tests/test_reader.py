from re import findall
from colorama import Style, Fore
from livelog.reader import Reader


def escape(string):
    return string.replace("\\", "\\\\")


DIM = escape(Style.DIM)
BRIGHT = escape(Style.BRIGHT)
NORMAL = escape(Style.NORMAL)
WHITE = escape(Fore.WHITE)
BLUE = escape(Fore.BLUE)
YELLOW = escape(Fore.YELLOW)
RED = escape(Fore.RED)
RESET_ALL = escape(Style.RESET_ALL)


def test_default(reader_test_file, capfd):
    Reader(
        file=reader_test_file,
        level="DEBUG",
        nocolors=False,
    )
    out, _ = capfd.readouterr()

    debug_line = findall(r"(^.* - .*debug.*\n)", out)[0]
    info_line = findall(r"(\n.* - .*info.*\n)", out)[0]
    warning_line = findall(r"(\n.* - .*warning.*\n)", out)[0]
    error_line = findall(r"(\n.* - .*error.*\n)", out)[0]

    assert all(x in debug_line for x in (DIM, BRIGHT, NORMAL, WHITE, RESET_ALL))
    assert all(x in info_line for x in (DIM, BRIGHT, NORMAL, BLUE, RESET_ALL))
    assert all(x in warning_line for x in (DIM, BRIGHT, NORMAL, YELLOW, RESET_ALL))
    assert all(x in error_line for x in (DIM, BRIGHT, NORMAL, RED, RESET_ALL))
