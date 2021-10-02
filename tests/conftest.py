import pytest
from livelog import Logger
from pathlib import Path


@pytest.fixture(scope="session")
def log_file(tmpdir_factory):
    return tmpdir_factory.mktemp("tmp").join("test.log")


@pytest.fixture(scope="function")
def reader_test_file(tmpdir_factory):
    log_file = tmpdir_factory.mktemp("tmp").join("test.log")
    logger = Logger(file=log_file)
    logger.debug("0")
    logger.info("1")
    logger.warn("2")
    logger.error("3")

    return Path(log_file)
