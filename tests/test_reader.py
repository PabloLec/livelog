from re import findall
from pytest import raises
from pathlib import Path
from colorama import Style, Fore
from livelog.reader import Reader
from livelog import errors


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


def test_reader_default(reader_test_file, capfd):
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


def test_reader_level_info(reader_test_file, capfd):
    Reader(
        file=reader_test_file,
        level="INFO",
        nocolors=False,
    )
    out, _ = capfd.readouterr()

    assert len(findall(r"(.* - .*debug.*\n)", out)) == 0
    assert len(findall(r"(^.* - .*info.*\n)", out)) == 1
    assert len(findall(r"(\n.* - .*warning.*\n)", out)) == 1
    assert len(findall(r"(\n.* - .*error.*\n)", out)) == 1


def test_reader_level_warning(reader_test_file, capfd):
    Reader(
        file=reader_test_file,
        level="WARNING",
        nocolors=False,
    )
    out, _ = capfd.readouterr()

    print(out)

    assert len(findall(r"(.* - .*debug.*\n)", out)) == 0
    assert len(findall(r"(.* - .*info.*\n)", out)) == 0
    assert len(findall(r"^(.* - .*warning.*\n)", out)) == 1
    assert len(findall(r"(\n.* - .*error.*\n)", out)) == 1


def test_reader_level_error(reader_test_file, capfd):
    Reader(
        file=reader_test_file,
        level="ERROR",
        nocolors=False,
    )
    out, _ = capfd.readouterr()

    print(out)

    assert len(findall(r"(.* - .*debug.*\n)", out)) == 0
    assert len(findall(r"(.* - .*info.*\n)", out)) == 0
    assert len(findall(r"(.* - .*warning.*\n)", out)) == 0
    assert len(findall(r"(^.* - .*error.*\n)", out)) == 1


def test_reader_nocolors(reader_test_file, capfd):
    Reader(
        file=reader_test_file,
        level="DEBUG",
        nocolors=True,
    )
    out, _ = capfd.readouterr()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - debug)", out))
        == 1
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - info)", out)) == 1
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - warning)", out))
        == 1
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - error)", out))
        == 1
    )


def test_reader_level_custom_case(reader_test_file, capfd):
    Reader(
        file=reader_test_file,
        level="iNfO",
        nocolors=True,
    )
    out, _ = capfd.readouterr()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - debug)", out))
        == 0
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - info)", out)) == 1
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - warning)", out))
        == 1
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - error)", out))
        == 1
    )


def test_reader_log_file_is_directory(reader_test_file):
    dir = Path(reader_test_file).parent
    with raises(errors.LogFileIsADirectory):
        Reader(file=dir, level="DEBUG", nocolors=True)


def test_reader_wrong_log_path():
    with raises(errors.LogPathDoesNotExist):
        Reader(file=Path("/foo/bar/test.log"), level="DEBUG", nocolors=True)


def test_reader_insufficient_permissions(restricted_dir, system_is_windows):
    if system_is_windows:
        return

    with raises(errors.LogPathInsufficientPermissions):
        Reader(file=Path(restricted_dir + "test.log"), level="DEBUG", nocolors=True)


def test_reader_unknow_log_level(reader_test_file):
    with raises(errors.LogLevelDoesNotExist):
        Reader(file=reader_test_file, level="TEST", nocolors=True)
