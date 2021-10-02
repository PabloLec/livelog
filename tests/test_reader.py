from livelog.reader import Reader


def test_default(reader_test_file, capfd):
    Reader(
        file=reader_test_file,
        level="DEBUG",
        nocolors=False,
    )
    out, err = capfd.readouterr()
    assert out == "Hello World!"
