import pytest
from os import getenv
from pathlib import Path
from livelog import Logger
from platform import system


@pytest.fixture(scope="session")
def restricted_dir():
    if "darwin" in system().lower():
        return getenv("HOME") + "/testfolder/"
    else:
        return "/root/"


@pytest.fixture(scope="session")
def system_is_windows():
    return "windows" in system().lower()


@pytest.fixture(scope="session")
def log_file(tmpdir_factory):
    return tmpdir_factory.mktemp("tmp").join("test.log")


@pytest.fixture(scope="function")
def default_log_file():
    logger = Logger()
    logger.debug("It works!")


@pytest.fixture(scope="function")
def reader_test_file(tmpdir_factory):
    log_file = tmpdir_factory.mktemp("tmp").join("test.log")
    logger = Logger(file=log_file)
    logger.debug("debug")
    logger.info("info")
    logger.warn("warning")
    logger.error("error")

    return Path(log_file)
