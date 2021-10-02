import pytest


@pytest.fixture(scope="session")
def log_file(tmpdir_factory):
    return tmpdir_factory.mktemp("tmp").join("test.log")
