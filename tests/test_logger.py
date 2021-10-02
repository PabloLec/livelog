from pytest import raises
from pathlib import Path
from re import findall
from livelog import Logger, LoggerSingleton, errors


def test_default(log_file):
    logger = Logger(file=log_file)
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 1
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 1
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 1
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 1
    )


def test_without_erasing(log_file):
    logger = Logger(file=log_file, erase=False)
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 2
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 2
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 2
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 2
    )


def test_with_erasing(log_file):
    logger = Logger(file=log_file)
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 1
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 1
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 1
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 1
    )


def test_log_level_info(log_file):
    logger = Logger(file=log_file, level="INFO")
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 0
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 1
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 1
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 1
    )


def test_log_level_warning(log_file):
    logger = Logger(file=log_file, level="WARNING")
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 0
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 0
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 1
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 1
    )


def test_log_level_error(log_file):
    logger = Logger(file=log_file, level="ERROR")
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 0
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 0
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 0
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 1
    )


def test_log_level_custom_case(log_file):
    logger = Logger(file=log_file, level="iNfO")
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 0
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 1
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 1
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 1
    )


def test_log_disabled(log_file):
    logger = Logger(file=log_file, enabled=False)
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 0
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 0
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 0
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 0
    )


def test_singleton(log_file):
    logger1 = LoggerSingleton(file=log_file)
    logger1.debug("0")
    logger1.info("1")
    logger2 = LoggerSingleton()
    logger2.warn("2")
    logger2.error("3")
    with open(log_file, "r") as f:
        logs = f.read()

    assert (
        len(findall(r"(DBUG \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 0)", logs)) == 1
    )
    assert (
        len(findall(r"(INFO \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 1)", logs)) == 1
    )
    assert (
        len(findall(r"(WARN \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 2)", logs)) == 1
    )
    assert (
        len(findall(r"(ERR! \\| [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} - 3)", logs)) == 1
    )


def test_log_file_is_directory(log_file):
    dir = Path(log_file).parent
    with raises(errors.LogFileIsADirectory):
        Logger(file=dir)


def test_wrong_log_path():
    with raises(errors.LogPathDoesNotExist):
        Logger(file="/foo/bar/test.log")


def test_insufficient_permissions():
    with raises(errors.LogPathInsufficientPermissions):
        Logger(file="/root/test.log")


def test_unknow_log_level(log_file):
    with raises(errors.LogLevelDoesNotExist):
        Logger(file=log_file, level="TEST")
