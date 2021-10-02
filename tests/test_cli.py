from subprocess import Popen, PIPE


def test_default(default_log_file):
    print("python3 -m livelog".split())
    process = Popen("python3 -m livelog".split(), stdout=PIPE)
    out, _ = process.communicate()
    assert "It works" in str(out)


def test_custom_file(reader_test_file):
    process = Popen(
        f"python3 -m livelog -f {reader_test_file}".split(),
        stdout=PIPE,
    )
    out, _ = process.communicate()
    assert "debug" in str(out)


def test_nocolors(reader_test_file):
    process = Popen(
        f"python3 -m livelog -f {reader_test_file} --nocolors".split(),
        stdout=PIPE,
    )
    out, _ = process.communicate()
    assert "DBUG" in str(out)
    assert "INFO" in str(out)
    assert "WARN" in str(out)
    assert "ERR!" in str(out)


def test_custom_level(reader_test_file):
    process = Popen(
        f"python3 -m livelog -f {reader_test_file} --level=INFO --nocolors".split(),
        stdout=PIPE,
    )
    out, _ = process.communicate()
    assert "INFO" in str(out)
    assert "DBUG" not in str(out)
